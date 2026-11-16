# 本仓库脚手架上的落点

先看仓库里有什么，再套对应一列。一个仓库可以同时命中多列。列里没写的检查仍以 [checklist.md](checklist.md) 为准。

| 信号 | 栈 |
| --- | --- |
| `fastapi` 依赖，且有 `api/`、`service/`、`repository/` | FastAPI 脚手架 |
| `flask` 依赖，且有 `api_1_0/`、`service/`、`models/` | Flask 脚手架 |
| `go.mod` 含 `gin` 与 `gorm` | Gin 脚手架 |
| `pom.xml` 或 Gradle，包名 `com.security.apisecurity` | Spring Boot 脚手架 |

四套脚手架的共同分层是：入口只调服务层，数据访问只做单表读写，**归属和权限在服务层**。只在页面上藏按钮不算数。

## FastAPI

生成技能写明：CRUD **默认不启用登录**，开箱没有 Token。审计时：

- 业务路由没有认证依赖：记为发现。用户接着要求补鉴权时，停止在本技能里设计登录，改用 `fastapi-api-security-authentication`（预检、白名单、Bearer JWT、对象权限都在那边）
- Resource 直接依赖 Repository：服务层上的归属判断会被绕开，记为 high
- 请求模型里若带 `role`、`is_admin`、`owner_id`、`tenant_id`、`price`、`status`，而客户端不该改这些字段：记为批量赋值
- 列表和导出要在分页、计数之前按当前用户过滤。只过滤详情接口不够

安全 API：SQLAlchemy 用 `text("... :name")` 加绑定参数，不用 `text(f"...")`。口令用 Argon2id。比较令牌用 `hmac.compare_digest`。

## Flask

- `api_1_0` 的 Resource 同样不能绕过 Service 去改别人的行
- SQLAlchemy `text(f"...")`、`raw()` / `extra()` 里拼接字符串，记为注入候选
- Jinja `|safe` 和 `mark_safe` 只在输入来自固定模板时才能放过，用户内容不行

## Gin

- `fmt.Sprintf`、字符串 `+` 拼进 SQL 或 `db.Raw`：注入候选。用 `?` 占位
- `exec.Command("sh", "-c", 用户字符串)`：命令注入候选。参数用数组，不要经 shell
- `InsecureSkipVerify: true`：记为 high，不接受「临时关闭校验」

## Spring Boot

- 控制器若把请求体直接绑到含 `role`、`price` 的实体：批量赋值
- `@Query`、`createQuery`、`createNativeQuery` 里拼接用户输入：注入候选。用命名参数或 `?`
- `ObjectInputStream` 读请求体：反序列化，记为 critical
- 方法级权限只写在前端菜单、服务端没有校验：记为 high

## 和鉴权技能的边界

本文件只帮助**认出** FastAPI 项目缺了什么。白名单怎么列、门禁怎么停、装饰器放在 `middleware/` 的哪一层，全部以 `fastapi-api-security-authentication` 的 `SKILL.md` 和 `references/` 为准。不要在审计报告里另写一套令牌或角色方案。
