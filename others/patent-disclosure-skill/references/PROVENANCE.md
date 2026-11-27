# 来源与许可（PROVENANCE）

## 上游信息

| 项目 | 内容 |
| --- | --- |
| 技能名称 | `patent-disclosure-skill`（中国专利技能，v5.4.0） |
| 上游仓库 | https://github.com/handsomestWei/patent-disclosure-skill |
| 作者 | handsomestWei |
| 许可证 | MIT License（见本技能根目录 `LICENSE`，Copyright (c) 2026 handsomestWei） |
| 收录日期 | 2026-11-27 |
| 收录范围 | 全仓库 560 个文件（约 12.4 MB），含根级 SKILL.md/README.md/INSTALL.md、10 个子技能包、docs/ 效果示例图、scripts/、requirements.txt 与 tests/ |

## 许可声明

MIT 许可，允许商用、修改、分发，须保留版权与许可声明。本技能 `LICENSE` 原文随收录保留，未作改动。

## 功能构成（10 个子技能）

| 子技能 | 能力 | 触发方式 |
| --- | --- | --- |
| `patent-disclosure` | 交底书编写：发明/实用新型/外观的专利点挖掘、轻量查新、成文、1+N 布局 | 默认入口 |
| `patent-application` | 申请文件四件套（权要/说明书/摘要/附图）、母案与分案规划 | 须点名 + 指定交底目录 |
| `patent-docket` | 案卷会稿：材料一趟出交底 + 申请，缺事实问人不编 | 须点名 |
| `patent-distill` | 专利蒸馏：合并文风、按案件抽取权要选择思路 | 须点名 |
| `patent-search` | 著录检索：国知局公布公告；点名后走 Google Patents 查海外 | 直接触发；海外须点名 |
| `patent-reader` | 专利通俗解读：公开号/PDF → 通俗笔记、图谱、Obsidian 入库 | 直接触发（优先） |
| `patent-chart` | 权利要求对照表：独权拆特征逐格比对，底稿非法律意见 | 须点名 |
| `patent-map` | 专利地图：基于已解读入库的 vault 生成五种图 | 须点名 |
| `patent-oa` | 审查意见答复辅助：问答与草稿 | 须点名 |
| `patent-exam-policy` | 政策简报：对照国知局口径说明对交底写法的影响 | 须点名 |

根级 `SKILL.md` 是**路由入口**，按路由判定表把用户意图分派到对应子技能；子技能 frontmatter 均为 `user-invocable: false`，不单独暴露。

## 本地改造记录

| # | 改造项 | 原因 | 处理方式 | 影响文件 |
| --- | --- | --- | --- | --- |
| 1 | INSTALL.md 增加「WorkBuddy（本仓库收录版）」章节 | 上游只写了 Claude Code / Cursor，本仓库目标平台为 WorkBuddy | 在文首新增章节：导入方式、技能名、产出目录、依赖分层、Windows 终端注意、上游出处 | `INSTALL.md` |
| 2 | 新增中文导读 | 仓库惯例：外部收录技能提供中文入口 | 新建 `README.zh-CN.md` | `README.zh-CN.md`（新增） |
| 3 | 新增本文件 | 仓库惯例：署名、许可、改造记录可追溯 | 新建 `references/PROVENANCE.md` | 本文件（新增） |

**未作功能性改动**：10 个子技能、全部 tools/ 脚本、prompts/、references/、tests/、docs/ 效果示例图均保持上游原文；未改名（本仓库无同名技能冲突）；未修改任何脚本逻辑。

## 验证记录（收录时）

在本机 Windows / Python 3.13 环境下执行：

- **完整性**：560 个文件逐一下载并与上游 git tree 的 size 校验，全部一致（含 9 个中文名文件经 URL percent-encoding 补齐）。
- **命名**：`patent-disclosure-skill` 及 10 个子技能名在本仓库均无重名冲突（全仓重复仅 `brainstorming`，为既有情况，与本次无关）。
- **测试**：`unittest discover` 逐子包运行——`patent-distill`、`patent-docket`、`patent-reader` 通过；其余子包报错均为 `requirements.txt` 已声明的依赖（`python-docx`、`playwright`、`PyYAML`）未安装所致，非代码缺陷。安装依赖后可复跑验证。
- **安全**：无硬编码用户路径；用户产出限定写入工作区 `outputs/`，不写技能安装目录。

## 使用提示

- 核心提示词路由与「解读/检索」基础流程**无需第三方依赖**即可用。
- Word 出图、公式转 OMML、Mermaid 渲染依赖 `pip install -r requirements.txt`。
- STEP 多视角解析（CadQuery，Python 3.10–3.12）、CNIPA 公布站抓取（Playwright + 系统浏览器）为可选能力，按需开启。
- 涉及法律边界的输出（对照表、无效/FTO 初筛、审查答复草稿）均为**底稿，不构成法律意见**。
