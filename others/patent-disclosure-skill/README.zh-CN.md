# 中国专利技能（patent-disclosure-skill）中文导读

一个覆盖专利工作全流程的技能合集：从「挖专利点、写交底书」到「撰写申请文件」，再到「检索、解读、对照表、专利地图、审查答复、政策简报」。按用户说法自动路由到对应子流程，不需要记一堆命令。

- 技能入口：[SKILL.md](SKILL.md)（根级路由文件）
- 完整安装说明：[INSTALL.md](INSTALL.md)
- 来源与许可：[references/PROVENANCE.md](references/PROVENANCE.md)（MIT，上游 handsomestWei/patent-disclosure-skill）
- 上游原版 README：[README.md](README.md)

## 能做什么（10 项能力）

| 你说的 | 它做什么 | 是否要点名 |
|---|---|---|
| 专利挖掘、交底书、查新、实用新型、外观设计 | 挖出真正能保护的点 → 轻量查新 → 写成交底书；首篇定稿后还能做 1+N 保护布局 | 直接触发 |
| 申请文件、申请底稿 | 把已有交底写成权利要求书、说明书、摘要、附图；规划母案与分案 | **须点名** + 指定交底目录 |
| 交底申请一起做、一条龙、案卷 | 从发明人材料一趟写出交底 + 申请，缺事实问人、不编 | **须点名** |
| 专利蒸馏、蒸文风、蒸思路 | 多份申请合并成统一文风；按案件抽取权要选择思路 | **须点名** |
| 专利检索（著录字段） | 按发明人/申请人/分类号/名称/摘要查国知局公布公告 | 直接触发 |
| 海外检索 | 用 Google Patents 查美欧日韩等海外专利 | **须点名国家** |
| 读专利、给公开号或 PDF | 通俗解读 + 图谱 + Obsidian 入库（中国及海外专利） | 直接触发（优先） |
| 对照表、claim chart、FTO 初筛、侵权对照 | 独权拆技术特征逐格比对，附证据与强弱（**底稿，非法律意见**） | **须点名** |
| 专利地图、案例地图 | 基于已解读入库的案例生成五种图 | **须点名**（需已有 vault） |
| 审查意见、OA、政策简报 | 审查答复问答与草稿；对照国知局口径出政策简报 | **须点名** |

「须点名」= 只有你明确说出该触发词才进入，防止写交底时误触发申请、地图、对照表等重流程。

## 使用方式（WorkBuddy）

1. 通过 WorkBuddy 的 Skills 导入功能导入 `others/patent-disclosure-skill/` 整目录（10 个 `skills/patent-*` 子包必须一并保留）。
2. 直接对话，例如：
   - 「帮我写一份关于 XX 装置的发明交底书」
   - 「读一下这个专利号 CN123456789A，用通俗话讲讲」
   - 「按申请人华为、分类号 G06F 检索国知局公布公告」
3. 产出写入当前工作区 `outputs/` 各子目录，不会污染技能安装目录。

## 依赖分层（按需安装）

| 能力层级 | 依赖 | 说明 |
|---|---|---|
| 路由、提示词流程、解读/检索基础 | 无 | 开箱即用 |
| Word 出图、公式转 OMML、Mermaid 渲染 | `pip install -r requirements.txt` | python-docx / latex2mathml / PyYAML / playwright / mammoth / python-pptx |
| STEP 多视角解析 | CadQuery（Python 3.10–3.12） | 可选，默认关闭 |
| CNIPA 公布站抓取 | Playwright + 系统 Chrome/Edge | 可选，限流即停、不重试 |

**Windows 终端**：脚本已自设 UTF-8，不需 `chcp 65001`；以退出码和机读前缀为准，stderr 出现中文或 `NativeCommandError` 不等于失败。

## 设计与安全要点

- **路由判定表**：根 SKILL.md 先定去向，须点名的流程用户没点名就停下说明。
- **事实不编造**：交底/案卷流程中材料缺口最多来回三轮，缺技术事实就问人。
- **法律边界**：对照表、FTO 初筛、审查答复草稿均声明为底稿，不构成法律意见。
- **WAF 与注入防护**：CNIPA 抓取脚本 `browser.py` 专门处理；各包自带所需脚本副本，脚本只用当前子技能自己的 `tools/`。

## 收录验证状态

560 个文件与上游 git tree 逐项校验一致。测试用 `unittest discover` 逐子包运行：`patent-distill`、`patent-docket`、`patent-reader` 通过；其余子包报错源于 `requirements.txt` 已声明依赖（python-docx / playwright / PyYAML）在本机未安装，非代码缺陷，安装后可复跑。
