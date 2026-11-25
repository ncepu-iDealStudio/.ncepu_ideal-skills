# research 技能分类说明

本目录收录面向**科研全流程**的 AI Agent Skills，覆盖从选题立项、文献调研、实验设计、论文写作到投稿答辩的完整研究生命周期。

## 技能总览

| 技能包 | 子技能数 | 定位 | 许可证 |
|---|---|---|---|
| supervisor-skills | 12 | 科研"导师"系列：选题评估、写作、润色、审稿、答辩 | CC BY 4.0 / CC BY-NC-SA 4.0 |
| auto-empirical-research | 6 | 实证研究自动化：找 idea、查文献、设计实验、验证引用 | CC BY-SA 4.0（合集；另查各上游资源） |
| research-weave | 1 | 文献证据网络：追溯学术谱系、梳理研究脉络 | MIT |
| best-paper-writing | 1 | 顶会最佳论文风格写作（60 篇获奖论文蒸馏） | CC BY 4.0 |
| agentero-skills | 2 | 论文精读讲解 + ML 论文写作示例库 | MIT |

## 各技能详细介绍

### 1. supervisor-skills — 科研导师技能集（12 项）

来源：[HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills)（香港科技大学团队）

模拟一位经验丰富的科研导师，按研究阶段分工：

- **vibe-research-workflow**：AI 辅助科研总工作流（Vibe Coding / Vibe Figure / Vibe Writing 三个子流程），用户主导学术判断、AI 承担机械工作。**适合作为整套技能的入口**。
- **idea-evaluator**：评估初步研究想法（五维框架：更高/更快/更强/更省/更广，附致命缺陷检查）。**在有了粗略 idea、不确定是否值得做时使用**。
- **deep-research**：调研级深度文献综述——冻结研究问题、多对抗视角检索、逐条验证引用、MECE 证据综合。**开题前做系统文献调研时使用**。
- **tech-paper-template**：用思考模板表搭建技术论文全文逻辑骨架（背景→局限→目标→挑战→方法→贡献）。**动笔前理清论文逻辑时使用**。
- **intro-drafter**：按六段式流程图起草 Introduction 正文。**论文 Introduction 写不出来时使用**。
- **paper-writer**：基于作者自己的材料起草可发表的论文段落乃至全文，每条事实性陈述可溯源。**初稿写作时使用**。
- **paper-polish**：润色已有学术文本——语法与流畅度修复、语气与证据强度校准、去除 AI 味、中译英。**完稿打磨时使用**。
- **figure-designer**：设计论文三大核心图（图 1 动机示例、方法总览图、实验结果图）。**画图没思路时使用**。
- **drawio-reconstruction**：把参考图片（架构图、截图等）重建为高保真、可编辑的 .drawio 文件。**需要复刻或修改他人图的版式时使用**。
- **benchmark-paper-template**：用五支柱框架（研究空白/构建流水线/评测框架/实证发现/可选配套方法）结构化 Benchmark 论文。**写评测基准类论文时使用**。
- **pre-submission-reviewer**：投稿前模拟审稿，从宏观逻辑、写作细节、英语语法、LaTeX 格式、图表质量五个维度给出严重度分级意见。**投稿最后一道关使用**。
- **rebuttal-guidance**：审稿意见回复（rebuttal）策略指导——按审稿人心态匹配说服策略，不直接代写全文。**收到审稿意见后使用**。

### 2. auto-empirical-research — 实证研究自动化（6 项）

来源：[brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)（斯坦福团队出品，本仓库选择性收录 6 项）

从研究方向到落地实验的自动化流水线：

- **idea-discovery**：找 idea 全流程——从宽泛方向出发，产出经试点验证的想法清单。**从零开始找研究方向时使用**。
- **dblp-api**：通过 DBLP 检索计算机科学领域的论文、作者、会议期刊。**查某位学者/某个会议的发表记录时使用**。
- **openalex**：通过 OpenAlex 检索学术文献元数据（DOI、ORCID、h 指数、引用追踪、机构信息）。**跨学科文献检索与引用分析时使用**。
- **bibliometrix-guide**：用 R 的 bibliometrix 包做科学制图与文献计量分析。**需要做领域文献计量、共被引分析时使用**。
- **experiment-plan**：把研究方案转化为以论点为核心的详细实验路线图（消融矩阵、评测协议、运行顺序、算力预算）。**idea 确定后、动手实验前使用**。
- **check-citations**：联网对照 CrossRef / Semantic Scholar / OpenAlex 验证参考文献真实性，识别 AI 幻觉引用。**审稿、核查引用、防 AI 编造文献时使用（本仓库已实测可用）**。

### 3. research-weave — 文献证据网络（1 项）

来源：[NeuraLiying/research-weave-skill](https://github.com/NeuraLiying/research-weave-skill)

围绕一个具体研究问题：找到并优先排序该读哪些论文，重构思想脉络（intellectual lineage），把散落的论断编织成证据网络，调查相互矛盾的发现。

**适用场景**：需要决定"该读什么"、"前人工作到底确立了什么"、"我的工作在竞争性解释中处于什么位置"时。**不适用**于简单参考文献列表或单篇论文摘要。

### 4. best-paper-writing — 顶会最佳论文风格写作（1 项）

来源：[gulucaptain/Best-Paper-Writing-Skill](https://github.com/gulucaptain/Best-Paper-Writing-Skill)

从 60 篇 CVPR/ICCV/NeurIPS 最佳论文中蒸馏的写作风格：起草或重写标题、Abstract、Introduction、Method、Experiments，并按获奖论文的版式规划与绘制论文配图，可直接写入 CVPR author kit 等 LaTeX 模板。

**适用场景**：两种入口——(A) 填写 intake 表单（描述问题、想法、方法、结果），(B) 粘贴已有摘要让推理更有说服力。**追求顶会投稿质量时使用**。不适用于 related work 综述、rebuttal 或纯校对。

### 5. agentero-skills — 论文精读与写作示例库（2 项，已独立化改造）

来源：[poco-ai/Agentero](https://github.com/poco-ai/Agentero)（上游为 Tauri 桌面应用，本仓库已剥离应用绑定、改造为可独立使用）

- **paper-reader**：中英文精读单篇科研论文。支持本地 PDF、链接或粘贴文本，默认在对话中交付讲义，按需保存笔记。**读不懂论文或需要精读笔记时使用**。
- **research-paper-writing**：面向 ML/CV/NLP 论文的写作质量提升，附 37 个真实获奖论文的写作示例库（Abstract/Introduction/Related Work/Method/Experiments 各节的模板与范例）。**写作某一节不知道怎么组织时查阅对应示例**。

## 使用说明

1. **安装单位**：安装包含 `SKILL.md` 的整棵子目录，保留其中的 `references/`、`scripts/`、`assets/` 等资源。入口的 YAML 至少有 `name` 和 `description`；不要把合集外壳当成技能，也不要只复制入口文件。分发或分享前，按对应来源说明附上合集或技能级许可与署名。
   - **WorkBuddy**：在「技能 → 添加技能 → 上传技能」导入本地包，启用后点名验证。若客户端要求压缩包，一个技能一个包，保留技能名目录。项目级路径以当前客户端的[官方技能说明](https://intl.cloud.tencent.com/zh/document/product/1316/84503)为准。
   - **DSH**：将各技能并列放进研究项目的 `.dsh/skills/` 或 `.agents/skills/`。例如 `.dsh/skills/research-weave/SKILL.md`。DSH 不递归发现嵌套技能；出现同名目录先检查现有版本，不覆盖。参见 [DSH 技能文档](https://deepseek-harness.github.io/deepseek-harness/reference/subsystems/skills)。
   - 若宿主没有技能注册功能，可以点名让助手读取对应入口并按文档执行；这不等同于自动发现。
2. **补充资料**：多数技能在 `references/` 子目录存放详细方法论与示例，AI 会在需要时按 SKILL.md 的指引加载，无需人工预读。
3. **许可合规**：本目录收录技能多数为 CC 系列（署名/非商业/相同方式共享）或 MIT 许可，使用前请阅读各技能包内的 `LICENSE` 与 `references/PROVENANCE.md`（含来源署名与本地改造记录）。**CC BY-NC-SA 类技能禁止商业用途**。
4. **改造说明**：部分技能（agentero-skills、check-citations 等）经过本地适配改造，详情见各技能包 `references/PROVENANCE.md` 中的改造记录表。

## 中英文适配原则 / Chinese and English

- **调研、精读、实验规划、审稿意见**：优先使用用户指定的交付语言，否则跟随任务指令的语言，不跟随附件或引文的语言。只在用户要求时提供中英双份。
- **论文正文**：明确指定的语言 → 期刊、会议或学位论文要求 → 被改写稿件的语言；新稿无其他信息时默认英文。正文和解释可用不同语言，例如中文讨论、英文引言。
- **检索和格式**：按研究范围决定是否同时检索中文和英文，说明覆盖限制；论文题名、DOI、BibTeX 键、代码、文件路径、JSON 键和枚举不翻译。英文语法规则只检查英文段落。

**In English:** Explicit output language wins. Otherwise, analytical deliverables follow the language of the request. Manuscript prose follows venue requirements, then the language of an existing draft, with English as the default for new drafts. Bilingual output is opt-in. Preserve citation identifiers and machine-readable fields.

## 首批单技能验收

例如，从独立研究项目根目录在 PowerShell 安装 `research-weave` 到 DSH（把 `$repo` 改成实际源码目录）：

```powershell
$repo = 'C:\src\ncepu_ideal-skills'
$src = Join-Path $repo 'research\research-weave'
$root = '.dsh\skills'
$target = Join-Path $root 'research-weave'
if (!(Test-Path -LiteralPath (Join-Path $src 'SKILL.md'))) { throw '未找到技能入口' }
if (Test-Path -LiteralPath $target) { throw "技能已存在，不覆盖：$target" }
New-Item -ItemType Directory -Path $root -Force | Out-Null
Copy-Item -LiteralPath $src -Destination $target -Recurse -ErrorAction Stop
```

在独立研究项目里，每次只安装下表中的一个技能。先确认技能目录或加载记录，再点名执行；另开会话去掉英文技能名，验证自然语言能否选中。不要把普通对话输出当成技能已加载的证据。

| 安装源 | 点名后的测试请求 | 验收结果 |
|---|---|---|
| [research-weave](./research-weave/SKILL.md) | 只用我提供的两段摘要，建议先读哪篇 | Scout 阅读顺序；标明仅有摘要，不声称已联网或读到全文 |
| [paper-reader](./agentero-skills/paper-reader/SKILL.md) | 用中文精读这篇本地 PDF，不要保存 | 对话交付；按实际可读范围引用，不生成笔记文件 |
| [experiment-plan](./auto-empirical-research/experiment-plan/SKILL.md) | 只用这段方案设计消融实验，预算未定 | 产出主张、对照、指标与运行顺序；预算待确认，无需其他技能，也不执行实验 |
| [check-citations](./auto-empirical-research/check-citations/SKILL.md) | 核查这份公开、测试用的 `.bib`，并观察断网表现（仅在隔离测试环境） | 无需第三方 Python 包；服务不可用不判定为伪造；JSON 可直接解析 |

语言追加验收：分别提交「请用中文精读这篇英文论文」和 “Explain this Chinese paper in English.”，检查说明语言正确且题名、引用定位未改动；再以「请用英文起草引言，用中文解释取舍」检查正文与说明可独立选语言。以上用例在 WorkBuddy 和 DSH 分别执行。

`idea-discovery` 尚依赖未收录的上游技能及包外资料，不纳入首批单装。文字起草、综述和润色按需增加对应技能即可。

## 推荐使用路径

- **开题/找方向**：vibe-research-workflow → idea-evaluator / idea-discovery → deep-research
- **文献调研**：dblp-api / openalex 检索 → research-weave 梳理脉络 → bibliometrix-guide 计量分析
- **实验设计**：experiment-plan（产出消融矩阵与算力预算）
- **论文写作**：tech-paper-template 搭骨架 → paper-writer / bestpaper-writing / research-paper-writing 起草 → intro-drafter 攻克 Introduction → paper-polish 润色 → figure-designer / drawio-reconstruction 处理配图
- **投稿与答辩**：check-citations 核查引用 → pre-submission-reviewer 模拟审稿 → rebuttal-guidance 撰写回复策略
