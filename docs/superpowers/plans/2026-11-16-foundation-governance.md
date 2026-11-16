# 毛选思想底座保护与持续蒸馏 Implementation Plan

> **For agentic workers:** 按本 checklist 顺序执行；本轮由当前执行者逐项实施与自检，不另起会话。涉及思想归属的候选表保留用户审核状态，不能把完成工程实施解释成用户批准思想内容。

**Goal:** 在保留当前 SKILL.md 和阅读副本的基础上，建立可追溯的原则候选、联网案例流程及无法由普通研究 PR 自行解除的变更检查。

**Architecture:** Python 标准库读取 Git 对象，不执行候选分支代码；pull_request_target 从目标分支取得可信检查器，比较确切 base/head。保护既有技能、研究原件及治理代码；普通研究只能增加案例、提案和说明。GitHub main 要求通过检查并经 PR 合并，自动化不负责发布或合并。

**Tech Stack:** Git、Python 3 unittest / hashlib / json、GitHub Actions、gh CLI。

## 保护范围及实际边界

- 技术检查能保护字节、路径、引用与变更范围，不能自动裁定思想忠实度。
- 核心原则是基于原文的候选提炼；没有用户逐条确认前，不标记 approved。
- 现有所有者凭证拥有修改仓库设置的权限。本轮不伪造独立身份或永久不可绕过的保证。
- 新增底座保护是一次 bootstrap。普通 PR 不能修改检查器、工作流、基线或现行 skill；未来需改变这些文件时，由所有者明确授权维护窗口，审查前后 SHA 后恢复保护。不得让 PR 自报审批来绕过。

## 文件职责

| 路径 | 职责 |
|---|---|
| governance/core-principles.json | 原文锚点、候选原则、适用边界、来源类别与待审核状态 |
| governance/CORE-PRINCIPLES.md | 面向人的候选原则审阅表与原文入口 |
| governance/foundation-lock.json | 当前技能及既有研究材料的固定指纹 |
| governance/MAINTENANCE.md | 演进流程、角色、联网取证、审核与维护窗口 |
| scripts/guard.py | 本地完整性检查、Git base/head 变更门禁、manifest 生成 |
| tests/test_guard.py | 真实临时 Git 仓库的破坏性变更回归测试 |
| .github/workflows/foundation-guard.yml | 只执行 base 中的检查器，读取 head 数据 |
| .github/workflows/verify.yml | 只读权限运行本地测试与完整性校验 |
| .github/PULL_REQUEST_TEMPLATE.md | 原文忠实度与现实适用性分开审阅 |
| AGENTS.md | 维护者的项目约束与可执行命令 |
| research/cases/ | 已联网取证的辅助案例，非底座思想来源 |
| research/proposals/ | 修改建议，不能被自动当作已生效 skill |
| docs/verification-2026-11-16.md | 实际检查结果与尚未完成的人类决策 |

## Checklist

- [x] 1. 检查本地与远端：main 没有分支保护，Actions 默认只读且禁止自动批准 PR。
- [x] 2. 写技术方案，创建 codex/foundation-governance 分支。
- [x] 3. 回读原文锚点，形成来源明确的候选原则表；隔离现代工程接口和用户增补。
- [x] 4. 先写 unittest：合法研究通过，底座/检查器/工作流修改、删文件、伪造指纹、符号链接与缺失引用被拒绝；实际观察失败后实施检查器。
- [x] 5. 固定当前技能与研究材料指纹；实现全量 manifest 与 Git 对象门禁。
- [x] 6. 编写联网案例及提案规范，实际读取至少一项一手案例来源及独立来源，记录来源依赖和检索时间。
- [x] 7. 编写只读 CI、PR 审核模板与项目维护约束；不新增自动合并、自动发布或定时任务。
- [x] 8. 完整运行测试、引用/指纹校验、格式检查；核对原技能与原文副本保持原字节。
- [x] 9. 提交、推送，创建 PR 并完成 bootstrap CI 验证；核对具体 diff 后合并工程设施。
- [x] 10. 启用 main 分支保护并读取设置确认；实测普通研究 PR 可通过、受保护改动会失败，关闭试验 PR。
- [x] 11. 保存实际验证报告，核对最终远端与本地；列出需要用户确认的事项。

## 验证命令与验收条件

```bash
python3 -m unittest discover -s tests -v
python3 scripts/guard.py verify
python3 scripts/guard.py review --base origin/main --head HEAD
git diff --check
```

本轮 bootstrap 的 governance / scripts / workflows 新增尚不受旧 main 的检查器保护，先运行测试再由已获授权的维护者合并。后续研究 PR 的 review 必须 PASS；修改受保护文件的 PR 必须失败，并列出路径，不依赖候选分支提交的标签、审批字段或新检查器。

## 需要用户完成的决策

- [ ] 审核并确认核心原则候选表，或提出原文理解上的修改。实施本方案不代替此审核。
- [ ] 为后续无人值守自动化配置独立、无仓库管理权限的身份；研究写入分支，仓库管理凭证由用户掌握。本轮没有创建定时运行器，也不需要为当前手动研究新增凭证。
