# PROVENANCE — last30days 收录来源与许可声明

## 来源

- **上游项目**：[mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)（v4.6.0）
- **拉取日期**：2026-11-25
- **本仓库落地路径**：`info-research/last30days/`（本仓库新增 `info-research/` 分类目录，定位于"全网信息/舆情调研"，与学术论文向的 `research/` 区分）
- **收录范围**：上游 `skills/last30days/` 技能本体全部 204 个文件 + 根目录 `LICENSE`（MIT），技能本体零改动。上游仓库级的 10 国语言 README、tests、mcp、media 等不属于技能本体，未收录。

## 技能简介

调研"最近 30 天人们在任何话题上实际说了什么"的全网信息调研技能：通过自带的 Python 引擎（200+ 模块）拉取 Reddit、X、YouTube、TikTok、Hacker News、Polymarket、GitHub、小红书、Bluesky、LinkedIn、Trustpilot 等来源的帖文与互动数据，综合生成带引用来源的调研报告；附带 doctor 健康检查（诊断数据源可用性）、setup wizard（凭据配置）、库检索/趋势发现/对比/竞品/招聘信号等多种模式。

## 许可

- 上游项目采用 **MIT License**，与本仓库技能的通行许可一致，无合规冲突。
- 上游原始 `LICENSE` 已随技能保留在本目录根（`info-research/last30days/LICENSE`）。
- SKILL.md frontmatter 自带 `license: MIT` 字段，保留原样。

## 文件对应关系

| 本仓库文件 | 上游文件 |
| --- | --- |
| `SKILL.md`、`agents/`、`assets/`、`references/`（16 个）、`scripts/`（约 190 个）、`.skillignore` | `skills/last30days/` 下对应文件，逐字一致 |
| `LICENSE` | 上游仓库根目录 `LICENSE` |

上游 `scripts/lib/vendor/bird-search/`（Node.js X 搜索客户端）自带独立 MIT `LICENSE` 文件，已随附保留。

## 使用前提（重要）

- **Python 3.12+**（本仓库收录环境 Python 3.13.14 实测 `--help` 可运行）；部分 vendor 依赖 Node.js。
- **数据源凭据为可选**：部分来源（如 X API、ScrapeCreators、Perplexity、Brave 等）需要 API Key 或浏览器 Cookie，首次使用会有 setup wizard 引导；也有 keyless 模式可用。详细清单见 SKILL.md frontmatter `metadata.openclaw.optionalEnv` 与 `references/setup-wizard.md`。
- 网络环境：引擎需访问境外平台（Reddit/X/YouTube 等），使用时需确保网络可达。
- `assets/` 内 5 个多媒体文件（约 14MB）为技能自带演示素材，保留原样。

## 改动说明

技能本体零改动，仅新增本 PROVENANCE.md 与顶层 README 登记。
