# 已有 Spring Boot 项目的增量更新规范（新增表 / 表结构变更 / 表下线）

本规范与 `resources/config/incremental_change_policy.json` 配套：后者是机器可读策略表，本文是执行流程。
**凡是目标项目已存在骨架（`pom.xml` + `ApiSecurityApplication.java` + `application.properties`），必须先走本文流程，禁止按首次生成口径全量重写。**

> 与 FastAPI 版技能的差异（勿照搬）：
> - Spring Boot 靠组件扫描 + `@RestController` 自动发现，**没有中央路由注册文件**，新表无需追加注册；
> - 本技能按用户既定要求**不生成测试代码**，增量也不生成，只给编译/冒烟验证清单；
> - 本技能只有 5 个 CRUD 端点，**不生成** `PATCH /{id}/status`；
> - `spring.jpa.hibernate.ddl-auto=none`，**DDL 一律人工执行**，技能不得改成 `update`。

---

## 1. 四种场景与判定

| 场景 | 判定条件 | 模式 |
|------|----------|------|
| 首次生成 | 项目骨架不存在 | `greenfield` → 从 `project_structure/` 生成完整骨架 + 全部表 |
| 已有项目 + 新表 | 骨架存在，且该表 6 个按表文件全部不存在 | `add_table` |
| 已有项目 + 表结构修改 | 骨架存在，且该表任一按表文件已存在 | `alter_table` |
| 已有项目 + 表下线 | 用户明确要求移除 | `drop_table`（只出清单，不自动删） |
| 残留文件不成套 | 例如只剩 Entity 与 Repository | **先询问用户**：补齐 or 重生成 |

6 个按表文件（均位于 `src/main/java/com/security/apisecurity/`）：

```text
entity/{ClassName}.java
repository/{ClassName}Repository.java
dto/request/{ClassName}Request.java
dto/response/{ClassName}Response.java
service/{ClassName}Service.java
controller/{ClassName}Controller.java
```

一次给多张表时**逐表独立判定**。判 `alter_table` 时，"用户又给了一次建表 SQL" 不等于"重新生成一张表"，必须做差异分析。

---

## 2. `alter_table`：差异识别（强制）

### 2.1 取得旧结构

优先级见 `incremental_change_policy.json → baseline_snapshot.source_priority`：

1. 用户提供的旧版 `CREATE TABLE` / 建库 SQL
2. `entity/{ClassName}.java` 的 `private` 字段声明与 `@Column(name=..., nullable=..., unique=...)` / `@Id` / `@JoinColumn`
3. `dto/request/{ClassName}Request.java`、`dto/response/{ClassName}Response.java` 字段（交叉校验）
4. 运行库 `information_schema`（**仅在用户明确同意连库时**）

取不到旧结构就**询问用户**，不要猜差异。

### 2.2 归一化后逐字段对比

按 `naming_rules.json` / `type_mappings.json` 归一：MySQL 列名大小写与反引号、snake_case ↔ camelCase、类型别名（`INT`/`INTEGER`、`BOOL`/`TINYINT(1)`、`DATETIME`/`TIMESTAMP`）、忽略字段顺序与格式。
`soft_delete_field`、`managed_field_set`（`exclude_from_request`）、`sensitive_field_set` 必须**用最新 SQL 依 `type_mappings.json` 重新计算**，不沿用旧结论。

### 2.3 输出差异清单（先给用户看，再动手）

```text
表 student：
  [added]     email       VARCHAR(120) NULL          risk=medium  会破坏编译（Service 映射）
  [removed]   age         INT                        risk=high    会破坏编译
  [flag]      新增 status  TINYINT                    risk=medium  → 进 exclude_from_request，不生成 PATCH
  [unchanged] 其余 8 列
```

`removed + added` 疑似重命名时，先问清是「重命名」还是「删旧列 + 加新列」。详细动作查 `change_types`。

---

## 3. 影响面矩阵（速查）

| 变更 | Entity | Repository | Request | Response | Service | Controller | README | DDL |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 新表 | 生成 | 生成 | 生成 | 生成 | 生成 | 生成 | 追加接口章节 | 建表 |
| 加列 | 覆盖 | — | 覆盖* | 覆盖* | **最小合并（必须）** | — | 更新 | `ADD COLUMN` |
| 删列 | 覆盖 | 视情况 | 覆盖 | 覆盖 | **最小合并（必须）** | 查自定义端点 | 更新 | `DROP COLUMN` |
| 改类型/约束 | 覆盖 | — | 覆盖 | 覆盖 | **最小合并（必须）** | — | 更新 | `MODIFY COLUMN` |
| 软删字段变化 | 覆盖 | **覆盖（派生查询名）** | 覆盖 | 覆盖 | **最小合并（必须）** | — | 更新软删章节 | 加/删列 |
| 主键变化 | 覆盖 | **覆盖（第二泛型）** | — | 覆盖 | **最小合并** | **最小合并 `@PathVariable`** | 更新 | 需人工确认 |
| 外键变化 | 覆盖 | 覆盖 | — | 覆盖 | **最小合并（校验/关联）** | — | 更新 | `ADD/DROP CONSTRAINT` |
| 仅注释 | 覆盖 | — | 覆盖 | 覆盖 | — | — | — | 可选 |
| 表重命名/下线 | — | — | — | — | — | — | — | **阻断自动执行** |

`*` 自动管理字段不进 Request DTO、敏感字段不进 Response DTO（按 `type_mappings.json`）。

---

## 4. 🔴 三条 Spring 特有的强制同步规则

### 4.1 DTO ↔ Service 是**编译级**耦合（最易翻车）

`ServiceTemplate.java` 里：

```java
// create() / update()：逐字段 setter，来自 Request DTO
entity.setEmail(request.getEmail());

// mapToResponse()：全参构造，来自 Response DTO（Lombok @AllArgsConstructor）
return new StudentResponse(
        entity.getStudentId(),
        entity.getName(),
        entity.getEmail()   // ← 新增列必须补在这里，且顺序与 Response DTO 一致
);
```

**任何 Request/Response 字段增删或改类型，不同步 Service 会直接 `mvn clean install` 编译失败**（构造器参数个数/类型不匹配、getter/setter 不存在）。
因此 Service 既不能整文件覆盖，也不能简单跳过，必须走第 5 节的「最小合并协议」。

### 4.2 软删字段 ↔ Repository 派生查询方法名

`RepositoryTemplate.java` 的方法名由字段名拼出：

```java
Optional<Student> findByIdAndIsDeleteFalse(String id, boolean isDelete);
Page<Student> findByIsDeleteFalse(boolean isDelete, Pageable pageable);
```

软删列增删/改名后若不整体重生成 Repository，Spring Data JPA 在**启动阶段**抛 `No property isDelete found for type Student`，应用起不来；`Service.findEntityById/getList/delete` 也必须同步。

### 4.3 主键 ↔ 泛型与路径参数三处一致

`JpaRepository<Entity, {pkType}>` 第二泛型、`Service.findEntityById({pkType} id)`、`Controller @PathVariable {pkType} id` 必须同时改，否则 CRUD 全线类型错配。

> 另：`status` / `state` / `version` / 时间戳 / 软删字段属于 `exclude_from_request`，**不进 Request DTO**；本技能只有 5 个 CRUD 端点，**不生成** `PATCH /{id}/status`。需要改状态接口时只写进人工待办，由用户自行添加，不要擅自新增端点。

---

## 5. 文件归属与最小合并协议

| 文件 | 头标记 | `alter_table` 动作 |
|------|--------|-------------------|
| `entity/*.java` | `【AUTO-GENERATED】` | 整文件重生成 |
| `repository/*Repository.java` | `【AUTO-GENERATED】` | 整文件重生成 |
| `dto/request/*Request.java` | `【AUTO-GENERATED】` | 整文件重生成 |
| `dto/response/*Response.java` | `【AUTO-GENERATED】` | 整文件重生成 |
| `service/*Service.java` | `【AUTO-GENERATED / 手写保护区】` | **绝不整文件覆盖** → 最小合并 |
| `controller/*Controller.java` | `【AUTO-GENERATED / 手写保护区】` | **绝不整文件覆盖** → 最小合并 |
| `pom.xml`、`application.properties` | 基线 | **完全不碰**（含真实 DB 账号、`ddl-auto=none`） |
| `config/` `security/` `exception/` `ApiResponse.java` `UserDetailsServiceImpl.java` `ApiSecurityApplication.java` | 基线 | **完全不碰** |
| `README.md` | 手写 | 只更新接口/字段章节，保留强制 11 章节结构 |

**最小合并协议**（`Service` / `Controller`）：

1. 展示准备改动的**具体方法片段**（`create()` / `update()` 的 setter 列表、`mapToResponse()` 构造参数、`@PathVariable` 类型），标明旧值与新值；
2. **取得用户确认**；不确认则明确提示「项目将无法编译」，并把改动列入人工待办；
3. 只做最小范围编辑，**禁止**整文件覆盖、**禁止**改动「手写业务代码区」里的自定义方法与 `@PreAuthorize`；
4. 变更报告记录「已最小合并到手写文件」及具体方法名。

文件存在但**没有**生成标记 → 视为用户已手改 → 禁止覆盖 → 出待办并询问。

---

## 6. `add_table`：无需注册，但要检查三件事

Spring 组件扫描自动发现，没有 `api/v1/__init__.py` 之类的中央注册文件。新表生成 6 个文件后：

1. **包路径**：6 个文件落在 `com.security.apisecurity` 的子包内，处于 `ApiSecurityApplication` 扫描范围；
2. **路由不冲突**：`@RequestMapping("/{resourcePath}")` 用复数资源名（按 `naming_rules.json`），与已有 Controller 不重复；
3. **README 追加**：只追加该表的接口章节（方法 / 完整 URL / 请求体 / 响应示例），不重写整份 README。

**幂等**：生成前按类名全文检索，同名 Entity/Repository/Service/Controller/DTO 已存在则不重复创建；同一份 SQL 连续跑两次必须零 diff。

---

## 7. 数据库迁移边界

技能**不执行 DDL**、不连库、**不改 `application.properties`**（尤其不得把 `spring.jpa.hibernate.ddl-auto=none` 改成 `update`/`create`）、不接 Flyway/Liquibase、不删数据也不删文件。

报告中必须：

- 逐条列出 `ddl_hint`（MySQL 语法），标注「需人工确认/执行」；
- 提示发布顺序：**加列先 DDL 后发代码；删列先发代码（停止引用）后 DDL**；
- 提醒 `@Column(name=...)` / Hibernate 物理命名策略与真实列名一致，以及备份、灰度、回滚。

```sql
-- 需人工确认后执行
ALTER TABLE student ADD COLUMN email VARCHAR(120) NULL COMMENT '邮箱';
```

---

## 8. 验证清单（不生成测试代码）

> 遵守本技能既定约定：README「不生成的文件」包含测试代码。以下是**验证命令**，不是产物；若用户项目已有测试则执行 `mvn test`。

```bash
# 1) 编译：捕获 Response 全参构造参数不匹配 / setter 缺失 / 类型错误
mvn clean install

# 2) 项目自带测试（如有）
mvn test

# 3) 启动：捕获 Repository 派生查询名、外键关联解析失败
mvn spring-boot:run

# 4) Swagger：核对 DTO Schema 与 5 个端点
#    http://localhost:{port}{contextPath}/swagger-ui.html
```

接口冒烟：`POST` 创建 → `GET` 列表 → `GET /{id}` 详情 → `PUT` 更新 → `DELETE` 删除，变化字段逐一读回校验。
最后：确认 `ddl-auto` 仍为 `none`、DB 账号未被覆盖，并把同一 SQL 重跑一次确认零 diff。

---

## 9. 执行顺序（`alter_table`）

1. 判定模式 → 取旧结构 → 输出差异清单（第 2 节）
2. `critical` / `high` 项（删列、改主键、软删变化、重命名、下线）**先向用户确认**
3. 整文件重生成 4 个 `【AUTO-GENERATED】` 层：`Entity` → `Repository` → `Request` → `Response`
4. 按最小合并协议更新 `Service`（必须）与 `Controller`（主键/路由变化时）
5. 只更新 README 的接口/字段章节；基线文件一律不碰
6. 汇总「人工待办清单」
7. 输出 DDL 建议与发布顺序
8. 按第 8 节验证

---

## 10. 变更报告模板

```text
运行模式：student = alter_table，course = add_table

【差异清单】
  [added]   student.email  VARCHAR(120)      risk=medium  会破坏编译（Service 映射）
  [flag]    student.status 新增              risk=medium  → 排除出 Request，不生成 PATCH

【已重生成（AUTO-GENERATED）】
  entity/Student.java、repository/StudentRepository.java
  dto/request/StudentRequest.java、dto/response/StudentResponse.java
  （add_table）entity/Course.java 等 6 个文件

【已最小合并到手写文件（经确认）】
  service/StudentService.java → create()/update() 补 setEmail；mapToResponse() 补构造参数
  controller/CourseController.java → 无改动

【跳过 / 人工待办】
  - 如需状态变更接口，请在 StudentController/StudentService 手工添加并同步 README（本技能不生成 PATCH status）
  - README.md：已更新接口与字段章节（11 章节结构保留）
  - 项目自带测试（若有）：补 email 的 payload 与断言
  - 未改动：pom.xml、application.properties（ddl-auto 仍为 none）、config/、security/

【DDL 建议（需人工确认执行）】
  ALTER TABLE student ADD COLUMN email VARCHAR(120) NULL COMMENT '邮箱';
  -- 加列：先 DDL 后发代码

【验证】
  mvn clean install            待执行
  mvn spring-boot:run         待执行（Swagger 核对）
  POST→GET→PUT→DELETE 冒烟    待执行
  同 SQL 重跑零 diff          待执行
```

---

## 11. 与既有资源的关系

- `type_mappings.json`：SQL → Java 类型、`exclude_from_request` / `exclude_from_response` / `soft_delete_fields` / 验证注解，增量场景照常适用且必须重新计算。
- `naming_rules.json`：类名/文件名/复数 `resourcePath` 与包路径，增量场景照常适用。
- `coding_standards.md` 第 8 节：文件头标记与手写保护区约定。
- `incremental_change_policy.json`：本节所有规则的可读策略源；与 `SKILL.md` 静态描述冲突时**以策略文件为准**。
- `check_skill_consistency.py` 只校验技能目录自洽，不渲染目标项目。
