# SQL-to-Flask-RESTfulAPI-Scaffold

## 项目简介

`sql-to-flask-restfulapi-scaffold` 是一个 Skill 项目，目标是基于 MySQL DDL 脚本自动生成 Flask + Flask-RESTful 风格的企业级接口项目脚手架。

目标结构参考：`test/api.study-flask.com`。

输入样例 SQL：`test/study_flask_api.sql`。

## V1 目标

V1 聚焦三件事：

- 生成可运行的 Flask RESTful 分层项目骨架
- 基于 SQL 自动生成表/视图对应接口代码
- 支持首次全量生成与后续增量生成

## 技术与风格对齐

- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- MySQL（PyMySQL）
- 分层结构：`models / controller / service / api_1_0`

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

- `manage.py`
- `app/`
- `api_1_0/`
- `models/`
- `controller/`
- `service/`
- `config/`
- `utils/`
- `requirements.txt`

### 2. 表实体生成（每张表）

- `models/{module_name}.py`
- `controller/{ClassName}Controller.py`
- `service/{ClassName}Service.py`
- `api_1_0/{resource_slug}Resource/__init__.py`
- `api_1_0/{resource_slug}Resource/{resource_slug}Resource.py`
- `api_1_0/{resource_slug}Resource/{resource_slug}OtherResource.py`
- `api_1_0/{resource_slug}Resource/urls.py`

### 3. 视图生成（每个 view）

- 只读 model
- 查询 controller/service
- 查询 resource（仅集合查询路由）

### 4. 增量生成

- 合并注册文件
- 已存在实体文件跳过
- 输出冲突告警

## 不生成清单（V1）

- 自动化测试代码
- 部署文件（Docker/Nginx/Gunicorn）
- CI/CD 配置
- 自动写入权限白名单
- 复杂联表分析接口

## 命名与主键规则

- `module_name` 统一为下划线风格（snake_case）
- URL 路径统一下划线风格
- 路径参数名统一下划线风格
- 接口主键统一使用 SQL 表定义的主键

说明：

- 若主键是 `auto_id/autoID`，则按该主键生成
- 若想使用业务主键，请在建表时定义为主键

## 字段与软删除规则

- 字段名尽量保持 SQL 原样，不自动改名
- 软删除字段识别：`is_delete`、`is_deleted`、`isDelete`、`isDeleted`
- `get/update` 默认过滤已软删除记录
- Model 字段行由渲染器根据 `entities[].fields` 自动拼接（不依赖手写 `fields_block`）

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
- `data`

## 分页约定

- `Page` 默认 `1`
- `Size` 默认 `10`
- `Size` 最大 `100`

超出上限时按 `100` 处理并提示。

## 依赖策略

为降低兼容性问题，V1 使用精确版本锁定的 `requirements.txt`。

## 目录建议（Skill 项目）

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
	├── static/
	│   └── utils/
	├── templates/
	│   ├── project_structure/
	│   └── layers/
	├── tools/
	│   ├── preview_generation_plan.py
	│   ├── render_demo_single_entity.py
	│   ├── render_preview_bundle.py
	│   ├── render_utils.py
	│   └── validate_template_context.py
	└── demo_output/
		└── student_demo/
```

## resources 资源说明（维护重点）

本技能的可维护性核心在 `resources/`。可以把它理解为“技能的知识库 + 模板库 + 辅助工具”。

### 1) config（规则配置层）

目录：`resources/config/`

- `generation_profiles.json`
	- 定义不同生成档位（minimal/standard/secure）启用哪些能力。
	- 维护建议：新增可选能力时，先改这里，再改模板，不要反过来。
- `naming_rules.json`
	- 定义命名策略：module、URL、路径参数、资源目录命名。
	- 维护建议：若命名风格要调整，优先改此文件并补回归验证。
- `type_mappings.json`
	- 定义 SQL 类型到 Flask-SQLAlchemy 类型映射、软删除字段候选、分页默认值。
	- 维护建议：新增数据库类型支持时只扩展映射，不直接改模板硬编码。
- `template_context_example.json`
	- 模板渲染上下文样例（含 table 与 view）。
	- 维护建议：每次修改渲染逻辑后同步更新这个样例，作为最小回归输入。

### 2) specifications（规范与契约层）

目录：`resources/specifications/`

- `coding_standards.md`
	- 生成代码风格规范（命名、响应、分页、软删除、冲突策略）。
- `sql_parser_contract.md`
	- SQL 解析边界契约（支持语法、跳过策略、view 规则）。
- `template_context_schema.md`
	- 模板上下文字段说明。
- `router_registry_merge_strategy.md`
	- 增量场景下 `api_1_0/__init__.py` 的合并策略与 marker 规则。
- `field_rendering_rules.md`
	- 字段行渲染规则（primary_key/nullable/default/info 的顺序与含义）。
- `generation_preview_study_flask_api.md`
	- 基于样例 SQL 的预估生成清单，便于评审与回归对照。

维护建议：

- 先改 specification 再改模板，避免“实现和文档脱节”。
- 如果出现生成歧义，优先补契约文档而不是临时改脚本。

### 3) templates（代码模板层）

目录：`resources/templates/`

- `project_structure/`
	- 首次生成时的工程骨架模板（app/api_1_0/models/config 等）。
	- 适合改“项目级结构”。
- `layers/`
	- 按实体（table/view）渲染的分层代码模板。
	- `model/`：模型模板（table 与 view）
	- `controller/`：控制器模板（CRUD 或 query）
	- `service/`：服务模板
	- `resource/`：路由资源模板（table urls 与 view urls 分离）

维护建议：

- 改骨架去 `project_structure`，改实体逻辑去 `layers`。
- view 与 table 的模板分离维护，避免在单模板里堆大量条件分支。

### 4) static（静态资源层）

目录：`resources/static/`

- `utils/core/`：必备基础工具（响应码、日志、通用函数）
- `utils/business/`：通用业务辅助工具（ID、校验、重复检查）
- `utils/security/`：安全相关占位或可选模块（按 profile 启用）

维护建议：

- core 保持最小且稳定，尽量不引入业务耦合。
- security 默认可选，避免对非安全场景造成强依赖。

### 5) tools（开发辅助层）

目录：`resources/tools/`

- `validate_template_context.py`
	- 校验上下文 JSON 结构是否满足渲染要求。
- `preview_generation_plan.py`
	- 从 SQL 预览 table/view 解析结果与文件生成计划。
- `render_utils.py`
	- 公共渲染函数（字段自动拼接、模板替换）。
- `render_demo_single_entity.py`
	- 单实体渲染演示。
- `render_preview_bundle.py`
	- table + view 组合渲染，并输出 manifest。

维护建议：

- 所有渲染脚本共享逻辑尽量收敛到 `render_utils.py`。
- 新增脚本时要保证输入/输出可复用，避免一次性脚本。

### 6) demo_output（演示产物层）

目录：`resources/demo_output/`

- 存放演示渲染结果与 manifest。
- 用于评审模板效果，不是最终业务代码仓库。

维护建议：

- 演示目录可定期清理并重建。
- 提交前确保示例结果与当前模板一致。

## 维护与优化建议流程

建议按下面顺序做变更，能显著降低回归风险：

1. 先修改契约：`specifications/*.md`
2. 再修改规则：`config/*.json`
3. 再修改模板：`templates/**`
4. 用 `tools/` 执行校验与渲染预览
5. 对照 `demo_output/**/manifest.json` 检查影响范围

推荐最小验证命令：

```bash
python resources/tools/validate_template_context.py resources/config/template_context_example.json
python resources/tools/preview_generation_plan.py ../test/study_flask_api.sql
python resources/tools/render_preview_bundle.py
```

## 工具脚本（当前可用）

### 1) 校验模板上下文

```bash
python resources/tools/validate_template_context.py resources/config/template_context_example.json
```

### 2) 预览 SQL 的生成计划

```bash
python resources/tools/preview_generation_plan.py ../test/study_flask_api.sql
```

### 3) 单实体模板渲染演示

```bash
python resources/tools/render_demo_single_entity.py
```

演示输出目录：`resources/demo_output/student_demo/`

### 4) table + view 组合渲染预览（含 manifest）

```bash
python resources/tools/render_preview_bundle.py
```

输出目录：`resources/demo_output/bundle_preview/`

manifest 示例：`resources/demo_output/bundle_preview/manifest.json`

## 使用文档

- Trae 使用说明：`../docs/Trea中使用skill配置.md`
- Claude 使用说明：`../docs/claude中使用skill配置.md`
- GitHub Copilot 使用说明：`../docs/GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md`

## 验收标准

至少覆盖：

- 单表样例
- 复杂多表样例

通过标准：

- 生成项目可启动
- 路由可访问
- CRUD 可跑通

## 下一步建议

建议按以下顺序推进实现：

1. 先完成 `resources/config` 与 `resources/specifications`
2. 再完成 `project_structure` 基础模板
3. 最后实现 `layers` 分层模板与增量注册逻辑

