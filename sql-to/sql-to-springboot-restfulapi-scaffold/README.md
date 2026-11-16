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
- ✅ 生成可直接照做的项目 README：JDK/Maven 安装步骤、Maven 阿里云镜像配置、环境自检、完整 Swagger 访问地址（含 context-path）、接口请求响应示例
- ✅ **已有项目新增表**：按表补齐 6 个分层文件，检查包路径与 `@RequestMapping` 不冲突（Spring 组件扫描，无需中央注册）
- ✅ **已有项目表结构修改**：字段级差异分析（加列/删列/改类型/改主键/软删字段/外键变化），分层重生成 + 手写文件最小合并
- ✅ **编译级同步保障**：`Request/Response DTO` 变化时同步 `Service` 的 setter 与 `mapToResponse()` 全参构造，避免 `mvn clean install` 失败
- ✅ **骨架与手写代码保护**：`pom.xml`、`application.properties`（`ddl-auto=none`）、`config/`、`security/` 一律不覆盖；输出 DDL 建议与验证清单
- ⛔ 按既定要求**不生成测试代码**、**不执行 DDL**（增量场景同样遵守）

## 技能项目结构

```
sql-to-springboot-restfulapi-scaffold/
├── resources/                          # 技能资源目录
│   ├── config/                         # 配置文件
│   │   ├── naming_rules.json           # 命名规则配置
│   │   ├── type_mappings.json          # SQL类型映射配置
│   │   └── incremental_change_policy.json # 增量模式/差异影响面/最小合并/DDL边界
│   ├── specifications/                 # 规范文档
│   │   ├── coding_standards.md         # 代码规范标准
│   │   └── incremental_update.md       # 已有项目增量更新流程
│   ├── tools/
│   │   └── check_skill_consistency.py  # 技能自洽校验（不渲染项目）
│   └── templates/                      # 代码模板
│       ├── layers/                     # 按表生成的分层模板
│       │   ├── entity/
│       │   ├── repository/
│       │   ├── service/
│       │   ├── controller/
│       │   └── dto/
│       │       ├── request/
│       │       └── response/
│       └── project_structure/          # 首次生成的项目骨架
│           ├── pom.xml
│           └── src/main/
│               ├── resources/
│               │   └── application.properties
│               └── java/com/security/apisecurity/
│                   ├── ApiSecurityApplication.java
│                   ├── config/         # SecurityConfig、CorsConfig
│                   ├── dto/response/   # ApiResponse
│                   ├── exception/
│                   ├── security/       # JWT 相关类
│                   └── service/        # UserDetailsServiceImpl
├── README.md                           # 技能说明文档
└── SKILL.md                            # 技能元数据配置
```

## 使用方法

### 1 配置技能到目标开发IDE中
- 如果你使用的是Trea IDE，你可以直接在IDE中配置技能环境。
- 操作文档请参考
[Trea IDE 配置技能](../docs/Trea中使用skill配置.md)

- 如果你使用的是claude code ，你可以通过扩展来配置技能环境。
- 操作文档请参考
[claude code 配置技能](../docs/claude中使用skill配置.md)

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

骨架来自 `resources/templates/project_structure/`。`entity/`、`repository/`、`controller/` 以及按表命名的 DTO / Service 在生成具体表时才出现。以 `student` 表为例，完整目录如下：

```
springboot_project/
├── pom.xml
├── src/main/resources/
│   └── application.properties
└── src/main/java/com/security/apisecurity/
    ├── ApiSecurityApplication.java
    ├── config/
    │   ├── SecurityConfig.java
    │   └── CorsConfig.java
    ├── exception/
    │   ├── GlobalExceptionHandler.java
    │   ├── ResourceNotFoundException.java
    │   ├── BadRequestException.java
    │   └── AccessDeniedException.java
    ├── security/
    │   ├── AuthEntryPointJwt.java
    │   ├── AuthTokenFilter.java
    │   └── JwtUtils.java
    ├── dto/
    │   ├── request/
    │   │   └── StudentRequest.java          # 按表生成
    │   └── response/
    │       ├── ApiResponse.java
    │       └── StudentResponse.java         # 按表生成
    ├── entity/
    │   └── Student.java                     # 按表生成
    ├── repository/
    │   └── StudentRepository.java           # 按表生成
    ├── service/
    │   ├── UserDetailsServiceImpl.java
    │   └── StudentService.java              # 按表生成
    └── controller/
        └── StudentController.java           # 按表生成
```

后续添加新表时，仅生成新增表的 6 个文件：

1. **entity/{TableName}.java** - JPA 数据模型
2. **repository/{TableName}Repository.java** - Spring Data JPA 接口
3. **dto/request/{TableName}Request.java** - 请求验证模型
4. **dto/response/{TableName}Response.java** - 响应模型
5. **service/{TableName}Service.java** - 服务层（业务逻辑）
6. **controller/{TableName}Controller.java** - REST 控制器（5 个 CRUD 端点）

新增表**无需中央路由注册**：Spring 组件扫描 + `@RestController` 自动发现。只需确认 6 个文件在 `com.security.apisecurity` 子包内、`@RequestMapping` 用复数资源名且不冲突，并在 `README.md` 追加接口章节。生成前按类名去重，同一 SQL 连跑两次零 diff。

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

## 已有项目的增量更新

技能不只用于"从零建项目"。目标项目已有骨架时，**先逐表判定运行模式**（`resources/config/incremental_change_policy.json`），执行流程见 `resources/specifications/incremental_update.md`。

| 你说的 | 模式 | 技能做什么 |
|--------|------|-----------|
| 「把这张新表加到现有项目」 | `add_table` | 生成 6 个分层文件 + 检查包路径与复数路由 + README 追加接口章节 |
| 「这张表加了几个字段 / 改了类型 / 改了软删字段」 | `alter_table` | 旧/新结构字段级差异 → 分层重生成 + 手写文件最小合并 → DDL 建议 |
| 「这张表要下线」 | `drop_table` | 只输出待删清单，不自动删文件、不执行 DDL |
| 空项目 | `greenfield` | 生成完整骨架 + 全部表 |

### 用法示例

**新增表**：把新的 `CREATE TABLE` 贴给技能，说明"加到已有项目"即可。

**表结构修改**（推荐同时给旧版 DDL，减少歧义）：

```text
现有项目里 student 表结构变了，请同步各层代码。
旧：CREATE TABLE student (student_id VARCHAR(20) PRIMARY KEY, name VARCHAR(100) NOT NULL, ...);
新：CREATE TABLE student (student_id VARCHAR(20) PRIMARY KEY, name VARCHAR(100) NOT NULL,
                         email VARCHAR(120), ...);
```

技能先给出差异清单，确认高风险项后：

- **整文件重生成**：`entity/`、`repository/`、`dto/request/`、`dto/response/`（4 个 `【AUTO-GENERATED】` 层）
- **最小合并**（展示片段 → 用户确认）：`service/{X}Service.java` 的 `create()/update()` setter 与 `mapToResponse()` 全参构造；主键/路由变化时 `controller/{X}Controller.java` 的 `@PathVariable` 类型
- **完全不碰**：`pom.xml`、`application.properties`（含真实 DB 账号、`ddl-auto=none`）、`config/`、`security/`、`exception/`、`ApiResponse.java`、`UserDetailsServiceImpl.java`
- **README**：只更新接口/字段章节，保留强制 11 章节结构

### 三个 Spring 特有的坑

1. **DTO ↔ Service 编译级耦合**：`mapToResponse()` 用 `new XxxResponse(...)` 全参构造（Lombok `@AllArgsConstructor`），Response 加字段而 Service 不补参数 → `mvn clean install` 直接失败。所以 Service 既不能整文件覆盖，也不能跳过。
2. **软删字段 ↔ Repository 派生查询名**：`findBy...AndIsDeleteFalse` 由字段名拼出，字段增删/改名不重生成 Repository → 启动期 `No property ... found`。
3. **主键三处类型一致**：`JpaRepository<Entity, PKType>`、`Service.findEntityById(PKType)`、`Controller @PathVariable PKType`。

> `status` / `state` / `version` / 时间戳属 `exclude_from_request`，不进 Request DTO；本技能只有 5 个 CRUD 端点，**不生成** `PATCH /{id}/status`，需要时列为人工待办。

### DDL 与测试边界

技能**不执行 DDL**、不连库、**不改 `application.properties`**（尤其不得把 `ddl-auto=none` 改成 `update`）、不接 Flyway/Liquibase、不删数据。只给 MySQL `ddl_hint` 建议与发布顺序：加列先 DDL 后发代码；删列先发代码后 DDL。

技能按既定要求**不生成测试代码**，增量也不生成；只输出验证清单：

```bash
mvn clean install        # 编译期捕获 DTO/Service 映射错误
mvn test                 # 仅当项目已有测试时
mvn spring-boot:run      # 启动期捕获 Repository 派生查询与外键关联错误
# Swagger: http://localhost:{port}{contextPath}/swagger-ui.html
```

再做 `POST → GET 列表 → GET /{id} → PUT → DELETE` 冒烟，最后同一 SQL 重跑确认零 diff。

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
