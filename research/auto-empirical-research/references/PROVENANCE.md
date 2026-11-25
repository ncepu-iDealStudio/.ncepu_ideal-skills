# PROVENANCE — auto-empirical-research（选择性收录）

## 来源

- 上游仓库：[brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)（Stanford Bryce Wang / CoPaper.AI，创建于 2026-04）
- 上游性质：**第三方技能快照合集**，catalog 编目 78 个合集 / 1,151 个技能条目（含重复与变体，非 1,151 种独立能力）
- 收录日期：2026-11-25（依据上游 main 分支当日状态）

## 许可

- 上游整体许可：**CC BY-SA 4.0**（署名-相同方式共享），版权方 CoPaper.AI
- 首次收录保留上游原文；后续本地改造见下文。分发时须保留合集 `LICENSE`（CC BY-SA 4.0 原文）、上游来源与改动声明，并核对各组件的上游许可。
- ⚠️ **相同方式共享（Share-Alike）提示**：后续对本目录内技能的修改、衍生版本也须以 **CC BY-SA 4.0** 授权，不能改用 MIT 闭源发布

## 收录范围（选择性收录，非整库）

本目录从上游 **~4,800 个文件 / 92.6MB** 中仅选取 6 个技能（11 个文件，约 122KB）+ 集合级 LICENSE + 上游中文 README，按用户分析评估挑选，适合计算机科研场景：

| 本地目录 | 上游路径 | 文件数 | 功能 |
|----------|----------|--------|------|
| `idea-discovery/` | `skills/42-wanshuiyin-ARIS/skills/idea-discovery/` | 1 | 研究想法发现全流程（文献调查→候选想法→查新→外部评议→实验规划） |
| `experiment-plan/` | `skills/42-wanshuiyin-ARIS/skills/experiment-plan/` | 1 | 从研究主张倒推实验设计（基线/消融/指标/算力预算/停止条件） |
| `dblp-api/` | `skills/43-wentorai-research-plugins/skills/domains/cs/dblp-api/` | 1 | DBLP 计算机文献检索指南 |
| `bibliometrix-guide/` | `skills/43-wentorai-research-plugins/skills/literature/metadata/bibliometrix-guide/` | 1 | R bibliometrix 文献计量与主题演化 |
| `openalex/` | `skills/59-shiquda-openalex-skill/openalex/` | 3 | OpenAlex CLI 学术元数据检索（含 references/ 2 个文件） |
| `check-citations/` | `skills/62-PHY041-claude-skill-citation-checker/` | 4 | 引用真实性核查（含 scripts/、tests/、原版 README） |
| `shared-references/` | `skills/42-wanshuiyin-ARIS/skills/shared-references/` | 8 | idea-discovery 与 experiment-plan 的共享参考协议文件（传递闭包选集） |
| `README.md` | 上游仓库级 README | 1 | 上游合集背景文档（含 78 合集总表），链接指向未收录的上游文件属预期 |
| `LICENSE` | 上游根目录 | 1 | CC BY-SA 4.0 原文，分发时必须保留 |

`shared-references/` 按**传递闭包**收录：idea-discovery 与 experiment-plan 直接引用 6 个文件（reviewer-backends / external-cadence / output-composition / output-versioning / output-manifest / output-language），其中 external-cadence 传递引用 `acceptance-gate.md`、output-composition 传递引用 `review-tracing.md`，合计 8 个文件，已验证闭包内不再有其他依赖、相对链接全部可解析。

## 未收录的上游依赖（后续改造清单）

以下依赖在当前选择性收录中缺失，独立使用时相关环节会"踩空"：

| 缺失项 | 引用方 | 说明 |
|--------|--------|------|
| `idea-creator` 技能 | idea-discovery（管线末段衔接） | 小规模试验执行技能，需单独收录或删改衔接 |
| `openalex` CLI 本体 | openalex | 技能只是 CLI 使用指南，命令行工具需另行安装 |
| R + bibliometrix 包 | bibliometrix-guide | 运行环境需自备 R 与 bibliometrix；部分文献数据库需订阅 |
| `mcp__codex__codex` MCP | idea-discovery（allowed-tools + reviewer 后端） | Codex 专用 MCP 工具，其他平台需替换评议后端（见 shared-references/reviewer-backends.md） |

## Harness 适配记录

- `experiment-plan` 移除上游命令、宿主专用工具声明和包外参考协议的硬依赖；接受用户直接提供的方案，默认不写文件、不执行实验。
- `check-citations` 原实现实际硬依赖 `requests`；现改为标准库。无匹配且存在服务失败时返回 `unverified`，并在 JSON 中记录 `source_errors`。以离线测试覆盖超时、限流、成功但无匹配和 JSON 输出。
