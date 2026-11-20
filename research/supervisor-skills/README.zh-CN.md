# Supervisor-Skills 科研技能集（本仓库收录版 · 中文导读）

> 收录自 [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills)——香港科技大学（广州）骆昱宇团队把十年顶会科研与审稿经验蒸馏成的 12 个可执行 AI 技能，覆盖从 Idea 构思、文献调研、论文写作、润色到投稿前审核的完整科研链路。

## ⚠️ 先看许可（与仓库其它技能不同）

本目录技能**不是 MIT 许可**，请务必先读 [`references/PROVENANCE.md`](references/PROVENANCE.md)：

| 项目 | 说明 |
|------|------|
| 整体来源许可 | **CC BY-NC-SA 4.0**（署名-非商业-相同方式共享） |
| 实际含义 | 可用于学习、研究等非商业用途；**不可用于商业目的**；改编后须以相同协议共享并注明出处 |
| 各技能差异 | 多数 SKILL.md 自带 `license` 字段（CC-BY 4.0 或 CC-BY-NC-SA 4.0），两个技能无该字段；`drawio-reconstruction` 的脚本与案例图来自另一 MIT 项目 |
| 与本仓库关系 | 本仓库 MIT 许可**不覆盖**本目录内容，这些文件保持其原始许可，未被改写 |

## 这是什么

12 个技能分成两条论文主线和一组横向工具：

- **技术类论文主线**：`idea-evaluator`（idea 体检）→ `tech-paper-template`（逻辑骨架）→ `intro-drafter`（Intro 正文）→ `paper-writer`（正文写作）→ `figure-designer`（配图设计）→ `drawio-reconstruction`（图片转可编辑 Draw.io）→ `paper-polish`（润色）→ `pre-submission-reviewer`（投稿前审核）
- **Benchmark 论文主线**：`benchmark-paper-template` 一站式覆盖 Gap→Design→Construction→Experiments→Structure→Checklist 六阶段
- **横向工具**：`deep-research`（综述级文献调研）、`vibe-research-workflow`（AI 辅助科研的行为守则）、`rebuttal-guidance`（Rebuttal 回应策略）

逐技能的 detailed 中文卡片见上游保留的 [`README.md`](README.md)（英文版 [`README.en.md`](README.en.md)）。

## 如何放入 AI 工具使用

技能本体是标准的 Agent Skills 结构（`SKILL.md` + 可选 `references/`），frontmatter 含 `name` / `description`，可被主流工具识别（Claude Code、Cursor、Codex、CodeBuddy、WorkBuddy 等）。

1. **作为一组整体安装**：技能间通过 `技能名` 互相引用（如 `idea-evaluator`、`paper-writer`），部分引用写作 "separate plugin"。请保持 12 个技能目录并列放在同一 skills 根目录，**不要零散挑选**，否则交叉引用会失效。
2. **安装方式**：把每个 `<skill>/` 目录复制到目标工具约定的 skills 目录（如 `.agents/skills/`、`.codebuddy/skills/` 等），或按工具文档配置 skills 目录指向本路径。安装后用自然语言即可触发，例如"帮我评估一下这个 idea" → `idea-evaluator`。
3. **语言**：技能正文为英文，但 `description` 里写明了触发场景，中文提问通常也能命中；若命中不稳定，可在 `description` 中补充中文触发词（属可选改造，不在本次收录范围）。

### 需要注意的环境依赖

绝大多数技能是纯提示词，**无需任何外部工具**。唯一例外：

- **`drawio-reconstruction`**：附带 5 个 Python 脚本（`scripts/`），依赖 **Python 3**、可选 **Pillow**（`pip install -r requirements.txt`）、**draw.io CLI**（用于导出 PNG 预览），批量任务还会用到**子代理并行**（不可用时自动降级为串行）。脚本路径通过运行时解析的 `$SKILL_DIR` 定位，不假定固定安装目录。若目标工具无法执行脚本，该技能只能作为参考文档使用。

## 目录结构说明

```
research/supervisor-skills/
├── README.md / README.en.md       # 上游保留的读者导读（其中指向 ../handbook/ 等链接在本仓库不可用，详见 PROVENANCE.md）
├── README.zh-CN.md                # 本文件：本仓库视角的中文导读
├── references/PROVENANCE.md       # 署名、许可与改动说明
├── idea-evaluator/                # 12 个技能，结构与上游一致
├── deep-research/
├── vibe-research-workflow/
├── tech-paper-template/
├── intro-drafter/
├── paper-writer/
├── benchmark-paper-template/
├── paper-polish/
├── pre-submission-reviewer/
├── figure-designer/
├── rebuttal-guidance/
└── drawio-reconstruction/         # 含 scripts/、assets/、examples/、LICENSE(MIT)
```

上游仓库另含 `handbook/`（六章科研系统指南）与根目录 `README.md`、`CONTRIBUTING.md` 等。本次仅收录可执行的 `skills/` 目录；需要方法论教程的读者请访问[上游仓库](https://github.com/HKUSTDial/Supervisor-Skills)。
