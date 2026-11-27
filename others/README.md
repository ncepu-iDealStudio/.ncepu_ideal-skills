# others 技能分类说明

本目录收录 **3 个技能包、12 个技能**，覆盖 DSH 插件工程化脚手架、中文成稿去 AI 味、中国专利全流程（交底 → 申请 → 检索 → 解读 → 地图 → 审查答复）。技能可用中文或英文发起；在 WorkBuddy 或 DSH 中按需安装当前任务需要的技能，不必一次安装整个合集。已有上游依赖或商业授权的技能见下文说明。

**English quick start:** Pick `dsh-plugin-starter` to scaffold a DSH plugin from a one-line request, `lieflat-less-ai-tone` to detect and minimally rewrite AI-writing traces in a finished draft (research-grounded rules), or `patent-disclosure-skill` to mine patent points, draft disclosures/application documents, search, read, and map Chinese patents. Import the complete skill folder through WorkBuddy's Skills UI, or place it directly under `.dsh/skills/` or `.agents/skills/` in a project. Ask in Chinese or English and specify the deliverable language if it differs.

## 技能总览

| 技能包 | 子技能数 | 定位 | 许可证 | 上游来源 |
|---|---|---|---|---|
| dsh-plugin-starter | 1（4 类插件模板） | DSH（DeepSeek Harness）插件起步工程脚手架：工具型 / 路由型 / 双面型 / 拦截器型，生成可直接开发、构建、装配的工程骨架 | 未随附 LICENSE；参考来源见该技能 README | [lansi-ai/dsh-plugin-starter](https://github.com/lansi-ai/dsh-plugin-starter)、[yanhua1010/dsh-harness-tutorial](https://github.com/yanhua1010/dsh-harness-tutorial)（本仓库整合改造） |
| lieflat-less-ai-tone | 1 | 中文成稿「去 AI 味」：基于两轮实测语料（1,169 篇 / 约 520 万字 / 约 50 万次语义判断）先检测出有指标与例句的改前报告，用户确认后再最小改写并复测 | CC BY-NC 4.0（**商用需另行购买授权**） | [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) |
| patent-disclosure-skill | 10 | 中国专利全流程：交底书编写、申请文件四件套、案卷会稿、专利蒸馏、著录检索、通俗解读、权利要求对照表、专利地图、审查答复辅助、政策简报 | MIT | [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) |

## 各技能详细介绍

### 1. dsh-plugin-starter — DSH 插件起步工程脚手架

来源：整合 [lansi-ai/dsh-plugin-starter](https://github.com/lansi-ai/dsh-plugin-starter) 的双面架构与 tsdown 双目标、[yanhua1010/dsh-harness-tutorial](https://github.com/yanhua1010/dsh-harness-tutorial) 的 Cordis 生命周期与事件模式，并吸收本仓库 `sql-to-*` / `prototype-to-*` 技能的分层组织方式（config / specifications / templates / tools / demo_output）。

把「我想要一个 DSH 插件，能……」或一份插件原型，变成**能直接用 VSCode 打开开发、能构建、能装进 DSH 的工程骨架**，并把「接下来怎么写、怎么调、怎么发」写进工程自带的 `DEVELOPMENT.md`。

- **支持四类插件**：
  - `tool-only`（工具型）：让 Agent 能查 / 抓 / 算 / 写，能力出口 `ctx.tools.register(defineTool(...))`，无界面
  - `route-only`（路由型）：提供 HTTP 接口给外部脚本调用，能力出口 `ctx.webServer.register()`，无界面
  - `dual-face`（双面型）：设置页 / 面板 / 可视化配置，路由 + `settings.section` 插槽，有界面
  - `interceptor`（拦截器型）：白名单 / 审计 / 审批，监听 `ctx.on('tools/pre-execute')`，无界面
- **六步工作流**：需求澄清（一次问 2-3 个选择题）→ 类型判定 → 写 spec → 生成 → 填业务逻辑（唯一填空处 `src/capability.ts`，纯函数便于单测）→ 验证交付。
- **自带两个零依赖 Python 工具**：`resources/tools/scaffold_plugin.py`（spec → 工程，支持 `--dry-run`）、`resources/tools/validate_plugin.py`（18 项静态自检，覆盖装配 / 声明 / 产物 / 运行期）。
- **生成工程自带 `DEVELOPMENT.md`（10 章）**：含「按类型扩展功能」与「症状 → 根因 → 修法」调试表，把 DSH 插件常见的静默失败（缺 `dsh.bundle.patch`、包名四不一致、Client 产物没被 `__ModuleLoader__` 包装等）固化进模板与校验器。
- **与 `modern-web-guidance` 叠加**：只有 `dual-face` 写设置页界面时才检索，其余三类无浏览器界面不调用。

**适用场景**：开发 DSH 插件、给 DSH 加工具 / 设置页 / 拦截器、把已有插件原型工程化、改造已有插件。**不适用**：纯概念咨询、写 DSH 技能（`SKILL.md` 走 skills 体系）、与仓库其他技能重叠的纯前端 / 后端脚手架。

### 2. lieflat-less-ai-tone — 中文成稿去 AI 味

来源：[larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)，官网与商业授权见 [lieflat.work](https://lieflat.work/skills/less-ai-tone/)。

一个基于**两轮实测语料**的去 AI 味技能：第一轮 629 篇对照（5 个模型 × 60 篇 vs 329 篇人类），第二轮 270 对同题同事实配对复测（约 50 万次模型语义判断）。核心思路是从「读着像 AI」的主观体验里，找出能客观量化的写作指标，先检测、用指标与例句讲清发现和改法、**等用户回复后再改写与复测**，管住模型不乱改、不误伤正常表达。

- **三层检测分工**：
  - 脚本层（`scripts/detect.py`）：数得出符号的，90 项可计算指标（标点密度、句长分布、词汇多样性 mtld/mattr、欧化构式、小节几何等）
  - 语义层（会话内模型按 `references/semantic-criteria.md` 封闭判据逐条判）：脚本测不了的 4 项——同义重命名段、段间衔接连环、结论提示冒号、高度同构三连
  - 人审层：比喻贴切度 / 暗喻 / 拟人化喻体（模型间共识仅 0–40%），只列出不判
- **分级报告**：A（机械改，零语义风险）/ B（建议改，需句式重组）/ C（只报告，整篇级问题默认不改）/ H（人审区，默认保留）/ X（已否决，配对复测反向，**永不改**，展示计数防误改）/ F（指纹，分模型特征，带方向解读）。
- **X 级防误改清单**（实测推翻的经典误区）：序数词小标题、「这意味着」复述、空转句引列表、概括替代、精确数字堆砌、赋能/闭环/抓手黑名单词、句长不参差——配对复测均显示人类用得更多或无差异，**永不据此删改**。
- **六条改写原则**：最小改动、信息守恒（每个实词须能在原文指出出处）、不制造参差（不为节奏改句长）、结构不动、有风格参考以参考为准、改后三查加复测。
- **交付物**：改前检测报告（指标 + 研究参照 + 原文例句 + 具体改法 + 排除项）→ 改写 → 复测 + 前后对比报告（默认 Markdown 与文稿同格式，`--format html` 出红绿划线网页版）。

**适用场景**：写作完成后的成稿清理。**不适用**：对话体 / 口语体、问句设问、文学性表达、代码块 / 引文。**许可提示**：CC BY-NC 4.0，用于商业写作、客户交付或产品集成须在 lieflat.work 购买授权。

### 3. patent-disclosure-skill — 中国专利全流程技能集（10 个子技能）

来源：[handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill)（v5.4.0，MIT），本仓库收录时新增了 WorkBuddy 安装章节、中文导读与 `references/PROVENANCE.md`，**未作功能性改动**（10 个子技能、全部 tools/ 脚本、prompts/、tests/、docs/ 示例图保持上游原文）。

根级 `SKILL.md` 是**路由入口**，按路由判定表把用户意图分派到对应子技能；子技能 frontmatter 为 `user-invocable: false`，不单独暴露。**「须点名」的子技能只有用户明确说出触发词才进入，禁止由写交底或读专利自动跳转。**

| 子技能 | 能力 | 触发 |
|---|---|---|
| `patent-disclosure` | **交底书编写**（默认入口）：发明 / 实用新型 / 外观的专利点挖掘、轻量查新、成文、迭代；首篇定稿后可做保护型 1+N 专利布局（围栏旁路） | 「交底书」「专利挖掘」「查新」 |
| `patent-application` | **申请文件四件套**：权要 / 说明书 / 摘要 / 附图；发明母案与分案规划、原始披露核对 | 「申请文件」「申请底稿」（须点名 + 指定交底目录） |
| `patent-docket` | **案卷会稿**：角色扮演交底工程师 vs 专利代理师，材料一趟出交底 + 申请，缺事实问人绝不瞎编 | 「交底申请一起做」「一条龙」（须点名） |
| `patent-distill` | **专利蒸馏**：从已有专利合并文风，按案件抽取权要选择思路 | 「专利蒸馏」「蒸文风」（须点名） |
| `patent-search` | **著录检索**：国知局公布公告（发明人 / 申请人 / 分类号 / 名称 / 摘要）；可由图或权要倒推检索式 | 「著录检索」；海外检索须点名（走 Google Patents 查美欧日韩等） |
| `patent-reader` | **通俗解读**（优先）：公开号（中国或海外）/ PDF → 通俗笔记 + 图谱，推进 Obsidian 入库串起多件专利 | 「读专利」 |
| `patent-chart` | **权利要求对照表**：独权拆特征格，与对比文件 / 产品 / 标准逐格填证据与强弱，主交付 Excel | 「对照表」「claim chart」（须点名，**底稿，不构成法律意见**） |
| `patent-map` | **专利地图**：基于已解读入库的 vault 生成五种图（语义地形、申请人四象限、同族引证网络、技术功效矩阵、仪表盘），本地私有化运行 | 「专利地图」「案例地图」（须点名） |
| `patent-oa` | **审查答复辅助**：拆条款问答、起草答复稿；历史案脱敏入库后对照旧打法 | 「审查答复」「审查意见」（须点名） |
| `patent-exam-policy` | **政策简报**：对照国知局口径说明对交底写法 / 本稿的影响 | 「政策简报」「政策雷达」（须点名） |

附带能力：结构图 / 外观图 / CAD 三维模型投影出图（Mermaid + 可选 CadQuery）、公式转 OMML、Markdown 转 Word、CNIPA 公布站抓取（Playwright）。涉及法律边界的输出（对照表、无效 / FTO 初筛、审查答复草稿）均为**底稿，不构成法律意见**。

**适用场景**：研发人员把技术贡献写进可交付的交底书、代理人 / 工程师写申请文件、读不懂公开专利想快速看懂、攒了一批解读想做专利地图。**依赖分层**：核心路由与解读 / 检索基础流程无需第三方依赖；Word 出图、公式、Mermaid 渲染需 `pip install -r requirements.txt`；STEP 解析、CNIPA 抓取为可选能力按需开启。

## 使用说明

1. **安装单位**：安装包含 `SKILL.md` 的整棵子目录，保留其中的 `references/`、`scripts/`、`tools/`、`assets/` 等资源。`patent-disclosure-skill` 是合集外壳（根级 `SKILL.md` 做路由），安装时要带上整个目录树及 10 个子技能，不要只复制根级入口；子技能不单独点名暴露。
   - **WorkBuddy**：在「技能 → 添加技能 → 上传技能」导入本地包，启用后点名验证。若客户端要求压缩包，一个技能一个包，保留技能名目录。
   - **DSH**：将各技能并列放进研究项目的 `.dsh/skills/` 或 `.agents/skills/`。DSH 不递归发现嵌套技能；出现同名目录先检查现有版本，不覆盖。`dsh-plugin-starter` 生成的产物工程本身不是技能，不要放进 skills 目录。
2. **补充资料**：多数技能在 `references/` 子目录存放方法论与示例，AI 会在需要时按 `SKILL.md` 指引加载，无需人工预读。
3. **许可合规**：
   - `patent-disclosure-skill` 为 MIT，可商用、修改、分发，须保留版权与许可声明；
   - `lieflat-less-ai-tone` 为 CC BY-NC 4.0，**禁止商业用途**，商业使用须在 [lieflat.work 授权页](https://lieflat.work/skills/less-ai-tone/#pricing) 购买；
   - `dsh-plugin-starter` 未随附 LICENSE 文件，使用前请阅读其参考来源的上游许可；分发或分享前按对应来源附上许可与署名。
4. **改造说明**：`patent-disclosure-skill` 经过本地适配（新增 WorkBuddy 安装章节、中文导读、PROVENANCE），功能性内容保持上游原文，详见 [patent-disclosure-skill/references/PROVENANCE.md](patent-disclosure-skill/references/PROVENANCE.md)。

## 中英文适配原则

- **交底、申请文件、检索、解读、审查答复**：默认跟随用户指定的交付语言，否则跟随任务指令的语言。专利题名、公开号、分类号、权要编号、法律术语、JSON 字段名不翻译。
- **去 AI 味报告**：默认与文稿同语言同格式（Markdown）；用户要求网页版时加 `--format html`。
- **DSH 插件生成**：界面文案一律走 `ctx.locale` 中英双语；需求澄清与交付说明跟随用户语言。
