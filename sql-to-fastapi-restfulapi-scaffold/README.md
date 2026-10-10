# SQL-to-FastAPI-Scaffold Skill

## 概述

`sql-to-fastapi-scaffold` 是一个技能，用于数据库的从SQL脚本语句自动生成完整的 FastAPI 项目脚手架代码。

## 功能特性

- ✅ 解析 SQL CREATE TABLE 语句
- ✅ 生成 SQLAlchemy Model
- ✅ 生成 Pydantic Schema（Base / Create / Update / Response；有状态字段时含 StatusUpdate）
- ✅ 生成 Repository（**仅单条** `create` / `get` / `update` / `delete`，可覆盖）
- ✅ 生成 Service（**已存在则跳过**；单条委托 Repository；`get_list` 等业务写在本层）
- ✅ 生成 FastAPI Resource（**统一只依赖 Service**；校验靠 Schema）
- ✅ 生成单元测试占位（`tests/unit/test_{table}_service.py`，已存在则跳过）
- ✅ 生成集成测试（`tests/integration/api/v1/test_{table}.py`：CRUD 可跑 + 业务占位，已存在则跳过）
- ✅ 支持软删除/硬删除自动判断
- ✅ 识别状态/标识位字段，自动生成专用改状态接口（`PATCH /{pk}/status`）
- ✅ 异步 SQLAlchemy（AsyncSession）
- ✅ 中文文档字符串和注释
- ✅ 目标项目默认用 **uv** 管理依赖与启动（`pyproject.toml` + `uv sync` / `uv run`）

## 分层约定

```text
API(Resource) → Service(单条委托 + 列表等业务) → Repository(仅 create/delete/update/get，增删改查顺序) → Model
```

| 层 | 路径 | 覆盖策略 | 职责 |
|----|------|----------|------|
| Repository | `repository/{table}_repository.py` | 可覆盖 | 仅单条 CRUD |
| Service | `service/{table}_service.py` | 仅首次生成 | 单条委托 + 列表/状态等业务 |
| Resource | `api/v1/...` | 可覆盖基础 CRUD | 只调 Service |

## 技能项目结构

```text
sql-to-fastapi-restfulapi-scaffold/
├── docs/
│   ├── Trea中使用skill配置.md
│   ├── claude中使用skill配置.md
│   └── GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md
├── resources/
│   ├── config/
│   │   ├── naming_rules.json
│   │   ├── type_mappings.json
│   │   ├── status_flag_fields.json
│   │   ├── package_manager.json    # uv 包管理与启动约定
│   │   └── project_baseline.json   # utils 等基线包清单与复用策略
│   ├── specifications/
│   │   └── coding_standards.md
│   └── templates/
│       ├── layers/
│       │   ├── model/
│       │   ├── schema/
│       │   ├── repository/
│       │   ├── service/
│       │   ├── resource/
│       │   └── test/
│       │       ├── unit/
│       │       └── integration/
│       └── project_structure/
│           ├── pyproject.toml      # uv 主依赖清单
│           ├── .python-version
│           ├── requirements.txt    # pip 兼容
│           ├── start.py
│           ├── .env.example
│           ├── .env.docker
│           ├── app/
│           ├── api/
│           ├── config/
│           ├── core/
│           ├── models/
│           ├── schemas/
│           ├── repository/
│           ├── service/
│           ├── utils/              # 基线工具包（与 project_baseline 对齐）
│           ├── middleware/         # 基线中间件：安全头 / 限流 / 审计
│           ├── docker/             # 起步 Docker：app + MySQL（Redis 可选）
│           └── deploy/             # 进阶运维配置（Nginx/监控/日志等）
├── README.md
└── SKILL.md
```

## 基线包 utils / middleware / docker / deploy

目标项目若已有常用工具、中间件或部署目录，技能通过 `resources/config/project_baseline.json` 声明：

- 默认 `brownfield_prefer_existing`：检测到对应目录已存在 → **整包跳过**
- 空项目从 `project_structure/` 写入：`utils/`、`middleware/`、`docker/`、`deploy/`、`.env.docker`
- **docker**：`Dockerfile` + `docker-compose.yml`（app + MySQL；`--profile redis` 可选）
- **deploy**：进阶运维素材，**不**进入默认 compose 必跑栈
- 层代码 import 必须以 `canonical_imports` 为准
- 禁止为单表新建 `utils/{table}_*.py` 或 `middleware/{table}_*.py`

## 使用方法

### 1 配置技能到目标开发IDE中

- 如果你使用的是 Trae IDE，你可以直接在 IDE 中配置技能环境。
- 操作文档请参考
[Trea IDE 配置技能](docs/Trea中使用skill配置.md)

- 如果你使用的是 Claude Code，你可以通过扩展来配置技能环境。
- 操作文档请参考
[claude code 配置技能](docs/claude中使用skill配置.md)

### 2 准备SQL语句

向技能提供 SQL CREATE TABLE 语句，例如：

```sql
CREATE TABLE student (
    studentID VARCHAR(20) PRIMARY KEY COMMENT '学号',
    userID VARCHAR(22) COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    phoneNumber VARCHAR(20) COMMENT '电话号码',
    age INT COMMENT '年龄',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (userID) REFERENCES sso_user(userID)
);
```

当然也可以使用sql语句初始化项目

### 3 请求技能生成代码

向 AI 开发工具进行对话：

例如：

```sql
请根据以下SQL CREATE TABLE 语句（或者是sql文件），生成对应的 FastAPI 项目脚手架代码：
CREATE TABLE student (
    studentID VARCHAR(20) PRIMARY KEY COMMENT '学号',
    userID VARCHAR(22) COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    phoneNumber VARCHAR(20) COMMENT '电话号码',
    age INT COMMENT '年龄',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (userID) REFERENCES sso_user(userID)
);
```

然后请求使用此技能生成脚手架代码。

## 生成的目标项目代码结构

首次运行时，技能将生成完整的项目结构：

```text
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── factory.py
│   ├── events.py
│   ├── exceptions.py
│   ├── middleware.py
│   ├── router.py
│   ├── routes.py
│   └── config.py
├── config/
│   ├── __init__.py
│   ├── config_unified.py
│   ├── config_factory.py
│   ├── manage.py
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── database.py
│   ├── dependencies.py
│   ├── cache.py
│   ├── security.py
│   ├── permissions.py
│   └── queue.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   └── student.py                 # 按表生成
├── schemas/
│   ├── __init__.py
│   ├── response.py
│   └── student.py                 # 按表生成
├── repository/                    # 可覆盖：仅 create/delete/update/get（增删改查，单条）
│   ├── __init__.py
│   └── student_repository.py      # 按表生成
├── service/                       # 人手维护：单条委托 + 列表等业务
│   ├── __init__.py
│   ├── dependencies.py
│   └── student_service.py         # 按表生成
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       └── student/               # 单数资源名，按表生成
│           └── studentResource.py
├── middleware/                    # BASELINE：安全头 / 限流 / 审计（配置开关默认关）
│   ├── __init__.py
│   ├── security_headers.py
│   ├── rate_limiter.py
│   └── audit_middleware.py
├── utils/                         # BASELINE：已存在则跳过（project_baseline.json）
│   ├── __init__.py
│   ├── logger.py
│   ├── loguru.py
│   ├── custom_exceptions.py
│   ├── response_code.py
│   ├── validators.py
│   ├── masking.py
│   ├── ids.py
│   ├── auth.py
│   ├── security.py
│   └── audit.py
├── docker/                        # BASELINE：Dockerfile + docker-compose.yml
├── deploy/                        # BASELINE：进阶运维，不进入默认 compose 必跑栈
├── start.py
├── pyproject.toml                 # uv / PEP 621 主依赖清单
├── .python-version                # uv Python 版本钉选
├── requirements.txt               # 兼容 pip（与 pyproject 同步）
├── .env.example
└── .env.docker
```

后续添加新表时，生成：

1. **models/{table_name}.py** - SQLAlchemy 数据模型
2. **schemas/{table_name}.py** - Pydantic 验证模型（Base、Create、Update、Response；有状态字段时含 StatusUpdate）
3. **repository/{table_name}_repository.py** - 仅 `create` / `delete` / `update` / `get`（增删改查顺序，可覆盖）
4. **service/{table_name}_service.py** - 单条委托 + `get_list` 等业务（仅不存在时新建；有状态字段时含 `update_status`）
5. **api/v1/{resource_singular}/{resource_singular}Resource.py** - 统一只调 Service（有状态字段时含 `PATCH /{pk}/status`）
6. **tests/unit/test_{table_name}_service.py** - Service 单元测试占位（仅不存在时新建）
7. **tests/integration/api/v1/test_{table_name}.py** - 接口 CRUD 集成测试 + 商业逻辑占位（仅不存在时新建）
8. **service/dependencies.py** - 注册 `get_*_service`（及可选 `get_*_repository`）

> 增量生成时 **不**覆盖 `utils/**`、`middleware/**`；import 使用 `project_baseline.json` 的 `canonical_imports`。

**路由结构**：

- `api/__init__.py` → `api_router` (prefix="/api")
- `api/v1/__init__.py` → `v1_router` (prefix="/v1")
- 子路由不额外加前缀，由具体API文件定义

**中间件结构**：

- `middleware/`：基线三件套（`security_headers` / `rate_limiter` / `audit_middleware`）
- `app/middleware.py`：统一注册；CORS 始终开启；安全中间件按 `middleware_*_enabled` 开关（默认关闭）

**不强制首次生成的进阶内容**（可选基线，见 `project_baseline.json`）：

- `deploy/` 进阶运维（Nginx / 监控等）；起步用 `docker/` 即可
- 完整业务表 SQL（由用户 `database/` 提供）
- 按表的业务规则实现（Service 占位，人手补齐）

## 特性说明

### 测试代码

按表生成两类测试（模板见 `resources/templates/layers/test/`）：

| 类型 | 路径 | 内容 |
|------|------|------|
| 单元占位 | `tests/unit/test_{table}_service.py` | 面向 Service；默认 `skip`，人手补齐 |
| 集成 | `tests/integration/api/v1/test_{table}.py` | **可跑** CRUD（真实 MySQL）+ 商业逻辑接口 `skip` 占位 |

运行示例：

```bash
uv run pytest tests/integration/api/v1/test_admin.py -c tests/pytest.ini -v
```

### 软删除/硬删除

技能会自动检测表中是否有软删除字段（支持以下字段名）：

- `is_deleted`
- `is_delete`
- `deleted`

**软删除逻辑**（有软删除字段时）：

- Service.`get_list()` - 只查询未删除的记录
- Repository.`get()` / `update()` - 只操作未删除的记录
- Repository.`delete()` - 设置软删除字段为 True

**硬删除逻辑**（无软删除字段时）：

- Service.`get_list()` - 查询所有记录
- Repository.`get()` / `update()` - 按主键操作
- Repository.`delete()` - 直接从数据库删除记录

### 状态/标识位专用接口

按 `resources/config/status_flag_fields.json` 识别状态字段（如 `status`、`is_active`、`*_flag` 等；排除软删与密码等）。

命中后额外生成：

| 层 | 产物 |
|----|------|
| Schema | `{ClassName}StatusUpdate`；状态字段从通用 `Update` 排除 |
| Service | `update_status`（业务入口；内部 `repo.update(字段字典)`） |
| Resource | `PATCH /{pk}/status` |

> Repository **仅** `create` / `get` / `update` / `delete`，不生成 `update_status` / `get_list`。

示例（`sso_user.status`）：

```http
PATCH /api/v1/sso-user/{user_id}/status
Content-Type: application/json

{"status": 0}
```

> 状态变更必须走专用接口，禁止通过通用 `PUT` 修改。

### 依赖注入

在 `service/dependencies.py` 中为每张表生成：

- `get_{table}_service` — **Resource 统一使用**
- `get_{table}_repository` — 一般仅供 Service 内部或特殊场景

```python
from service.dependencies import get_student_service

async def get_student_list(
    ...,
    service: StudentService = Depends(get_student_service),
):
    result = await service.get_list(...)
    ...
```

### 数据验证

自动为以下字段生成验证器：

- 手机号（字段名包含 `phone`）：中国手机号格式验证
- 邮箱（字段名包含 `email`）：邮箱格式验证
- 年龄（字段名为 `age`）：0-150 范围验证
- 性别（字段名包含 `gender` 或 `sex`）：枚举值验证

### 数据脱敏

自动为敏感字段生成脱敏属性：

- 手机号（显示前 3 位 + **** + 后 4 位）
- 邮箱（显示前 3 位 + **** + 后 4 位）

## 项目启动（推荐 uv）

生成完成后，按以下步骤启动项目。依赖与虚拟环境默认用 [uv](https://docs.astral.sh/uv/) 管理（约定见 `resources/config/package_manager.json`）。

1. 安装 uv（若尚未安装）

   参见：<https://docs.astral.sh/uv/getting-started/installation/>

2. 同步依赖（创建/更新 `.venv`）

   ```bash
   uv sync
   ```

   > `pyproject.toml` 中 `default-groups = ["dev"]`，会一并安装测试依赖。  
   > 增删依赖：`uv add <package>` / `uv add --dev <package>`

3. 配置环境变量

   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置数据库连接等
   ```

4. 启动应用

   ```bash
   uv run uvicorn start:app --reload
   # 或
   uv run python start.py
   ```

5. 访问 API 文档

   - Swagger UI: <http://localhost:8000/docs>
   - ReDoc: <http://localhost:8000/redoc>

### 兼容：未安装 uv 时

```bash
pip install -r requirements.txt
uvicorn start:app --reload
# 或: python start.py
```
