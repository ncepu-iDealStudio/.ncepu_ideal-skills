# GitHub Copilot 项目指令

本仓库内置一个「SQL → FastAPI 脚手架」技能，位于：

```
.skills/sql-to-fastapi-restfulapi-scaffold/
├── SKILL.md                      # 技能主文件（必读）
├── README.md                     # 使用说明
└── resources/
    ├── config/                   # 类型映射、命名规则
    ├── specifications/           # 代码规范
    └── templates/                # 分层 / 项目结构模板
```

完整技能副本也同步在 `.codebuddy/skills/` 与 `.trae/skills/`。

## 触发场景

当用户提出以下需求时，请主动采用该技能：

- 提供 `SQL CREATE TABLE` 语句，要求生成 FastAPI 代码
- 要求从数据库表生成 RESTful 接口 / 脚手架
- 要求搭建 API、生成 Model / Schema / Repository / Service / Resource 分层代码
- 提到「SQL 转 FastAPI」「表到 API」「生成脚手架」等表述

## 使用方式

1. 先阅读并遵循 `.skills/sql-to-fastapi-restfulapi-scaffold/SKILL.md`，
   以及 `resources/specifications/coding_standards.md` 中的规范。
2. 读取 `resources/config/type_mappings.json` 与 `resources/config/naming_rules.json`
   作为类型映射与命名依据。
3. 参考 `resources/templates/` 下的分层模板与项目结构模板生成代码。
4. 可复用 `.github/prompts/sql-to-fastapi-restfulapi-scaffold.prompt.md`
   作为标准生成流程。

## 分层约定（务必遵守）

```text
API(Resource) → Service → Repository → Model
```

- Resource/API **只**依赖 Service；**禁止** Resource 直接 Depends Repository
- Repository：仅单条 `create` / `delete` / `update` / `get`，可覆盖生成
- Service：单条委托 + 列表/过滤/状态等业务；已存在则跳过
- Schema：进入 API 前完成字段校验；有状态字段时含 `StatusUpdate` + `PATCH /{pk}/status`

## 硬约束（务必遵守）

- 资源文件夹与路由前缀使用**表名单数**（如 `student` → `api/v1/student/`、前缀 `/student`），**禁止**复数化。
- 主键由数据库生成，不在创建输入中接收。
- 表中含 `is_deleted` / `is_delete` / `deleted` 字段时采用软删除，否则硬删除。
- 响应结构统一遵循本仓库规范。
- 所有文档字符串、注释、API 文档使用**中文**。
