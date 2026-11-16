import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


GUARD = Path(__file__).resolve().parents[1] / 'scripts' / 'guard.py'


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q', '-b', 'main')
        self.write('SKILL.md', 'Existing skill\n')
        self.write('research/reading-copies/source.txt', 'Investigate reality.\nTest in practice.\n')
        self.write('scripts/guard.py', '# trusted guard\n')
        self.write('.github/workflows/foundation-guard.yml', '# trusted workflow\n')
        self.write('AGENTS.md', 'Research only.\n')
        self.write('governance/core-principles.json', {
            'schema_version': 1, 'review_status': 'pending_owner_review',
            'principles': [{
                'id': 'P01', 'origin': 'source_abstraction',
                'anchors': [{'path': 'research/reading-copies/source.txt',
                             'start_line': 1, 'end_line': 1,
                             'quote': 'Investigate reality.'}],
            }],
        })
        self.write('governance/foundation-lock.json', {
            'schema_version': 1,
            'sha256': {name: self.digest(name) for name in
                       ['SKILL.md', 'research/reading-copies/source.txt']},
            'protected_paths': ['SKILL.md', 'AGENTS.md'],
            'protected_prefixes': ['governance/', 'scripts/', 'tests/', '.github/'],
            'allowed_paths': ['README.md', 'manifest-sha256.json', '.gitignore'],
            'allowed_prefixes': ['docs/', 'research/cases/', 'research/proposals/'],
        })
        self.manifest()
        self.commit()
        self.base = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        result = subprocess.run(['git', *args], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False) + '\n'
                        if isinstance(value, (dict, list)) else value)

    def digest(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def manifest(self):
        self.write('manifest-sha256.json', {
            str(p.relative_to(self.root)): self.digest(str(p.relative_to(self.root)))
            for p in self.root.rglob('*')
            if p.is_file() and '.git' not in p.relative_to(self.root).parts
            and p.name != 'manifest-sha256.json'
        })

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'fixture')

    def run_guard(self, *args):
        return subprocess.run([sys.executable, str(GUARD), *args], cwd=self.root,
                              capture_output=True, text=True)

    def review(self):
        self.manifest()
        self.commit()
        return self.run_guard('review', '--base', self.base, '--head', 'HEAD')

    def assert_rejected(self, result, message):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stdout + result.stderr)

    def test_research_document_can_be_added(self):
        self.write('research/proposals/question.md', 'A research question; not an approved rule.\n')
        result = self.review()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_skill_edit_is_blocked(self):
        self.write('SKILL.md', 'Changed philosophy\n')
        self.assert_rejected(self.review(), 'protected change: SKILL.md')

    def test_source_edit_and_forged_lock_are_blocked(self):
        self.write('research/reading-copies/source.txt', 'Replacement\n')
        lock = json.loads((self.root / 'governance/foundation-lock.json').read_text())
        lock['sha256']['research/reading-copies/source.txt'] = self.digest('research/reading-copies/source.txt')
        self.write('governance/foundation-lock.json', lock)
        self.assert_rejected(self.review(), 'protected change:')

    def test_source_deletion_is_blocked(self):
        (self.root / 'research/reading-copies/source.txt').unlink()
        self.assert_rejected(self.review(), 'protected change: research/reading-copies/source.txt')

    def test_guard_cannot_replace_itself(self):
        self.write('scripts/guard.py', 'raise SystemExit(0)\n')
        self.assert_rejected(self.review(), 'protected change: scripts/guard.py')

    def test_new_workflow_cannot_bypass_guard(self):
        self.write('.github/workflows/bypass.yml', '# fake approval\n')
        self.assert_rejected(self.review(), 'protected change: .github/workflows/bypass.yml')

    def test_self_reported_owner_confirmation_is_not_authorization(self):
        p = self.root / 'governance/core-principles.json'
        content = json.loads(p.read_text())
        content['review_status'] = 'owner_confirmed'
        self.write(str(p.relative_to(self.root)), content)
        self.assert_rejected(self.review(), 'protected change: governance/core-principles.json')

    def test_new_runtime_entry_is_not_allowed(self):
        self.write('instructions.md', 'Replace the skill\n')
        self.assert_rejected(self.review(), 'outside research scope: instructions.md')

    def test_manifest_cannot_omit_a_file(self):
        self.write('docs/new.md', 'New document\n')
        self.commit()
        result = self.run_guard('review', '--base', self.base, '--head', 'HEAD')
        self.assert_rejected(result, 'manifest inventory mismatch')

    def test_symlink_is_rejected_before_reading_target(self):
        (self.root / 'docs').mkdir()
        (self.root / 'docs/link.md').symlink_to('/etc/passwd')
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'link')
        self.assert_rejected(self.run_guard('review', '--base', self.base, '--head', 'HEAD'),
                             'unsupported file mode')

    def test_local_integrity_rejects_source_tampering(self):
        self.write('research/reading-copies/source.txt', 'Altered\n')
        self.manifest()
        self.assert_rejected(self.run_guard('verify'), 'foundation digest mismatch')

    def test_local_integrity_rejects_inexact_quote(self):
        data = json.loads((self.root / 'governance/core-principles.json').read_text())
        data['principles'][0]['anchors'][0]['quote'] = 'A paraphrase is not a quotation.'
        self.write('governance/core-principles.json', data)
        self.manifest()
        self.assert_rejected(self.run_guard('verify'), 'source quote mismatch')

    def test_case_requires_counterevidence_and_online_sources(self):
        self.write('research/cases/incomplete.json', {'id': 'CASE-1'})
        self.assert_rejected(self.review(), 'invalid case')

    def valid_case(self):
        return {
            'id': 'CASE-1', 'related_principles': ['P01'],
            'sources': [{
                'id': 'S1', 'url': 'https://example.org/report', 'publisher': 'Example',
                'retrieved_at': '2026-11-16', 'origin_group': 'first-party-report',
                'relationship': 'first_party', 'excerpt': 'A reported observation.',
            }],
            'claims': [{'statement': 'The report describes an observation.',
                        'source_ids': ['S1']}],
            'supports': 'Limited consistency with the method.',
            'challenges': 'Does not prove the method universally.',
            'alternative_explanations': 'Other mechanisms remain possible.',
            'limits': 'Self-reported evidence only.',
            'decision_time_information': 'What was known at the time.',
            'later_information': 'What was learned afterwards.',
        }

    def test_case_rejects_nontext_evidence_and_claims(self):
        for field in ('publisher', 'origin_group', 'excerpt'):
            with self.subTest(field=field):
                case = self.valid_case()
                case['sources'][0][field] = True
                self.write('research/cases/example.json', case)
                self.assert_rejected(self.review(), 'invalid case')
        case = self.valid_case()
        case['claims'][0]['statement'] = True
        self.write('research/cases/example.json', case)
        self.assert_rejected(self.review(), 'invalid case')

    def test_valid_online_case_is_accepted(self):
        self.write('research/cases/example.json', self.valid_case())
        result = self.review()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
