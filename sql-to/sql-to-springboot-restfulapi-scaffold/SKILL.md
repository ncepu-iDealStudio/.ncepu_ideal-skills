---
name: "sql-to-springboot-scaffold"
description: "从SQL CREATE TABLE语句生成完整的Spring Boot RESTful API项目脚手架，包含Entity、Repository、Service、Controller、Request/Response DTO层。支持已有项目增量：按 incremental_change_policy.json 判定 greenfield/add_table/alter_table/drop_table，做字段级差异分析、分层重生成、DTO↔Service 编译级最小合并、骨架与手写代码保护、DDL建议与验证清单。按既定要求不生成测试代码、不执行DDL。"
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
- **已有项目中新增表**：在现有 Spring Boot 工程里按表补齐 6 个分层文件
- **已有项目中表结构修改**：新增/删除列、改类型或约束、改主键、软删字段与外键变化 → 走字段级差异分析
- 用户说「表加了几个字段」「同步一下新的 DDL」「把新表加进已有项目」等增量表述

## 核心设计原则

### 资源驱动架构

本技能不使用脚本，而是通过以下资源文件驱动代码生成：

```
resources/
├── templates/              # 代码模板
│   ├── project_structure/   # 首次生成的项目骨架（不含按表代码）
│   │   ├── pom.xml
│   │   ├── README.md        # 项目说明骨架（含环境准备、镜像源、Swagger 地址，按实际结果补全）
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
│   ├── naming_rules.json   # 命名规则配置
│   └── incremental_change_policy.json # 增量模式/差异影响面/最小合并/DDL边界
├── specifications/         # 规范文档
│   ├── coding_standards.md # 代码规范
│   └── incremental_update.md # 已有项目增量更新流程（新增表/表结构变更/表下线）
└── tools/
    └── check_skill_consistency.py # 技能自洽校验（含增量资源检查，不渲染项目）
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

> 共 **6 个按表文件**（第 3 项含 Request + Response 两个 DTO）。均位于 `src/main/java/com/security/apisecurity/` 下对应子包。
> 本技能按既定要求**不生成测试代码**；增量验证只给编译/启动/Swagger 冒烟清单。

**增量场景永不覆盖的骨架（BASELINE）**：`pom.xml`、`src/main/resources/application.properties`（含真实 DB 账号与 `spring.jpa.hibernate.ddl-auto=none`）、`ApiSecurityApplication.java`、`config/`、`security/`、`exception/`、`dto/response/ApiResponse.java`、`service/UserDetailsServiceImpl.java`。`README.md` 只增量更新接口/字段章节，保留强制 11 章节结构。

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
- **软删字段 / 自动管理字段 / 敏感字段**（按 `type_mappings.json` 重算，增量场景不沿用旧结论）
- **变更场景额外解析**：用户是否同时给出旧版 DDL / 是否声明「已有项目改动」；记录旧结构来源，供步骤 3.2 差异分析使用

### 步骤 2: 识别自动管理字段

根据 `exclude_from_request` 配置识别以下字段，不放入 Request DTO：
- 主键字段
- 自动生成时间字段
- 软删除字段
- 状态字段
- 版本号字段
- 创建人/修改人字段

### 步骤 3: 判定运行模式（强制，逐表）

**先读 `resources/config/incremental_change_policy.json` 与 `resources/specifications/incremental_update.md`**，按 `mode_detection` 逐表判定：

| 模式 | 判定 | 动作 |
|------|------|------|
| `greenfield` | 骨架（`pom.xml` + `ApiSecurityApplication.java` + `application.properties`）不存在 | 从 `project_structure/` 生成完整骨架 + 本次全部表 |
| `add_table` | 骨架存在，且该表 6 个按表文件全部不存在 | 生成 6 个文件（步骤 3.3 检查包路径与路由） |
| `alter_table` | 骨架存在，且该表任一按表文件已存在 | **先做字段级差异分析**（步骤 3.2），再按 `change_types` 分层更新 |
| `drop_table` | 用户明确要求下线表 | 只输出待删清单，**不自动删文件、不执行 DDL** |

- 一次给多张表时逐表判定，允许同批混用 `add_table` 与 `alter_table`。
- 残留文件不成套 → **先询问用户**补齐还是重生成，禁止默认覆盖。
- 「用户又给了一遍建表 SQL」≠ 重新建表：已有文件就必须走 `alter_table`。
- 骨架与基线文件（`pom.xml`、`application.properties`、`config/`、`security/` 等）在任何模式下都不覆盖。

### 步骤 3.1: 覆盖策略与文件归属（强制）

| 文件 | 头标记 | `alter_table` 动作 |
|------|--------|-------------------|
| `entity/{X}.java`、`repository/{X}Repository.java`、`dto/request/{X}Request.java`、`dto/response/{X}Response.java` | `【AUTO-GENERATED】` | 整文件重生成 |
| `service/{X}Service.java`、`controller/{X}Controller.java` | `【AUTO-GENERATED / 手写保护区】` | **绝不整文件覆盖** → 走步骤 3.2 最小合并协议 |
| `pom.xml`、`application.properties`、`config/`、`security/`、`exception/`、`ApiResponse.java`、`UserDetailsServiceImpl.java`、`ApiSecurityApplication.java` | BASELINE | **完全不碰**（尤其不得把 `ddl-auto=none` 改成 `update`） |
| `README.md` | 手写 | 只更新接口/字段章节，保留强制 11 章节结构 |

文件存在但**没有**生成标记 → 视为用户已手改，禁止覆盖 → 输出人工待办并询问。

### 步骤 3.2: 表结构变更的差异分析与分层更新（`alter_table` 强制）

完整流程见 `resources/specifications/incremental_update.md`，策略表见 `incremental_change_policy.json → change_types`。

1. **取旧结构**：依次尝试「用户旧版 CREATE TABLE / 建库 SQL」→ `entity/{X}.java` 的字段声明与 `@Column`/`@Id`/`@JoinColumn` → Request/Response DTO 交叉校验 →（仅用户同意时）`information_schema`。取不到就询问用户，**不要猜差异**。
2. **归一化后逐字段比对**：列名大小写/反引号、snake_case ↔ camelCase、类型别名、字段顺序差异忽略；软删字段、`exclude_from_request`、`exclude_from_response` 集合**按最新 SQL 依 `type_mappings.json` 重算**。
3. **先输出差异清单**（`added` / `removed` / `type_changed` / `constraint_changed` / `managed_flag_changed` / `comment_only` / 风险等级 / **是否破坏编译**）；`critical`+`high` 项先确认；`removed + added` 疑似重命名时先问清语义。
4. **分层更新**：重生成 4 个 `AUTO-GENERATED` 层 → 按最小合并协议更新 `Service`（字段变化时必须）与 `Controller`（主键/路由变化时）→ 骨架不碰 → README 只更新接口/字段章节。
5. **🔴 三条 Spring 特有强制同步规则**（漏一条就编译失败或应用起不来）：
   - **DTO ↔ Service 编译级耦合**：`Service.create()/update()` 用 setter 逐字段写入，`mapToResponse()` 用 `new {X}Response(...)` 全参构造（Lombok `@AllArgsConstructor`）。**任何 Request/Response 字段增删或改类型，不同步 Service 会直接 `mvn clean install` 编译失败**。Service 既不能整文件覆盖，也不能简单跳过。
   - **软删字段 ↔ Repository 派生查询方法名**：`findBy...And{SoftDeleteFieldFalse}` 由字段名拼出，字段增删/改名后不整体重生成 Repository，Spring Data JPA 启动即抛 `No property ... found`；Service 的 `findEntityById/getList/delete` 同步。
   - **主键 ↔ 三处类型**：`JpaRepository<Entity, {pkType}>` 第二泛型、`Service.findEntityById({pkType} id)`、`Controller @PathVariable {pkType} id` 必须一致。
6. **状态字段按本技能约定处理**：`status` / `state` / `version` / 时间戳 / 软删字段属 `exclude_from_request`，不进 Request DTO；本技能只有 5 个 CRUD 端点，**不生成** `PATCH /{id}/status`。业务需要改状态接口时只写进人工待办，不擅自新增端点。

**最小合并协议**（`Service` / `Controller`）：展示将改动的具体方法片段（`create()`/`update()` setter 列表、`mapToResponse()` 构造参数、`@PathVariable` 类型）→ **取得用户确认**（不确认则明确提示「项目将无法编译」并列入待办）→ 只做最小编辑 → 禁止改动「手写业务代码区」的自定义方法与 `@PreAuthorize` → 报告记录已合并的方法名。

### 步骤 3.3: 新增表检查与幂等（`add_table` 强制）

Spring 靠组件扫描 + `@RestController` 自动发现，**没有中央路由注册文件**，无需追加注册。但要检查：

1. 6 个文件落在 `com.security.apisecurity` 子包内，处于 `ApiSecurityApplication` 扫描范围；
2. `@RequestMapping("/{resourcePath}")` 用复数资源名（按 `naming_rules.json`），与已有 Controller 不冲突；
3. 只在 `README.md` 追加该表接口章节，不重写整份 README。

**幂等**：生成前按类名全文检索，同名 Entity/Repository/Service/Controller/DTO 已存在则不重复创建；**同一 SQL 连跑两次必须零 diff**。`alter_table` 默认不动 `@RequestMapping` 与包路径。

### 步骤 3.4: 增量后的验证（强制，不生成测试代码）

```bash
mvn clean install        # 编译期捕获 Response 全参构造参数不匹配 / setter 缺失 / 类型错误
mvn test                 # 仅当项目已有测试时执行
mvn spring-boot:run      # 启动期捕获 Repository 派生查询名与外键关联解析失败
# 打开 http://localhost:{port}{contextPath}/swagger-ui.html 核对 DTO Schema 与 5 个端点
```

变化字段做最小冒烟：`POST` → `GET` 列表 → `GET /{id}` → `PUT` → `DELETE`；确认 `ddl-auto` 仍为 `none`、DB 账号未被覆盖；最后重跑同一 SQL 确认零 diff。

**DDL 边界**：技能不执行任何 DDL、不连库、不改 `application.properties`、不接 Flyway/Liquibase、不删数据；只在报告中给 MySQL `ddl_hint` 与发布顺序（加列先 DDL 后发代码；删列先发代码后 DDL）、备份与回滚提示。

### 步骤 4: 生成代码

使用 `resources/templates/project_structure/` 下的模板生成项目骨架（**仅 `greenfield`**；增量场景骨架已存在则跳过）。
使用 `resources/templates/layers/` 下的模板生成各层代码；按步骤 3.1 的覆盖策略决定是重生成、最小合并还是跳过。

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

**后续生成 - `add_table`（新增表）**：
- 只生成该表的 6 个文件，落 `com.security.apisecurity` 对应子包；**无中央注册文件**，靠组件扫描自动发现
- 检查 `@RequestMapping` 复数路径不冲突；`README.md` 追加接口章节
- 不覆盖 `pom.xml`、`application.properties`、`config/`、`security/`、`exception/` 等骨架
- 不生成测试代码

**后续生成 - `alter_table`（表结构修改，见步骤 3.2）**：
- 先输出旧/新字段级差异清单，高风险项先确认
- 整文件重生成：`entity/{X}.java`、`repository/{X}Repository.java`、`dto/request/{X}Request.java`、`dto/response/{X}Response.java`
- 最小合并（经确认）：`service/{X}Service.java` 的 `create/update/mapToResponse`；主键或路由变化时 `controller/{X}Controller.java`
- 只更新 README 接口/字段章节；骨架完全不碰
- 输出 DDL 建议与人工待办清单；仍不生成测试代码

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

**生成 README.md**：在生成完所有文件后，AI 必须以 `resources/templates/project_structure/README.md` 为骨架，读取实际生成结果后动态补全，生成一份**让初学者可以照着一步步跑起来**的 README.md。

要求：
- 占位符（`{{projectName}}`、`{{port}}`、`{{contextPath}}`、`{{tableName}}`、`{{resourcePath}}`、`{{databaseName}}` 等）必须替换为真实值，禁止保留或照抄；
- 所有接口地址必须写成完整 URL：`http://localhost:{port}{contextPath}/{resourcePath}`，不能只写 `/students`；
- 环境相关命令必须区分 Windows（PowerShell）与 macOS/Linux，并给出验证命令。

README 必须包含以下 11 个章节（缺一不可）：

| 顺序 | 章节 | 必须写清楚的内容 |
| --- | --- | --- |
| 1 | 项目简介与技术栈 | Spring Boot 3.2.0、JDK 17、Maven、JPA、springdoc 版本、包名 |
| 2 | **环境准备（首次运行必读）** | JDK 17 安装步骤（Windows/macOS/Linux）、Maven 3.8+ 安装步骤、`JAVA_HOME`/`M2_HOME`/`Path` 配置、`java -version` 与 `mvn -v` 验证 |
| 3 | **Maven 镜像源配置** | settings.xml 路径（`%USERPROFILE%\.m2\settings.xml` 或 `${MAVEN_HOME}/conf/settings.xml`）、阿里云 mirror 完整 XML、`mvn help:effective-settings` 验证、内网私服提示 |
| 4 | 环境自检清单 | `java -version`、`mvn -v`、`mysql --version` 三条可复制命令及期望输出 |
| 5 | 项目结构 | 按实际生成目录输出（含 `security-placeholder/` 等实际存在的目录） |
| 6 | 接口说明 | 每个端点的 方法 / 完整路径 / 说明 / 成功状态码，并给出请求体与响应示例 |
| 7 | **接口文档（Swagger）访问地址** | Swagger UI、`swagger-ui/index.html`、OpenAPI JSON、OpenAPI YAML 的**完整可点击 URL**；注明必须带 context-path、改端口/前缀要同步替换、404 排查项 |
| 8 | 配置说明 | 数据源、`ddl-auto`、Swagger 路径、CORS，从 `application.properties` 读取；提醒环境变量 `DB_USERNAME`/`DB_PASSWORD` |
| 9 | 快速开始 | 建库建表 → 编译 → 启动 → 打开 Swagger，命令可直接复制执行；附无 MySQL 时的 H2 方案 |
| 10 | DTO 设计说明 + 软删除机制 | Request 排除字段及原因、Response 排除敏感字段、软删除字段识别与查询过滤 |
| 11 | 安全配置说明 | 已生成但未启用、文件为何不在 `src/main/java`、启用步骤 |

> **增量场景**：`add_table` 时只**追加**新表接口章节；`alter_table` 时只**更新**受影响的字段与接口示例，禁止重写整份 README（用户可能已手写环境、镜像源与部署说明），11 章节结构必须保留。

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
📝 无中央路由注册（Spring 组件扫描）；已确认包路径与 @RequestMapping 复数路径不冲突
📝 未改动：pom.xml、application.properties（ddl-auto 仍为 none）、config/、security/、exception/
📝 下一步：
1. mvn clean install
2. mvn spring-boot:run 后打开 Swagger 核对 5 个端点
3. 重启应用即可使用新接口
```

**表结构变更时（alter_table）：**
```
运行模式：{TableName} = alter_table

【差异清单】
  [added]   {col}  {type}                        risk=medium  会破坏编译（Service 映射）
  [removed] {col}                                risk=high    会破坏编译
  [flag]    {status} 新增 → 排除出 Request，本技能不生成 PATCH /{id}/status

【已重生成（AUTO-GENERATED）】
  entity/、repository/、dto/request/、dto/response/ 四个层
【已最小合并到手写文件（经确认）】
  service/{TableName}Service.java → create()/update() setter、mapToResponse() 构造参数
【跳过 / 人工待办】
  - 如需状态变更接口请手工添加并同步 README
  - README.md 已更新接口/字段章节（11 章节结构保留）
  - 项目自带测试（若有）补 payload 与断言
  - 未改动骨架：pom.xml、application.properties、config/、security/
【DDL 建议（需人工确认执行，技能不执行 DDL）】
  ALTER TABLE {table} ADD COLUMN ...;   -- 加列：先 DDL 后发代码
【验证】
  mvn clean install / mvn spring-boot:run / Swagger 核对 / POST→GET→PUT→DELETE 冒烟 / 同 SQL 重跑零 diff
```

> 完整报告模板见 `resources/specifications/incremental_update.md` 第 10 节。

## 错误处理

当 SQL 解析失败时，提供清晰的错误报告，包括：
- 错误类型
- 错误位置
- 错误原因
- 修复建议
- 正确示例

## 增量相关必读资源

| 文件 | 作用 |
|------|------|
| `resources/config/incremental_change_policy.json` | 机器可读策略：4 种运行模式、旧结构来源优先级、字段差异维度、6 类按表文件的归属标记、17 类 `change_types` 的影响面与动作、最小合并协议、骨架保护、幂等、DDL 边界、验证与报告字段 |
| `resources/specifications/incremental_update.md` | 执行流程：差异识别、影响面矩阵、三条 Spring 特有同步规则、最小合并协议、新表检查清单、DDL 发布顺序、验证命令、变更报告模板 |
| `resources/tools/check_skill_consistency.py` | 技能目录自洽校验（含增量资源、模板标记、文档引用），**不渲染目标项目** |

`resources/specifications/coding_standards.md` 第 8 节给出文件头标记与手写保护区约定。

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
10. **README 环境准备**：必须写出 JDK 17、Maven 3.8+ 的安装与环境变量配置步骤，以及 Maven 镜像源（阿里云）配置，否则初学者无法跑起来
11. **README 接口文档地址**：必须给出完整可点击的 Swagger UI 与 OpenAPI 地址（含 `http://localhost:{port}{contextPath}` 前缀），并说明 context-path 与端口变化时的同步要求
12. **README 可执行性**：所有命令（编译、启动、建表）必须可直接复制执行，不能出现 `xxx`、`<你的路径>` 之外的模糊占位
13. **🔴 已有项目必须先判模式**：骨架存在时禁止按首次生成口径全量重写；逐表判 `greenfield` / `add_table` / `alter_table` / `drop_table`，规则见 `incremental_change_policy.json`
14. **🔴 表结构变更必须做差异分析**：先取旧结构 → 字段级对比 → 输出差异清单 → 高风险项确认 → 按 `change_types` 分层更新；**禁止**把「又给了一遍 CREATE TABLE」当成新表覆盖
15. **🔴 DTO ↔ Service 编译级耦合**：`create()/update()` 的 setter 与 `mapToResponse()` 的 `new {X}Response(...)` 全参构造必须随 DTO 字段变化同步，否则 `mvn clean install` 直接失败。Service 是手写保护区，须走「展示片段 → 用户确认 → 最小合并」，既不整文件覆盖也不跳过
16. **🔴 软删字段 / 主键变化**：Repository 派生查询方法名由软删字段名拼出，字段变化不重生成会导致启动期 `No property ... found`；主键变化须同步 `JpaRepository` 第二泛型、`Service.findEntityById`、`Controller @PathVariable` 三处类型
17. **🔴 骨架与手写代码保护**：`pom.xml`、`application.properties`（`ddl-auto=none` 不得改成 `update`）、`config/`、`security/`、`exception/`、`ApiResponse.java`、`UserDetailsServiceImpl.java` 一律不覆盖；Controller 自定义端点与 `@PreAuthorize` 必须保留
18. **🔴 边界**：Spring 无中央路由注册（组件扫描自动发现，检查包路径与复数 `@RequestMapping` 不冲突即可）；按既定要求**不生成测试代码**；技能**不执行 DDL**、不连库、不接 Flyway/Liquibase；`status` 不进 Request DTO、本技能**不生成** `PATCH /{id}/status`，需要时列为人工待办
