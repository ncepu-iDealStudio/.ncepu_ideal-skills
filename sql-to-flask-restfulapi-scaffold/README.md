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
	│   └── validate_template_context.py
	└── demo_output/
		└── student_demo/
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

