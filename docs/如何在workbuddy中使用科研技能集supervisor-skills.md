# 在 WorkBuddy 中使用科研技能集 Supervisor-Skills

> 面向第一次用 AI 辅助做科研的同学。本文用 **「端侧轻量化故障诊断小模型训练方法」** 贯穿选题、文献调研、实验设计、论文写作和投稿前检查。以电机轴承振动信号为例：小模型在训练阶段接受知识蒸馏、部署时只保留学生模型，在同样的端侧资源预算下，能否更好地识别未见负载工况下的故障？

---

## 1. 这个技能集是做什么的

`supervisor-skills` 不是一个需要整体调用的技能，而是一组可以单独调用的科研技能。它适合在研究卡住时处理一个具体问题：选题是否站得住、实验能不能支撑主张、论文哪里说过头了，或者审稿意见该先回哪一条。

它不替你做实验，也不能把尚未核实的文献、结果或创新点变成事实。第一次使用时，**先选一个技能解决当前问题，不必让 WorkBuddy 一次跑完整条流程**。

## 2. 遇到什么问题，该选哪个技能

| 当前卡点 | 技能 | 应该期待的产出 |
| --- | --- | --- |
| 有想法，但不确定值不值得做 | [`idea-evaluator`](../research/supervisor-skills/idea-evaluator/SKILL.md) | 关键缺陷、可行性判断和下一步验证建议 |
| 想做一份深入的文献调研 | [`deep-research`](../research/supervisor-skills/deep-research/SKILL.md) | 带来源的综合分析、争议和证据缺口 |
| 已有技术方案，但论文逻辑没理顺 | [`tech-paper-template`](../research/supervisor-skills/tech-paper-template/SKILL.md) | 连接问题、方法、主张与验证的论文骨架 |
| 主要贡献是新的评测基准或系统性的评测研究 | [`benchmark-paper-template`](../research/supervisor-skills/benchmark-paper-template/SKILL.md) | 从研究缺口、数据构建到实验与论文结构的检查清单 |
| 论文逻辑已明确，想起草引言 | [`intro-drafter`](../research/supervisor-skills/intro-drafter/SKILL.md) | 基于已有研究材料的引言草稿 |
| 有实验、图表或笔记，想写某一节正文 | [`paper-writer`](../research/supervisor-skills/paper-writer/SKILL.md) | 基于作者材料的章节草稿，以及缺失材料的提示 |
| 不知道论文里该画哪些图、怎么表达 | [`figure-designer`](../research/supervisor-skills/figure-designer/SKILL.md) | 动机示例、方案总览或实验结果图的设计建议 |
| 已有参考图，需要可编辑版本 | [`drawio-reconstruction`](../research/supervisor-skills/drawio-reconstruction/SKILL.md) | 可编辑的 `.drawio` 文件；渲染环境可用时可提供 PNG 预览 |
| 已有正文，只想改善语言 | [`paper-polish`](../research/supervisor-skills/paper-polish/SKILL.md) | 保留原意的学术表达修改 |
| 已有完整稿件，想模拟投稿前检查 | [`pre-submission-reviewer`](../research/supervisor-skills/pre-submission-reviewer/SKILL.md) | 分严重程度的审查意见，覆盖逻辑、写作、语法、LaTeX 和图表等 |
| 收到审稿意见，不知怎么回应 | [`rebuttal-guidance`](../research/supervisor-skills/rebuttal-guidance/SKILL.md) | 意见分类、回应优先级和策略，而不是代写完整回复 |
| 想为 AI 辅助编程、写作和制图建立检查习惯 | [`vibe-research-workflow`](../research/supervisor-skills/vibe-research-workflow/SKILL.md) | 分场景的协作流程和人工核查建议 |

如果只是想知道**先精读哪几篇论文**，先用 [research-weave 的 Scout 模式](../research/research-weave/SKILL.md)；如果已经确定问题，要综合多篇文献解释结论和分歧，再考虑 `deep-research`。

## 3. 在 WorkBuddy 中安装并确认可用

### 3.1 先确认来源和许可

技能来自 [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills)。上游技能集整体采用 **CC BY-NC-SA 4.0**，不受本仓库其他内容的 MIT 许可覆盖。各技能和附带资源可能有不同许可；使用、改编或分发前，请先核对[来源与许可说明](../research/supervisor-skills/references/PROVENANCE.md)。

### 3.2 按子技能导入，不要把外层目录当作单个技能

1. 在本仓库的[技能集目录](../research/supervisor-skills/)中找到各个含 `SKILL.md` 的子目录。建议成组安装 12 个，避免某个阶段需要接力时找不到下一个技能。
2. 在 WorkBuddy 打开研究项目，再到 **技能 → 添加技能 → 上传技能**，按客户端提示逐个导入本地技能包。若客户端要求压缩包，按**一个技能一个包**准备，保留该子目录的完整内容（如 `references/`、`scripts/`），不要只上传 `SKILL.md`。通过界面上传的技能默认可跨项目使用；若只想在当前项目使用，按该版本[官方技能说明](https://intl.cloud.tencent.com/zh/document/product/1316/84503)使用项目级技能目录。
3. 在技能管理页确认技能已启用，然后在对话中用英文技能名发起一次简短测试。本仓库没有预装 WorkBuddy 专用副本，仅打开仓库不等于已安装。

项目级安装时，各子技能应在技能根目录下并列，而不是再套一层 `supervisor-skills`：

```text
<项目技能根目录>/
├── idea-evaluator/
│   ├── SKILL.md
│   └── references/
├── tech-paper-template/
│   ├── SKILL.md
│   └── references/
└── ...（其余子技能并列）
```

可以把下面这段发给 WorkBuddy 做一次最小验证：

```text
请使用 idea-evaluator 评估这个初步想法：用知识蒸馏训练一个在低功耗开发板上运行的电机轴承故障诊断小模型。先指出一个最可能让选题不成立的问题，以及验证它需要的数据和设备，不要撰写论文。
```

如果技能没被调用，先检查它是否启用、当前打开的是不是预期项目、`SKILL.md` 是否位于对应子目录，以及是否误把整个技能集导入成一个包。不要仅凭一段看起来合理的回答判断安装成功。

## 4. 完整案例：端侧轻量化故障诊断小模型训练方法

### 4.1 用 `idea-evaluator` 把课题缩成一个可验证的问题

“训练一个更准、更快的故障诊断小模型”很难直接验证。先固定任务：用电机轴承的振动信号区分正常状态和几类已知故障；把**训练时是否使用知识蒸馏**作为主要变量。教师模型只在训练时提供监督，部署时两组都使用相同结构的学生模型。这里的“未见负载工况”指测试负载不出现在训练或调参数据中，不是识别训练中从未出现的故障类别。

```text
请使用 idea-evaluator 评估课题「端侧轻量化故障诊断小模型训练方法」。
研究问题：用教师模型蒸馏训练的轴承故障诊断小模型，相比同结构的普通监督训练模型，能否在未见负载下取得更高的宏平均 F1，同时满足端侧延迟和内存预算？
目前条件：计划使用有故障和工况标注的公开振动数据，并选择一块低功耗开发板；尚无实验结果，具体资源预算待确认。
我的决策：是否值得先做小规模验证。请指出最可能使课题不成立的问题、需要核实的相关工作和最低可行实验，并区分已知条件与待验证假设。
```

一个有用的回答可能会指出：知识蒸馏本身不是创新。先看相关工作是否已在同类工况和硬件约束下回答了同一个问题。也可以先确认普通小模型能否在目标板运行，以及数据能否按负载和原始采集记录可靠地划分，再决定是否投入后续训练。

### 4.2 用 `deep-research` 查缺口，再用 `tech-paper-template` 设计对照

先让 `deep-research` 帮你比较论文实际测了什么，而不只是罗列诊断准确率：

```text
请使用 deep-research 调研轴承振动故障诊断中的知识蒸馏、跨负载评估和端侧小模型部署。逐篇注明是否用同结构的非蒸馏模型作对照、如何划分工况和原始采集记录，以及延迟和内存是硬件实测还是估算。请给出可核查的来源，区分已读正文、仅见摘要和无法核实的材料；不要把“没有检索到”写成“没人做过”。
```

如果当前环境无法联网，就先提供已核实的论文和笔记，让 WorkBuddy 基于现有材料分析。核对后，把调研结论和资源约束交给 `tech-paper-template`：

```text
请使用 tech-paper-template，把选题评估和文献笔记整理成“问题 → 方法 → 主张 → 验证”的论文骨架，先不要写正文。
对照：同一轻量一维卷积模型分别做普通监督训练和蒸馏训练；两组使用相同的数据、输入预处理和部署配置。若采用 INT8，两个学生模型都用同一量化流程，校准不使用测试数据。
数据划分：预先保留测试负载；其余负载中的训练、验证按原始采集记录分组，划分后再切窗。教师模型也不能使用留出的测试数据。
评估：报告未见负载上的宏平均 F1 和各故障类召回率；在同一块开发板上按相同输入长度和计时范围测量推理延迟与峰值内存，并明确计时是否包含预处理。先确认预算和验收标准，再看结果。
请为每条主张列出所需的证据、失败条件和不能外推的范围。没有实测的结果留空，不要编造数据。
```

拿到骨架后，重点检查两件事：**诊断收益**是否来自公平对照，**端侧可行性**是否有目标板实测。即使蒸馏提高了离线 F1，也不能据此说模型更快或更省电。延迟和内存看实测值；想主张更省电，就要另外测量能耗。仅在公开数据的未见负载上验证，也不等于能泛化到其他设备或现场。

### 4.3 有材料再写；有完整稿件再审

| 已准备的材料 | 可以怎样继续问 |
| --- | --- |
| 已核实的文献和论文骨架 | “请用 `intro-drafter` 起草引言，说明为什么要同时评估未见负载上的故障诊断表现和端侧资源开销；不要把研究假设写成已证实的贡献。” |
| 数据划分记录、训练配置、诊断指标和开发板日志 | “请用 `paper-writer` 写实验小节，交代教师与学生模型的训练数据、两组的区别、未见负载表现和目标板测量方法；未测的指标标为待补。” |
| 已有稿件和对照图表 | “请用 `pre-submission-reviewer` 审查是否存在切窗数据泄漏、对照组不公平，或把跨负载结果夸大为跨设备泛化。按严重程度列出相关段落或图表和修改建议，不直接改稿。” |

如果只想改英语表达，用 `paper-polish`；若问题是论证缺证据，先补实验证据，不要靠润色把语气写得更肯定。收到审稿意见后，再把意见原文、稿件和可补实验的时间交给 `rebuttal-guidance`，让它帮助区分“需要补证据”和“可以澄清表述”的问题。

## 5. 常见问题

- **能不能一句话让它做完整篇论文？** 不建议。每一轮先确认一个交付物，再把你认可的结果带到下一阶段。尤其不要为了填满草稿而编造引用、数字或实验设置。
- **为什么 `deep-research` 没有给出可核查的来源？** 检查当前会话是否具备检索能力，关键论文是否能访问。没有全文时，明确哪些判断只依据摘要，必要时自行补齐材料。
- **为什么没有生成 Draw.io 预览？** 文本类技能一般不需要单独安装脚本依赖，但 `drawio-reconstruction` 的脚本需要 Python 3；导出 PNG 预览需要 draw.io CLI，部分图像辅助操作可用 Pillow。是否可执行还取决于 WorkBuddy 的权限和环境，详见 [Draw.io 依赖说明](../research/supervisor-skills/drawio-reconstruction/README.zh-CN.md#依赖要求)。
- **能不能直接上传企业设备的振动记录？** 先确认数据授权和单位的工具使用规定。可以用公开数据、经批准的脱敏样例或汇总指标来讨论；不上传未经授权的原始振动记录、设备编号或生产工艺参数。

**新手速查：** 有想法先用 `idea-evaluator`；证据不足就先调研和做实验；有真实材料再用 `intro-drafter` 或 `paper-writer`；有完整稿件再用 `pre-submission-reviewer`。最终由作者核对引用、数据和论文主张。

更多信息见[仓库中文导读](../research/supervisor-skills/README.zh-CN.md)与 [WorkBuddy 官方技能说明](https://intl.cloud.tencent.com/zh/document/product/1316/84503)。
