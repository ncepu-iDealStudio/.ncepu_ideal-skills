# 技能部署说明（sql-to-fastapi-restfulapi-scaffold）

本目录是「SQL → FastAPI RESTful 脚手架」技能的多工具分发源。技能本体位于
`sql-to-fastapi-restfulapi-scaffold/`，其结构遵循标准 skill 规范：

```
sql-to-fastapi-restfulapi-scaffold/
├── SKILL.md          # 入口：YAML frontmatter(name + description) + Markdown 指令
├── README.md         # 技能说明与各 IDE 配置指引
└── resources/        # 资源驱动：templates / config / specifications
    ├── templates/layers/{model,schema,repository,service,resource,test}/
    ├── config/{naming_rules.json, type_mappings.json, status_flag_fields.json, ...}
    └── specifications/coding_standards.md
```

同级技能目录内还有 `docs/`：各 IDE 配置说明（Trae / Claude / Copilot 归档等）。

`name` 字段统一为 `sql-to-fastapi-restfulapi-scaffold`（与文件夹名一致、无引号），
已通过 hyphen-case 校验，可被各工具识别。

**架构约定**：`API (Resource) → Service → Repository → Model`。

| 层 | 职责 | 生成策略 |
|----|------|----------|
| Repository | 仅单条 `create` / `get` / `update` / `delete` | 可覆盖 |
| Service | 单条委托；列表 / 过滤 / 状态等业务 | 已存在则跳过 |
| Resource | 只依赖 Service | CRUD 可覆盖 |
| Tests | `unit` 占位 + `integration` CRUD | 已存在则跳过 |
| 基线 | `utils` / `middleware` / `docker` / `deploy` / `.env.docker` | 已存在则跳过；空项目完整拷贝 |

---

## 四套工具的技能位置对照

| 工具 | 技能目录 / 配置文件 | 发现机制 | 是否需要额外配置 |
| ------ | --------------------- | ---------- | ------------------ |
| **CodeBuddy** | `.codebuddy/skills/sql-to-fastapi-restfulapi-scaffold/` | 自动扫描项目级 `.codebuddy/skills/` | 否，打开项目即生效 |
| **Trae** | `.trae/skills/sql-to-fastapi-restfulapi-scaffold/` | 在 Trae 设置中把 `.trae/skills/` 添加为技能目录 | 是，需在设置里添加目录后重启 |
| **GitHub Copilot** | `.github/copilot-instructions.md` + `.github/prompts/sql-to-fastapi-restfulapi-scaffold.prompt.md` | 项目指令自动加载；prompt 文件可在 Copilot Chat 中调用 | 否（指令自动生效）；prompt 可在 Chat 中 `#` 引用 |
| **其它 AI 工具（原始副本）** | `.skills/sql-to-fastapi-restfulapi-scaffold/`（本目录） | 视具体工具约定，作为通用源 | 取决于目标工具 |

> CodeBuddy / Trae 的副本为完整拷贝（34 个文件）；GitHub Copilot 通过
> `copilot-instructions.md` 中的相对路径直接引用本目录下的 `SKILL.md` 与 `resources/`，
> 避免多处重复维护。

---

## 触发场景（各工具一致）

当对话中出现以下意图时，技能应被触发：
- 用户提供 SQL `CREATE TABLE` 语句
- 用户要求从数据库表生成 FastAPI 接口代码（RESTful 风格）
- 用户要求搭建 API 或生成脚手架代码
- 用户提到「SQL 转 FastAPI」「表到 API」「生成脚手架」等表述

---

## 配置参考文档

各工具配置说明在技能目录的 **`sql-to-fastapi-restfulapi-scaffold/docs/`**：
- `docs/Trea中使用skill配置.md` —— Trae
- `docs/claude中使用skill配置.md` —— Claude Code
- `docs/GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md` —— 归档：
  **注意** 这是 *另一个 Flask 技能* 的文档，**不可直接套用**本 FastAPI 技能。
  Copilot 请以仓库根目录 `.github/copilot-instructions.md` 与对应 prompt 为准。

---

## 维护约定

- 修改技能逻辑（模板 / 规范 / 配置）时，**先改本目录的源副本**，再同步到
  `.codebuddy/` 与 `.trae/` 两份完整副本（资源文件较多，建议用 `robocopy /E` 整体覆盖）。
- `name` 字段、目录名必须始终保持一致且为小写连字符、不带引号。
- 不要在本目录源副本里写 `copilot-instructions.md` 相关内容（那是 Copilot 专属，
  已在 `.github/` 单独维护）。
