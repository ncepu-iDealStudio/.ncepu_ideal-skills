---
name: "sql-to-gin-restfulapi-scaffold"
description: "从 MySQL DDL（CREATE TABLE/CREATE VIEW）生成 Gin + GORM 风格的分层 RESTful API 项目脚手架。支持已有项目增量：按 incremental_change_policy.json 判定 greenfield/add_table/alter_table/drop_table，做字段级差异分析、分层重生成、手写代码保护、路由注册幂等（复用 merge_router_registry.py）、go build 验证与 DDL 建议。"
---

# SQL-to-Gin-RESTfulAPI-Scaffold Skill

## 里程碑状态

- 当前阶段：V1 可用
- 全量覆盖：12/12（11 表 + 1 视图，基于 `test/api_security_demo-20260717.sql`）
- 回归入口：
  - `python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py`
- 防回归机制：快照校验（context + manifest）已接入流水线
- 基线 SQL：`test/api_security_demo-20260717.sql`（真实存在的仓库内文件；旧版 `test/study_flask_api.sql` 已移除，文档与产物均已对齐）
- 增量能力：已支持已有项目的 `add_table` / `alter_table` / `drop_table`（见步骤 2）

## 概述

`sql-to-gin-restfulapi-scaffold` 是一个资源驱动技能，用于从 SQL 建表/视图语句生成 Gin RESTful 风格的分层接口项目脚手架。

本技能强调：

- 可启动
- 路由可访问
- CRUD 可跑通
- 支持首次全量生成与后续增量生成

## 适用场景

当用户出现以下需求时应触发本技能：

- 提供 SQL 脚本并要求生成 Gin RESTful API 项目
- 根据数据库表结构自动生成分层 Go 代码
- 希望快速搭建 Gin + GORM 的企业级接口骨架
- **已有项目中新增表**：在现有脚手架里按实体补齐 5 类文件并追加路由注册
- **已有项目中表结构修改**：新增/删除列、改类型或约束、改主键、状态位与软删字段变化 → 走字段级差异分析
- 用户说「表加了几个字段」「更新一下这张表的接口」「重新同步 DDL」「把新表加进已有项目」等增量表述

## V1 解析边界

V1 仅支持常见 MySQL DDL：

- `CREATE TABLE`
- `CREATE VIEW`
- 主键
- 默认值
- 注释

超出边界语法：

- 跳过该语句
- 在生成报告中写入告警

## V1 生成范围

### 首次生成（完整骨架）

- `main.go`
- `cmd/`
- `apis/`
- `internal/`
- `configs/`
- `utils/`
- `go.mod`
- `go.sum`（可选）

### 表实体生成（每张表）

- `internal/models/{Entity}.go`
- `internal/dao/{Entity}.go`
- `internal/services/{Entity}.go`
- `apis/api_1_0/{resource}/urls.go`
- `apis/api_1_0/{resource}/{Entity}Resource.go`
- 更新 `apis/api_1_0/urls.go` 的路由注册

### 视图生成（每个 view）

- 只读 model
- 查询 service
- 查询 resource（仅集合查询路由）
- 不生成新增/更新/删除

### 增量生成（详见步骤 2）

- **先判定运行模式**（逐实体）：`greenfield` / `add_table` / `alter_table` / `drop_table`
- **新增表**：按实体生成 5 类文件 + **幂等追加** `apis/api_1_0/urls.go` 注册（优先复用 `merge_router_registry.py`）
- **表结构变更**：先做**字段级差异分析**，输出差异清单与风险等级，用户确认后按文件归属分层更新
- **表下线**：只输出待删清单，**不自动删文件、不执行 DDL**
- 手写文件（`services/`）**绝不覆盖**，只输出人工待办
- 每次增量后**必须 `go build ./...` 通过**

## 命名与主键规则

- `module_name` 统一下划线风格（snake_case）
- URL 风格统一下划线（如 `/student_selected_course`）
- 路径参数名统一下划线
- API 路由主键统一使用 SQL 中定义的主键

说明：

- 若主键为 `auto_id/autoID`，则使用该主键
- 若希望使用业务主键，应在建表时将业务主键定义为主键

## 字段处理规则

- 模型属性尽量保持 SQL 原字段名，不自动改名
- 软删除字段识别支持常见命名（如 `is_delete`、`is_deleted`、`isDelete`、`isDeleted`）
- 在 `get/update` 默认附加未删除过滤条件

## 响应协议

统一响应字段：

- `code`
- `message`
- `data`
- `totalCount`
- `totalPage`

错误响应最小字段：

- `code`
- `message`
- `err`

## 分页约定

固定分页参数与默认值：

- `Page` 默认 `1`
- `Size` 默认 `10`
- `Size` 最大 `100`

当 `Size` 超过上限时，按上限处理并返回提示信息。

## 文件冲突策略

> ⚠️ 本节是最简表述。**已有项目场景请以「步骤 2 增量流程」为准**，那里按文件归属做了分级处理，不再一律跳过。

- 默认合并注册文件
- 跳过已存在实体文件
- 在输出中追加告警

---

## 使用流程

### 步骤 1: 解析 SQL 并识别实体

解析 `CREATE TABLE` / `CREATE VIEW`，逐实体提取：

- `entity_name`（PascalCase）、`resource_slug`、`router_init_func`
- 字段定义（`go_field_name` / `gorm_tag` / `json_tag` / `form_tag` / 类型 / 主键 / 外键 / 注释）
- **软删除字段**、**状态/标识位字段**
- 路由参数名 `route_param_name`（来自主键）

增量场景额外解析：

- 用户是否同时给出**旧版 DDL**（供差异分析使用）
- 项目内 `resources/demo_output/generated_context_*.json` 是否可作为结构基线

### 步骤 2: 判定运行模式（强制，逐实体）

**先读 `resources/config/incremental_change_policy.json` 与 `resources/specifications/incremental_update.md`**，按 `mode_detection` 逐实体判定：

| 模式 | 判定 | 动作 |
|------|------|------|
| `greenfield` | 骨架（`go.mod` / `main.go` / `internal/models` / `apis/api_1_0/urls.go`）不存在 | 生成完整骨架 + 本次全部实体 |
| `add_table` | 骨架存在，且该实体 5 类文件全部不存在 | 按实体生成文件 + **幂等追加注册** |
| `alter_table` | 骨架存在，且该实体任一文件已存在 | **先做字段级差异分析**，再按 `change_types` 分层更新 |
| `drop_table` | 用户明确要求下线表 | 只输出待删清单，**不自动删文件、不执行 DDL** |

判定要点：

- 一次给多张表时逐实体判定，允许同批混用 `add_table` 与 `alter_table`
- 残留文件不成套 → **先询问用户**补齐还是重生成，禁止默认覆盖
- **「用户又给了一遍建表 SQL」≠ 重新建表**：已有文件就必须走 `alter_table`
- 基线包（`internal/settings/`、`internal/globals/`、`internal/rpcServer/`、`configs/`、`utils/`、`cmd/`、`init/`）在以上任何模式下都**完全不碰**

### 步骤 2.1: 表结构变更的差异分析与分层更新（`alter_table` 强制）

完整流程见 `resources/specifications/incremental_update.md`，策略表见 `incremental_change_policy.json → change_types`。

1. **取旧结构**：依次尝试「用户旧版 DDL / `database/*.sql`」→ `internal/models/{Entity}.go` 的 struct 与 gorm tag → `demo_output` 的 context JSON →（仅用户同意时）`information_schema`。取不到就询问用户，**不要猜差异**。
2. **归一化后逐字段比对**：大小写、字段顺序、驼峰↔下划线差异忽略；但 **`int64` 与 `int` 不视为等价**（影响 json 大数精度，必须报告）；`soft_delete_field` 与 `status_flag_set` 用最新 SQL **重新计算**。
3. **先输出差异清单**（`added` / `removed` / `type_changed` / `tag_changed` / `flag` / `comment_only` / 风险等级），`critical`+`high` 项先向用户确认；`removed + added` 疑似重命名时先问清。
4. **按影响面更新**（详见规范第 3 节矩阵）：
   - 覆盖 `internal/models/{Entity}.go`（带生成标记）；
   - 覆盖 `internal/dao/{Entity}.go`（仅基础 CRUD，通用性强）；
   - 重生成 `apis/api_1_0/{slug}/{Entity}Resource.go` 的 CRUD，**保留自定义 handler**；`urls.go`（组内）可整体重生成；
   - `internal/services/{Entity}.go` 与 `README.md` **绝不整文件覆盖**，改为输出「人工待办清单」；
   - `internal/settings/**` `internal/globals/**` `configs/**` `utils/**` `cmd/**` `init/**` 完全不碰。
5. **三条强制同步规则**（漏一条就会编译失败或运行期报错）：
   - 状态位：`Resource` handler ↔ `urls.go` 路由 ↔ `Service` 业务校验 **同进同退**。新增状态位时，若 Service 需补方法，须**展示代码片段 → 取得用户确认 → 追加到文件末尾**；追加后立即 `go build` 验证。
   - 软删字段：`models` 与 `dao` 可覆盖，但 `services` 里 `GetList` 的软删过滤在手写文件中，**必须列入待办**。
   - 主键：变化会贯穿 `models` 的 `primaryKey` tag → `services` 签名 → `Resource` 路径参数 → `urls.go` 的 `url_item` 模板。Go 特有风险：`urls.go` 的 `:param` 与 `Resource` 里 `c.Param(...)` **必须字面一致**。
6. **输出 DDL 建议**：技能不执行任何 DDL、不改写 `database/`、不接 golang-migrate、**不启用 GORM AutoMigrate 作为生产迁移**、不删数据；只给 `ddl_hint` 与发布顺序建议。

### 步骤 2.2: 新增表的注册与幂等（`add_table` 强制）

1. 按实体生成 5 类文件（`services` 仅在不存在时生成）。
2. **优先复用既有工具**做注册幂等：

   ```bash
   python resources/tools/merge_router_registry.py <context.json> <urls.go>
   ```

   该工具已实现去重、排序、重复执行零 diff。
3. 手工追加时，在 `apis/api_1_0/urls.go` 的 marker 区块内：
   - `AUTO_IMPORTS` 区：`{alias} "{module_name}/apis/api_1_0/{resource_slug}"`
   - `AUTO_REGISTRY` 区：`{alias}.{router_init_func}(Api)`
4. **幂等要求**：追加前检查 import 路径是否已存在；同一 SQL 重复生成必须**零 diff**；marker 缺失时不自动修改，输出待办并告警。

### 步骤 3: 生成代码

按判定出的模式与影响面，从 `resources/templates/` 渲染对应文件。

### 步骤 4: 自检（强制）

- **编译自检**：`go build ./...`（Go 无运行时容错，字段改名/签名不一致会直接失败）
- **静态检查**：`go vet ./...`
- **回归自检**：`python resources/tools/run_regression_pipeline.py`
- **幂等自检**：`python resources/tools/check_snapshots.py`，确认零 diff

> `go build` 不通过时**不得宣称完成**。

### 步骤 5: 输出变更报告

必含：运行模式判定、结构差异清单（含风险）、逐文件动作（覆盖/追加/跳过/待办）、人工待办清单、DDL 建议与发布顺序、编译与回归结果。

## 输出结果要求

生成完成后必须输出：

- 新增文件列表
- 更新文件列表
- 跳过文件列表
- 语法跳过告警
- 冲突告警
- 成功/失败统计

## 生成 README.md

在生成完所有文件后，AI 应读取生成的项目结构，动态生成一份详细的 README.md 文档，包含：

- 项目简介和技术栈
- 完整的项目结构说明
- 所有生成的 API 接口说明（包含请求/响应示例）
- 配置说明
- 快速开始步骤
- 统一响应协议说明
- 软删除机制说明

## V1 不生成清单

- 自动化测试代码
- Docker/Nginx 等部署文件
- CI/CD 配置
- 自动鉴权白名单写入逻辑
- 复杂联表分析接口生成

## 验收标准

至少覆盖两组样例：

- 单表
- 复杂多表（含视图）

判定标准：

- 项目可启动
- 路由可访问
- CRUD 可跑通
