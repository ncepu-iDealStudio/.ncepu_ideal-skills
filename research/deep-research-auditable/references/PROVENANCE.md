# 来源与许可（PROVENANCE）

## 上游信息

| 项目 | 内容 |
| --- | --- |
| 技能名称（上游） | `deep-research-skill`，技能名 `deep-research` |
| 上游仓库 | https://github.com/hyderhusainarastu/deep-research-skill |
| 作者 | hyderhusainarastu |
| 许可证 | MIT License（见本目录 `../LICENSE`，Copyright (c) 2026 hyderhusainarastu） |
| 收录日期 | 2026-11-27 |
| 收录范围 | 全仓库 29 个文件（SKILL.md、PROMPT(.short).md、README、AGENTS/CLAUDE/GEMINI 指针、install.sh、test_install.sh、references/ 7 篇、templates/ 3 份、scripts/ 2 个、tests/ 2 个、examples/toy-run 3 个、.github 2 个） |

## 许可声明

本技能遵循 MIT 许可证，允许商用、修改、分发，但须保留版权与许可声明。本仓库的收录与本地改造同样在 MIT 框架下进行，`LICENSE` 原文随技能一同保留，未作改动。

## 本地改造记录

| # | 改造项 | 原因 | 处理方式 | 影响文件 |
| --- | --- | --- | --- | --- |
| 1 | 技能改名 `deep-research` → `deep-research-auditable`，目录同步改名 | 与本仓库已收录的 `research/supervisor-skills/deep-research` 同名；两个技能同时安装会互相覆盖，导致触发错乱 | 修改 `SKILL.md` frontmatter `name`，并把目录 `deep-research-skill/` 改名为 `deep-research-auditable/` | `SKILL.md`、目录名 |
| 2 | 更新测试中的名字断言 | 上游测试硬编码校验 `name == "deep-research"`，改名后测试会失败 | 同步断言为 `deep-research-auditable` | `tests/test_package.py` |
| 3 | 精简 description | 改名时补充了触发条件，需满足上游测试对 description ≤300 字符的约束 | 重写为 253 字符的触发条件描述 | `SKILL.md` |
| 4 | AGENTS.md / README.md 名字引用同步 | 文档内部仍指向旧名 | 更新标题、技能名、安装路径、示例调用语；保留上游 git clone 地址不变 | `AGENTS.md`、`README.md` |
| 5 | README 增加本地说明与 WorkBuddy 行 | 说明改名来源、补充本仓库目标平台的安装方式 | 在 README 顶部加本地说明块，Works with 表加 WorkBuddy 行 | `README.md` |
| 6 | 新增中文导读 | 仓库惯例：外部收录技能提供中文入口 | 新建 `README.zh-CN.md` | `README.zh-CN.md`（新增） |
| 7 | 新增本文件 | 仓库惯例：署名、许可、改造记录可追溯 | 新建 `references/PROVENANCE.md` | 本文件（新增） |

## 未改动的部分

- 核心方法论（Wave 0-5、验证等级、饱和停止规则、有界否定）保持上游原文，未作内容改动。
- 全部脚本（`scripts/lexical_audit.py`、`scripts/check_csv.py`）保持上游原文。
- `templates/`、`examples/toy-run/`、`references/` 其余 7 篇方法论文档保持上游英文原文。
- 未新增任何运行时依赖；脚本仅用 Python 标准库。

## 验证记录（收录时）

在本机 Windows / Python 环境下执行：

- `python -m pytest -q` → **12 passed**（含改名后的断言）
- `python scripts/check_csv.py examples/toy-run` → `1 file(s) checked, 0 problem(s)`
- `bash install.sh --help` → 正常输出用法，安装路径已显示新名 `deep-research-auditable`

## 与同类技能的关系

- **`supervisor-skills/deep-research`**（本仓库已收录，CC BY-NC-SA）：调研级深度文献综述，冻结研究问题、多对抗视角检索、MECE 证据综合，输出证据优先的综述报告。偏「出报告」。
- **`deep-research-auditable`**（本技能，MIT）：偏「可审计流程」——显式验证等级、查询日志、角色分离、饱和停止规则、有界否定结论，强调"查了什么、开了什么、何时停止"。
- **`research-weave`**（本仓库已收录，MIT）：偏「决定读什么」，论文淘金与证据网络。
- **`auto-empirical-research/check-citations`**（本仓库已收录）：引用真实性事后核查，可与本技能叠加使用于产出物。
