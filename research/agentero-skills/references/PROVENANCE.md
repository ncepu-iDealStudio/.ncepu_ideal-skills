# PROVENANCE — agentero-skills（Agentero 内置科研技能）

## 来源

- 上游仓库：[poco-ai/Agentero](https://github.com/poco-ai/Agentero)（MIT 许可，Tauri 桌面应用：PDF 问答 + 双链笔记 + Agent 协作的人机科研工作台）
- 技能实际路径：上游 `templates/vault/.agents/skills/`（应用创建 Vault 时播种到用户知识库的内置技能）
- 收录日期：2026-11-25（依据上游 main 分支当日状态，应用更新频繁，最后推送 2026-11-24）

## 收录范围（非整库，应用本体未收录）

上游是完整桌面应用（2787 文件 / 33.9MB：Rust + TypeScript + React），**未收录应用源码**。2026-11-25 首轮收录上游 5 项技能（48 文件），同日按"相对独立使用"原则完成第二轮整理（见下文改造记录），**当前保留 2 个可独立使用的技能**：

| 本地目录 | 许可 | 来源 | 独立性 |
|----------|------|------|--------|
| `paper-reader/` | Agentero MIT | 一方技能（已适配） | ✅ 独立使用。**中文**论文精读：默认在对话交付讲义式笔记（贡献/方法/实验/局限），可按需保存；配图提取可选 |
| `research-paper-writing/` | MIT（Master-cai） | 一方技能（致谢 Master-cai） | ✅ 完全自包含。英文论文写作：Abstract/Intro/Related Work/Method/Experiments/Conclusion 分节规范 + 37 个示例文件（introduction 六种写法、method 三要素等） |
| `AGENTS.md` | Agentero MIT | 上游 `templates/vault/AGENTS.md` | Vault 级 Agent 约定（paper-reader 引用的阅读流程来源，含 `papers/` 目录约定） |
| `README.md` | Agentero MIT | 上游 `templates/vault/.agents/skills/README.md` | 内置技能清单与版本升级机制说明（已加编辑注记） |

首轮收录后已删除的 3 个强绑定技能见下文改造记录；未收录的 2 项同源技能见下一节。

## 未收录的 2 项（避免重复）

上游 `idea-evaluator` 与 `deep-research` 是从 [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills)（Yuyu Luo et al.，**CC BY-NC-SA 4.0**）**vendored** 的技能，经逐行 diff 验证与本仓库已收录的 [`research/supervisor-skills/`](../../supervisor-skills/README.zh-CN.md) 对应版本**内容完全一致**（唯一差异是 Agentero 加了一行 `version: 1` frontmatter），故不重复收录。

## 2026-11-25 独立化改造记录

按"相对独立使用和运行"原则对本集合做了第二轮整理：

**删除 3 个强绑定技能**（离开 Agentero 应用完全无法使用，改造无意义）：

| 删除项 | 原因 |
|--------|------|
| `agentero-cli/` | 全文是 `agentero` CLI 命令用法（16 处绑定），须先安装 Agentero 应用 |
| `vault-normalizer/` | 目标是把目录规范化为 Agentero vault 布局与 `catalog.sqlite` 约定（24 处绑定） |
| `openui-blocks/` | OpenUI Lang UI 块只能在 Agentero 聊天界面渲染，另依赖 `agentero paper regions` CLI |

**改造 `paper-reader`**（保留，中度绑定 → 基本独立）：

| 改动 | 原文 | 适配后 |
|------|------|--------|
| "标记已读"步骤 | `agentero paper update --state read` | 移除，改为 NOTES.md 乱码自查（注记说明如何在 Agentero 环境恢复） |
| 引用定位校验 | `agentero search / read / paper regions` CLI | 改为直接阅读 PDF 按页/节确认后引用（注记保留 CLI 恢复说明） |
| 引用路径 | 假定 Agentero vault 的 `papers/<id>/` 约定 | 保留示例但注明"相对于文献库根目录、可按实际目录调整" |
| frontmatter `version: 13` | 应用自动升级机制 | 移除（按上游约定，无 version = 用户自有，不被应用覆盖） |
| `wikilink.md` | `agentero paper list --json` 确认目标 | 改为直接检查文献库文件；marks 标注链接改为"仅当 marks/ 存在时" |
| `author-lookup.md` | 输入限定 Agentero vault | 改为任意论文文件夹（保留 `papers/` 约定推荐） |

**`research-paper-writing` 零改动**（本就完全自包含）。当前集合保留 2 个技能：`paper-reader`（中文精读，基本独立）、`research-paper-writing`（写作规范，完全独立）。

## 独立使用现状（改造后）

| 技能 | 应用绑定程度 | 独立使用 |
|------|-------------|----------|
| `research-paper-writing` | **无绑定**，自包含 | ✅ 可直接用（MIT，与 best-paper-writing 基础技能同源但内容不同） |
| `paper-reader` | 已解除 CLI 绑定（见改造记录） | ✅ 可独立用：核心精读流程自包含；仅配图提取的 `pdftoppm`（poppler 工具）为可选依赖，无该工具时跳过配图或用其他方式转换 |

后续 Harness 适配：`paper-reader` 不再依赖 Vault 布局，接受本地 PDF、链接或粘贴文本。默认在对话交付；按需保存时，配图和 PDF 链接统一相对笔记目录。若无法读取全文或提取配图，显式标明覆盖范围并使用可验证的页码或图号。

## 版本机制（上游约定，已随 README 收录）

内置技能 frontmatter 带 `version: <int>` 字段，应用打开 vault 时与模板比对：低版本自动升级；同版本不覆盖；**删除 version 字段或调高版本可保留用户自定义修改**。未来从上游更新时注意此机制。

## 本机验证记录（2026-11-25）

- 48 个文件全部到位，与上游文件树一致
- `research-paper-writing` 引用的 8 个分节 references + 37 个示例文件全部随附，自包含
- 网络代理逐文件下载（约 8 分钟），无脚本运行验证需求（均为提示词型技能，`paper-reader` 运行时才需 pdftoppm）
