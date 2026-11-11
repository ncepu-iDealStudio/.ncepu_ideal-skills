# 代码规范标准

## 1. 命名规范

### 1.1 Java类和方法命名
- **类名**：使用 PascalCase（首字母大写）
  - 正确：`StudentService`, `UserController`
  - 错误：`studentService`, `user_controller`
- **方法名**：使用 camelCase（首字母小写）
  - 正确：`getStudentById`, `createUser`
  - 错误：`GetStudentById`, `create_user`
- **变量名**：使用 camelCase
  - 正确：`studentId`, `userName`
  - 错误：`student_id`, `user_name`

### 1.2 数据库命名
- **表名**：使用 snake_case（全部小写，下划线分隔）
  - 正确：`student`, `sys_class`
  - 错误：`Student`, `SysClass`
- **列名**：使用 snake_case 或根据数据库配置转换
  - 正确：`student_id`, `created_at`
  - 错误：`studentId`, `CreatedAt`

### 1.3 包命名
- 统一使用 `com.security.apisecurity`
- 分层包：`controller`, `service`, `repository`, `entity`, `dto`, `config`, `exception`, `security`

## 2. 代码结构规范

### 2.1 分层架构
```
controller/     # 控制层，处理HTTP请求
service/        # 服务层，业务逻辑
repository/     # 数据访问层，数据库操作
entity/         # 实体类，JPA实体
dto/            # 数据传输对象
config/         # 配置类
exception/      # 异常类
security/       # 安全相关类
```

### 2.2 Entity 规范
- 每个 Entity 必须有 `@Entity` 和 `@Table` 注解
- 主键使用 `@Id` 注解
- 字段使用 `@Column` 注解配置列名、约束等
- 外键关系使用 `@ManyToOne`、`@OneToOne` 等注解
- 必须有无参构造函数

### 2.3 Controller 规范
- 使用 `@RestController` 注解
- 使用 `@RequestMapping` 定义基础路径
- 使用 Swagger 注解提供 API 文档
- 方法参数使用 `@PathVariable`、`@RequestParam`、`@RequestBody`
- 使用 `@Valid` 启用参数校验

### 2.4 Service 规范
- 使用 `@Service` 注解
- 使用 `@Transactional` 注解开启事务
- 使用 `@Autowired` 注入依赖
- 业务方法返回 DTO/Response，不直接返回 Entity

### 2.5 Repository 规范
- 继承 `JpaRepository`
- 使用方法命名约定自动生成查询
- 复杂查询使用 `@Query` 注解

## 3. 安全规范

### 3.1 输入验证
- 所有用户输入必须经过验证
- 使用 `@NotNull`、`@NotBlank`、`@Size` 等注解
- 敏感字段使用 `@JsonIgnore` 避免序列化

### 3.2 SQL注入防护
- 使用参数化查询（Spring Data JPA 自动处理）
- 禁止使用字符串拼接构建 SQL

### 3.3 权限控制
- 使用 `@PreAuthorize` 注解控制访问权限
- 示例：`@PreAuthorize("hasRole('ADMIN')")`

## 4. 注释规范

### 4.1 类注释
```java
/**
 * {{类描述}}
 *
 * @author {{作者}}
 * @date {{日期}}
 */
```

### 4.2 方法注释
```java
/**
 * {{方法描述}}
 *
 * @param {{参数名}} {{参数描述}}
 * @return {{返回值描述}}
 */
```

## 5. 异常处理规范

### 5.1 自定义异常
- 使用业务异常而非系统异常
- 统一异常码和消息格式

### 5.2 全局异常处理
- 使用 `@RestControllerAdvice` 统一处理异常
- 返回统一的 `ApiResponse` 格式

## 6. 软删除规范

### 6.1 字段命名
支持以下软删除字段命名：
- `is_deleted`
- `is_delete`
- `deleted`
- `isDelete`

### 6.2 查询逻辑
- 查询时自动添加 `is_delete = false` 条件
- 删除时设置为 `true` 而非物理删除

## 7. API响应规范

### 7.1 统一响应格式
```json
{
  "success": true,
  "message": "操作成功",
  "data": {...},
  "timestamp": "2024-01-01T12:00:00"
}
```

### 7.2 分页响应
```json
{
  "success": true,
  "message": "查询成功",
  "data": {
    "content": [...],
    "totalElements": 100,
    "totalPages": 10,
    "size": 10,
    "number": 0
  }
}
```

## 8. 已有项目增量变更规范

策略源：`resources/config/incremental_change_policy.json`；执行流程：`resources/specifications/incremental_update.md`。凡目标项目已有骨架（`pom.xml` + `ApiSecurityApplication.java` + `application.properties`），本节优先。

### 8.1 文件头标记（增量保护依据）

| 文件 | 必须包含的标记 | 含义 |
|------|----------------|------|
| `entity/*.java`、`repository/*Repository.java`、`dto/request/*Request.java`、`dto/response/*Response.java` | `【AUTO-GENERATED】` | 允许技能按新 DDL 整文件重生成 |
| `service/*Service.java`、`controller/*Controller.java` | `【AUTO-GENERATED / 手写保护区】` + `手写业务代码区` 注释 | **绝不整文件覆盖**；仅在确认后做最小合并 |
| `pom.xml`、`application.properties`、`config/`、`security/`、`exception/`、`ApiResponse.java`、`UserDetailsServiceImpl.java`、`ApiSecurityApplication.java` | 基线，无标记 | 任何增量模式下都不覆盖 |
| `README.md` | 手写 | 只更新接口/字段章节，保留强制 11 章节结构 |

Java 文件用类注释承载标记，例如：

```java
/**
 * 【AUTO-GENERATED】由 sql-to-springboot-scaffold 生成；表结构变更时技能会重生成。
 * 若已手工修改，请改为 【HAND-WRITTEN】，技能将跳过覆盖并输出人工待办。
 */
```

文件存在但**没有**生成标记 → 视为用户已手改 → 禁止覆盖。

### 8.2 变更处理规则

- `add_table`：生成 6 个按表文件；**无中央路由注册**（组件扫描），确认包路径在 `ApiSecurityApplication` 扫描范围内、`@RequestMapping` 复数路径不冲突；README 只追加接口章节。生成前按类名去重，同一 SQL 连跑两次零 diff。
- `alter_table`：先取旧结构 → 归一化后字段级对比 → 输出差异清单 → 高风险项确认 → 按 `change_types` 分层更新。禁止把「重复提供 CREATE TABLE」当作新表覆盖。
- `drop_table` / 表重命名：阻断自动执行，只输出清单。

### 8.3 三条强制同步规则

1. **DTO ↔ Service 编译级耦合**：`Service.create()/update()` 用 setter 逐字段写入 Entity，`mapToResponse()` 以 `new {X}Response(...)` 全参构造（Lombok `@AllArgsConstructor`）组装响应。Request/Response 字段增删或改类型时，必须同步 Service，否则 `mvn clean install` 编译失败。Service 属手写保护区，须「展示片段 → 用户确认 → 最小合并」，禁止整文件覆盖，也不能跳过。
2. **软删字段 ↔ Repository 派生查询名**：`findBy{pk}And{SoftDeleteFieldFalse}` / `findBy{SoftDeleteField}` 由字段名拼出；软删列变化必须整体重生成 Repository 并同步 Service 的 `findEntityById/getList/delete`，否则启动期 `No property ... found`。
3. **主键 ↔ 三处类型**：`JpaRepository<Entity, {pkType}>` 第二泛型、`Service.findEntityById({pkType} id)`、`Controller @PathVariable {pkType} id` 必须一致。

> `status` / `state` / `version` / 时间戳 / 软删字段按 `type_mappings.json` 的 `exclude_from_request` 排除；本技能只有 5 个 CRUD 端点，不生成 `PATCH /{id}/status`，需要时列入人工待办。

### 8.4 迁移与验证边界

技能不执行 DDL、不连库、**不改 `application.properties`**（`spring.jpa.hibernate.ddl-auto=none` 不得改成 `update`/`create`）、不接 Flyway/Liquibase、不删数据；只输出 MySQL `ddl_hint` 与发布顺序（加列先 DDL 后发代码；删列先发代码后 DDL）。

按既定要求**不生成测试代码**。增量后验证：`mvn clean install` →（项目已有测试时）`mvn test` → `mvn spring-boot:run` → Swagger 核对 DTO Schema 与 5 个端点 → `POST/GET/PUT/DELETE` 冒烟 → 同一 SQL 重跑零 diff。变更报告须列出「已重生成 / 已最小合并 / 跳过与待办 / DDL 建议 / 验证结果」。
