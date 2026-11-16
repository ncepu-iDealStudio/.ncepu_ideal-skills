# 安全检查清单

类别用名称，不用 OWASP 编号。编号会随 2021 / 2025 版本变化（例如 SSRF 在不同版本里的归属不同）。报告若必须引用官方编号，再查当前版本，不要凭记忆编号。

不适用的类别在报告「不适用」一节写原因，不要留空勾。

## 访问控制失效

- [ ] 每条路由都有明确的认证要求。匿名访问是逐条放行，不是默认放开再去补
- [ ] 读取、更新、删除、列表、导出、搜索、批量操作都带调用者条件（`owner_id = :me` 或租户条件）
- [ ] 路径、查询、正文、请求头里的 ID 不作为授权依据
- [ ] 管理接口在服务端核对角色
- [ ] 请求绑定用 DTO 或字段白名单。客户端不能提交自己不该改的 `role`、`isAdmin`、`tenantId`、`ownerId`、`price`、`status`
- [ ] 响应里的敏感字段由服务端删除，而不是只靠界面不展示
- [ ] 重定向和 `returnUrl` 用白名单
- [ ] CORS 是明确源站列表。反射任意 Origin 时不能同时 `Allow-Credentials: true`
- [ ] 测试能证明：用户 A 不能读、改、删用户 B 的资源；租户之间不能互访

## 服务端请求伪造（SSRF）

用户能影响服务器去请求的 URL 时（webhook、链接预览、导入、拉图片）：

- [ ] 协议白名单只留 `https`（业务需要时才加 `http`）
- [ ] 能限定主机时用主机白名单
- [ ] 解析后的 IP 拒绝回环、链路本地、私网、元数据地址和 IPv6 本地范围，并且连接落到已校验的那个 IP。拒绝范围包括 `127.0.0.0/8`、`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`、`169.254.0.0/16`（含云元数据 `169.254.169.254`）、`::1`、`fc00::/7`、`fe80::/10`，以及 IPv4 映射的 IPv6
- [ ] 关闭自动重定向，或每一跳都重新校验
- [ ] 执行拉取的进程没有云凭据
- [ ] 内网响应体和错误详情不回显给用户

## 加密失败

- [ ] 对外和对内流量使用 TLS 1.2+。证书校验保持开启。禁止 `verify=False`、`InsecureSkipVerify: true`
- [ ] 对称加密用 AES-GCM 或 ChaCha20-Poly1305，同一密钥下 nonce 不重复。不用 ECB，不自造算法
- [ ] 口令用 Argon2id、scrypt 或 bcrypt。不用裸 MD5、SHA-1、SHA-256，也不要可逆加密保存口令
- [ ] 令牌和密钥来自 CSPRNG：Python `secrets`、Node `crypto.randomBytes`、Java `SecureRandom`、Go `crypto/rand`、.NET `RandomNumberGenerator`。比较用常数时间函数
- [ ] 敏感数据不进 URL、查询串、日志、分析事件或前端存储

## 注入

- [ ] SQL 全部参数化。列名、表名、`ORDER BY` 走白名单，因为它们不能当绑定参数
- [ ] 原始查询 API 逐个看过。安全写法是绑定参数，不是把输入拼进字符串：

| 栈 | 不安全 | 安全 |
| --- | --- | --- |
| Prisma | `$queryRawUnsafe`、`$executeRawUnsafe` | `$queryRaw` 标签模板 |
| EF Core | 插值字符串交给 `FromSqlRaw` / `ExecuteSqlRaw` | `FromSqlInterpolated` 或显式参数 |
| SQLAlchemy | `text(f"... {x}")` | `text("... :x")` 加绑定 |
| Django | `raw()` / `extra()` / `RawSQL` 拼接 | `params` 参数 |
| Sequelize / TypeORM / Knex | 模板字符串或拼接进 `query` / `knex.raw` | replacements / bindings |
| Rails | `where("name = '#{x}'")` | `where(name: x)` 或 `?` 占位 |
| JPA / Hibernate | 拼接 JPQL / HQL | 命名参数或位置参数 |

- [ ] 命令用参数数组，且不经 shell：Python `subprocess.run([...], shell=False)`，Node `execFile` / `spawn`，Go `exec.Command(name, args...)`，Java `ProcessBuilder(List)`
- [ ] NoSQL 拒绝用户传入的操作符对象（例如查询里的 `$gt`）。先做类型和 schema 校验
- [ ] 不把用户输入当作模板源码渲染
- [ ] 框架的逃生舱要有理由，且输入经过仍在维护的净化库：React `dangerouslySetInnerHTML`、Vue `v-html`、Svelte `{@html}`、Angular `bypassSecurityTrust*`、Jinja/Django `|safe` 与 `mark_safe`、Handlebars `{{{ }}}`、EJS `<%- %>`、Thymeleaf `th:utext`、Razor `Html.Raw`
- [ ] DOM 写入用 `textContent`。用户可控的 `href` / `src` 只允许 `https:`（需要时再加 `mailto:`）
- [ ] 响应头和日志去掉或转义 CR/LF
- [ ] XML 解析关闭外部实体和 DTD

## 不安全设计

- [ ] 动钱、改权限、处理个人敏感信息、请求用户提供的 URL 时，有一段短的威胁说明（资产、谁能调用、失败时谁受损）
- [ ] 数量、金额、次数在服务端限制
- [ ] 一次性令牌不能重放；付款和改购物车的顺序不能绕开
- [ ] 余额、库存、优惠券的并发用事务、行锁或唯一约束
- [ ] 租户隔离在查询条件或行级策略里，不靠每个作者记得加

## 安全配置错误

- [ ] 生产关闭调试、堆栈回显、目录列表和示例应用
- [ ] 默认口令已改。管理台和指标接口不对公网开放
- [ ] 有 HSTS、`X-Content-Type-Options: nosniff`、带 `frame-ancestors` 的 CSP（或 `X-Frame-Options: DENY`）、`Referrer-Policy`
- [ ] Cookie 为 `HttpOnly`、`Secure`、`SameSite`
- [ ] 对象存储默认私有。容器不以 root 运行，镜像里不烤进密钥

## 易受攻击的组件

- [ ] 锁文件已提交，安装从锁文件来（`npm ci`、带锁定的 `pip`、`go.sum`）
- [ ] CI 会跑本生态的依赖审计。没有工具时报告写明未跑
- [ ] 新依赖核对包名、维护状态和安装脚本，避开抢注包
- [ ] CI Action 和基础镜像钉死到摘要或完整 SHA

## 身份识别与认证失败

- [ ] 认证用框架或身份提供商，不自写密码学和令牌解析
- [ ] 登录、重置、MFA 有速率限制。未知用户和口令错误的提示相同
- [ ] 登录和权限变化时轮换会话。退出和改口令会使旧会话失效
- [ ] JWT 固定算法并拒绝 `none`；每次校验签名、`exp`、`nbf`、`iss`、`aud`。载荷里不放密钥。浏览器会话优先 HttpOnly Cookie，不把令牌放进 `localStorage`
- [ ] 重置链接和魔法链接：CSPRNG、一次有效、短过期、只存哈希

## 软件与数据完整性

- [ ] 不反序列化不可信数据：Python `pickle`、`yaml.load`（用 `yaml.safe_load`）、Java `ObjectInputStream`、.NET `BinaryFormatter`、PHP `unserialize`、Ruby `Marshal`
- [ ] Webhook 对原始 body 验签，并检查时间戳以防重放
- [ ] CI 中来自 fork 的工作流不能带着部署凭据跑不可信代码

## 文件

- [ ] 上传有大小限制。类型看内容，不看扩展名或客户端 `Content-Type`
- [ ] 存储文件名由服务端生成，文件不在 Web 根目录下
- [ ] 下载使用 `Content-Disposition: attachment` 和 `nosniff`。用户上传的 HTML/SVG 不从主站内联打开
- [ ] 路径先规范成绝对路径，再确认仍在基目录内。解压压缩包时检查每个条目（Zip Slip）

## 日志与告警

- [ ] 记录认证成败、拒绝访问、权限变更和管理操作：谁、做了什么、对谁、何时、从哪来
- [ ] 日志里没有口令、令牌、会话 ID、密钥、完整卡号
- [ ] 日志是结构化的，用户输入不能伪造新的一条日志

## 异常路径

- [ ] 授权或校验抛错时拒绝请求，不能落到默认允许
- [ ] 用户看到通用错误和关联 ID。细节只进日志
- [ ] 请求体、字段、正则输入、分页和解压有上限，避免耗尽资源

## 密钥

- [ ] 代码、已提交的配置、镜像、前端包、日志和错误信息里没有密钥
- [ ] 运行时从环境或密钥管理器读取
- [ ] 一旦暴露，告诉用户轮换。从历史里删掉文件不够，因为克隆和缓存还在。不要代为轮换生产凭据
