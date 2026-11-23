# PROVENANCE — gorden-ppt-skill 收录来源与许可声明

## 来源

- **上游项目**：[GordenSun/GordenPPTSkill](https://github.com/GordenSun/GordenPPTSkill)（用户提供的链接 `GordenPPTSkil` 少一个 L，实际仓库为 `GordenPPTSkill`）
- **拉取日期**：2026-11-23
- **本仓库落地路径**：`ppt/gorden-ppt-skill/`（本仓库新增顶层 `ppt/` 分类目录）
- **收录范围**：上游全部 108 个文件（剔除 `.gitattributes`/`.gitignore`），含 SKILL.md、6 个脚本、5 个 references、21 套中文模板（每套 template.pptx + intro.md + detail.json + preview.png）及版本管理文件

## 技能简介

AI 友好的中文 PPT 生成/编辑技能：21 套手工打磨的中文 PPTX 模板（工作汇报、述职竞聘、教学课件、商务提案、数据可视化等场景），基于 python-pptx 的**非破坏性纯文字编辑**（只换文字不动排版），内置按文本框尺寸的出框检测与同级标题字号一致校验。三种模式：内置模板挑选 / 用户自带模板 / 完全原创简洁版式。

## 许可（两层结构，务必完整保留）

| 部分 | 许可 | 说明 |
| --- | --- | --- |
| 源代码（`scripts/`、`references/`、SKILL.md、模板元数据 intro.md/detail.json、版本文件） | **MIT** | 上游根目录 `LICENSE` 已随附，允许商用与修改 |
| `templates/*/template.pptx` 与 `preview.png`（模板视觉资产） | **非商业 + 禁止二次分发** | 模板来自公开渠道（稻壳儿 / WPS 在线模板等），**版权归原模板作者，上游维护者不持有模板版权**，详见上游 `NOTICE.md` |

**⚠️ 合规警示（重要）**：

1. 上游 README 明确声明：本仓库没有 PPT 模板的版权，**禁止任何二次分发 / 商业使用**。本仓库收录模板文件属于二次分发行为，仅限**个人学习与研究**场景使用；对外分发前请自行评估风险，必要时可移除 `templates/` 仅保留代码与文档。
2. 模板**严禁用于任何商业用途**（商业演示、销售提案、付费培训、企业内部以营利为目的的使用等）。如需商用，必须联系**原模板作者**（见 PPTX 内"作者/设计师"元数据）取得书面授权——上游维护者无权授权。
3. `NOTICE.md`、`LICENSE` 两个许可文件必须随技能一并分发，不得移除或修改。

## 与本仓库的适配说明（为在 WorkBuddy 中可用所做的修订）

技能本体逻辑零改动，仅做了三处环境适配（源代码 MIT 允许修改）：

1. **自动更新机制改为可选**：上游 SKILL.md 要求"每次会话首次使用必须先跑 `python3 scripts/apply_update.py`"（从 GitHub 上游拉取增量更新）。在本仓库场景下该机制会从上游拉取并覆盖本地文件、且依赖 GitHub 网络访问，已改为**可选操作**并加编辑注记说明；`updates.json` 的 `update_source` 保持原样未动。
2. **Windows / WorkBuddy 环境注记**：脚本用 `python3` 调用，Windows 环境用 `python` 即可；`build_pptx.py` 依赖 `python-pptx`（`pip install python-pptx`）；`render_slides.py` 预览渲染依赖 LibreOffice + poppler（可选，无此环境可跳过预览直接交付 pptx）；SKILL.md 中提到的 `AskQuestion` 提问工具，在 WorkBuddy 中对应 `AskUserQuestion`。
3. **模板预览提示**：在 WorkBuddy 中向用户展示模板预览图时，直接读取 `templates/<slug>/preview.png` 文件即可。

其余工作流、编辑铁律、模板内容均保持上游原样。

## 文件对应关系

本目录与上游仓库根目录一一对应（差异：不含 `.gitattributes`/`.gitignore`；本 PROVENANCE.md 与顶层 README 登记为本仓库新增；SKILL.md 含上述第 1、2 点的适配注记）。
