# api_security_demo — FastAPI 脚手架

基于 `.skill`（`sql-to-fastapi-restfulapi-scaffold`）与 `database/api_security_demo-20260717.sql` 自动生成的 FastAPI 项目脚手架。

## 技术栈

- Python 3.10+
- FastAPI + Uvicorn
- SQLAlchemy 2.x（AsyncSession + aiomysql）
- Pydantic v2 / pydantic-settings
- loguru、pytest、httpx

## 分层约定

```text
API(Resource) → Service（单条委托 + 列表/状态等业务） → Repository（仅 create/get/update/delete） → Model
```

- Resource **只**依赖 Service
- Repository **仅**单表单条 CRUD
- 列表分页、过滤、状态变更写在 Service
- 请求校验由 Schema 在进入 API 前完成

## 项目结构

```text
.
├── app/                 # 应用工厂、中间件、异常、路由注册
├── api/v1/              # 各资源 Resource（单数路径）
├── config/              # 配置
├── core/                # 数据库与依赖注入
├── models/              # SQLAlchemy 模型
├── schemas/             # Pydantic DTO + 统一响应
├── repository/          # 数据访问层（可覆盖）
├── service/             # 业务服务（已存在不覆盖）
├── utils/               # 异常、日志
├── tests/               # 单元占位 + 集成 CRUD
├── database/            # 原始 SQL 脚本
├── .skill/              # 生成技能定义
├── start.py
├── requirements.txt
└── .env.example
```

## 快速开始（推荐 uv）

```bash
# 1. 导入数据库
mysql -u root -p < database/api_security_demo-20260717.sql

# 2. 同步依赖（需已安装 uv：https://docs.astral.sh/uv/）
uv sync

# 3. 配置环境
cp .env.example .env
# 编辑 DATABASE_URL=mysql+pymysql://user:password@localhost:3306/api_security_demo

# 4. 启动
uv run uvicorn start:app --reload
# 或: uv run python start.py
```

未安装 uv 时：`pip install -r requirements.txt`，再执行 `uvicorn start:app --reload`。

- Swagger：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc
- 健康检查：`GET /health`

## 配置说明

| 变量 | 说明 |
|------|------|
| `DATABASE_URL` | MySQL 连接串（`mysql+pymysql://...`，运行时自动转为 aiomysql） |
| `HOST` / `PORT` | 服务监听地址 |
| `SECRET_KEY` | JWT 等密钥（脚手架预留） |
| `CORS_*` | 跨域配置 |
| `LOG_LEVEL` / `LOG_FILE` | 日志 |

## 已生成资源与 API

路由前缀均为 **单数**（`_` → `-`）。每张表默认提供：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/{resource}` | 分页列表 |
| GET | `/api/v1/{resource}/{pk}` | 详情 |
| POST | `/api/v1/{resource}` | 创建 |
| PUT | `/api/v1/{resource}/{pk}` | 更新（不含状态字段） |
| DELETE | `/api/v1/{resource}/{pk}` | 软删或硬删 |
| PATCH | `/api/v1/{resource}/{pk}/status` | 仅 `sso_user`（`status`） |

### 资源一览

| 表 | 路由前缀 | 主键 | 软删除 | 状态接口 |
|----|----------|------|--------|----------|
| admin | `/api/v1/admin` | `auto_id` | `is_delete` | — |
| course | `/api/v1/course` | `auto_id` | `is_delete` | — |
| course_arrangement | `/api/v1/course-arrangement` | `auto_id` | `is_delete` | — |
| sso_user | `/api/v1/sso-user` | `auto_id` | — | `PATCH .../status` |
| student | `/api/v1/student` | `auto_id` | `is_delete` | — |
| student_selected_course | `/api/v1/student-selected-course` | `auto_id` | `is_delete` | — |
| sys_class | `/api/v1/sys-class` | `class_id` | `is_delete` | — |
| sys_classinfo | `/api/v1/sys-classinfo` | `auto_id` | `is_deleted` | — |
| sys_college | `/api/v1/sys-college` | `college_id` | `is_delete` | — |
| sys_department | `/api/v1/sys-department` | `department_id` | `is_delete` | — |
| teacher | `/api/v1/teacher` | `auto_id` | `is_delete` | — |

> 视图 `v_student_course_score` 未生成 CRUD（非物理表）。

### 请求/响应示例

**创建学生**

```http
POST /api/v1/student
Content-Type: application/json

{
  "student_id": "20260001",
  "user_id": "U001",
  "class_id": "C01",
  "college_id": "COL01",
  "name": "张三",
  "phone_number": "13800138000",
  "age": 20,
  "gender": "男"
}
```

**成功响应**

```json
{
  "code": "SUCCESS",
  "message": "学生基本信息创建成功",
  "timestamp": "2026-07-17T12:00:00",
  "data": {
    "auto_id": 1,
    "student_id": "20260001",
    "name": "张三",
    "is_delete": false
  }
}
```

**修改账号状态（sso_user）**

```http
PATCH /api/v1/sso-user/1/status
Content-Type: application/json

{ "status": 0 }
```

**分页列表响应**

```json
{
  "code": "SUCCESS",
  "message": "操作成功",
  "data": {
    "items": [],
    "total": 0,
    "page": 1,
    "size": 20,
    "pages": 0
  }
}
```

## Schema 设计

每张表生成：

- `{Class}Base` / `{Class}Create` / `{Class}Update` / `{Class}Response`
- 有状态字段时额外：`{Class}StatusUpdate`（并从 `Update` 中排除状态字段）
- 手机号 / 邮箱 / 性别 / 年龄等按规范生成校验器
- `Update` 设置 `extra = "forbid"`

字段名：数据库驼峰列名映射为 Python `snake_case`（如 `studentID` → `student_id`）。

## 软删除机制

存在 `is_delete` / `is_deleted` / `isDelete` / `isDeleted` 等字段时：

- `DELETE` → 将软删字段置为 `True`/`1`，记录仍留在库中
- `GET` 详情 / 列表 → 自动排除已软删记录
- 无软删字段（如 `sso_user`）→ 硬删除

## 测试

```bash
# 单元测试占位（默认 skip）
uv run pytest tests/unit -c tests/pytest.ini -v

# 集成测试（需真实 MySQL + .env）
uv run pytest tests/integration -c tests/pytest.ini -v
```

集成测试使用 `Authorization: Bearer test-token`，并对真实库执行 CRUD 校验。

## 后续扩展建议

1. 在对应 `service/*_service.py` 中补充业务方法（文件已标注 HAND-WRITTEN，skill 不会覆盖）
2. 按需接入认证（`get_current_user`）
3. 为跨表流程编写集成测试（文件内已有 skip 占位）
