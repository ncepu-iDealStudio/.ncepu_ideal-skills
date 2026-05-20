# sql-to-flask-restfulapi-scaffold

## 项目简介

### 1. 本项目是干嘛的

`sql-to-flask-restfulapi-scaffold` 是一个面向 AI 开发场景的 Skill 项目，用于把 MySQL DDL（`CREATE TABLE` / `CREATE VIEW`）转换为 Flask + Flask-RESTful 分层接口脚手架。

本项目的核心价值：

1. 将规则（命名、类型、分页、软删除）和模板解耦，降低后续维护成本。
2. 通过上下文校验、生成计划预览、渲染预览提高生成可控性。
3. 支持增量生成与注册合并，减少覆盖人工代码的风险。

参考目标工程：`test/sql-to-flask-example`。  
基线 SQL：`test/study_flask_api.sql`。

### 2. 技术栈和依赖版本

本项目包含两类依赖：

1. 目标项目模板依赖（`resources/templates/project_structure/requirements.txt`）
- Flask: `3.0.1`
- Flask-RESTful: `0.3.10`
- Flask-SQLAlchemy: `3.1.1`
- Flask-Session: `0.6.0`
- SQLAlchemy: `2.0.25`
- PyMySQL: `1.1.0`
- loguru: `0.7.2`

2. Skill 工具链依赖（`resources/tools/*.py`）
- Python: 建议 `3.10+`
- 使用标准库为主（`json`、`pathlib`、`sys` 等），无额外第三方依赖要求。

### 3. 本项目的代码文件夹结构详细说明

```text
sql-to-flask-restfulapi-scaffold/
├── README.md
├── SKILL.md
└── resources/
    ├── config/
    │   ├── generation_profiles.json
    │   ├── naming_rules.json
    │   ├── template_context_example.json
    │   └── type_mappings.json
    ├── specifications/
    │   ├── coding_standards.md
    │   ├── field_rendering_rules.md
    │   ├── generation_preview_study_flask_api.md
    │   ├── router_registry_merge_strategy.md
    │   ├── sql_parser_contract.md
    │   └── template_context_schema.md
    ├── templates/
    │   ├── project_structure/
    │   │   ├── manage.py
    │   │   ├── requirements.txt
    │   │   ├── app/
    │   │   ├── api_1_0/
    │   │   ├── models/
    │   │   ├── controller/
    │   │   ├── service/
    │   │   ├── config/
    │   │   └── utils/
    │   └── layers/
    │       ├── model/
    │       ├── controller/
    │       ├── service/
    │       └── resource/
    ├── tools/
    │   ├── validate_template_context.py
    │   ├── preview_generation_plan.py
    │   ├── render_demo_single_entity.py
    │   ├── render_preview_bundle.py
    │   └── render_utils.py
    ├── demo_output/
    │   ├── student_demo/
    │   └── bundle_preview/
    └── static/
        └── utils/
```

目录职责：

1. `resources/config/`
- 管理可配置策略（命名规则、类型映射、生成档位、上下文样例）。

2. `resources/specifications/`
- 管理契约与规范（解析边界、上下文 schema、合并策略、字段渲染规则）。

3. `resources/templates/`
- 管理代码模板：
- `project_structure/` 负责项目骨架。
- `layers/` 负责实体分层代码渲染。

4. `resources/tools/`
- 管理开发辅助脚本（校验、预览、渲染）。

5. `resources/demo_output/`
- 存放渲染演示产物和 manifest，作为评审与对照依据。

---

## 生成的目标项目说明

### 1. 生成的目标项目结构

目标项目是 Flask 分层接口工程，典型结构如下（参考 `test/sql-to-flask-example`）：

```text
target-project/
├── manage.py
├── app/
├── api_1_0/
├── models/
├── controller/
├── service/
├── config/
├── utils/
├── test/
└── requirements.txt
```

分层职责：

1. `models/`
- SQLAlchemy 模型定义。

2. `controller/`
- 业务控制层，封装接口调用前后的业务逻辑。

3. `service/`
- 数据访问与通用查询封装。

4. `api_1_0/`
- RESTful 资源与路由注册。

5. `app/`
- 应用工厂与运行模式配置。

6. `test/`
- 单元测试与性能测试样例目录。

### 2. 目标项目启动和测试方法

以下步骤基于 `test/sql-to-flask-example`：

1. 安装依赖
- `cd test/sql-to-flask-example`
- `python -m pip install -r requirements.txt`

2. 启动项目
- `python manage.py`

3. 本地冒烟验证
- 默认启动后访问配置端口对应 API 路由。
- 如需要，先在 `manage.py` 的 permission 列表和配置文件中确认鉴权放行策略。

4. 单元测试
- 示例工程包含 `test/unitest/`。
- 建议命令：`python -m unittest discover -s test/unitest -p "test_*.py"`

5. 性能测试（可选）
- 示例目录包含 `test/performance_test/`，可按其中脚本进行压测准备。

---

## 本项目的使用指南

### 1. 在 AI 开发工具中使用的指南或文档

优先阅读 `docs/` 下文档：

1. `docs/GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md`
2. `docs/claude中使用skill配置.md`
3. `docs/Trea中使用skill配置.md`

说明：

- 上述文档覆盖 AI 工具中 Skill 接入与调用方式。
- 本 README 重点补充 Flask Skill 的工程结构与维护流程。

### 2. 本地最小可用命令

在仓库根目录执行：

```bash
python sql-to-flask-restfulapi-scaffold/resources/tools/validate_template_context.py sql-to-flask-restfulapi-scaffold/resources/config/template_context_example.json
python sql-to-flask-restfulapi-scaffold/resources/tools/preview_generation_plan.py test/study_flask_api.sql
python sql-to-flask-restfulapi-scaffold/resources/tools/render_preview_bundle.py
```

执行顺序建议：先校验 context，再预览计划，最后渲染预览产物。

---

## 项目的进一步开发与维护

建议遵循以下流程，避免“文档、规则、模板、产物”失配：

1. 先改规范再改实现
- 先更新 `resources/specifications/*.md`，再调整 `config` 和 `templates`。

2. 保持规则集中化
- 命名与类型策略优先落到 `resources/config/*.json`，避免散落到模板中硬编码。

3. 模板分层维护
- 项目骨架问题优先改 `templates/project_structure/`。
- 实体渲染问题优先改 `templates/layers/`。

4. 每次变更都做最小回归
- 至少执行：context 校验 + 计划预览 + bundle 渲染。
- 核对 `resources/demo_output/` 产物是否符合预期。

5. 提交前补齐说明
- 在提交说明中写清楚：改动文件、影响范围、验证命令与结果。

---

## 项目中其他工具的使用说明

`resources/tools/` 工具说明：

1. `validate_template_context.py`
- 输入：context JSON。
- 输出：结构校验结果（通过/失败与错误信息）。
- 作用：防止模板渲染时出现缺字段问题。

2. `preview_generation_plan.py`
- 输入：SQL 文件。
- 输出：解析结果和预计生成文件清单。
- 作用：在真正渲染前预估影响面。

3. `render_demo_single_entity.py`
- 输入：示例上下文（默认内置或配置）。
- 输出：单实体渲染样例。
- 作用：调试单个模板最快路径。

4. `render_preview_bundle.py`
- 输入：完整上下文。
- 输出：`resources/demo_output/bundle_preview/` 及 manifest。
- 作用：评估 table + view 组合渲染结果。

5. `render_utils.py`
- 作用：脚本公共渲染函数集合（字段拼接、模板替换等复用逻辑）。

建议工具链顺序：

1. `validate_template_context.py`
2. `preview_generation_plan.py`
3. `render_demo_single_entity.py`
4. `render_preview_bundle.py`
