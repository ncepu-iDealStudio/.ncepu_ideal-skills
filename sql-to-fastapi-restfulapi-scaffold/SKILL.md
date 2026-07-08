---
name: "sql-to-fastapi-scaffold"
description: "从SQL CREATE TABLE语句生成完整的FastAPI项目脚手架，包含Model、Schema、Resource、Service层。调用时用户提供SQL表结构，或要求搭建API/生成代码。"
---

# SQL-to-FastAPI-Scaffold Skill

## 概述

`sql-to-fastapi-scaffold` 是一个基于资源驱动的技能，用于从SQL表结构语句自动生成完整的 FastAPI 项目脚手架代码。该技能不依赖脚本，而是通过资源文件（模板、配置等）驱动大模型生成代码。

## 什么时候使用此技能

使用此技能的场景：
- 用户提供 SQL CREATE TABLE 语句
- 用户要求从数据库表生成 FastAPI 接口代码，符合RESTful 风格
- 用户要求搭建 API 或创建 API 端点
- 用户提到 "SQL 转 FastAPI"、"表到 API"、"生成脚手架" 等类似表述

## 核心设计原则

### 资源驱动架构

本技能不使用脚本，而是通过以下资源文件驱动代码生成：

```
resources/
├── templates/              # 代码模板
│   ├── project_structure/   # 完整项目结构模板
│   │   ├── config/         # 配置模块
│   │   ├── core/           # 核心模块
│   │   ├── models/         # 模型基类
│   │   ├── schemas/        # 响应模型
│   │   ├── api/            # API路由
│   │   ├── service/        # 服务层
│   │   ├── utils/          # 工具模块
│   │   ├── app/            # 应用模块
│   └── start.py         # 应用入口
│   ├── layers/             # 各层代码模板
│   │   ├── model/
│   │   ├── schema/
│   │   ├── resource/
│   │   └── service/
├── config/                 # 配置文件
│   ├── type_mappings.json  # 类型映射配置
│   └── naming_rules.json   # 命名规则配置
└── specifications/         # 规范文档
    └── coding_standards.md # 代码规范
```

### 生成范围

**首次生成时生成完整的项目骨架**：
- `app/__init__.py` - 应用初始化包，导出create_app
- `app/factory.py` - 应用工厂函数，调用各模块注册
- `app/events.py` - 生命周期管理器（lifespan）
- `app/exceptions.py` - 异常处理器
- `app/middleware.py` - 中间件注册（直接在app层）
- `app/router.py` - 路由注册（调用api模块）
- `config/__init__.py` - 配置包
- `config/settings.py` - 应用配置（CORS、日志等）
- `middleware/__init__.py` - 中间件包（仅占位，具体实现可能在app层）
- `core/__init__.py` - 核心模块
- `core/database.py` - 数据库连接
- `core/dependencies.py` - 依赖注入容器
- `models/__init__.py` - 模型包（导出Base）
- `schemas/__init__.py` - Schema包
- `schemas/response.py` - 统一响应模型（含ErrorResponse）
- `utils/__init__.py` - 工具包
- `utils/loguru.py` - loguru日志配置
- `utils/custom_exceptions.py` - 自定义异常
- `api/__init__.py` - API包（导出api_router）
- `api/v1/__init__.py` - API v1路由注册（导出v1_router）
- `start.py` - 应用启动脚本
- `requirements.txt` - 依赖清单
- `.env.example` - 环境变量模板

**路由结构**：
- `api/__init__.py` → `api_router` (prefix="/api")
- `api/v1/__init__.py` → `v1_router` (prefix="/v1")
- 子路由不额外加前缀，由具体API文件定义

**中间件结构**：
- `app/middleware.py` 直接注册中间件
- `middleware/` 目录保留，用于后续扩展中间件实现

**每个表生成的文件**：
1. SQLAlchemy Model 层 - 数据模型 (`models/{table_name}.py`)
2. Pydantic Schema 层 - 数据验证模型 (`schemas/{table_name}.py`)
3. FastAPI Resource 层 - API 路由端点 (`api/v1/{resource_name}/{resource_name}Resource.py`)
4. Service 层 - 业务逻辑 (`service/{table_name}_service.py`)

**不生成的文件**（根据用户要求）：
- 测试代码
- 部署相关配置（Docker、Nginx等）
- 数据库初始化脚本
- 监控和日志系统

## 使用流程

### 步骤 1: 解析用户输入

当用户提供 SQL 语句时，首先解析：
- 表名（用于文件命名和类名）
- 字段定义（字段名、类型、约束、注释）
- 主键信息
- 外键关系
- 表注释

### 步骤 2: 检查项目是否存在

检查是否为首次生成：
- 如果项目骨架不存在，先生成完整的项目骨架
- 如果已有项目骨架，只生成新增表的4个文件

### 步骤 3: 应用配置规则

使用 `resources/config/` 下的配置：
- 类型映射：SQL 类型 → SQLAlchemy 类型 → Pydantic 类型
- 命名规则：表名 → 类名 → 文件名 → 路由名
- 约束处理规则

### 步骤 4: 生成代码

**重要**：使用 `resources/templates/project_structure/` 下的模板生成项目骨架时，必须完整准确地复制模板文件内容，**不能遗漏任何内容**。

生成项目骨架时应复制以下文件：
- `requirements.txt` - 依赖清单，**必须包含所有依赖项**
- `.env.example` - 环境变量模板，**必须包含所有配置项**
- `start.py` - 应用启动脚本
- `app/` 目录下的所有文件
- `config/` 目录下的所有文件
- `core/` 目录下的所有文件
- `models/` 目录下的所有文件
- `schemas/` 目录下的所有文件
- `utils/` 目录下的所有文件
- `api/` 目录下的所有文件

使用 `resources/templates/layers/` 下的模板生成各层代码。

### 步骤 5: 输出生成结果

以清晰的格式展示生成的文件列表和内容。

### 步骤 6: 生成 README.md

在生成完所有文件后，AI 应读取生成的项目结构，动态生成一份详细的 README.md 文档，包含：
- 项目简介和技术栈
- 完整的项目结构说明
- 所有生成的 API 接口说明（包含请求/响应示例）
- 配置说明
- 快速开始步骤
- Schema 设计说明
- 软删除机制说明

## 代码生成规范

### 命名约定

| 源 | 目标 | 示例 |
|-----|-------|------|
| 表名（snake_case） | 类名（PascalCase） | `student` → `Student` |
| 表名 | 文件名（snake_case） | `sys_class` → `sys_class.py` |
| 表名 | 资源路由名（snake_case） | `student` → `student` |

### 文件结构

**首次生成 - 完整项目骨架**：
```
fastapi_project/
├── app/                    # 应用初始化层
│   ├── __init__.py        # 导出create_app
│   ├── factory.py          # 应用工厂函数
│   ├── events.py           # 生命周期管理器
│   ├── exceptions.py       # 异常处理器
│   ├── middleware.py       # 中间件注册
│   └── router.py           # 路由注册
├── config/
│   ├── __init__.py
│   └── settings.py         # 应用配置
├── middleware/
│   └── __init__.py        # 中间件包（仅占位）
├── core/
│   ├── __init__.py
│   ├── database.py        # 数据库连接
│   └── dependencies.py    # 依赖注入容器
├── models/
│   └── __init__.py        # 导出Base
├── schemas/
│   ├── __init__.py
│   └── response.py        # 统一响应模型（含ErrorResponse）
├── utils/
│   ├── __init__.py
│   ├── loguru.py         # 日志配置
│   └── custom_exceptions.py # 自定义异常
├── service/               # 业务逻辑层（每个表一个文件）
│   └── {table_name}_service.py
├── api/                   # API路由层
│   ├── __init__.py        # 导出api_router（prefix="/api"）
│   └── v1/
│       ├── __init__.py    # 注册v1子路由，导出v1_router（prefix="/v1"）
│       └── {resource_name}/
│           └── {resource_name}Resource.py
├── start.py               # 应用启动脚本（uvicorn启动）
├── requirements.txt       # 依赖清单
└── .env.example          # 环境变量模板
```

**后续生成 - 仅新增文件**：
每次用户添加新表时，只需生成该表的4个文件：
- `models/{table_name}.py`
- `schemas/{table_name}.py`
- `service/{table_name}_service.py`
- `api/v1/{resource_name}/{resource_name}Resource.py`

并更新 `api/v1/__init__.py` 中的 `v1_router.include_router` 注册新路由。

## 各层代码详细说明

### Model 层

**文件位置**：`models/{table_name}.py`

**继承关系**：所有模型继承自 `Base`（SQLAlchemy 的 declarative_base）

**包含内容**：
- 字段定义（含 SQLAlchemy 类型、约束、注释）
- 外键关系（relationship + ForeignKey）
- 敏感字段脱敏属性（如手机号、邮箱）

**模板资源位置**：`resources/templates/layers/model/`

### Schema 层

**文件位置**：`schemas/{table_name}.py`

**包含内容**：
1. `{ClassName}Base` - 基础模型（不含主键）
2. `{ClassName}Create` - 创建模型（不含主键，由数据库自动生成）
3. `{ClassName}Update` - 更新模型（所有字段可选，禁止额外字段）
4. `{ClassName}Response` - 响应模型（含所有字段）

**主键处理规则**：
- 主键不包含在创建模型的输入参数中（假设主键为自增主键，由数据库自动生成）
- 主键在响应模型中返回，供客户端获取
- 更新和删除通过路径参数接收主键

**模板资源位置**：`resources/templates/layers/schema/`

### Resource 层

**文件位置**：`api/v1/{resource_name}/{resource_name}Resource.py`

**包含内容**：
- GET / - 获取列表（分页）
- GET /{pk} - 获取详情
- POST / - 创建记录
- PUT /{pk} - 更新记录
- DELETE /{pk} - 删除记录（根据表中是否有 `is_deleted`/`is_delete`/`deleted` 字段，自动选择软删除或硬删除）

**安全特性**：
- 所有端点包含 `@handle_service_exceptions` 装饰器
- 完整的 OpenAPI 文档
- 可选认证：根据业务需求添加 `get_current_user` 依赖

**模板资源位置**：`resources/templates/layers/resource/`

### Service 层

**文件位置**：`service/{table_name}_service.py`

**类定义**：每个资源对应一个独立的 Service 类，直接注入 `db: Session`

**包含内容**：
- `create()` - 创建（含外键检查）
- `get_list()` - 获取列表（分页）
- `get_detail()` - 获取详情
- `update()` - 更新（含外键检查）
- `delete()` - 删除（根据表中是否有 `is_deleted`/`is_delete`/`deleted` 等字段，自动选择软删除或硬删除）

**创建策略**：
- 创建记录时，主键由数据库自动生成，不在输入参数中接收
- 不对主键进行唯一性检查（由数据库自增保证）

**删除策略**：
- **软删除**：当表中有 `is_deleted`、`is_delete`、`deleted` 等字段时，设置该字段为 `True`
- **硬删除**：当表中没有软删除字段时，直接从数据库删除记录

**模板资源位置**：`resources/templates/layers/service/`

## 类型映射规则

使用 `resources/config/type_mappings.json` 定义的映射关系：

| SQL 类型 | SQLAlchemy 类型 | Pydantic 类型 |
|-----------|-----------------|---------------|
| VARCHAR(n) | String(n) | str |
| INT | Integer | int |
| BIGINT | BigInteger | int |
| TINYINT(1) | Boolean | bool |
| DATETIME | DateTime | datetime |
| DATE | Date | date |
| TEXT | Text | str |
| DECIMAL(p,s) | Numeric(p,s) | Decimal |
| FLOAT | Float | float |
| JSON | JSON | dict/list |

## 约束处理

- `PRIMARY KEY` → `primary_key=True`
- `NOT NULL` → `nullable=False`
- `DEFAULT` → `default` 或 `server_default`
- `COMMENT` → `comment` 参数
- `FOREIGN KEY` → `ForeignKey` + `relationship`
- `UNIQUE` → `unique=True`

## 特殊字段验证

自动为以下字段生成验证器：
- 手机号（含 `phone`）：中国手机号格式验证
- 邮箱（含 `email`）：邮箱格式验证
- 年龄（`age`）：0-150 范围验证
- 性别（含 `gender`/`sex`）：枚举值验证

## 输出格式

生成完成后，向用户展示：

**首次生成时：**
```
✅ 已生成完整的 FastAPI 项目脚手架

📁 生成的项目结构：
├── app/
│   ├── __init__.py        # 导出create_app
│   ├── factory.py          # 应用工厂函数
│   ├── events.py           # 生命周期管理器
│   ├── exceptions.py       # 异常处理器
│   ├── middleware.py       # 中间件注册
│   └── router.py           # 路由注册
├── config/
│   ├── __init__.py
│   └── settings.py         # 应用配置
├── middleware/
│   └── __init__.py        # 中间件包（仅占位）
├── core/
│   ├── __init__.py
│   ├── database.py        # 数据库连接
│   └── dependencies.py    # 依赖注入容器
├── models/
│   └── __init__.py        # 导出Base
├── schemas/
│   ├── __init__.py
│   └── response.py        # 统一响应模型（含ErrorResponse）
├── utils/
│   ├── __init__.py
│   ├── loguru.py         # loguru日志配置
│   └── custom_exceptions.py # 自定义异常
├── service/               # 业务逻辑层（每个表一个文件）
│   └── {table_name}_service.py
├── api/                   # API路由层
│   ├── __init__.py        # 导出api_router（prefix="/api"）
│   └── v1/
│       ├── __init__.py    # 注册v1子路由，导出v1_router
│       └── {resource_name}/
│           └── {resource_name}Resource.py
├── start.py               # 应用启动脚本
├── requirements.txt       # 依赖清单
└── .env.example          # 环境变量模板

🔒 安全特性：
- ✅ 输入验证（Pydantic）
- ✅ 批量赋值保护
- ✅ 敏感数据脱敏
- ⚪ 用户认证依赖（可选）

📝 下一步：
1. pip install -r requirements.txt
2. cp .env.example .env 并配置数据库
3. uvicorn start:app --reload
```

**后续添加新表时：**
```
✅ 已添加 {table_name} 的 CRUD 代码

📁 生成/更新的文件：
1. models/{table_name}.py
2. schemas/{table_name}.py
3. service/{table_name}_service.py
4. api/v1/{resource_name}/{resource_name}Resource.py
5. api/v1/__init__.py (已更新)

📝 下一步：
1. 重启应用即可使用新接口
```

## 错误处理

当 SQL 解析失败时，提供清晰的错误报告，包括：
- 错误类型
- 错误位置
- 错误原因
- 修复建议
- 正确示例

## 资源文件结构说明

所有模板和配置都存储在 `resources/` 目录下，不使用任何脚本代码，完全由大模型根据这些资源生成输出。

## 重要提示

1. **Base继承**：所有模型继承 `Base`，不要重复定义公共字段
2. **软删除/硬删除**：根据表中是否有 `is_deleted`/`is_delete`/`deleted` 等字段，自动选择软删除或硬删除
3. **低耦合**：Service 类不继承任何基类，直接注入 `db: Session`
4. **中文文档**：所有文档字符串、注释、API 文档使用中文
5. **安全性**：所有端点必须包含异常处理，认证根据业务需求添加
