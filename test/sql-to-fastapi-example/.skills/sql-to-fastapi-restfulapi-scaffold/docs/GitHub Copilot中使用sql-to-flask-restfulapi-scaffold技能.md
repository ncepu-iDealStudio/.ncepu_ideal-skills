# GitHub Copilot 中使用 sql-to-flask-restfulapi-scaffold 技能指南

## 1. 目的

本文档说明如何在 VS Code 的 GitHub Copilot Chat 中使用本仓库的 `sql-to-flask-restfulapi-scaffold` 技能资源，完成从 SQL DDL 到 Flask RESTful 项目脚手架代码的生成。

适用目录：

- `sql-to-flask-restfulapi-scaffold/`

## 2. 前置条件

1. 已安装 VS Code。
2. 已安装并登录 GitHub Copilot 插件。
3. 已打开本仓库工作区。
4. 已准备 SQL 文件（例如：`test/study_flask_api.sql`）。

## 3. 核心资源说明

在 Copilot 对话中，建议明确引用以下文件作为生成依据：

- `sql-to-flask-restfulapi-scaffold/SKILL.md`
- `sql-to-flask-restfulapi-scaffold/README.md`
- `sql-to-flask-restfulapi-scaffold/resources/config/type_mappings.json`
- `sql-to-flask-restfulapi-scaffold/resources/config/naming_rules.json`
- `sql-to-flask-restfulapi-scaffold/resources/specifications/coding_standards.md`
- `sql-to-flask-restfulapi-scaffold/resources/specifications/sql_parser_contract.md`
- `sql-to-flask-restfulapi-scaffold/resources/specifications/router_registry_merge_strategy.md`

## 4. 推荐交互方式

### 4.1 首次全量生成

在 Copilot Chat 中输入类似提示：

```text
请严格按照 sql-to-flask-restfulapi-scaffold/SKILL.md 与 resources 下的配置和规范，
读取 test/study_flask_api.sql，
生成 Flask + Flask-RESTful 分层脚手架代码。
要求：
1) 使用 SQL 主键作为路由主键；
2) URL 与路径参数使用 snake_case；
3) 保持字段名与 SQL 原样尽量一致；
4) get/update 默认过滤软删除；
5) 响应字段统一 code/message/data/totalCount/totalPage；
6) 分页参数固定 Page/Size，默认 1/10，Size 最大 100。
```

### 4.2 增量生成

```text
基于现有项目做增量生成：
1) 合并 api_1_0 注册文件；
2) 已存在实体文件跳过；
3) 输出冲突告警与跳过清单。
```

### 4.3 视图生成（只读）

```text
针对 SQL 中的 VIEW，仅生成查询接口与只读映射，不生成写操作。
```

## 5. 建议工作流

1. 先让 Copilot 读取并总结 `SKILL.md` 与关键规范文件。
2. 再执行一次“生成计划预览”。
3. 确认计划后，再执行代码生成。
4. 生成完成后，要求 Copilot 输出：
   - 新增文件清单
   - 更新文件清单
   - 跳过文件清单
   - 解析告警/冲突告警
5. 最后运行项目并验证核心路由。

## 6. 辅助工具脚本（本仓库内）

可先在终端执行以下脚本做前置校验：

```bash
python sql-to-flask-restfulapi-scaffold/resources/tools/validate_template_context.py sql-to-flask-restfulapi-scaffold/resources/config/template_context_example.json
python sql-to-flask-restfulapi-scaffold/resources/tools/preview_generation_plan.py test/study_flask_api.sql
python sql-to-flask-restfulapi-scaffold/resources/tools/render_preview_bundle.py
```

## 7. 常见问题

### 7.1 Copilot 没有按技能规则生成

处理建议：

1. 在提示词中明确要求“严格遵守 SKILL.md + resources/config + resources/specifications”。
2. 要求先输出“生成计划”再生成代码。
3. 在提示里重复关键硬约束（主键规则、命名规则、冲突策略、分页与响应协议）。

### 7.2 增量生成覆盖了已有文件

处理建议：

1. 在提示中明确“仅合并注册文件，实体文件存在则跳过”。
2. 要求输出跳过原因并列出冲突文件。

### 7.3 视图被错误生成为 CRUD

处理建议：

1. 明确说明“VIEW 只生成查询接口”。
2. 引用 `sql_parser_contract.md` 的视图规则。

## 8. 最佳实践

1. 先小规模（单表）验证，再执行复杂多表。
2. 每次生成后立即运行并检查路由。
3. 把生成日志和文件清单提交到 PR 说明，便于审查。
4. 固定依赖版本，减少跨环境偏差。
