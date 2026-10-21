# 在 CodeBuddy 中用 sql-to-fastapi-restfulapi-scaffold 快速生成 FastAPI 脚手架

> 面向第一次使用技能的同学。照着下面的步骤操作，可以从一个空目录开始，生成并跑起来一套带分层、测试、Docker 配置的 FastAPI 项目。

---

## 0. 这个技能能做什么

你给它一段建表 SQL，它还你一整套后端代码：

| 你提供 | 技能产出 |
|---|---|
| `CREATE TABLE` 语句，或一个 `.sql` 文件 | Model / Schema / Repository / Service / Resource / 测试 / 项目骨架 |

生成的项目大致长这样：

```text
fastapi_project/
├── app/                    # 应用工厂、异常、中间件、基础路由
├── config/                 # 配置（唯一配置源）
├── core/                   # 数据库、缓存、队列、权限
├── models/                 # SQLAlchemy 模型
├── schemas/                # Pydantic 校验与响应模型
├── repository/             # 数据访问（仅单条 CRUD）
├── service/                # 业务逻辑（分页、过滤、状态变更）
├── api/v1/student/         # 路由（只调用 Service）
├── tests/                  # 单元测试占位 + 集成测试
├── utils/                  # 日志、异常、校验、脱敏等
├── middleware/             # 安全头、限流、审计（默认关闭）
├── docker/                 # Dockerfile + compose（app + MySQL）
├── deploy/                 # Nginx / 监控 / 日志等进阶配置
├── start.py
├── pyproject.toml
└── .env.example
```

你不需要手写这 7 个按表生成的文件：`models`、`schemas`、`repository`、`service`、`resource`、`tests/unit`、`tests/integration`。

---

## 1. 准备工作

开始前确认本机具备：

- [ ] CodeBuddy IDE 或 CodeBuddy 插件
- [ ] Python 3.10+（技能模板默认钉选 3.12）
- [ ] `uv`（推荐）。没装也没关系，后面有 pip 兼容方案
- [ ] 一个可连接的 MySQL（只启动服务、看 Swagger 可以不连；跑集成测试需要）
- [ ] 本仓库代码（提供技能目录 `sql-to-fastapi-restfulapi-scaffold/`）

安装 `uv`（可选）：

```powershell
# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 2. 第 1 步：新建目标项目并安装技能

### 2.1 新建空目录

新建一个专门放生成结果的项目目录，例如 `D:\work\student-api`，然后用 CodeBuddy 打开这个目录。

> 不要直接在本技能仓库里生成项目，否则生成物会和技能源码混在一起。

### 2.2 把技能复制到项目中

在 CodeBuddy 的终端里执行（把 `<本仓库路径>` 换成你机器上的实际路径）。

**PowerShell（Windows）**

```powershell
New-Item -ItemType Directory -Force -Path .codebuddy/skills | Out-Null
Copy-Item -Recurse -Force "<本仓库路径>\sql-to-fastapi-restfulapi-scaffold" .codebuddy/skills/
```

例如：

```powershell
Copy-Item -Recurse -Force "E:\Open_source_project\ncepu_ideal-skills\sql-to-fastapi-restfulapi-scaffold" .codebuddy/skills/
```

**Bash（macOS / Linux）**

```bash
mkdir -p .codebuddy/skills
cp -r <本仓库路径>/sql-to-fastapi-restfulapi-scaffold .codebuddy/skills/
```

### 2.3 为什么必须复制整个目录

这个技能是**资源驱动**的：`SKILL.md` 只写规则，真正生成代码时还要读取：

```text
sql-to-fastapi-restfulapi-scaffold/
├── SKILL.md
└── resources/
    ├── config/               # 类型映射、命名规则、状态字段、基线策略
    ├── specifications/       # 代码规范
    ├── templates/
    │   ├── project_structure/  # 首次生成的完整骨架
    │   └── layers/             # 按表生成的各层模板
    └── tools/
        └── check_skill_consistency.py
```

只复制 `SKILL.md`，技能就会因为读不到模板而“自由发挥”，生成结果不可控。

### 2.4 可选：安装到用户级

希望所有项目都能用时，安装到用户目录，而不是某个项目：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.codebuddy\skills" | Out-Null
Copy-Item -Recurse -Force "<本仓库路径>\sql-to-fastapi-restfulapi-scaffold" "$HOME\.codebuddy\skills\"
```

---

## 3. 第 2 步：确认安装成功

### 3.1 检查文件是否齐全

在目标项目根目录执行：

```powershell
Test-Path .codebuddy/skills/sql-to-fastapi-restfulapi-scaffold/SKILL.md
Test-Path .codebuddy/skills/sql-to-fastapi-restfulapi-scaffold/resources/templates/project_structure
Test-Path .codebuddy/skills/sql-to-fastapi-restfulapi-scaffold/resources/config/project_baseline.json
```

三条都返回 `True` 才算复制完整。

### 3.2 在 CodeBuddy 中确认

- 新开一个对话（或重启 IDE，让它重新扫描技能）
- 在 CodeBuddy Code 中输入 `/skills`，应能看到 `sql-to-fastapi-restfulapi-scaffold`
- 在 IDE 的「设置 → 技能 / Skills」中，也能在 Project Skills 里看到它

**看到技能名出现在列表中，就说明安装成功。**

---

## 4. 第 3 步：准备 SQL

### 4.1 新建 SQL 文件

在项目里建一个 `sql/` 目录，把建表语句放进去，例如 `sql/student.sql`：

```sql
CREATE TABLE student (
    id INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    student_no VARCHAR(20) NOT NULL COMMENT '学号',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    phone VARCHAR(20) COMMENT '手机号',
    age INT COMMENT '年龄',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用 0停用',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_student_no (student_no)
) COMMENT='学生表';
```

> 字段名会统一转成 Python 的 snake_case：`student_no` 保持 `student_no`；如果建表时写的是 `phoneNumber`，接口里就是 `phone_number`。
>
> 这张表故意带上了三样东西，方便一次看到技能的完整能力：
> - `is_deleted` → 自动走软删除
> - `status` → 自动生成专用的状态接口
> - `phone` / `age` → 自动生成校验与脱敏逻辑

### 4.2 也可以直接用仓库里的完整示例

仓库提供了包含 11 张表的完整 SQL：

```text
test/api_security_demo-20260717.sql
```

但**第一次不建议直接用**。先用一张表跑通全流程，确认生成风格符合预期，再批量处理。

---

## 5. 第 4 步：发起生成

在 CodeBuddy 对话框里粘贴下面的提示词（按需修改文件名和表名）：

```text
请使用 sql-to-fastapi-restfulapi-scaffold 技能，根据 sql/student.sql 生成 FastAPI 项目脚手架。

这是首次生成，需要完整的项目骨架。

要求：
1) 严格按 Resource → Service → Repository → Model 分层，Resource 只依赖 Service；
2) Repository 只保留 create / delete / update / get 四个方法；
3) 资源目录与路由前缀使用单数：api/v1/student/、/student；
4) 生成单元测试占位和集成测试；
5) 依赖使用 uv 管理；
6) 注释和接口文档用中文。
```

不点名技能通常也能触发，但**点名更稳**，尤其是在装了多个技能时。

生成过程中，你会看到 Agent 依次：

1. 读取 `SKILL.md`
2. 读取 `resources/config/` 下的映射与规则
3. 读取 `resources/templates/` 下的骨架和层模板
4. 逐个写出文件

如果它跳过读模板、直接开始写代码，停下来，让它先读 `SKILL.md` 和 `resources/`。

---

## 6. 第 5 步：检查生成结果

### 6.1 应该生成哪些文件

首次生成会产出完整骨架；就 `student` 这一张表而言，会多出 7 个文件：

| 序号 | 文件 | 说明 |
|---|---|---|
| 1 | `models/student.py` | SQLAlchemy 模型 |
| 2 | `schemas/student.py` | Base / Create / Update / StatusUpdate / Response |
| 3 | `repository/student_repository.py` | 仅单条 CRUD |
| 4 | `service/student_service.py` | 单条委托 + 列表等业务 |
| 5 | `api/v1/student/studentResource.py` | 路由，只调 Service |
| 6 | `tests/unit/test_student_service.py` | 单元测试占位（默认 skip） |
| 7 | `tests/integration/api/v1/test_student.py` | 集成测试（CRUD 可跑） |

另外还会更新两处注册：

- `api/v1/__init__.py`：挂载新的路由
- `service/dependencies.py`：追加 `get_student_service`

### 6.2 逐条核对

- [ ] 目录是 `api/v1/student/`，不是 `api/v1/students/`
- [ ] 路由前缀是 `/student`，不是 `/students`
- [ ] `repository/student_repository.py` 里只有 `create` / `delete` / `update` / `get`
- [ ] 分页、过滤、软删排除在 `service/student_service.py` 的 `get_list` 里
- [ ] `Resource` 用的是 `Depends(get_student_service)`，没有直接依赖 Repository
- [ ] 有 `status` 字段，所以存在 `PATCH /{id}/status`
- [ ] 项目根目录有 `pyproject.toml`、`.env.example`、`start.py`

### 6.3 发现不对怎么让它改

不要自己手动改生成结果，直接指出问题让它重做对应的那一层，例如：

```text
api/v1 下的资源目录被生成成了复数 students，请改回单数 student，
同时把路由前缀改成 /student，并同步更新 api/v1/__init__.py。
```

---

## 7. 第 6 步：配置并启动

### 7.1 同步依赖

```bash
uv sync
```

`uv` 会读取 `.python-version`（模板为 3.12），按需下载对应 Python，并创建 `.venv`。

### 7.2 配置环境变量

```powershell
# Windows
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

打开 `.env`，把数据库连接改成你自己的：

```env
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/你的库名?charset=utf8mb4
```

其他项第一次可以先用默认值：

```env
FASTAPI_ENV=development
DEBUG=true
CACHE_ENABLED=false
```

### 7.3 启动

```bash
uv run uvicorn start:app --reload
```

或者：

```bash
uv run python start.py
```

### 7.4 看到什么算成功

终端出现类似输出：

```text
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

浏览器打开：

- Swagger UI：<http://localhost:8000/docs>
- ReDoc：<http://localhost:8000/redoc>

在 Swagger 里能看到 `/api/v1/student` 下的 5 个接口（列表、详情、创建、更新、删除）和 1 个状态接口 `PATCH /api/v1/student/{id}/status`。

### 7.5 没装 uv 时的兼容方案

```bash
pip install -r requirements.txt
uvicorn start:app --reload
```

---

## 8. 第 7 步：验证接口

### 8.1 在 Swagger 里点

打开 <http://localhost:8000/docs>：

1. 展开 `POST /api/v1/student`
2. 点「Try it out」
3. 填入请求体，例如：

```json
{
  "student_no": "S2026001",
  "name": "张三",
  "phone": "13800138000",
  "age": 20,
  "status": 1
}
```

4. 点「Execute」，看到 `200` 或 `201` 即为成功
5. 再用 `GET /api/v1/student` 查列表

### 8.2 用命令行

```bash
curl -X POST http://127.0.0.1:8000/api/v1/student \
  -H "Content-Type: application/json" \
  -d '{"student_no":"S2026001","name":"张三","phone":"13800138000","age":20,"status":1}'
```

```bash
curl http://127.0.0.1:8000/api/v1/student
```

PowerShell 里 `curl` 是 `Invoke-WebRequest` 的别名，建议写成：

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/student `
  -ContentType 'application/json' `
  -Body '{"student_no":"S2026001","name":"张三","phone":"13800138000","age":20,"status":1}'
```

### 8.3 验证状态接口

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/student/1 \
  -H "Content-Type: application/json" \
  -d '{"status":0}'
```

状态变更必须走这个接口，不要用通用 `PUT`。

### 8.4 跑集成测试

集成测试会直连真实 MySQL：

```bash
uv run pytest tests/integration/api/v1/test_student.py -c tests/pytest.ini -v
```

单元测试默认是 `@pytest.mark.skip` 占位，需要你补完用例后自行取消跳过。

---

## 9. 第 8 步：继续添加新表

项目骨架已经存在后，不要再让它“重新生成整个项目”，而是做**增量生成**：

```text
请使用 sql-to-fastapi-restfulapi-scaffold 技能，为 sql/course.sql 做增量生成。

要求：
1) 只生成 course 相关文件，不要重建项目骨架；
2) 资源目录 api/v1/course/，路由前缀 /course，保持单数；
3) 已存在的 service 和测试文件不要覆盖；
4) 不要改动 utils / middleware / docker / deploy。
```

### 覆盖策略（很重要）

| 路径 | 生成时的行为 |
|---|---|
| `utils/**`、`middleware/**`、`docker/**`、`deploy/**`、`.env.docker` | 已存在就**整包跳过**，绝不覆盖 |
| `repository/{表}_repository.py` | **始终覆盖**（自动生成，别手改） |
| `service/{表}_service.py` | **仅不存在时创建**，已存在则跳过 |
| `models/{表}.py`、`schemas/{表}.py` | 默认可覆盖 |
| `api/v1/...Resource.py` | 可覆盖基础 CRUD |
| `tests/unit/...`、`tests/integration/...` | 仅不存在时创建 |

因为 `repository` 会被覆盖、`service` 不会被覆盖，所以：

- **业务逻辑写在 Service**，不会丢
- **不要手改 Repository**，改了也会被下次生成覆盖

> 建议每次增量生成前先 `git commit` 一次，出问题可以直接对比或回滚。

---

## 10. 常见问题

### 10.1 对话里没有任何反应，技能没被调用

- 在提示词里直接点名：`请使用 sql-to-fastapi-restfulapi-scaffold 技能`
- 确认技能在 `.codebuddy/skills/` 下，且目录里有 `SKILL.md`
- 新开一个对话或重启 IDE

### 10.2 提示找不到模板 / 读不到配置

只复制了 `SKILL.md`。回到第 2 步，用 `Copy-Item -Recurse` 或 `cp -r` **整目录复制**，并跑第 3 步的三条 `Test-Path`。

### 10.3 生成的目录或路由是复数

这是这个技能最容易被模型“顺手改错”的地方。规则是**表名原样、不加 s**：

| 表名 | ❌ 错误 | ✅ 正确 |
|---|---|---|
| `student` | `api/v1/students/`、`/students` | `api/v1/student/`、`/student` |
| `company_file` | `api/v1/company_files/`、`/company-files` | `api/v1/company_file/`、`/company-file` |
| `sys_class` | `api/v1/sys_classes/`、`/sys-classes` | `api/v1/sys_class/`、`/sys-class` |

在提示词里显式写上“单数”，生成后按 6.2 核对。

### 10.4 我手写的 Service 业务被覆盖了

正常策略是“Service 已存在则跳过”。如果确实被覆盖：

1. 先 `git diff` 看范围
2. 恢复文件
3. 重新发起时明确说：`service/student_service.py 已存在，请跳过，不要覆盖`

### 10.5 `utils/`、`docker/` 等目录被重写了

默认应该是“已存在就整包跳过”。如果被覆盖，重新发起并要求：

```text
utils / middleware / docker / deploy 已存在，请整包跳过，不要覆盖。
```

### 10.6 状态字段还是只能用 PUT 改

检查字段名是否命中状态规则：`status`、`state`、`enabled`、`locked`、`is_active`、`*_flag`、`status_*` 等。
`is_deleted`、`password`、`type`、`user_type` 是排除项，不会生成状态接口。

### 10.7 集成测试连不上数据库

集成测试用真实 MySQL，检查：

- `.env` 是否已从 `.env.example` 复制并填写
- `DATABASE_URL` 的用户名、密码、库名、端口是否正确
- 数据库是否已启动，表是否已建（建表脚本由你自己放入 `database/`）

只想先看接口的话，可以先不跑集成测试。

### 10.8 表太多，生成到一半中断了

拆分处理：一次一到两张表，每张生成后立刻启动并跑测试，再继续下一张。

### 10.9 主键是业务主键（如 `studentID`）怎么办

技能默认按“自增主键”处理：主键不进 Create 模型，由数据库生成。
如果主键是业务主键（如 `studentID`、`classID`），在提及时明确说明：

```text
主键 studentID 是业务主键，不是自增主键，请把它包含在 Create 模型中。
```

---

## 附录 A：生成的项目结构

```text
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── factory.py            # 应用工厂，lifespan 在这里
│   ├── config.py
│   ├── exceptions.py
│   ├── middleware.py
│   └── routes.py
├── config/                   # 唯一配置源
├── core/                     # database / cache / queue / security / permissions
├── models/                   # base.py + 按表生成
├── schemas/                  # response.py + 按表生成
├── repository/               # 仅单条 CRUD
├── service/                  # 单条委托 + 列表等业务
│   └── dependencies.py
├── api/
│   └── v1/
│       └── student/
│           └── studentResource.py
├── middleware/               # 安全头 / 限流 / 审计（默认关闭）
├── utils/                    # logger / exceptions / validators / masking ...
├── docker/                   # Dockerfile + docker-compose.yml
├── deploy/                   # 进阶运维素材
├── tests/
│   ├── conftest.py
│   ├── pytest.ini
│   ├── unit/
│   └── integration/api/v1/
├── start.py
├── pyproject.toml
├── .python-version
├── requirements.txt
├── .env.example
└── .env.docker
```

## 附录 B：分层速记

```text
Resource（路由，只调 Service）
    ↓
Service（单条委托 + 分页/过滤/状态等业务）
    ↓
Repository（只有 create / delete / update / get）
    ↓
Model（SQLAlchemy）
```

三条硬规则：

1. Resource **禁止**直接依赖 Repository
2. Repository **只有** 4 个方法，列表和状态变更属于业务，放 Service
3. Schema 负责请求校验，校验不通过不会进入 API

---

## 一句话总结

```text
建空项目 → 复制技能到 .codebuddy/skills/ → 准备 SQL → 点名技能生成
→ 核对单数与分层 → uv sync → 配置 .env → 启动 → 打开 /docs
```

跑通第一张表后，后续加表只需要重复“准备 SQL + 增量生成”两步。
