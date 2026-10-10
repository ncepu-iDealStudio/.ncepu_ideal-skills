# sql-to-gin-restfulapi-scaffold

## 项目简介

### 1. 本项目是干嘛的

`sql-to-gin-restfulapi-scaffold` 是一个面向 AI 开发场景的 Skill 项目，用于将 MySQL DDL（`CREATE TABLE` / `CREATE VIEW`）转换为 Gin + GORM 风格的分层 RESTful API 脚手架。

它的核心目标是：

1. 通过规则和模板把生成行为标准化。
2. 通过上下文校验、计划预览、快照比对保证可验证。
3. 通过路由增量合并机制支持后续演进，避免覆盖人工代码。

当前参考生成对象为 `test/sql-to-gin-example`，基线 SQL 为 `test/study_flask_api.sql`。

### 2. 技术栈和依赖版本

本项目分为两类依赖：

1. 生成目标项目（Go）依赖模板
- Go: `1.21`
- `github.com/gin-gonic/gin`: `v1.9.1`
- `gorm.io/gorm`: `v1.25.10`
- `gorm.io/driver/mysql`: `v1.5.7`
- `github.com/spf13/cobra`: `v1.8.0`
- `github.com/spf13/viper`: `v1.18.2`

2. Skill 工具链（Python）依赖
- Python: 建议 `3.10+`
- 当前 `resources/tools/*.py` 使用标准库（`json`、`argparse`、`pathlib`、`subprocess`、`re` 等），无需额外第三方包。

### 3. 本项目代码文件夹结构详细说明

```text
sql-to-gin-restfulapi-scaffold/
├── README.md
├── SKILL.md
└── resources/
    ├── config/
    │   ├── naming_rules.json
    │   ├── type_mappings.json
    │   ├── generation_profiles.json
    │   └── template_context_example.json
    ├── specifications/
    │   ├── coding_standards.md
    │   ├── sql_parser_contract.md
    │   ├── template_context_schema.md
    │   ├── router_registry_merge_strategy.md
    │   ├── field_rendering_rules.md
    │   └── generation_preview_study_gin_api.md
    ├── templates/
    │   ├── project_structure/
    │   │   ├── main.go
    │   │   ├── go.mod
    │   │   ├── apis/
    │   │   ├── cmd/
    │   │   ├── configs/
    │   │   ├── internal/
    │   │   └── utils/
    │   └── layers/
    │       ├── model/
    │       ├── dao/
    │       ├── service/
    │       └── resource/
    ├── tools/
    │   ├── generate_context_from_sql.py
    │   ├── validate_template_context.py
    │   ├── preview_generation_plan.py
    │   ├── render_demo_single_entity.py
    │   ├── render_preview_bundle.py
    │   ├── render_utils.py
    │   ├── merge_router_registry.py
    │   ├── check_snapshots.py
    │   └── run_regression_pipeline.py
    ├── demo_output/
    │   ├── generated_context_study_flask_api.json
    │   ├── pipeline_report.json
    │   ├── regression_report_study_gin_api.md
    │   ├── urls_merge_preview.go
    │   ├── bundle_preview/
    │   ├── single_entity/
    │   └── snapshots/
    └── static/
        └── utils/
            ├── README.md
            └── core/
                ├── path.go
                ├── errors.go
                ├── case.go
                └── struct_map.go
```

目录职责说明：

1. `resources/config/`
- 管理命名规则、类型映射、生成档位等策略输入。

2. `resources/specifications/`
- 定义解析契约、模板上下文约束、路由合并策略与编码规范。

3. `resources/templates/`
- 存放项目骨架模板与分层代码模板，是最终代码产出的渲染来源。

4. `resources/tools/`
- 提供从 SQL 到 context、校验、预览、渲染、合并、快照、回归的一体化工具链。

5. `resources/demo_output/`
- 存放演示产物与回归证据，便于结果审查与防回归。

6. `resources/static/utils/`
- 存放可复用的轻量 runtime 工具资产（当前包含 `core` 通用方法）。

---

## 生成的目标项目说明

### 1. 生成的目标项目结构

目标项目为 Gin 分层结构。技能模板 `resources/templates/project_structure/` 提供 `main.go`、`cmd/`、`apis/`、`internal/`、`configs/`、`utils/`、`go.mod`。下面是示例工程 `test/sql-to-gin-example` 的实际目录：

```text
sql-to-gin-example/
├── main.go
├── go.mod
├── go.sum
├── cmd/
├── init/
├── apis/
│   ├── routers/
│   ├── middlewares/
│   └── api_1_0/
├── internal/
│   ├── models/
│   ├── dao/
│   ├── services/
│   ├── globals/
│   ├── settings/
│   ├── remote/
│   └── rpcServer/
├── configs/
├── utils/
├── pkg/
├── assets/
├── scripts/
└── deploy/
```

其中 `init/`、`pkg/`、`assets/`、`scripts/`、`deploy/`、`apis/middlewares/`、`internal/remote/`、`internal/rpcServer/` 属于示例工程自带目录，不在技能骨架模板里。

各层职责：

1. `models`
- GORM 模型定义，字段映射数据库结构。

2. `dao`
- 数据访问层，封装 CRUD 和查询逻辑。

3. `services`
- 业务编排层，连接 resource 与 dao。

4. `apis/api_1_0`
- 接口资源与路由注册层，承载 HTTP 输入输出。

5. `internal/globals` 与 `internal/settings`
- 全局能力与基础设施初始化（数据库、解析器、引擎配置等）。

### 2. 目标项目启动和测试方法

以下步骤基于 `test/sql-to-gin-example`：

1. 启动前准备
- 进入目录：`cd test/sql-to-gin-example`
- 确认 `configs/config.yaml` 中 `system.SysIP`、`system.SysPort`、数据库连接等配置可用。
- 如首次运行，先拉取依赖：`go mod tidy`

2. 启动服务
- 方式一：`go run main.go`
- 方式二：`go build -o app.exe .` 后执行 `./app.exe`

3. 基础验证
- 端口监听以 `configs/config.yaml` 为准（默认 `0.0.0.0:8000`）。
- 可通过健康检查路由或已生成业务路由做 smoke test。

4. 测试说明
- 当前示例工程中未发现 `_test.go` 单元测试文件。
- 建议最小验证命令：`go test ./...`（用于快速检查编译与基础行为）。

---

## 本项目的使用指南

### 1. 在 AI 开发工具中使用的指南

可先阅读仓库根目录 `docs/` 下通用使用文档，再结合本 README 操作本 Skill：

1. [`docs/claude中使用skill配置.md`](../docs/claude中使用skill配置.md)
2. [`docs/Trea中使用skill配置.md`](../docs/Trea中使用skill配置.md)
3. [`docs/GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md`](../docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md)

说明：

- 仓库根目录 `docs/` 中暂无 Gin 专项使用文档，上述文档可作为 AI 工具接入流程参考。
- Gin Skill 的具体执行步骤与命令，请以本 README 和 `SKILL.md` 为准。

常用命令（仓库根目录执行）：

```bash
python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py
```

该命令会串联执行：context 生成、context 校验、计划预览、模板渲染、路由合并预演、覆盖率统计、快照校验。

---

## 项目的进一步开发与维护

建议遵循以下维护原则：

1. 先规范后实现
- 先修改 `resources/specifications/`，再改 `templates/` 与 `tools/`。

2. 先跑回归再提交
- 每次改动后执行 `run_regression_pipeline.py`，并检查 `resources/demo_output/pipeline_report.json`。

3. 快照变更要可解释
- 先 compare，确认是预期变化后再 update：
  - `python sql-to-gin-restfulapi-scaffold/resources/tools/check_snapshots.py`
  - `python sql-to-gin-restfulapi-scaffold/resources/tools/check_snapshots.py --update`

4. 增量合并保持幂等
- 路由注册合并依赖 marker 机制，避免直接覆盖注册文件。

5. 保持跨 Skill 一致性
- 新能力优先抽象为可复用规则/规范，减少与 FastAPI/Flask/SpringBoot Skill 的行为漂移。

---

## 项目中其他工具的使用说明

`resources/tools/` 主要工具及用途：

1. `generate_context_from_sql.py`
- 输入 SQL DDL，输出统一 context JSON。

2. `validate_template_context.py`
- 校验 context 必填字段和结构合法性。

3. `preview_generation_plan.py`
- 输出实体与文件的生成计划，不落盘代码。

4. `render_demo_single_entity.py`
- 渲染单实体示例，便于调试模板。

5. `render_preview_bundle.py`
- 渲染全量预览产物并生成 manifest。

6. `merge_router_registry.py`
- 基于 marker 对路由注册做增量合并与幂等处理。

7. `check_snapshots.py`
- 对 context 与 manifest 做快照 compare/update。

8. `run_regression_pipeline.py`
- 一键执行完整回归流水线，是日常开发默认入口。

推荐操作顺序：

1. `generate_context_from_sql.py`
2. `validate_template_context.py`
3. `preview_generation_plan.py`
4. `render_preview_bundle.py`
5. `merge_router_registry.py`
6. `check_snapshots.py`
7. `run_regression_pipeline.py`（或直接作为唯一入口）
