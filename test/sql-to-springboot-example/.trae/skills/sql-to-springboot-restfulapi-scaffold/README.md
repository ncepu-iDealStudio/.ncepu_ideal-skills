# SQL-to-SpringBoot-Scaffold

## 概述

`sql-to-springboot-scaffold` 是一个基于资源驱动的技能，用于从 SQL 表结构语句自动生成完整的 Spring Boot RESTful API 项目脚手架代码。

## 功能特性

- ✅ 解析 SQL CREATE TABLE 语句
- ✅ 生成 JPA Entity（数据模型，支持外键关系）
- ✅ 生成 Spring Data JPA Repository（数据访问层）
- ✅ 生成 Request/Response DTO（数据传输对象）
- ✅ 生成 Service Layer（业务逻辑层：CRUD 操作）
- ✅ 生成 Controller Layer（REST 控制器：5 个 CRUD 端点）
- ✅ 支持软删除/硬删除自动判断
- ✅ 遵循项目代码规范和最佳实践
- ✅ 包含安全特性（JWT 认证、权限控制）
- ✅ 中文文档字符串和注释

## 技能项目结构

```
sql-to-springboot-restfulapi-scaffold/
├── resources/                          # 技能资源目录
│   ├── config/                         # 配置文件
│   │   ├── naming_rules.json          # 命名规则配置
│   │   └── type_mappings.json         # SQL类型映射配置
│   ├── specifications/                 # 规范文档
│   │   └── coding_standards.md        # 代码规范标准
│   └── templates/                      # 代码模板
│       ├── layers/                    # 分层模板
│       │   ├── entity/                 # 数据模型模板
│       │   ├── repository/            # 数据访问模板
│       │   ├── service/                # 服务层模板
│       │   ├── controller/             # 控制器模板
│       │   └── dto/                    # DTO模板
│       └── project_structure/         # 项目结构模板
│           ├── pom.xml
│           ├── src/main/java/com/security/apisecurity/
│           │   ├── config/
│           │   ├── controller/
│           │   ├── dto/
│           │   ├── entity/
│           │   ├── exception/
│           │   ├── repository/
│           │   ├── security/
│           │   └── service/
│           └── src/main/resources/
│               └── application.properties
├── README.md                          # 技能说明文档
└── SKILL.md                          # 技能元数据配置
```

## 使用方法

### 1. 配置技能到目标开发IDE中

如果你使用的是 Trea IDE，你可以直接在 IDE 中配置技能环境。

### 2. 准备SQL语句

向技能提供 SQL CREATE TABLE 语句，例如：

```sql
CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    user_id VARCHAR(22) COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    phone_number VARCHAR(20) COMMENT '电话号码',
    age INT COMMENT '年龄',
    gender VARCHAR(10) COMMENT '性别',
    is_delete BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES sso_user(user_id)
);
```

### 3. 请求技能生成代码

向 AI 开发工具进行对话：

```
请根据以下 SQL CREATE TABLE 语句，生成对应的 Spring Boot 项目脚手架代码：
CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    user_id VARCHAR(22) COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    phone_number VARCHAR(20) COMMENT '电话号码',
    age INT COMMENT '年龄',
    gender VARCHAR(10) COMMENT '性别',
    is_delete BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES sso_user(user_id)
);
```

## 生成的目标项目代码结构

首次运行时，技能将生成完整的项目结构：

```
springboot_project/
├── pom.xml
├── src/main/resources/
│   └── application.properties
└── src/main/java/com/security/apisecurity/
    ├── ApiSecurityApplication.java
    ├── config/
    │   ├── SecurityConfig.java
    │   └── WebConfig.java
    ├── exception/
    │   ├── GlobalExceptionHandler.java
    │   ├── ResourceNotFoundException.java
    │   ├── BadRequestException.java
    │   └── AccessDeniedException.java
    ├── dto/
    │   └── response/
    │       └── ApiResponse.java
    ├── security/
    │   ├── AuthEntryPointJwt.java
    │   ├── AuthTokenFilter.java
    │   └── JwtUtils.java
    ├── service/
    │   └── UserDetailsServiceImpl.java
    ├── entity/
    │   └── Student.java
    ├── repository/
    │   └── StudentRepository.java
    ├── dto/
    │   ├── request/
    │   │   └── StudentRequest.java
    │   └── response/
    │       └── StudentResponse.java
    ├── service/
    │   └── StudentService.java
    └── controller/
        └── StudentController.java
```

后续添加新表时，仅生成新增表的 6 个文件：

1. **entity/{TableName}.java** - JPA 数据模型
2. **repository/{TableName}Repository.java** - Spring Data JPA 接口
3. **dto/request/{TableName}Request.java** - 请求验证模型
4. **dto/response/{TableName}Response.java** - 响应模型
5. **service/{TableName}Service.java** - 服务层（业务逻辑）
6. **controller/{TableName}Controller.java** - REST 控制器（5 个 CRUD 端点）

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
- `isDelete`

**软删除逻辑**（有软删除字段时）：
- `getList()` - 只查询未删除的记录
- `getById()` - 只查询未删除的记录
- `update()` - 只更新未删除的记录
- `delete()` - 设置软删除字段为 true

**硬删除逻辑**（无软删除字段时）：
- `getList()` - 查询所有记录
- `getById()` - 查询所有记录
- `update()` - 更新所有记录
- `delete()` - 直接从数据库删除记录

### 输入验证

自动为以下字段生成验证注解：
- 手机号（字段名包含 `phone`）：中国手机号格式验证
- 邮箱（字段名包含 `email`）：邮箱格式验证
- 年龄（字段名为 `age`）：0-150 范围验证
- 性别（字段名包含 `gender` 或 `sex`）：枚举值验证

### 权限控制

Controller 层使用 `@PreAuthorize` 注解控制访问权限：
- `POST /` - 需要 ADMIN 或 USER 角色
- `GET /{id}` - 需要 ADMIN 或 USER 角色
- `GET /` - 需要 ADMIN 或 USER 角色
- `PUT /{id}` - 需要 ADMIN 或 USER 角色
- `DELETE /{id}` - 需要 ADMIN 角色

## 项目启动

生成完成后，按以下步骤启动项目：

1. 安装依赖：
```bash
mvn clean install
```

2. 配置数据库连接：
编辑 `src/main/resources/application.properties` 文件，配置 MySQL 数据库连接。

3. 启动应用：
```bash
mvn spring-boot:run
```

4. 访问 API 文档：
- Swagger UI: http://localhost:8080/api/v1/swagger-ui.html
- API Docs: http://localhost:8080/api/v1/api-docs
