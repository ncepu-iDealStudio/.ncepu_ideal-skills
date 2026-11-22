# PROVENANCE — research-weave 移植来源与许可声明

## 来源

- **上游项目**：[NeuraLiying/research-weave-skill](https://github.com/NeuraLiying/research-weave-skill)
- **上游技能路径**：`skills/research-weave/`
- **拉取日期**：2026-11-20
- **本仓库落地路径**：`research/research-weave/`

## 许可

- 上游项目采用 **MIT License**，与本仓库技能的通行许可一致，无合规冲突。
- 上游原始 `LICENSE` 文件已随技能一并保留在本目录（`research/research-weave/LICENSE`）。
- SKILL.md frontmatter 自带 `license: MIT` 字段，保留原样。

## 文件对应关系

本目录文件与上游 `skills/research-weave/` 逐字一致（未做任何内容改写）：

| 本仓库文件 | 上游文件 |
| --- | --- |
| `SKILL.md` | `skills/research-weave/SKILL.md` |
| `agents/openai.yaml` | `skills/research-weave/agents/openai.yaml` |
| `references/contradictions.md` | `skills/research-weave/references/contradictions.md` |
| `references/evidence-method.md` | `skills/research-weave/references/evidence-method.md` |
| `references/output-contract.md` | `skills/research-weave/references/output-contract.md` |
| `references/scout-format.md` | `skills/research-weave/references/scout-format.md` |
| `scripts/check_evidence.py` | `skills/research-weave/scripts/check_evidence.py` |
| `LICENSE` | 上游仓库根目录 `LICENSE` |

上游仓库级的 README、evals、tests、docs 未纳入本仓库（不属于技能本体）。

## 改动说明

仅新增本 PROVENANCE.md 与顶层 README 登记，技能本体零改动。

## 使用提示

- `agents/openai.yaml` 为 Codex 专用界面配置，其他工具会自动忽略，无害。
- `scripts/check_evidence.py` 仅依赖 Python 标准库（已在 Python 3.13 下实测可运行）。
- 与 `research/supervisor-skills/deep-research` 定位互补：后者产出综述级调研报告，本技能侧重阅读决策与可追溯证据账本。
