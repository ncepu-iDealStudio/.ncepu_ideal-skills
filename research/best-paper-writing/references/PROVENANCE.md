# PROVENANCE — best-paper-writing 收录来源与许可声明

## 来源

- **上游项目**：[gulucaptain/Best-Paper-Writing-Skill](https://github.com/gulucaptain/Best-Paper-Writing-Skill)（v1.2）
- **拉取日期**：2026-11-23
- **本仓库落地路径**：`research/best-paper-writing/`（保留上游完整目录结构）
- **收录范围**：上游全部 150 个文件（剔除 `.gitignore`），首次收录时未改动。含技能本体 `skills/bestpaper-writing/`、60 篇获奖论文清单 `PAPER_LIST.md`、语料数据 `data/`、CVPR 2027 LaTeX 模板 `template/`、语料统计工具 `tools/` 与上游 README。

## 技能简介

写作规律提炼自 60 篇 CVPR / ICCV / NeurIPS 获奖论文（55 篇拟合规则 + 5 篇留出测试），支持撰写/改写论文的标题、摘要、引言、方法、实验与配图规划，按八类论文路由论证结构，自带草稿检查器（`check_draft.py`）、风格度量（`style_metrics.py`）与配图检查（`check_figures.py`）。

## 许可（三层结构，务必完整保留）

| 部分 | 许可 | 说明 |
| --- | --- | --- |
| 上游原创内容（技能说明、references、模板、脚本等） | **CC BY 4.0** | 上游根目录 `LICENSE` 已随附；允许商用，**须署名** |
| `skills/bestpaper-writing/references/exemplars/` 中的获奖论文短句引用 | **不许可**（版权归原论文作者） | 仅作教学评论引用，**严禁复制进新论文**；上游明确声明不含任何论文 PDF 或全文 |
| 基础技能部分（后向再前向推理、摘要/引言模板等） | **MIT** | 改编自 [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills)（其知识源自彭思达的学习笔记），MIT 文本见 `skills/bestpaper-writing/LICENSE-base-skill`，署名见 `skills/bestpaper-writing/NOTICE.md` |

**注意**：本目录**不受本仓库 MIT 许可覆盖**——主体为 CC BY 4.0（需署名），exemplars 引用句完全不在许可范围内。`NOTICE.md`、`LICENSE`、`LICENSE-base-skill` 三个许可文件必须随技能一并分发。

## 与本仓库的适配说明

- 后续为入口补充中文触发词及稿件语言规则；中文稿件按中文学术规范人工检查，不套用英文语料阈值。许可字段与来源未变。
- 上游 `install.sh` 为 bash 一键安装（面向 Claude Code / Codex），Windows 用户直接将 `skills/bestpaper-writing/` 复制到目标工具的技能目录即可。
- `agents/openai.yaml` 为 Codex 专用界面配置，其他工具自动忽略。
- `plot_style.py` 依赖 matplotlib（仅绘制结果图时需要）；其余脚本（`check_draft.py` 等）纯 Python 标准库，已在 Python 3.13 下实测可运行。

## 文件对应关系

本目录与上游仓库根目录一一对应（唯一差异：不含上游 `.gitignore`；本 PROVENANCE.md 与顶层 README 登记为本仓库新增）。
