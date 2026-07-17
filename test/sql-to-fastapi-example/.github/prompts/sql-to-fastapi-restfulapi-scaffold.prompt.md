---
description: 从 SQL CREATE TABLE 语句生成 FastAPI 项目脚手架（Model/Schema/Repository/Service/Resource），遵循本仓库技能规范
mode: agent
---

# SQL → FastAPI 脚手架生成

当用户提供 `SQL CREATE TABLE` 语句，或要求从数据库表生成 FastAPI 接口 / 脚手架时，
严格按以下步骤执行。

## 步骤

1. 先阅读并遵循技能规范：
   - 读取 `.skills/sql-to-fastapi-restfulapi-scaffold/SKILL.md`
   - 读取 `.skills/sql-to-fastapi-restfulapi-scaffold/resources/specifications/coding_standards.md`
2. 读取类型映射与命名规则：
   - `.skills/sql-to-fastapi-restfulapi-scaffold/resources/config/type_mappings.json`
   - `.skills/sql-to-fastapi-restfulapi-scaffold/resources/config/naming_rules.json`
3. 参考分层模板生成代码：
   - `.skills/sql-to-fastapi-restfulapi-scaffold/resources/templates/layers/`（model / schema / repository / service / resource）
   - `.skills/sql-to-fastapi-restfulapi-scaffold/resources/templates/project_structure/`（完整项目骨架）
4. 先输出「生成计划预览」：新增 / 更新 / 跳过文件清单、冲突与解析告警，
   **经用户确认后再生成代码**。
5. 生成完成后，输出：新增文件清单、更新文件清单、跳过文件清单、解析/冲突告警。

## 分层约定

```text
API(Resource) → Service → Repository → Model
```

- Resource/API **只**依赖 Service；**禁止** Resource 直接 Depends Repository
- Repository：可覆盖；仅单条 `create` / `delete` / `update` / `get`
- Service：仅不存在时生成；单条委托 + 列表/过滤/状态等业务
- DI：Resource 使用 `Depends(get_*_service)`；Service 内部构造 Repository

## 硬约束（务必遵守）

- 资源文件夹与路由前缀使用**表名单数**（如 `company_file` → `api/v1/company_file/`、前缀 `/company-file`），
  **严禁**复数化；复数仅可用于中文 `tags` 展示文案。
- 主键由数据库生成，不在创建输入中接收；不对主键做唯一性检查。
- 表中含 `is_deleted` / `is_delete` / `deleted` 字段时采用软删除；否则硬删除。
- 响应结构统一遵循本仓库规范；分页参数按项目约定。
- 所有文档字符串、注释、API 文档使用**中文**；对手机号 / 邮箱等敏感字段做脱敏。
