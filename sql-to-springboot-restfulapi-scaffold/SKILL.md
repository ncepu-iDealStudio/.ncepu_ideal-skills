---
name: "sql-to-springboot-scaffold"
description: "从SQL CREATE TABLE语句生成完整的Spring Boot RESTful API项目脚手架，包含Entity、Repository、Service、Controller层。调用时用户提供SQL表结构，或要求搭建API/生成代码。"
---

# SQL-to-SpringBoot-Scaffold Skill

## 概述

`sql-to-springboot-scaffold` 是一个基于资源驱动的技能，用于从SQL表结构语句自动生成完整的 Spring Boot 项目脚手架代码。该技能不依赖脚本，而是通过资源文件（模板、配置等）驱动大模型生成代码。

## 什么时候使用此技能

使用此技能的场景：
- 用户提供 SQL CREATE TABLE 语句
- 用户要求从数据库表生成 Spring Boot 接口代码，符合RESTful 风格
- 用户要求搭建 API 或创建 API 端点
- 用户提到 "SQL 转 SpringBoot"、"表到API"、"生成脚手架" 等类似表述

## 核心设计原则

### 资源驱动架构

本技能不使用脚本，而是通过以下资源文件驱动代码生成：

```
resources/
├── templates/              # 代码模板
│   ├── project_structure/   # 首次生成的项目骨架（不含按表代码）
│   │   ├── pom.xml
│   │   └── src/main/
│   │       ├── resources/application.properties
│   │       └── java/com/security/apisecurity/
│   │           ├── ApiSecurityApplication.java
│   │           ├── config/          # SecurityConfig、CorsConfig
│   │           ├── dto/response/    # ApiResponse
│   │           ├── exception/
│   │           ├── security/        # JWT 相关类
│   │           └── service/         # UserDetailsServiceImpl
│   └── layers/             # 按表生成的分层模板
│       ├── entity/
│       ├── repository/
│       ├── service/
│       ├── controller/
│       └── dto/
│           ├── request/
│           └── response/
├── config/                 # 配置文件
│   ├── type_mappings.json  # SQL类型到Java类型映射配置
│   └── naming_rules.json   # 命名规则配置
└── specifications/         # 规范文档
    └── coding_standards.md # 代码规范
```

### 生成范围

**首次生成时生成完整的项目骨架**：
- `pom.xml` - Maven配置（Spring Boot 3.2.0, JPA, Validation 等基础依赖）
- `src/main/resources/application.properties` - 应用配置
- `README.md` - 项目说明文档
- `src/main/java/com/security/apisecurity/ApiSecurityApplication.java` - 应用入口
- `src/main/java/com/security/apisecurity/exception/GlobalExceptionHandler.java` - 全局异常处理
- `src/main/java/com/security/apisecurity/exception/*Exception.java` - 自定义异常
- `src/main/java/com/security/apisecurity/dto/response/ApiResponse.java` - 统一响应模型
- `src/main/java/com/security/apisecurity/security/` - JWT安全相关类（代码生成但暂不启用）
- `src/main/java/com/security/apisecurity/config/SecurityConfig.java` - 安全配置（代码生成但暂不启用）
- `src/main/java/com/security/apisecurity/config/CorsConfig.java` - 跨域配置
- `src/main/java/com/security/apisecurity/service/UserDetailsServiceImpl.java` - 用户详情服务

**每个表生成的文件**：
1. Entity 层 - JPA实体类 (`entity/{TableName}.java`)
2. Repository 层 - Spring Data JPA接口 (`repository/{TableName}Repository.java`)
3. DTO 层 - 请求/响应模型
   - Request: `dto/request/{TableName}Request.java` - **只包含业务字段**
   - Response: `dto/response/{TableName}Response.java` - **包含所有展示字段**
4. Service 层 - 业务逻辑类 (`service/{TableName}Service.java`)
5. Controller 层 - REST控制器 (`controller/{TableName}Controller.java`)

## DTO 设计规范（重要）

### Request DTO（请求数据传输对象）

**包含字段**：用户需要提供的业务字段

**排除字段**（以下字段由数据库或后端自动管理，Request DTO中不应出现）：

| 字段类型 | 字段名模式 | 说明 |
|---------|-----------|------|
| 主键字段 | id, auto_id, autoId, uuid, uuid_id, uuidId | 数据库自动生成 |
| 创建时间 | create_time, createTime, created_at, createdAt | 后端自动填充 |
| 更新时间 | update_time, updateTime, updated_at, updatedAt | 后端自动填充 |
| 软删除字段 | is_deleted, is_delete, deleted, isDelete | 后端自动管理 |
| 状态字段 | status, state | 后端自动管理 |
| 版本号 | version | 后端自动管理 |
| 创建人/修改人 | creator, modifier, create_by, update_by | 后端自动填充 |

### Response DTO（响应数据传输对象）

**包含字段**：所有需要展示给用户的业务字段

**排除字段**：
- 敏感字段：password, pwd, passwd, token, secret 等

### 软删除机制

**软删除字段识别**：当表中存在以下字段时，删除操作使用软删除：
- is_deleted, is_delete, deleted, isDelete
- is_enabled, isEnable, enabled

**软删除实现**：
- 删除时设置软删除字段为 `true`，而非物理删除
- 查询时自动过滤已软删除的记录（`is_delete = false`）

### 外键约束检查

**创建/更新时**：检查外键关联是否存在，如关联的记录不存在则抛出异常

## 使用流程

### 步骤 1: 解析用户输入

当用户提供 SQL 语句时，首先解析：
- 表名（用于文件命名和类名）
- 字段定义（字段名、类型、约束、注释）
- 主键信息
- 外键关系
- 表注释

### 步骤 2: 识别自动管理字段

根据 `exclude_from_request` 配置识别以下字段，不放入 Request DTO：
- 主键字段
- 自动生成时间字段
- 软删除字段
- 状态字段
- 版本号字段
- 创建人/修改人字段

### 步骤 3: 检查项目是否存在

检查是否为首次生成：
- 如果项目骨架不存在，先生成完整的项目骨架
- 如果已有项目骨架，只生成新增表的5个文件

### 步骤 4: 生成代码

使用 `resources/templates/project_structure/` 下的模板生成项目骨架。
使用 `resources/templates/layers/` 下的模板生成各层代码。

### 步骤 5: 输出生成结果

以清晰的格式展示生成的文件列表和内容。

## 代码生成规范

### 命名约定

| 源 | 目标 | 示例 |
|-----|-------|------|
| 表名（snake_case） | 类名（PascalCase） | `student` → `Student` |
| 表名 | 文件名（PascalCase） | `student` → `Student.java` |
| 表名 | 资源路由名（复数） | `student` → `/students` |
| 字段名（snake_case） | Java属性名（camelCase） | `student_id` → `studentId` |

### 文件结构

**首次生成 - 完整项目骨架**：
```
springboot_project/
├── README.md                          # 项目说明文档
├── pom.xml
├── src/main/resources/
│   └── application.properties
└── src/main/java/com/security/apisecurity/
    ├── ApiSecurityApplication.java
    ├── config/
    │   └── SecurityConfig.java          # 安全配置（暂不启用）
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
    │   └── response/
    │       └── ApiResponse.java
    ├── service/
    │   └── UserDetailsServiceImpl.java
    ├── entity/
    │   └── {TableName}.java
    ├── repository/
    │   └── {TableName}Repository.java
    ├── dto/
    │   ├── request/
    │   │   └── {TableName}Request.java
    │   └── response/
    │       └── {TableName}Response.java
    ├── service/
    │   └── {TableName}Service.java
    └── controller/
        └── {TableName}Controller.java
```

## 各层代码详细说明

### Entity 层

**文件位置**：`entity/{TableName}.java`

**包含内容**：
- `@Entity` + `@Table` 注解
- 字段定义（含 JPA 注解、约束、注释）
- 外键关系（`@ManyToOne`/`@OneToOne`）
- Lombok `@Data` 注解

**模板资源位置**：`resources/templates/layers/entity/`

### Repository 层

**文件位置**：`repository/{TableName}Repository.java`

**包含内容**：
- 继承 `JpaRepository<{TableName}, {PKType}>`
- 软删除查询方法（`findByIsDeleteFalse` 等）
- 按外键查询方法

**模板资源位置**：`resources/templates/layers/repository/`

### DTO 层

**请求 DTO**：`dto/request/{TableName}Request.java`

**包含内容**：
- 业务字段（排除自动管理字段）
- `@NotBlank`、`@NotNull` 等验证注解
- Lombok `@Data` 注解

**响应 DTO**：`dto/response/{TableName}Response.java`

**包含内容**：
- 所有展示字段（排除敏感字段）
- Lombok `@Data`、`@NoArgsConstructor`、`@AllArgsConstructor` 注解

**模板资源位置**：`resources/templates/layers/dto/`

### Service 层

**文件位置**：`service/{TableName}Service.java`

**包含内容**：
- `@Service` + `@Transactional` 注解
- Lombok `@RequiredArgsConstructor`
- CRUD 业务方法
- 分页查询
- **软删除逻辑**（设置软删除字段为 true）
- **外键约束检查**（创建/更新时验证关联记录是否存在）

**模板资源位置**：`resources/templates/layers/service/`

### Controller 层

**文件位置**：`controller/{TableName}Controller.java`

**包含内容**：
- `@RestController` + `@RequestMapping`
- 5个REST端点：
  - `POST /` - 创建记录
  - `GET /` - 获取列表（分页）
  - `GET /{id}` - 获取详情
  - `PUT /{id}` - 更新记录
  - `DELETE /{id}` - 删除记录（软删除）
- Swagger 文档注解
- Lombok `@Slf4j`、`@RequiredArgsConstructor` 注解

**模板资源位置**：`resources/templates/layers/controller/`

## 类型映射规则

AI 应读取 `resources/config/type_mappings.json` 获取 SQL 类型到 Java/JPA 类型的完整映射规则。

## 字段分类规则

AI 应读取 `resources/config/type_mappings.json` 获取字段分类规则，包括：
- **exclude_from_request**：Request DTO 中排除的字段（如主键、时间戳、软删除字段等）
- **exclude_from_response**：Response DTO 中排除的字段（如密码等敏感字段）
- **soft_delete_fields**：软删除字段识别模式

## 约束处理

- `PRIMARY KEY` → `@Id`
- `NOT NULL` → `nullable=false`
- `DEFAULT` → `@PrePersist` 处理
- `COMMENT` → `@Column(comment="...")`
- `FOREIGN KEY` → `@ManyToOne`/`@OneToOne` + `@JoinColumn` + 外键检查
- `UNIQUE` → `unique=true`

## 软删除/硬删除

**识别条件**：检查表中是否存在软删除字段

**软删除实现**（有软删除字段时）：
- `getList()` - 使用 `findByIsDeleteFalse`
- `getById()` - 查询未删除记录
- `update()` - 更新未删除记录
- `delete()` - 设置软删除字段为 `true`

**硬删除实现**（无软删除字段时）：
- `delete()` - 直接删除记录

## 输出格式

生成完成后，向用户展示：

**首次生成时：**
```
✅ 已生成完整的 Spring Boot 项目脚手架

📁 生成的项目结构：
├── pom.xml
├── src/main/resources/application.properties
└── src/main/java/com/security/apisecurity/
    ├── ApiSecurityApplication.java
    ├── config/          # SecurityConfig.java、CorsConfig.java（安全配置暂不启用）
    ├── exception/
    ├── dto/response/    # ApiResponse.java
    ├── security/        # JWT 相关类（暂不启用）
    └── service/         # UserDetailsServiceImpl.java

按表生成后才会追加 entity/、repository/、controller/ 以及对应的 DTO、Service。

📝 重要说明：
- 安全配置已生成但暂不启用（pom.xml中依赖已注释）
- 删除操作默认使用软删除（设置 is_delete = true）
- Request DTO 不包含自动管理字段（id、时间戳、status等）
- Response DTO 不包含敏感字段（password等）

📝 下一步：
1. mvn clean install
2. 配置数据库连接
3. 运行 Application 主类
```

**生成 README.md**：在生成完所有文件后，AI 应读取生成的项目结构，动态生成一份详细的 README.md 文档，包含：
- 项目简介和技术栈
- 完整的项目结构说明
- 所有生成的 API 接口说明（包含请求/响应示例）
- 配置说明（从 application.properties 读取）
- 快速开始步骤
- DTO 设计说明
- 软删除机制说明
- 安全配置说明（暂未启用）

**后续添加新表时：**
```
✅ 已添加 {TableName} 的 CRUD 代码

📁 生成/更新的文件：
1. entity/{TableName}.java
2. repository/{TableName}Repository.java
3. dto/request/{TableName}Request.java  （不包含自动管理字段）
4. dto/response/{TableName}Response.java
5. service/{TableName}Service.java       （包含软删除逻辑、外键检查）
6. controller/{TableName}Controller.java

📝 软删除检测：{检测结果}
📝 下一步：重启应用即可使用新接口
```

## 错误处理

当 SQL 解析失败时，提供清晰的错误报告，包括：
- 错误类型
- 错误位置
- 错误原因
- 修复建议
- 正确示例

## 重要提示

1. **包名**：统一使用 `com.security.apisecurity`
2. **Spring Boot 版本**：3.2.0
3. **Java 版本**：17
4. **Lombok**：所有 DTO、Entity、Service、Controller 使用 Lombok 注解
5. **自动管理字段**：Request DTO 不包含 id、status、version、create_time 等自动管理字段
6. **软删除**：有软删除字段时删除操作使用软删除
7. **外键检查**：创建/更新时检查外键关联是否存在
8. **中文文档**：所有文档字符串、注释使用中文
9. **安全配置**：代码照常生成，但暂不启用（依赖注释状态）
