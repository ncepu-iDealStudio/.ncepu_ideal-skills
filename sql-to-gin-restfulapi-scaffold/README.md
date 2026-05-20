# SQL-to-Gin-RESTfulAPI-Scaffold

## 里程碑状态

- 当前阶段：V1 可用
- 全量覆盖：11/11（基于 `test/study_flask_api.sql`）
- 回归方式：支持一键执行
    - `python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py`
- 防回归机制：已启用快照校验（context + manifest）

## 项目简介

`sql-to-gin-restfulapi-scaffold` 是一个 Skill 项目，目标是基于 MySQL DDL 自动生成 Gin + GORM 风格的企业级 RESTful API 脚手架。

目标结构参考：`test/sql-to-gin-example`。

输入样例 SQL：`test/study_flask_api.sql`。

## V1 目标

V1 聚焦三件事：

- 生成可运行的 Gin 分层项目骨架
- 基于 SQL 自动生成表/视图对应接口代码
- 支持首次全量生成与后续增量生成

## 技术与风格对齐

- Gin
- GORM
- Viper
- Cobra
- 分层结构：`models / dao / services / apis`

## 解析边界（V1）

V1 仅覆盖常见 MySQL DDL：

- `CREATE TABLE`
- `CREATE VIEW`
- 主键
- 默认值
- 注释

超出边界语法处理：

- 跳过
- 输出告警

## 生成清单（V1）

### 1. 首次生成（项目骨架）

- `main.go`
- `cmd/`
- `apis/`
- `internal/`
- `configs/`
- `utils/`
- `go.mod`

### 2. 表实体生成（每张表）

- `internal/models/{Entity}.go`
- `internal/dao/{Entity}.go`
- `internal/services/{Entity}.go`
- `apis/api_1_0/{resource}/urls.go`
- `apis/api_1_0/{resource}/{Entity}Resource.go`
- `apis/api_1_0/urls.go` 增量注册

### 3. 视图生成（每个 view）

- 只读 model
- 查询 service
- 查询 resource（仅集合查询路由）

### 4. 增量生成

- 合并注册文件
- 已存在实体文件跳过
- 输出冲突告警

## 不生成清单（V1）

- 自动化测试代码
- 部署文件（Docker/Nginx）
- CI/CD 配置
- 自动鉴权白名单
- 复杂联表分析接口

## 命名与主键规则

- `module_name` 统一为 snake_case
- URL 路径统一 snake_case 风格
- 路径参数名统一 snake_case 风格
- 接口主键统一使用 SQL 表定义的主键

说明：

- 若主键是 `auto_id/autoID`，则按该主键生成
- 若想使用业务主键，请在建表时定义为主键

## 字段与软删除规则

- 字段名尽量保持 SQL 原样，不自动改名
- 软删除字段识别：`is_delete`、`is_deleted`、`isDelete`、`isDeleted`
- `get/update` 默认过滤已软删除记录

## 统一响应协议

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

- `Page` 默认 `1`
- `Size` 默认 `10`
- `Size` 最大 `100`

超出上限时按 `100` 处理并提示。

## 目录建议（Skill 项目）

```text
sql-to-gin-restfulapi-scaffold/
├── README.md
├── SKILL.md
└── resources/
    ├── config/
    ├── specifications/
    ├── templates/
    │   ├── project_structure/
    │   └── layers/
    ├── static/
    │   └── utils/
    ├── tools/
    └── demo_output/
```

## 下一步开发顺序

1. 完成 `resources/config/` 的规则文件（命名、类型映射、生成档位、上下文样例）。
2. 完成 `resources/specifications/` 的规范契约文档（解析边界、路由合并、字段渲染规则）。
3. 补齐 `resources/templates/` 的项目骨架模板与分层模板。
4. 增加 `resources/tools/` 的校验与预览脚本。
5. 用 `test/study_flask_api.sql` 做预览渲染与回归比对。

## 本地预演命令

在仓库根目录执行以下命令可快速验证 Skill 资源闭环：

```bash
python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py

# initialize/refresh snapshots when expected output intentionally changes
python sql-to-gin-restfulapi-scaffold/resources/tools/check_snapshots.py --update

# validate snapshots only
python sql-to-gin-restfulapi-scaffold/resources/tools/check_snapshots.py

# or run each step manually
python sql-to-gin-restfulapi-scaffold/resources/tools/generate_context_from_sql.py test/study_flask_api.sql sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json study_flask_api study_flask_api
python sql-to-gin-restfulapi-scaffold/resources/tools/validate_template_context.py sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json
python sql-to-gin-restfulapi-scaffold/resources/tools/preview_generation_plan.py sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json
python sql-to-gin-restfulapi-scaffold/resources/tools/render_demo_single_entity.py sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json 0
python sql-to-gin-restfulapi-scaffold/resources/tools/render_preview_bundle.py sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json
python sql-to-gin-restfulapi-scaffold/resources/tools/merge_router_registry.py sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json sql-to-gin-restfulapi-scaffold/resources/templates/project_structure/apis/api_1_0/urls.go

# legacy example-context quick checks
python sql-to-gin-restfulapi-scaffold/resources/tools/validate_template_context.py sql-to-gin-restfulapi-scaffold/resources/config/template_context_example.json
python sql-to-gin-restfulapi-scaffold/resources/tools/preview_generation_plan.py sql-to-gin-restfulapi-scaffold/resources/config/template_context_example.json
python sql-to-gin-restfulapi-scaffold/resources/tools/render_demo_single_entity.py sql-to-gin-restfulapi-scaffold/resources/config/template_context_example.json 0
python sql-to-gin-restfulapi-scaffold/resources/tools/render_preview_bundle.py sql-to-gin-restfulapi-scaffold/resources/config/template_context_example.json
python sql-to-gin-restfulapi-scaffold/resources/tools/merge_router_registry.py sql-to-gin-restfulapi-scaffold/resources/config/template_context_example.json sql-to-gin-restfulapi-scaffold/resources/templates/project_structure/apis/api_1_0/urls.go
```

说明：

- `run_regression_pipeline.py`：一键执行 generate + validate + preview + render + merge + coverage，并输出 pipeline_report.json。
- `check_snapshots.py`：校验（或用 `--update` 刷新）context 与 manifest 的快照基线。
- `generate_context_from_sql.py`：从 SQL DDL 自动生成完整 context JSON。
- `validate_template_context.py`：校验渲染上下文字段完整性。
- `preview_generation_plan.py`：预览实体对应文件生成计划。
- `render_demo_single_entity.py`：渲染单实体样例。
- `render_preview_bundle.py`：渲染全部实体预览并生成 manifest。
- `merge_router_registry.py`：按标记块增量合并 `urls.go` 的导入和路由注册。
