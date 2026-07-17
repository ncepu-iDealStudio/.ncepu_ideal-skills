---
name: sql-to-fastapi-restfulapi-scaffold
description: "从SQL CREATE TABLE生成FastAPI脚手架：Model/Schema/Repository/Service/Resource/测试。API统一只调Service。Repository仅单条CRUD且按增删改查顺序：create/delete/update/get；列表与状态等业务写在Service。按表生成unit占位与integration CRUD测试。表含status时额外生成PATCH /{pk}/status。目标项目默认用uv（pyproject.toml）管理依赖与启动。"
---

# SQL-to-FastAPI-Scaffold Skill

## 概述

`sql-to-fastapi-scaffold` 是一个基于资源驱动的技能，用于从SQL表结构语句自动生成完整的 FastAPI 项目脚手架代码。该技能不依赖脚本，而是通过资源文件（模板、配置等）驱动大模型生成代码。

**分层架构**：

```text
API(Resource) → Service(单条委托 + 列表等业务, 人手维护) → Repository(仅单条 create/delete/update/get 增删改查, 可覆盖) → Model
（请求校验由 Schema 在进入 API 前完成）
```

**强制约定**：
- Resource/API **只**依赖 Service；**禁止** Resource 直接 Depends Repository。
- Repository **仅**单表单条 CRUD，方法名固定为 `create` / `delete` / `update` / `get`（源码按增删改查顺序）。
- 列表分页、过滤、状态变更等一律视为业务逻辑，放在 Service。

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
│   │   ├── start.py        # 应用入口
│   │   ├── pyproject.toml  # uv / PEP 621 主依赖清单
│   │   ├── .python-version # uv Python 版本
│   │   └── requirements.txt # pip 兼容清单
│   ├── layers/             # 各层代码模板
│   │   ├── model/
│   │   ├── schema/
│   │   ├── repository/     # 仅单条 create/delete/update/get（增删改查，可覆盖）
│   │   ├── service/        # 单条委托 + 列表等业务（已存在则跳过）
│   │   ├── resource/       # 统一 Depends Service
│   │   └── test/           # 单元占位 + 集成 CRUD/业务占位
│   │       ├── unit/
│   │       └── integration/
├── config/                 # 配置文件
│   ├── type_mappings.json      # 类型映射配置
│   ├── naming_rules.json       # 命名规则配置
│   ├── status_flag_fields.json # 状态/标识位敏感字段识别
│   └── package_manager.json    # 包管理与启动（默认 uv）
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
- `start.py` - 应用启动脚本（含 `main()`，支持 `uv run python start.py`）
- `pyproject.toml` - **uv / PEP 621 依赖与工具配置（主清单，必须生成）**
- `.python-version` - uv 使用的 Python 版本钉选
- `requirements.txt` - 与 pyproject 运行时依赖同步的兼容清单（次选 pip）
- `.env.example` - 环境变量模板

**路由结构**：
- `api/__init__.py` → `api_router` (prefix="/api")
- `api/v1/__init__.py` → `v1_router` (prefix="/v1")
- 子路由不额外加前缀，由具体API文件定义

**中间件结构**：
- `app/middleware.py` 直接注册中间件
- `middleware/` 目录保留，用于后续扩展中间件实现

**每个表生成的文件**：
1. SQLAlchemy Model - `models/{table_name}.py`
2. Pydantic Schema - `schemas/{table_name}.py`
3. Repository（仅单条 create/delete/update/get，增删改查顺序，可覆盖）- `repository/{table_name}_repository.py`
4. Service（单条委托 + 列表等业务，**已存在则跳过**）- `service/{table_name}_service.py`
5. FastAPI Resource（统一只调 Service）- `api/v1/{resource_name}/{resource_name}Resource.py`
6. 单元测试占位（Service，**已存在则跳过**）- `tests/unit/test_{table_name}_service.py`
7. 集成测试（CRUD 可运行 + 业务占位，**已存在则跳过**）- `tests/integration/api/v1/test_{table_name}.py`

> ⚠️ **【强制规则】资源文件夹与路由前缀必须全部使用单数（singular）**
> `resource_name` 由**表名原样**作为单数使用，**严禁**对资源名做任何复数化处理。
> - 表 `company_file` → 文件夹 `api/v1/company_file/`（❌ 错误：`api/v1/company_files/`）
> - 表 `company_file` → 路由前缀 `/company-file`（❌ 错误：`/company-files`）
> - 表 `student` → 文件夹 `api/v1/student/`、路由前缀 `/student`
> - 表 `sys_class` → 文件夹 `api/v1/sys_class/`、路由前缀 `/sys-class`
>
> 只有以下位置使用表名/单数形式，其余（文件名、类名、前缀）均不得加 `s` 或变复数。
> 复数（`company_files`、`students`）只会出现在 `tags=["xxx管理"]` 的中文展示文案里，绝不进入任何路径或文件名。

**不生成的文件**（根据用户要求）：
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
- 如果项目骨架不存在，先生成完整的项目骨架（含 `repository/` 包）
- 如果已有项目骨架，只生成/更新该表相关文件（遵守覆盖策略）

### 步骤 2.1: 覆盖策略（强制）

| 文件 | 策略 |
|------|------|
| `repository/{table}_repository.py` | **始终覆盖**（AUTO-GENERATED） |
| `service/{table}_service.py` | **仅当文件不存在时生成**；已存在则跳过并提示 |
| `models/{table}.py` / `schemas/{table}.py` | 默认可覆盖；若用户声明已手改则询问后跳过 |
| `api/v1/...Resource.py` | 默认可覆盖基础 CRUD；若含手写业务路由，优先跳过或合并提示 |
| `tests/unit/test_{table}_service.py` | **仅当文件不存在时生成**（Service 单元测试占位） |
| `tests/integration/api/v1/test_{table}.py` | **仅当文件不存在时生成**（CRUD 集成测试 + 业务占位） |

### 步骤 3: 应用配置规则

使用 `resources/config/` 下的配置：
- 类型映射：SQL 类型 → SQLAlchemy 类型 → Pydantic 类型
- 命名规则：表名 → 类名 → 文件名 → 路由名
- 约束处理规则
- **状态/标识位识别**：按 `status_flag_fields.json` 标记敏感字段（见下文）
- **包管理与启动**：按 `package_manager.json`，目标项目默认用 **uv**（`pyproject.toml` + `uv sync` / `uv run`）

### 步骤 3.1: 状态/标识位字段（强制）

解析字段时，按 `resources/config/status_flag_fields.json` 识别状态/标识位：

| 命中规则 | 示例 |
|----------|------|
| 精确名 | `status`、`state`、`enabled`、`locked`、`is_active`、`is_enabled`、`is_locked`、`is_disabled` |
| 后缀 | `*_status`、`*_state`、`*_flag` |
| 前缀 | `status_*`、`state_*` |
| **排除** | `is_delete` / `is_deleted` / `deleted`（软删走 DELETE）、`password`、`user_type` / `usertype`、`type` |

匹配时同时检查 **SQL 原字段名** 与 **规范化后的 Python 属性名**（如 `userType` → `user_type`）。

**一旦命中 ≥1 个字段，必须额外生成：**

1. Schema：`{ClassName}StatusUpdate`（仅含状态字段）；并从通用 `{ClassName}Update` 中**排除**这些字段
2. Service：`update_status(...)`（业务入口；内部调用 `repo.update` 传入字段字典；**Repository 不暴露 `update_status`**）
3. Resource：`PATCH /{pk}/status` → `service.update_status`

示例（`sso_user.status`）：`PATCH /sso-user/{user_id}/status`，Body `{"status": 0}`。

> 软删除字段**不是**状态接口；账号类型等业务枚举字段按 exclude 名单处理。

### 步骤 4: 生成代码

**重要**：使用 `resources/templates/project_structure/` 下的模板生成项目骨架时，必须完整准确地复制模板文件内容，**不能遗漏任何内容**。

生成项目骨架时应复制以下文件：
- `pyproject.toml` - **uv 主依赖清单**，替换 `{{project_name}}` / `{{project_description}}`；规则见 `resources/config/package_manager.json`
- `.python-version` - Python 版本钉选（供 uv 使用）
- `requirements.txt` - 与 `pyproject.toml` 运行时依赖保持一致的兼容清单
- `.env.example` - 环境变量模板，**必须包含所有配置项**
- `start.py` - 应用启动脚本（含 `main()`）
- `app/` 目录下的所有文件
- `config/` 目录下的所有文件
- `core/` 目录下的所有文件
- `models/` 目录下的所有文件
- `schemas/` 目录下的所有文件
- `utils/` 目录下的所有文件
- `repository/` 目录（含 `__init__.py`）
- `service/` 目录
- `api/` 目录下的所有文件

使用 `resources/templates/layers/` 下的模板生成各层代码。

**包管理与启动（强制优先 uv）**：
- 目标项目以 **uv** 管理依赖与虚拟环境（见 `package_manager.json`）
- 生成后的 README「快速开始」与对话收尾「下一步」**必须**写 uv 命令；可附带 pip 兼容说明
- 推荐命令：`uv sync` → `uv run uvicorn start:app --reload`（或 `uv run python start.py`）
- 增删依赖优先指导用户使用 `uv add` / `uv add --dev`，并同步更新 `pyproject.toml`（及兼容用的 `requirements.txt`）

### 步骤 5: 输出生成结果

以清晰的格式展示生成的文件列表和内容。

### 步骤 6: 生成 README.md

在生成完所有文件后，AI 应读取生成的项目结构，动态生成一份详细的 README.md 文档，包含：
- 项目简介和技术栈（注明使用 **uv** 管理依赖）
- 完整的项目结构说明（含 `pyproject.toml`、`.python-version`）
- 所有生成的 API 接口说明（包含请求/响应示例）
- 配置说明
- 快速开始步骤（**优先** `uv sync` / `uv run ...`；可选附 pip 兼容步骤）
- Schema 设计说明
- 软删除机制说明

## 代码生成规范

### 命名约定

| 源 | 目标 | 示例 |
| ----- | ------- | ------ |
| 表名（snake_case） | 类名（PascalCase） | `student` → `Student` |
| 表名 | 文件名（snake_case） | `sys_class` → `sys_class.py` |
| 表名（**原样，强制单数**） | 资源名（**单数**，用于文件夹与路由前缀，**禁止任何形式的复数化**） | `company_file` → `company_file`；文件夹 `api/v1/company_file/`（❌`company_files`）、路由前缀 `/company-file`（❌`/company-files`） |
| 表名（**原样，强制单数**） | 资源名（**单数**） | `student` → `student`；文件夹 `api/v1/student/`、路由前缀 `/student` |

> 🔴 **再次强调**：`resource_name` = 表名单数形式，**绝不要**对资源名做复数转换。
> 即使表名是 `company_file`，文件夹也必须是 `company_file`（不是 `company_files`），路由前缀必须是 `/company-file`（不是 `/company-files`）。
> 复数只用于中文 tag 文案（如 `tags=["企业管理"]`），绝不进入路径/文件名/前缀。

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
├── repository/            # 数据访问层（仅 create/delete/update/get，增删改查，可覆盖）
│   └── {table_name}_repository.py
├── service/               # 业务服务（单条委托 + 列表等业务；已存在则跳过）
│   └── {table_name}_service.py
├── api/                   # API路由层
│   ├── __init__.py        # 导出api_router（prefix="/api"）
│   └── v1/
│       ├── __init__.py    # 注册v1子路由，导出v1_router（prefix="/v1"）
│       └── {resource_name}/
│           └── {resource_name}Resource.py
├── start.py               # 应用启动脚本（uvicorn；含 main()）
├── pyproject.toml         # uv / PEP 621 主依赖清单
├── .python-version        # uv Python 版本钉选
├── requirements.txt       # 兼容 pip 的依赖导出（与 pyproject 同步）
└── .env.example          # 环境变量模板
```

**后续生成 - 按表增量（遵守覆盖策略）**：
- `models/{table_name}.py`
- `schemas/{table_name}.py`
- `repository/{table_name}_repository.py`（覆盖）
- `service/{table_name}_service.py`（**仅不存在时创建**）
- `api/v1/{resource_name}/{resource_name}Resource.py`
- `tests/unit/test_{table_name}_service.py`（**仅不存在时创建**，Service 占位）
- `tests/integration/api/v1/test_{table_name}.py`（**仅不存在时创建**，CRUD + 业务占位）
- 更新 `api/v1/__init__.py`、`core/dependencies.py` 注册

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
3. `{ClassName}Update` - 更新模型（所有字段可选，禁止额外字段；**不含**状态/标识位字段）
4. `{ClassName}StatusUpdate` - **有状态字段时生成**；仅含状态/标识位，字段必填
5. `{ClassName}Response` - 响应模型（含所有字段）

**主键处理规则**：
- 主键不包含在创建模型的输入参数中（假设主键为自增主键，由数据库自动生成）
- 主键在响应模型中返回，供客户端获取
- 更新和删除通过路径参数接收主键

**模板资源位置**：`resources/templates/layers/schema/`

### Repository 层

**文件位置**：`repository/{table_name}_repository.py`

**职责**：仅「单表、单条记录」的基础 CRUD（`AsyncSession` + `select()`）

**方法名固定（仅这 4 个；源码定义顺序按增删改查）**：
- `create()` — 增：插入一条
- `delete()` — 删：删除一条（有软删字段则软删，否则硬删）
- `update()` — 改：更新一条（可接受 Update Schema 或字段字典）
- `get()` — 查：按主键获取一条

**禁止出现在 Repository**：
- `get_list` / 分页 / 过滤（属业务，放 Service）
- `update_status` / `exists_by_pk` / `update_fields` 等扩展方法名

**模板**：`resources/templates/layers/repository/`

### Resource 层

**文件位置**：`api/v1/{resource_name}/{resource_name}Resource.py`

**包含内容**：
- GET / - 列表；GET /{pk} - 详情；POST / - 创建；PUT /{pk} - 更新；DELETE /{pk} - 删除
- 有状态字段时额外：`PATCH /{pk}/status` → `service.update_status`
- **统一** `Depends(get_*_service)`，**禁止**直接依赖 Repository
- `@handle_service_exceptions` + OpenAPI 文档

**模板**：`resources/templates/layers/resource/`

### Service 层（CRUD 委托 + 业务）

**文件位置**：`service/{table_name}_service.py`

**职责**：
- 单条：`create` / `get_detail` / `update` / `delete` 委托 Repository 的 `create` / `get` / `update` / `delete`（Repository 源码顺序为增删改查）
- **业务逻辑**（默认生成）：`get_list`（分页/过滤/软删排除）写在本层，直接使用 `self.db` + Model 查询
- 有状态字段时额外：`update_status`（内部 `repo.update(pk, fields_dict)`）
- 跨表、流程、复杂校验继续写在本文件
- Resource 只调用本层

**覆盖策略**：文件已存在 → **跳过生成**

**模板**：`resources/templates/layers/service/`

### 测试代码生成（强制，按表增量）

**前提**：若项目尚无 `tests/` 骨架，先确保存在（可参考目标项目的 `tests/conftest.py`、`tests/pytest.ini`）：

```text
tests/
├── conftest.py                 # session(sqlite) + app(真实 MySQL) fixtures
├── pytest.ini
├── unit/
│   └── test_{table_name}_service.py
└── integration/
    └── api/v1/
        └── test_{table_name}.py
```

#### 1) 单元测试占位 — Service

| 项 | 说明 |
|----|------|
| 路径 | `tests/unit/test_{table_name}_service.py` |
| 模板 | `resources/templates/layers/test/unit/test_service_template.py` |
| 覆盖 | **仅不存在时生成** |
| 内容 | 面向 `{{ClassName}}Service` 的占位用例（`create` / `get_detail` / `update` / `delete` / `get_list`；有状态字段时含 `update_status`），默认 `@pytest.mark.skip` |
| Fixture | 使用项目 `session`（sqlite 内存库） |

#### 2) 集成测试 — API（CRUD 可运行 + 业务占位）

| 项 | 说明 |
|----|------|
| 路径 | `tests/integration/api/v1/test_{table_name}.py` |
| 模板 | `resources/templates/layers/test/integration/test_api_template.py` |
| 覆盖 | **仅不存在时生成** |
| CRUD | 生成**可执行**的 `test_{table}_crud_flow`：POST→列表→详情→PUT→（可选 PATCH status）→DELETE，并查真实 MySQL 校验 |
| 业务占位 | 同文件内 `test_{table}_business_api_placeholder`，默认 skip，供后续商业逻辑接口补充 |
| Fixture | 使用项目 `app`（直连真实 MySQL + Bearer test-token） |

**生成集成测试时必须填充的变量**：

| 变量 | 含义 | 示例（admin） |
|------|------|----------------|
| `resource_path` | 路由前缀（表名 `_`→`-`） | `admin` / `sso-user` |
| `create_payload_fields` | Create 请求字段 + `example_expr` | `admin_id: _new_admin_id()` |
| `update_payload_fields` | Update 抽样字段 | `name: "Skill更"` |
| `unique_helper_fields` | 需唯一值的业务字段辅助函数 | `admin_id` → `_new_admin_id()` |
| `soft_delete_field` | 软删字段名，无则空 | `is_delete` |
| `status_flag_fields` | 状态字段及锁定/可用测试值 | `status: 0 / 1` |

**约定**：
- 集成测试路径必须与 Resource 前缀一致：`/api/v1/{resource_path}`
- 唯一约束字段（account、业务 ID 等）必须用随机/时间戳生成，避免重复跑失败
- 密码等敏感字段可用固定测试串；Response 断言中不应出现 password
- 单元测试默认 skip，不阻塞 CI；集成 CRUD 用例默认**不** skip，应能对真实库跑通

## 类型映射规则

使用 `resources/config/type_mappings.json` 定义的映射关系：

| SQL 类型 | SQLAlchemy 类型 | Pydantic 类型 |
| ----------- | ----------------- | --------------- |
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
├── repository/            # 数据访问层（仅 create/delete/update/get，增删改查，可覆盖）
│   └── {table_name}_repository.py
├── service/               # 业务服务（单条委托 + 列表等业务）
│   └── {table_name}_service.py
├── api/                   # API路由层
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       └── {resource_name}/
│           └── {resource_name}Resource.py
├── start.py
├── pyproject.toml
├── .python-version
├── requirements.txt
└── .env.example

🔒 分层约定：
- Repository = 仅单条 `create` / `delete` / `update` / `get`（增删改查顺序，可覆盖）
- Service = 单条委托 + 列表/状态等业务（已存在不覆盖）
- Schema = 进入 API 前的字段校验
- Resource/API **只**依赖 Service

📝 下一步（推荐 uv）：
1. 安装 uv（若尚未安装）：https://docs.astral.sh/uv/
2. uv sync
3. cp .env.example .env 并配置数据库
4. uv run uvicorn start:app --reload
   （或：uv run python start.py）

（兼容）未使用 uv 时：pip install -r requirements.txt && uvicorn start:app --reload
```

**后续添加新表时：**
```
✅ 已添加 {table_name} 的 CRUD 代码

📁 生成/更新的文件：
1. models/{table_name}.py
2. schemas/{table_name}.py
3. repository/{table_name}_repository.py（覆盖）
4. service/{table_name}_service.py（仅不存在时新建）
5. api/v1/{resource_name}/{resource_name}Resource.py
6. tests/unit/test_{table_name}_service.py（仅不存在时新建，占位）
7. tests/integration/api/v1/test_{table_name}.py（仅不存在时新建，CRUD+业务占位）
8. 注册：api/v1/__init__.py、core/dependencies.py（Resource 使用 get_*_service）

📝 下一步：
1. 重启应用即可使用新接口（`uv run uvicorn start:app --reload`）
2. 运行集成测试：`uv run pytest tests/integration/api/v1/test_{table_name}.py -c tests/pytest.ini -v`
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

1. **Base继承**：模型继承项目 `BaseModel`/`Base`，公共字段按项目约定放在具体模型中
2. **软删除/硬删除**：由 Repository 根据是否存在软删字段决定
3. **状态/标识位**：命中 `status_flag_fields.json` 时必须在 **Service** 生成 `update_status` + Schema `StatusUpdate` + Resource `PATCH /{pk}/status`；Repository 仅有 `create/delete/update/get`，不暴露 `update_status`
4. **分层**：API → Service（单条委托 + 列表等业务）→ Repository（仅单条 CRUD）→ Model；**禁止** API 直调 Repository。Schema 负责请求校验。
5. **Repository 方法名固定**：仅 `create` / `delete` / `update` / `get`（单条；源码按增删改查顺序）
6. **测试**：按表生成 `tests/unit/test_{table}_service.py`（占位）与 `tests/integration/api/v1/test_{table}.py`（CRUD 可跑 + 业务占位）；已存在则跳过
7. **覆盖策略**：Repository 可覆盖；Service / 测试文件已存在则跳过
8. **异步**：使用 `AsyncSession` + `select()`
9. **中文文档**：文档字符串、注释、API 文档使用中文
10. **安全性**：端点含异常处理；认证按业务可选；状态字段不走通用 PUT
11. **包管理默认 uv**：首次骨架必须生成 `pyproject.toml` + `.python-version`；README 与收尾步骤优先 `uv sync` / `uv run`；`requirements.txt` 仅兼容
12. **🔴 资源名必须单数（最高优先级）**：生成 `api/v1/{resource_name}/` 文件夹与路由前缀时，
   `resource_name` 必须严格等于**表名单数形式**，**绝对禁止**复数化。
   以下为错误 ↔ 正确对照（务必避免左侧）：

   | 表名 | ❌ 错误（复数） | ✅ 正确（单数） |
   |------|----------------|----------------|
   | `company_file` | `api/v1/company_files/`、前缀 `/company-files` | `api/v1/company_file/`、前缀 `/company-file` |
   | `student` | `api/v1/students/`、前缀 `/students` | `api/v1/student/`、前缀 `/student` |
   | `sys_class` | `api/v1/sys_classes/`、前缀 `/sys-classes` | `api/v1/sys_class/`、前缀 `/sys-class` |

   - 复数**只**允许出现在中文展示文案（`tags=["企业文件管理"]` 等），**永不**进入文件夹名、文件名、路由前缀。
   - 生成前务必自检：`resource_name` 是否等于表名原样？若发现 `s`/`es` 结尾的文件夹或前缀，即为错误，必须改回单数。
