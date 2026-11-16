# 毛选方法论 · 辩证战略参谋

基于《毛泽东选集》四卷的研究记录整理而成的 AI skill，用于复杂决策、资源约束、多方协作、长期规划与受挫复盘。

它把实事求是、矛盾分析、条件建设和实践反馈转化为可操作的参谋协议。原文方法、跨域抽象、现代工程接口与用户增补分别说明，不以引用权威代替事实核验，也不把普通分歧自动转化为对抗。

## 核心内容

- **6 条认知公理**：从事实形成判断，再用行动校准；分析条件、关系与主次。
- **4 步决策协议**：态势感知 → 矛盾分析 → 战略规划 → 动态反馈。
- **4 种态势**：强弱悬殊、错综复杂、受挫调整、优势发展。
- **5 条自检**：检查教条、冒进、无限妥协或对抗、单点迷信，以及物质基础与反馈责任。

完整入口见 [SKILL.md](SKILL.md)。

## 安装

仓库根目录就是 skill 目录；目录名应保持为 `dialectical-strategic-advisor`。

### Claude Code

```bash
git clone https://github.com/zhuxinfei/dialectical-strategic-advisor.git \
  ~/.claude/skills/dialectical-strategic-advisor
```

### Codex

```bash
git clone https://github.com/zhuxinfei/dialectical-strategic-advisor.git \
  ~/.codex/skills/dialectical-strategic-advisor
```

目标目录已有同名 skill 时，先备份或比较版本。安装后开启新会话，使工具重新发现 skill。其他支持 `SKILL.md` 的工具可按其技能目录约定安装。

## 使用示例

在支持 `$技能名` 的工具中显式调用：

```text
$dialectical-strategic-advisor
我们只有两名开发，预算有限，同时面对交付延期和客户流失。
请先区分事实与假设，分析主要约束，给出首个可逆行动及调整条件。
```

也可以要求工具读取本仓库的 `SKILL.md`，再描述问题。尽量提供目标、期限、资源、不可接受的代价、已有证据和关键未知；缺少材料时先形成条件判断，不编造确定答案。

## 目录与研究链

```text
SKILL.md                       当前可安装版本
README.md                      项目与使用说明
manifest-sha256.json            本整理版全部交付文件的 SHA-256
research/
  article-index.json           159 篇索引
  evidence-volume-{1..4}.md     按卷逐篇证据与迁移条件
  CROSS-VOLUME-SYNTHESIS.md     跨卷机制归纳与技能映射
  reading-copies/              研究时使用的阅读副本与附录
  history/                    4 个历史 skill 快照
  provenance.json             原始语料指纹与编码
  original-manifest-sha256.json 原始归档指纹（整理前）
  *.md                        历次验收、修复与校准记录
```

阅读顺序建议：当前 skill → [跨卷综合](research/CROSS-VOLUME-SYNTHESIS.md) → 对应卷证据 → 阅读副本。证据中的 V1—V4、L/R 行号指阅读副本物理行，不是出版页码；不同版本的文本不能直接套用这些行号。[article-index.json](research/article-index.json) 中的起止行号对应原始语料，不能直接用于阅读副本；字符数、标题和卷号用于辅助核对。

## 版本与验证边界

现行 skill 为 2026-11-06 原文回查后的版本；2026-11-16 整理上传。`SKILL.md` 与原本已安装版本保持字节一致，本次没有重写决策规则。

原始归档的 25 个文件已逐项核对 SHA-256。公开整理版保留研究记录与阅读副本，将机器绝对路径改为仓库相对路径；PDF 和原始 `MX1-4.txt` 未包含于仓库。历史记录中的文件位置、行号、工具输出与验收结论对应当时版本，不应视作当前版本重新通过了同样评测。

- [初版验收](research/VALIDATION-RESULTS.md)：结构检查、工具扫描和静态反例走查。
- [独立验收](research/INDEPENDENT-ACCEPTANCE.md)：六组规则定向抽查，随后有[验收修复](research/ACCEPTANCE-REPAIR.md)。
- [使用反馈校准](research/CALIBRATION-UPDATE-20261106.md)与[原文回查](research/SOURCE-GROUNDED-UPDATE-20261106.md)：区分事实、解释与推荐强度。

已有记录不构成独立模型 A/B、真实决策效果或历史事实全部核验的证据。本次整理仅验证文件、格式和可移植性，不宣称能力提升。

核验当前整理版文件：

```bash
python3 - <<'PY'
import hashlib, json
from pathlib import Path
root = Path('.')
manifest = json.loads((root / 'manifest-sha256.json').read_text())
for name, expected in manifest.items():
    actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
    assert actual == expected, f'文件不一致：{name}'
print(f'通过：{len(manifest)} 个文件')
PY
```
