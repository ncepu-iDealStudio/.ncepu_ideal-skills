---
name: "sql-to-flask-restfulapi-scaffold"
description: "从 MySQL DDL（CREATE TABLE/CREATE VIEW）生成 Flask + Flask-RESTful 风格的分层接口项目脚手架。"
---

# SQL-to-Flask-RESTfulAPI-Scaffold Skill

## 概述

`sql-to-flask-restfulapi-scaffold` 是一个资源驱动技能，用于从 SQL 建表/视图语句生成 Flask RESTful 风格的接口项目脚手架。


本技能强调：

- 可启动
- 路由可访问
- CRUD 可跑通
- 支持首次全量生成与后续增量生成

## 适用场景

当用户出现以下需求时应触发本技能：

- 提供 SQL 脚本并要求生成 Flask RESTful API 项目
- 根据数据库表结构自动生成分层代码

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

- `manage.py`
- `app/`
- `api_1_0/`
- `models/`
- `controller/`
- `service/`
- `config/`
- `utils/`
- `requirements.txt`

### 表实体生成（每张表）

- `models/{module_name}.py`
- `controller/{ClassName}Controller.py`
- `service/{ClassName}Service.py`
- `api_1_0/{resource_slug}Resource/__init__.py`
- `api_1_0/{resource_slug}Resource/{resource_slug}Resource.py`
- `api_1_0/{resource_slug}Resource/{resource_slug}OtherResource.py`（占位也生成）
- `api_1_0/{resource_slug}Resource/urls.py`

### 视图生成（每个 view）

- 只读 model
- 查询 controller/service
- 查询 resource（仅集合查询路由）
- 不生成新增/更新/删除

### 增量生成

- 合并路由注册文件
- 实体文件已存在时跳过
- 输出冲突告警

## 命名与主键规则

- `module_name` 统一下划线风格（snake_case）
- URL 风格统一下划线（如 `/student_selected_course`）
- 路径参数名也统一下划线
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
- `data`

## 分页约定

固定分页参数与默认值：

- `Page` 默认 `1`
- `Size` 默认 `10`
- `Size` 最大 `100`

当 `Size` 超过上限时，按上限处理并返回提示信息。

## 文件冲突策略

- 默认合并注册文件
- 跳过已存在实体文件
- 在输出中追加告警

## 依赖策略

`requirements.txt` 使用精确版本锁定，优先保证一键调试稳定性。

## 输出结果要求

生成完成后必须输出：

- 新增文件列表
- 更新文件列表
- 跳过文件列表
- 语法跳过告警
- 冲突告警
- 成功/失败统计

## V1 不生成清单

- 自动化测试代码
- Docker/Nginx/Gunicorn 等部署文件
- CI/CD 配置
- 自动白名单写入逻辑
- 复杂联表分析接口生成

## 验收标准

至少覆盖两组样例：

- 单表
- 复杂多表

判定标准：

- 项目可启动
- 路由可访问
- CRUD 可跑通

