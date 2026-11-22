# 预检与门禁

在改任何业务鉴权代码之前执行。脚本只收集证据，**放行或停问由本文件规则决定**。

```powershell
python "<skill目录>/scripts/preflight_auth.py" "<目标项目根>" -o auth-preflight.json
```

再阅读 `models/`、`sql/`、`service/`、`api/`、实际 `include_router` 注册，补上脚本可能漏掉的项。

## 1. 账号密码表

同时看 SQL `CREATE TABLE` 与 ORM 模型。密码列名（规范化为小写、去下划线后匹配）包括：`password`、`passwd`、`pwd`、`passwordhash`、`hashedpassword`、`passhash`。账号列线索：`account`、`username`、`user_name`、`login_name`、`email`（仅当同行已有密码列时作为登录名候选）。

排除：`password_policy` 一类策略配置表；没有密码列的资料表（如 `admin` 只有 `user_id` 外键）不是登录账号表，可记为「关联资料」。

无任何账号密码表时，停问：

```text
未发现含账号/密码字段的表，本技能无法在现有数据上做登录鉴权。
是否需要我增加最小账号表并实现登录接口？请回复「是」或「否」。
```

多张账号密码表时列出表名、模型文件、密码/账号字段；未选定鉴权主体前不继续。

## 2. 登录接口（Service + Resource）

脚手架约定：HTTP 在 Resource，业务在 Service，Resource 只调 Service。登录接口要两边都有：

| 层 | 视为已定义的证据 |
| --- | --- |
| Service | `*_service.py` 中存在 `login` / `signin` / `sign_in` / `authenticate` 方法，且针对某张账号表 |
| Resource | 实际注册的 `POST`（或项目已有的等价方法）路径含 `login`、`signin`、`sign-in`、`/auth/token` 等，并调用上述 Service |

只有 Service 没有 HTTP，或只有 Resource 在路由里直接查库，都算**没有合格登录接口**。不能把 CRUD 的 `POST /` 创建用户当成登录。

有账号表但无登录接口时，停问（把括号换成实际表名与文件）：

```text
检查结果：发现账号表（例如 sso_user，密码字段 password），
但对应服务层未定义登录方法，Resource 也未暴露登录 HTTP 接口。
本技能依赖已有登录入口才能继续鉴权加固。
是否需要我帮忙实现相应的登录接口代码？请回复「是」或「否」。
若否，请指出已有登录入口的文件与路径。
```

用户回复「是」：只实现登录（Service 方法 + Resource 路由 + JWT 签发 + 失败不泄露账号是否存在），保持分层，完成后重新跑门禁 1。不要顺带改全部业务接口权限。

## 3. 令牌鉴权是否合格

合格需同时满足：

1. 登录成功后签发签名令牌（JWT 或用户明确允许的同等方案），响应中有获取令牌的稳定字段。
2. 业务接口从 `Authorization: Bearer <token>` 取令牌（用户另指定协议除外）。
3. 校验签名、算法与过期时间；密钥来自配置/环境，非代码内默认口令。
4. 令牌主体映射到唯一非空真实账号，并按当前库中的状态/角色加载；不信任客户端提交的 `user_id`/`role`。
5. 不是仅用 Cookie Session、明文密码、硬编码 `Bearer test-token`、或验签后不查账号。

脚手架里已有 `utils.auth` / `core.security` 只说明**具备签发能力**，若没有任何登录接口调用它们，门禁 1 仍失败。集成测试里的 `Bearer test-token` 是待替换的假身份，不能当作已合格登录。

不合格时停问：

```text
检查结果：已有登录接口（方法、路径、文件），但不符合令牌鉴权要求：
- （列出缺口，例如：未签发 JWT / 未使用 Authorization Bearer / 使用硬编码 test-token）
要求：登录成功签发 JWT，业务接口使用 Authorization: Bearer <token> 校验签名与过期。
是否需要我帮忙修订这些登录接口？请回复「是」或「否」。
```

## 4. 角色

门禁 1、2 通过后再做。角色线索：字段 `user_type` / `usertype` / `role` / `role_id` / `role_name` / `is_admin` / `user_role`；独立角色/权限表；注释中的账号类型枚举。

**发现一类以上业务角色或类型**（例如学生/教师/管理员）时停止实现，停问：

```text
检查结果：发现用户角色或类型（例如 sso_user.user_type：1 学生 / 2 老师 / 3 管理人员）。
请补充这些角色的权限范围：各角色可读、可写、可删哪些资源；能否管理他人数据；哪些字段禁止普通角色修改。
在您补充之前，本技能暂停后续加固实现。
```

**完全没有角色设计**：默认 `user` 与 `admin`，在权限说明中标记「默认选择」，然后继续。不要把组 ID `1` 或用户名自动当成管理员。

## 5. 初始管理员与种子数据

门禁 1–3 通过后执行。鉴权加固后所有业务接口都要求登录，**没有可登录管理员的项目等于不可用**：无法登录、无法创建第一个账号、无法验证任何正向用例。

证据来源（命中任一即可，但仍需可复现的创建/轮换说明）：

- 种子脚本：`scripts/seed_admin.py`、`seed*.py`、`bootstrap*.py` 等，读取环境变量并写入账号；
- 初始化 SQL / 迁移：`database/*seed*.sql`、`INSERT INTO <账号表>`、Alembic/Flyway 迁移；
- 已核实的既有管理员行（需给出账号标识与创建方式，不输出口令）。

不合格或缺失的情形：

- 完全没有创建管理员的入口；
- 只在应用启动/lifespan 里自动 `INSERT` 管理员；
- 代码里硬编码通用管理员账号/口令；
- 只有测试 fixture 创建账号，交付后没有任何初始化手段。

缺失时停止并询问：

```text
检查结果：项目没有任何创建初始管理员的入口（无种子脚本 / 初始化 SQL / 迁移），
而鉴权加固后所有业务接口都要求登录，系统将无法产生第一个管理员，交付后不可用。
是否需要我生成幂等初始化脚本 scripts/seed_admin.py，
从 .env 读取 INITIAL_ADMIN_USERNAME / INITIAL_ADMIN_PASSWORD，用项目统一哈希写入管理员账号？
请回复「是」或「否」。
```

用户回复「是」：按[权限与结构规范](policy-and-architecture.md)第三节「初始管理员种子数据」生成脚本与 `.env.example` 占位，实跑一次并验证真实登录；完成后重新检查本节。用户回复「否」：终止收尾，只报告「系统缺少可登录初始管理员，交付不可用」，不得宣称完成。

不允许把初始化写成公开的无条件 HTTP 接口，也不允许以「用户名等于 admin 即管理员」之类规则替代受控初始化。

## 6. 常规白名单

门禁通过后，对**实际注册路由**逐条标 `public` 或 `protected`，精确到方法+路径。

| 默认 public | 条件 |
| --- | --- |
| 登录 `POST` | 门禁确认的登录路径 |
| `GET /health`、`GET /healthz`、`GET /ready` | 项目里真实存在 |
| `GET /docs`、`GET /redoc`、`GET /openapi.json` | 项目启用了 OpenAPI |

| 候选 public（未确认则 protected） | 例子 |
| --- | --- |
| 注册、验证码、静态资源、回调 | `/register`、`/captcha`、`/static`、webhook |

其余业务接口默认 `protected`。禁止用 `/api` 前缀或忽略 HTTP 方法放行。CORS 的 OPTIONS 按框架行为说明，不要用模糊规则代替白名单。健康检查与文档若在生产关闭，权限说明里写清环境差异。

## 7. 与后续步骤的衔接

门禁与白名单完成后，才进入 `middleware/` 装饰器、对象权限和测试。可选脚本 `route_inventory.py`、`check_policy_coverage.py`、`http_auth_probe.py` 不能代替门禁停问，也不能代替查库的越权测试。
