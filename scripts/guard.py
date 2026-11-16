#!/usr/bin/env python3
"""Verify research artifacts; review Git data with the trusted base checker."""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
from urllib.parse import urlparse


MANIFEST = 'manifest-sha256.json'
LOCK = 'governance/foundation-lock.json'
PRINCIPLES = 'governance/core-principles.json'


def git(*args):
    return subprocess.check_output(['git', *args], stderr=subprocess.PIPE)


def safe_path(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or str(path) != name:
        raise ValueError('unsafe repository path: ' + name)
    return name


def local_files():
    names = git('ls-files', '--cached', '--others', '--exclude-standard', '-z')
    files = {}
    for raw in names.split(b'\0'):
        if not raw:
            continue
        name = safe_path(raw.decode('utf-8'))
        path = Path(name)
        if path.is_symlink() or not path.is_file():
            raise ValueError('unsupported file mode or missing file: ' + name)
        files[name] = path.read_bytes()
    return files


def commit_id(ref):
    return git('rev-parse', '--verify', '--end-of-options', ref + '^{commit}').decode().strip()


def tree_files(ref):
    files = {}
    entries = git('ls-tree', '-rz', '--full-tree', ref)
    for entry in entries.split(b'\0'):
        if not entry:
            continue
        meta, raw_path = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = safe_path(raw_path.decode('utf-8'))
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('unsupported file mode: ' + name)
        files[name] = git('cat-file', 'blob', oid)
    return files


def document(files, name):
    return json.loads(files[name].decode('utf-8'))


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest()
            for name, data in sorted(files.items()) if name != MANIFEST}


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def check_cases(files, principle_ids):
    required = ('supports', 'challenges', 'alternative_explanations', 'limits',
                'decision_time_information', 'later_information')
    case_ids = set()
    for name in sorted(files):
        if not name.startswith('research/cases/') or not name.endswith('.json'):
            continue
        try:
            case = document(files, name)
            assert nonempty_text(case['id']) and case['id'] not in case_ids
            case_ids.add(case['id'])
            assert case['related_principles']
            assert set(case['related_principles']) <= principle_ids
            assert all(nonempty_text(case[key]) for key in required)
            assert case['sources'] and case['claims']
            source_ids = set()
            for source in case['sources']:
                assert nonempty_text(source['id']) and source['id'] not in source_ids
                source_ids.add(source['id'])
                assert nonempty_text(source['url'])
                url = urlparse(source['url'])
                assert url.scheme == 'https' and url.netloc
                date.fromisoformat(source['retrieved_at'])
                assert all(nonempty_text(source[key]) for key in ('publisher', 'origin_group', 'excerpt'))
                assert source['relationship'] in ('first_party', 'independent_reporting', 'republication')
            for claim in case['claims']:
                assert nonempty_text(claim['statement']) and claim['source_ids']
                assert set(claim['source_ids']) <= source_ids
        except (KeyError, TypeError, ValueError, AssertionError) as error:
            raise ValueError('invalid case: ' + name) from error


def verify(files):
    manifest = document(files, MANIFEST)
    expected = hashes(files)
    if set(manifest) != set(expected):
        raise ValueError('manifest inventory mismatch')
    if manifest != expected:
        raise ValueError('manifest digest mismatch')

    lock = document(files, LOCK)
    if lock['schema_version'] != 1:
        raise ValueError('unsupported foundation schema')
    for name, digest in lock['sha256'].items():
        safe_path(name)
        if name not in files or hashlib.sha256(files[name]).hexdigest() != digest:
            raise ValueError('foundation digest mismatch: ' + name)

    core = document(files, PRINCIPLES)
    if core['schema_version'] != 1 or core['review_status'] not in (
            'pending_owner_review', 'owner_confirmed'):
        raise ValueError('invalid principle review state')
    ids = set()
    for principle in core['principles']:
        if principle['id'] in ids or principle['origin'] != 'source_abstraction':
            raise ValueError('invalid or duplicate principle')
        ids.add(principle['id'])
        if not principle['anchors']:
            raise ValueError('principle requires source anchors')
        for anchor in principle['anchors']:
            name = safe_path(anchor['path'])
            if name not in lock['sha256']:
                raise ValueError('source anchor is outside the foundation: ' + name)
            lines = files[name].decode('utf-8').splitlines()
            start, end = anchor['start_line'], anchor['end_line']
            if (type(start) is not int or type(end) is not int
                    or not 1 <= start <= end <= len(lines)):
                raise ValueError('source anchor range invalid: ' + name)
            if '\n'.join(lines[start - 1:end]) != anchor['quote']:
                raise ValueError('source quote mismatch: ' + principle['id'])
    if not ids:
        raise ValueError('principle registry is empty')
    check_cases(files, ids)
    return core['review_status']


def review(base, head):
    base, head = commit_id(base), commit_id(head)
    subprocess.run(['git', 'merge-base', '--is-ancestor', base, head], check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    original, candidate = tree_files(base), tree_files(head)
    verify(original)
    policy = document(original, LOCK)
    errors = []
    for name in sorted(set(original) | set(candidate)):
        if original.get(name) == candidate.get(name):
            continue
        if (name in policy['sha256'] or name in policy['protected_paths']
                or any(name.startswith(prefix) for prefix in policy['protected_prefixes'])):
            errors.append('protected change: ' + name)
        elif not (name in policy['allowed_paths']
                  or any(name.startswith(prefix) for prefix in policy['allowed_prefixes'])):
            errors.append('outside research scope: ' + name)
    if errors:
        raise ValueError('\n'.join(errors))
    state = verify(candidate)
    print('PASS: research-only change; trusted base=' + base + '; head=' + head)
    print('Principle review state: ' + state + ' (informational; not an approval token)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('verify')
    commands.add_parser('manifest')
    check = commands.add_parser('review')
    check.add_argument('--base', required=True)
    check.add_argument('--head', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'review':
            review(args.base, args.head)
        else:
            files = local_files()
            if args.command == 'manifest':
                Path(MANIFEST).write_text(json.dumps(hashes(files), ensure_ascii=False, indent=2) + '\n')
                print('Updated distribution manifest; foundation lock was NOT changed.')
            else:
                state = verify(files)
                print('PASS: manifest, foundation digests, exact source anchors and case structure')
                print('Principle review state: ' + state + '; semantic fidelity requires human review.')
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
