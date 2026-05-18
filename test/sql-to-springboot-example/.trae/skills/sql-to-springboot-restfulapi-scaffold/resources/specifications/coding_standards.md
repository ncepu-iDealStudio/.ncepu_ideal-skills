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
