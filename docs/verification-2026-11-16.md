# 底座保护实施验证记录

日期：2026-11-16。原始发布提交：`207ff323c7371b448f2db89732b51f2b65ef99f9`。

## 已实际完成

- 原始skill及既有研究共26个文件固定指纹，保持字节一致；原有阅读副本未改写。
- 7项方法论原则候选、13处逐字原文锚点；检查器核对行号和完整引文，状态仍为 `pending_owner_review`。
- Python标准库门禁和15项临时Git仓库回归测试全部通过，包括合法研究、删改原文、伪造基线、替换检查器、新工作流、自报审核、额外入口、遗漏manifest文件、符号链接、错误引文和无文本证据。
- 测试先运行失败，再实施检查器。独立代码审查发现案例字段真值检查可接受布尔值；已补非空字符串校验和回归测试，观察旧实现失败后修复通过。
- 交付清单、原文指纹、引文、案例结构及 `git diff --check` 均通过。
- 实际联网读取GitHub官方2018事故复盘及同期Hacker News讨论，保存URL、日期、短摘录、来源依赖、反例和无法证明的结论。技术事实主要是官方自报，公开评论不当独立事故核验。候选媒体404及不可用检索没有计入成功来源。
- 项目约束、研究流程、维护窗口、PR模板和只读CI均已编写；没有改动原skill规则，没有创建定时运行、自动合并或自动发布。

## GitHub验证阶段

- [Bootstrap PR #1](https://github.com/zhuxinfei/dialectical-strategic-advisor/pull/1) 已合并，main设施提交为 `233bbfd445962994c506fc1016f2aecc5ff0478a`。分支与PR的 verification 均通过，实际包含15项测试和完整性校验。
- CLI OAuth缺少workflow权限时没有扩权；用户明确允许后，通过已登录Chrome提交两个工作流。远端文件与本地测试文件逐字节一致。
- [负向验证 PR #2](https://github.com/zhuxinfei/dialectical-strategic-advisor/pull/2)：候选 `47b804a51a6f636e03488326aaa3ec430a4e7061` 仅追加skill测试注释并刷新manifest。可信base门禁失败，日志为 `FAIL: protected change: SKILL.md`；对应check-run的head_sha确实为候选SHA，来源GitHub Actions app 15368。[运行记录](https://github.com/zhuxinfei/dialectical-strategic-advisor/actions/runs/43794628588)。测试PR已关闭，未合并，main skill没有变化。
- main分支保护PUT后已GET回读：必需 `foundation-guard` 且绑定app 15368、strict=true、enforce_admins=true；禁止force push和删除；要求PR、解决讨论；未要求独立审批票数（个人所有者不能审批本人PR），没有自动合并。
- 启用保护后PR #2的API `mergeable_state` 为 `blocked`。没有为了试验尝试强行合并底座修改。
- [正向验证 PR #3](https://github.com/zhuxinfei/dialectical-strategic-advisor/pull/3)：仅更新文档和manifest；候选 `c207e59fc7cbce2f4bb588795f30ce6e31e89fc8` 的 foundation-guard 与 verification 均成功，check-run head_sha为该候选，API合并状态为 `clean`。[门禁运行](https://github.com/zhuxinfei/dialectical-strategic-advisor/actions/runs/43794900353)。本次补记后仍需最新CI通过再手动合并；最终提交和合并状态以PR记录为准。原文含义审核和独立身份限制仍见下节。

## 不能由本次工程替代的事项

- 用户逐条审核原则候选，特别是P04原文强断言与现行skill现代限缩的关系，以及候选范围是否覆盖用户期待的基本立场。
- 无人值守前配置独立研究身份，拒绝管理/工作流/检查/状态写权限并实际做负向权限测试。当前会话的所有者认证仍有管理能力，不声称已隔离。
- 技术校验不裁定思想含义，也不构成独立模型A/B、现实决策成效或历史事实全量核验。
