# 深度研究·可审计（deep-research-auditable）中文导读

一个「能查账」的深度研究技能：给它一个需要大量来源的问题，它会产出一条别人能复核的证据链——查过什么、真正打开了什么、每条结论的可信等级、什么时候停止，以及有边界的否定结论。

- 技能入口：[SKILL.md](SKILL.md)
- 来源与许可：[references/PROVENANCE.md](references/PROVENANCE.md)
- 上游：[hyderhusainarastu/deep-research-skill](https://github.com/hyderhusainarastu/deep-research-skill)（MIT）
- 本地改名：因与 `supervisor-skills/deep-research` 同名冲突，本地改为 `deep-research-auditable`

## 解决什么问题

让 AI 做文献/证据调研时，常见的问题是：不知道它到底搜了什么、把搜索结果摘要当成"已读"、找不到负面证据、查到自以为饱和就停不下来或停得太早。本技能用四个机制把过程约束成可审计：

| 机制 | 说明 |
| --- | --- |
| **验证等级** | 每条来源只能处于 `DISCOVERED` / `OPENED` / `METADATA-VERIFIED` / `ABSTRACT-VERIFIED` / `FULL-TEXT-VERIFIED` 之一，且只能升级不能虚标 |
| **饱和停止规则** | 一个主题满足 8 条条件（多组检索词、两条不同路径、正反检索都做了、连续两批新查询无高优先级新项等）才停，防止"为显得全面而无限查" |
| **有界否定结论** | 否定结论必须写成"在所检索材料中未找到"，并列出检索了哪些来源、什么访问级别、用什么检索词 |
| **角色分离** | 发现者与验证者分离（FULL 用不同 agent；SCOPED 用重新打开来源的"换位自审"），另有对抗式审查 Wave |

## 何时使用

- 需要多来源、可追溯的文献综述或证据盘点
- 需要明确区分"搜到了"与"真读了"、需要给出可信度分级
- 需要诚实地报告"没找到什么"，而不是含糊其辞
- 科研开题前的系统性检索、事实核查、竞品/技术调研的严谨版

**不适用**：快速事实查询、单篇论文摘要、纯 STS 写作（用 `research/` 其他技能）。

## 两种运行档位

| 档位 | 适用 | 做法 |
| --- | --- | --- |
| **FULL** | 有并行 agent 的运行环境 | 每条发现流分配给独立 agent，各自只写一个输出文件；控制器只做分派、合并与报告；验证者与发现者不同 |
| **SCOPED** | 单 agent / 单次对话 / 聊天工具 | 顺序跑各流，用"重新打开来源"的换位自审代替角色分离；MANIFEST 写明跑了哪些流、没跑哪些及原因 |

## 六步流程（Wave 0-5）

1. **Wave 0 基线**：建 `OUT_DIR`、填 RUN_MANIFEST、写 `01_BASELINE.md`（用户已有什么、已主张什么、已引用什么），设计检索词格（偏好词/旧词/跨领域词/对立词 + 至少一条反驳主主张的查询）。
2. **Wave 1 独立发现**：跑各发现流（学术核心、引文链、近期预印本、实务/灰色来源、代码仓库、音视频、论坛、负面证据、术语），每条查询都记入 `03_QUERY_LOG.csv`（包括空结果）。
3. **Wave 2 去重与溯源**：标 `NEW`/`EXACT-DUPLICATE`/`WORK-DUPLICATE`/`VERSION-SIBLING`/`POSSIBLE-MATCH`/`ALREADY-HELD`，非正式线索向学术文献追溯。
4. **Wave 3 验证**：先验身份元数据，再验内容；核对每条引文与定位符，否则删掉引文只留转述。
5. **Wave 4 综合**：写主题、最近邻、反对意见、开放缺口与摘要，每条实质陈述都引 lead/candidate ID。
6. **Wave 5 对抗审查**：审查者试图攻破整个包（无支撑主张、非正式来源冒充学术、单边检索、重复泄漏、超长引文、注入指令），问题交回文件所有者修复。

流程细节见 [references/waves.md](references/waves.md)，CSV 表头见 [references/schemas.md](references/schemas.md)。

## 产物结构

在 `OUT_DIR`（唯一允许写入的目录）下生成编号文件：`00_RUN_MANIFEST.md`、`01_BASELINE.md`、`02_SEARCH_PROTOCOL.md`、`03_QUERY_LOG.csv`、`04_LEADS.csv`、`05_CANDIDATES.csv`、`06_CLAIM_EVIDENCE.csv`、`07_SYNTHESIS.md`、`08_NEAREST_NEIGHBORS.md`、`09_OBJECTIONS.md`、`10_ACQUISITION_QUEUE.csv`、`11_SOURCE_STATUS.md`、`12_COVERAGE.md`、`13_EXECUTIVE_SUMMARY.md`，以及 `agents/`（FULL）与 `reviews/`。

## 在 WorkBuddy 中使用

1. 通过 WorkBuddy 的技能导入功能导入本技能目录，或把本目录放到 WorkBuddy 的技能路径下。
2. 直接对话触发，例如：
   > 使用 deep-research-auditable 技能，SCOPED 档位，输出到 `research/run-qwerty/`，研究问题：为什么 QWERTY 键盘布局成为标准？
3. 开始前先固定四个参数：`QUESTIONS`（1-5 个）、`OUT_DIR`（唯一写入目录）、`PROFILE`（FULL/SCOPED）、`BOUNDS`（agent 上限、时间/查询预算、排除的来源类别）。缺哪项 AI 会先问。
4. 聊天工具（粘贴提示词）场景可用 [PROMPT.md](PROMPT.md) 或 [PROMPT.short.md](PROMPT.short.md)。

## 本地验证状态

收录时在本机执行：`python -m pytest -q` → 12 passed；`python scripts/check_csv.py examples/toy-run` → 0 problem。两个 Python 脚本仅依赖标准库、离线可用；其余平台适配状态见上游 README 的 "Works with" 表。
