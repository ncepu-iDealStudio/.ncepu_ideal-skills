# SQL-to-FastAPI-Scaffold Skill

## 概述

`sql-to-fastapi-scaffold` 是一个技能，用于数据库的从SQL脚本语句自动生成完整的 FastAPI 项目脚手架代码。

## 功能特性

- ✅ 解析 SQL CREATE TABLE 语句
- ✅ 生成 SQLAlchemy Model（数据模型，支持外键关系）
- ✅ 生成 Pydantic Schema（数据验证模型：Base、Create、Update、Response）
- ✅ 生成 FastAPI Resource（API 路由：5个CRUD端点）
- ✅ 生成 Service Layer（业务逻辑层：5个业务方法）
- ✅ 支持软删除/硬删除自动判断
- ✅ 遵循项目代码规范和最佳实践
- ✅ 包含安全特性（输入验证、数据脱敏）
- ✅ 中文文档字符串和注释

## 技能项目结构

```
sql-to-fastapi-scaffold/
├── resources/                          # 技能资源目录
│   ├── config/                         # 配置文件
│   │   ├── naming_rules.json          # 命名规则配置
│   │   └── type_mappings.json         # SQL类型映射配置
│   ├── specifications/                 # 规范文档
│   │   └── coding_standards.md        # 代码规范标准
│   └── templates/                      # 代码模板
│       ├── layers/                    # 分层模板
│       │   ├── model/                 # 数据模型模板
│       │   ├── resource/             # API路由模板
│       │   ├── schema/                # Pydantic模式模板
│       │   └── service/               # 服务层模板
│       └── project_structure/         # 项目结构模板
│           ├── app/                   # 应用核心
│           ├── config/                # 配置模块
│           ├── core/                  # 核心模块
│           ├── models/                # 数据模型
│           ├── schemas/               # 数据验证模型
│           ├── service/              # 业务逻辑层
│           ├── api/                   # API路由
│           └── utils/                 # 工具函数
├── README.md                          # 技能说明文档
└── SKILL.md                          # 技能元数据配置
```

## 使用方法

### 1 配置技能到目标开发IDE中
- 如果你使用的是Trea IDE，你可以直接在IDE中配置技能环境。
- 操作文档请参考
[Trea IDE 配置技能](../../docs/Trea中使用skill配置.md)

- 如果你使用的是VS Code，你可以通过扩展来配置技能环境。
- 操作文档请参考
[VS Code 配置技能](../../docs/VSCode中使用skill配置.md)

- 如果你使用的是claude code ，你可以通过扩展来配置技能环境。
- 操作文档请参考
[claude code 配置技能](../../docs/claude中使用skill配置.md)



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

向ai开发工具进行对话: 
例如：
```
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

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── factory.py
│   ├── events.py
│   ├── exceptions.py
│   ├── middleware.py
│   └── router.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── database.py
│   └── dependencies.py
├── models/
│   ├── __init__.py
│   └── student.py
├── schemas/
│   ├── __init__.py
│   ├── response.py
│   └── student.py
├── service/
│   ├── __init__.py
│   └── student_service.py
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       └── students/
│           └── studentsResource.py
├── utils/
│   ├── __init__.py
│   ├── loguru.py
│   └── custom_exceptions.py
├── start.py
├── requirements.txt
└── .env.example
```

后续添加新表时，仅生成新增表的 4 个文件：

1. **models/{table_name}.py** - SQLAlchemy 数据模型
2. **schemas/{table_name}.py** - Pydantic 验证模型（Base、Create、Update、Response）
3. **api/v1/{resource_plural}/{resource_plural}Resource.py** - FastAPI 路由（5个CRUD端点）
4. **service/{table_name}_service.py** - 服务层（5个业务方法）

**路由结构**：
- `api/__init__.py` → `api_router` (prefix="/api")
- `api/v1/__init__.py` → `v1_router` (prefix="/v1")
- 子路由不额外加前缀，由具体API文件定义

**中间件结构**：
- `app/middleware.py` 直接注册中间件
- `middleware/` 目录保留，用于后续扩展中间件实现

**不生成的文件**（根据用户要求）：
- 测试代码
- 部署相关配置（Docker、Nginx等）
- 数据库初始化脚本
- 监控和日志系统

## 特性说明

### 软删除/硬删除

技能会自动检测表中是否有软删除字段（支持以下字段名）：
- `is_deleted`
- `is_delete`
- `deleted`

**软删除逻辑**（有软删除字段时）：
- `get_list()` - 只查询未删除的记录
- `get_detail()` - 只查询未删除的记录
- `update()` - 只更新未删除的记录
- `delete()` - 设置软删除字段为 True

**硬删除逻辑**（无软删除字段时）：
- `get_list()` - 查询所有记录
- `get_detail()` - 查询所有记录
- `update()` - 更新所有记录
- `delete()` - 直接从数据库删除记录

### 依赖注入

使用简洁的函数注入方式，在 `core/dependencies.py` 中生成独立的 `get_{service_name}` 函数，然后在 Resource 层使用：

```python
from core.dependencies import get_student_service

def get_student_list(
    ...,
    service: StudentService = Depends(get_student_service)
):
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

## 项目启动

生成完成后，按以下步骤启动项目：

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等
```

3. 启动应用：
```bash
uvicorn start:app --reload
```

4. 访问 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
