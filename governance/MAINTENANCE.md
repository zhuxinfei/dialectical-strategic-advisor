# 持续蒸馏与底座维护

## 目标与当前状态

主线是原文精读 → 论证还原 → 跨篇综合 → 条件化蒸馏 → 联网案例检验 → 回读原文 → 提交候选修订。原文确定思想归属，事实检验现实有效性；两项分别审阅。

当前7项核心原则是待审核候选，不代表完整毛泽东思想体系，也不代表用户已确认。既有skill含现代限缩和用户增补，本次没有重写其正文；保护现有字节不等于裁定现有解释永远正确。应先经用户审核原则表，再考虑拆分不可自动修改的核心和可演进的应用模块。

## 两条修改路径

**普通研究路径：** 在 `codex/` 分支新增 `research/cases/`、`research/proposals/` 或 `docs/`；允许同步README、根目录gitignore和全量manifest。通过检查后仍由维护者决定是否合并。新案例、提案、评分或自报审核字段不会成为现行skill，也不会获得改写底座的权限。

**底座维护路径：** 修改skill、原典、副本、既有证据、原则表、检查器或工作流，普通门禁一律拒绝。维护者先取得所有者对具体变更、base/head SHA和原文论证的明确批准，再开启有范围、有时限的维护窗口。窗口内仅实施已批准变更，运行完整测试、复查指纹及思想差异，恢复并回读main保护设置；记录批准证据、前后SHA及恢复结果。没有代码内的 `--approve`、标签绕过或自报批准开关。

初次bootstrap仅安装治理设施；原则候选仍待审。此后的每次底座维护都需要新的具体授权，不能沿用本次实施授权。维护者不会要求普通研究者自行关闭保护。

## 论证记录与联网取证

一项提案至少写明：实际问题；原文问题和上下文；旧解释→新解释；相关原则编号；原文依据；跨篇张力；现代补充；案例支持与反例；不确定性；首个验证动作、依赖、验收和停止条件。不得只提交新增口号或成功故事。

案例采用JSON（见已联网读取的 `research/cases/github-2018-outage.json`），字段由检查器校验：

- `id`、`related_principles`；关联仅表示分析问题，不表示该案例证明原文普遍成立。
- `sources`：每条有 `id`、实际读取的HTTPS `url`、`publisher`、`retrieved_at`、`origin_group`、`relationship` 和短 `excerpt`。`relationship` 为 `first_party` / `independent_reporting` / `republication`。
- `claims`：每项 `statement` 明确关联 `source_ids`，关键数字和因果说法标清谁报告、谁核验。
- `supports`、`challenges`、`alternative_explanations`、`limits`：均须填写有意义的文字。
- `decision_time_information`、`later_information`：区分当时能知道与事后才知道的材料。

优先一手材料；寻找独立报道、反面材料和不同解释。报道即使由另一家媒体撰写，若关键事实仍来自同一官方复盘，应使用相同 `origin_group`，不能计为独立事实验证。只有单方材料时可收录，但必须限制结论。网页无法访问、时间线不完整、材料有冲突，都留在 `limits` 或研究记录中；不得用模型记忆补成已核验事实。

CI仅校验结构、可追溯字段和引用一致性，不会上网访问不可信URL，也不裁定网页真实性或独立性。每次实际研究由研究者联网读取；定期抽查失效链接，不编造“已交叉验证”。涉及个人隐私的原始案例不提交公开仓库。

## 门禁的可信边界

`foundation-lock.json` 固定原有26个skill/研究文件的字节指纹；根manifest覆盖当前所有交付文件。两者作用不同：更新manifest不等于获准重写底座。

GitHub `foundation-guard` 在 `pull_request_target` 中检出base SHA的受信任代码，只把head当Git对象读取；不检出或执行候选脚本，不读取候选工作流执行指令。候选即使同时改skill、基线和检查器，也会被base策略拒绝。符号链接、子模块和范围外入口同样拒绝。读取的是完整base/head差异，不是只检查最后一次提交。

普通 `verification` 测试用于发现实现错误，运行候选代码，权限为只读，无凭证持久化或机密，不能代替受信任的底座门禁。只有base运行的 `foundation-guard` 是main必需的检查；保护设置将其绑定到GitHub Actions来源。维护者不要把候选分支跑出的同名结果视为独立授权。

GitHub main应要求PR、最新base及 `foundation-guard`，禁止强推与删分支，对管理员也生效；不配置自动合并。个人仓库所有者不能批准自己提交的PR，因此不假装“所有者本人创建PR＋一条必需review”就实现了独立人审。本轮采用技术门禁＋维护者手动合并；语义人审是另一个有记录的步骤。

## 身份隔离与不能承诺的事情

分支保护不是对仓库所有者的永久限制；管理员可修改设置。若自动化持有同一个所有者token，它也能关闭保护。不得声称已经实现不可绕过的自进化。

后续无人值守运行使用独立GitHub App或其他受限身份，只授予指定仓库的研究所需内容/PR权限；不授予管理、工作流修改、审核、状态写入、检查结果写入权限，不注入所有者token和机密。它不能改工作流制造同名成功检查。即使同为GitHub Actions来源，拥有工作流写权限的身份仍可能伪造检查，所以单靠check名称或app绑定不够。

当前会话使用所有者gh认证；本轮可以验证门禁和实际分支设置，无法证明此身份没有管理能力。无人值守前，用户须在独立身份完成权限配置；完成后另做负向权限验证。当前没有创建无人值守自动化。

## 日常命令与回退

```bash
python3 scripts/guard.py manifest
python3 scripts/guard.py verify
python3 -m unittest discover -s tests -v
python3 scripts/guard.py review --base origin/main --head HEAD
git diff --check
```

保留每次正式提交SHA，原始版本为 `207ff323c7371b448f2db89732b51f2b65ef99f9`。普通研究可以PR撤回；受保护内容回退也走底座维护路径，不能借回退之名绕过审批。不要通过重置或强推抹去审核记录。
