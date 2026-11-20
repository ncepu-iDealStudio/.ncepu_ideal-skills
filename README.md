# 🎯 ncepu_ideal-skills

> 企业级项目技能（Skills）集合仓库 | 覆盖代码生成、设计需求、工程规范与安全审计，以资源驱动设计为核心

![License](https://img.shields.io/badge/license-多协议-blue)
![Go](https://img.shields.io/badge/Go-1.21%2B-00ADD8)
![Java](https://img.shields.io/badge/Java-17%2B-007396)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.100%2B-orange)
![Flask](https://img.shields.io/badge/Flask-v2.0%2B-purple)
![SpringBoot](https://img.shields.io/badge/Spring%20Boot-2.7%2B-green)
![uni-app x](https://img.shields.io/badge/uni--app%20x-vapor-2B6DE5)
![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B)
![iOS](https://img.shields.io/badge/iOS-SwiftUI-000000)
![Android](https://img.shields.io/badge/Android-Compose-3DDC84)

[English](./README.en.md) | 📝 中文

---

## ✨ 特性亮点

- 🔄 **资源驱动架构** - 模板 + 配置 + 规范，完全由资源文件驱动代码生成
- 🚀 **一键生成脚手架** - 后端从 SQL 表结构、前端从原型设计自动生成完整项目代码
- 🎨 **多技术栈支持** - Go / Java / FastAPI / Flask / Gin / Spring Boot / uni-app x / Flutter / iOS / Android
- 📦 **增量生成** - 支持首次全量生成和后续增量更新
- 🔒 **安全内置** - 软删除/硬删除、敏感数据脱敏、输入验证，以及独立的安全审计技能
- 🧩 **开箱即用** - 生成的前端工程内置 mock 数据，无需后端即可运行预览
- 📚 **参考型技能** - 现代 Web 指南、Java / Go 工程规范等技能在动手前注入专家知识，不接管你的目录结构

---

## 🎯 当前技能清单

按目录分组。主体技能共 **33 个**，另有 4 个 IDE 专用技能副本与 20 个 superpowers-zh 通用技能。

### 🏭 SQL → 后端脚手架（`sql-to/`，4 个）

| 技能 | 输入 → 输出 |
| --- | --- |
| [`sql-to-fastapi-restfulapi-scaffold`](sql-to/sql-to-fastapi-restfulapi-scaffold/README.md) | SQL `CREATE TABLE` → FastAPI 分层脚手架（Model / Schema / Repository / Service / Resource + 测试骨架） |
| [`sql-to-flask-restfulapi-scaffold`](sql-to/sql-to-flask-restfulapi-scaffold/README.md) | MySQL DDL → Flask + Flask-RESTful 接口项目脚手架 |
| [`sql-to-springboot-restfulapi-scaffold`](sql-to/sql-to-springboot-restfulapi-scaffold/README.md) | SQL `CREATE TABLE` → Spring Boot 分层脚手架，并导出 `docs/openapi.json` / `docs/api.md` |
| [`sql-to-gin-restfulapi-scaffold`](sql-to/sql-to-gin-restfulapi-scaffold/README.md) | MySQL DDL → Gin + GORM 分层脚手架，含一键回归流水线 |

> 表结构未定先用 [`database-schema-designer`](design/database-schema-designer/README.md) 出 MySQL 脚本；这些脚手架技能不执行 DDL。

---

### 🎨 设计与需求（`design/`，5 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `database-schema-designer` | 自然语言或已有库结构 → 分引擎 DDL（PostgreSQL / MySQL 为主，SQLite / MongoDB 补充）+ `database-design.md`；改编自 OneWave AI（MIT） | [README](design/database-schema-designer/README.md) |
| `frontend-design` | 前端视觉设计指导：审美方向、排版、避免模板化默认样式，与具体框架无关 | [SKILL.md](design/frontend-design/SKILL.md) |
| `huashu-design` | 花叔 Design：一句话产出高保真 HTML 原型、幻灯片、动画、可视化与专家评审；先出三方向初稿供选择（MIT） | [README](design/huashu-design/README.md) |
| `md-prd-to-html-prototype` | 读取本地 Markdown PRD → 单文件 HTML 低保真原型；字段以文档为准，信息不足先提问 | [README](design/md-prd-to-html-prototype/README.md) |
| `modern-web-guidance` | 参考型：编写 Web 前端前检索随仓库自带的 209 份现代平台指南，离线自包含、中文驱动 | [README](design/modern-web-guidance/README.md) |

> `modern-web-guidance` 的指南为上游英文原文（CC-BY 4.0 / 代码 Apache-2.0），署名见 [ATTRIBUTION.md](design/modern-web-guidance/ATTRIBUTION.md)。Web UI 技能可在各自目录、分层与组件库不变的前提下叠加它。

---

### 📱 原型 → 应用工程（`prototype-to/`，7 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `prototype-to-app-uniappx` | 原型 → uni-app x 蒸汽模式（TS）工程，`.uvue` 页面 + services 分层 + mock 数据 | [README](prototype-to/prototype-to-app-uniappx/README.md) |
| `prototype-to-flutter-app` | 原型 → Flutter 工程，features 分层 + Repository + `ChangeNotifier`，零重型依赖 | [README](prototype-to/prototype-to-flutter-app/README.md) |
| `prototype-to-web(Nuxt UI Starter)` | 原型 → Nuxt UI Starter 工程，内置页面与组件分层 | [README](<prototype-to/prototype-to-web(Nuxt UI Starter)/README.md>) |
| `prototype-to-taro-app` | 原型 → Taro 4 多端工程，Vue3 / React 双分支由用户确认 | [README](prototype-to/prototype-to-taro-app/README.md) |
| `prototype-to-ios-native-app(AwesomeSwift)` | 原型 → SwiftUI 原生 iOS 工程（Swift 5.10 / XcodeGen / MVVM + Combine） | [README](<prototype-to/prototype-to-ios-native-app(AwesomeSwift)/README.md>) |
| `prototype-to-android-native-app(Fragmject)` | 原型 → Jetpack Compose 原生 Android 工程（Kotlin 2.1 / 单 Activity MVI / Hilt） | [README](<prototype-to/prototype-to-android-native-app(Fragmject)/README.md>) |
| `requirements-to-vue_vben_admin` | 后台管理需求 → vue-vben-admin（vben5）可运行脚手架，含 CRUD 页面 / 看板 / mock 数据 | [README](prototype-to/requirements-to-vue_vben_admin/README.md) |

> 各技能均内置数据访问接缝：切真实后端只改一个开关（`useMock` / `AppContainer` 装配），页面代码不动。H5 界面可按需叠加 [`modern-web-guidance`](design/modern-web-guidance/README.md)，小程序与原生端不套用。

---

### ☕ Java 工程（`java/`，5 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `create-spring-boot-java-project` | 从 start.spring.io 脚手架新 Spring Boot 项目（Maven / Gradle），带配置、PostgreSQL、日志、安全、测试与 Docker 默认值 | [SKILL.md](java/create-spring-boot-java-project/SKILL.md) |
| `java-development` | 无框架日常 Java 开发：Maven / Gradle、JDK 版本习惯用法（records / sealed / 虚拟线程）、日志、空值、并发、静态分析与打包 | [SKILL.md](java/java-development/SKILL.md) |
| `java-springboot` | 在已有 Spring Boot 3/4 项目中写和评审业务代码：Controller / 校验 / ProblemDetail / JPA / RestClient / 缓存 / 调度 | [SKILL.md](java/java-springboot/SKILL.md) |
| `java-upgrade` | 升级 Java 项目到更高 JDK（11→17→21→25），按当前版本加载对应指南并采用新语言特性 | [SKILL.md](java/java-upgrade/SKILL.md) |
| `openapi-to-application-java-spring-boot` | OpenAPI 3 规约 → Spring Boot 应用：openapi-generator 产出接口与 DTO，再实现 Controller / Service / 持久化 / 安全 / 测试 | [SKILL.md](java/openapi-to-application-java-spring-boot/SKILL.md) |

---

### 🐹 Go 工程（`go/`，4 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `go-api-design` | HTTP/REST API 设计：handler、ServeMux 路由、中间件、校验、分页、幂等、健康检查、错误响应与优雅关闭 | [SKILL.md](go/go-api-design/SKILL.md) |
| `golang-grpc` | gRPC 使用规范：protobuf 组织、拦截器、状态码、TLS/mTLS、bufconn 测试与流式 RPC | [SKILL.md](go/golang-grpc/SKILL.md) |
| `golang-project-layout` | Go 项目布局：cmd / internal / pkg、模块与包命名、go.work workspace、多 main 包 CLI | [SKILL.md](go/golang-project-layout/SKILL.md) |
| `golang-testing` | Go 测试实践：表驱动、testify、并行、fuzz、fixtures、goleak、快照、覆盖率与集成测试 | [SKILL.md](go/golang-testing/SKILL.md) |

---

### 🔒 安全（`security/`，6 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `fastapi-api-security-authentication` | 给已有 FastAPI CRUD 项目补白名单、Bearer JWT 与角色/对象权限；不满足前置条件会停下来询问 | [SKILL.md](security/fastapi-api-security-authentication/SKILL.md) |
| `go-security-audit` | Go 应用安全评审：输入校验、SQL/命令注入、SSRF、路径穿越、认证、密钥、加密与 OWASP Top 10（只读报告） | [SKILL.md](security/go-security-audit/SKILL.md) |
| `golang-continuous-integration` | Go 项目 CI/CD：GitHub Actions 的 test / lint / SAST / 覆盖率 / 依赖扫描任务，Dependabot、Renovate、GoReleaser | [SKILL.md](security/golang-continuous-integration/SKILL.md) |
| `security-audit` | 审计已有代码：越权、注入、XSS、SSRF、认证与 JWT、密钥、反序列化、上传与路径、依赖和日志 | [README](security/security-audit/README.md) |
| `spring-boot-testing` | Spring Boot 测试技术选型：测试切片、Testcontainers `@ServiceConnection`、Failsafe、MockitoBean、JUnit / AssertJ | [SKILL.md](security/spring-boot-testing/SKILL.md) |
| `spring-security` | Spring Security 6/7 配置与评审：SecurityFilterChain lambda DSL、方法安全、OAuth2 资源服务器、CSRF/CORS、MockMvc 安全测试 | [SKILL.md](security/spring-security/SKILL.md) |

> `security-audit` 候选扫描：`python security/security-audit/scripts/scan_sinks.py <项目根>`，命中不等于结论。报告不写攻击步骤与密钥原文。改编自 [developer-agent-skills/security-audit](https://github.com/reddygopalkrishna/developer-agent-skills/blob/main/skills/security-audit/SKILL.md)（MIT），见目录内 `NOTICE`。

---

### 🧰 独立技能与通用技能

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `dsh-plugin-starter` | 从一句话需求或插件原型生成 DSH 插件起步项目，四类插件 + 内置《开发者指南》 | [README](dsh-plugin-starter/README.md) |
| `common-website-design` | 自然语言网站需求 → 框架无关的静态 HTML 设计原型（多页面 + 统一样式 + `site-manifest.json`） | [README](.dsh/skills/common-website-design/README.md) |
| `it-requirement-analysis` | 业务诉求 → 可落地、可验收的 PRD、用户故事、功能/非功能需求与风险依赖 | 安装位置见下方目录树 |
| `prd-html-skill` | PRD / 需求文档 / 页面清单 → 可交互多页面 HTML 原型，支持单文件离线打包 | [README](.cursor/skills/prd-html-skill/README.md) |
| `supervisor-skills` | 12 个科研全流程技能（Idea 评估、文献调研、论文写作、投稿审核与 Rebuttal 等） | [中文导读](research/supervisor-skills/README.zh-CN.md) |

- `common-website-design` 安装在 `.workbuddy/skills/`、`.dsh/skills/`；`it-requirement-analysis` 安装在 `.cursor/skills/`、`.dsh/skills/`、`.workbuddy/skills/`；`prd-html-skill` 安装在 `.cursor/skills/`、`.dsh/skills/`
- 12 个科研技能需**作为一组整体安装**（技能间相互引用），多数为纯提示词；`drawio-reconstruction` 额外依赖 Python 脚本与 draw.io CLI
- ⚠️ `supervisor-skills` 整体为 **CC BY-NC-SA 4.0**（非商业 + 相同方式共享），**不受本仓库 MIT 许可覆盖**，商用前请阅读 [`references/PROVENANCE.md`](research/supervisor-skills/references/PROVENANCE.md)
- `.codebuddy/skills/` 与 `.agents/skills/` 各有 20 个 superpowers-zh 通用技能（brainstorming、TDD、systematic-debugging、writing-plans 等），供 CodeBuddy / Agent 工作流使用

---

## 🏗️ 仓库结构

```text
ncepu_ideal-skills/
├── 📄 README.md / README.en.md / CODEBUDDY.md
├── 📁 .docs/                                       # 各 IDE 配置指南 + 设计方法 + plans/ + specs/ + images/
├── 📁 sql-to/                                      # 🏭 SQL → 后端脚手架（4 个技能，均含 README + SKILL + resources/）
│   ├── sql-to-fastapi-restfulapi-scaffold/         # ⚡ 另含 docs/
│   ├── sql-to-flask-restfulapi-scaffold/           # 🐍
│   ├── sql-to-springboot-restfulapi-scaffold/      # ☕
│   └── sql-to-gin-restfulapi-scaffold/             # 🌀
├── 📁 design/                                      # 🎨 设计 / 需求 / 数据库（5 个技能）
│   ├── database-schema-designer/                   # README + SKILL + NOTICE + LICENSE + references/
│   ├── frontend-design/                            # SKILL.md
│   ├── huashu-design/                              # README(.en) + SKILL + assets/ demos/ references/ scripts/
│   ├── md-prd-to-html-prototype/                   # README + SKILL + references/ resources/ scripts/
│   └── modern-web-guidance/                        # README + SKILL + ATTRIBUTION + resources/（209 份指南）
├── 📁 prototype-to/                                # 📱 原型 → 应用工程（7 个技能，均含 resources/）
│   ├── prototype-to-app-uniappx/
│   ├── prototype-to-flutter-app/
│   ├── prototype-to-web(Nuxt UI Starter)/
│   ├── prototype-to-taro-app/
│   ├── prototype-to-ios-native-app(AwesomeSwift)/
│   ├── prototype-to-android-native-app(Fragmject)/
│   └── requirements-to-vue_vben_admin/
├── 📁 go/                                          # 🐹 Go 工程规范（4 个技能，SKILL + references/ 等）
│   ├── go-api-design/
│   ├── golang-grpc/
│   ├── golang-project-layout/
│   └── golang-testing/
├── 📁 java/                                        # ☕ Java 工程规范（5 个技能，SKILL + references/ 等）
│   ├── create-spring-boot-java-project/
│   ├── java-development/
│   ├── java-springboot/
│   ├── java-upgrade/
│   └── openapi-to-application-java-spring-boot/
├── 📁 security/                                    # 🔒 安全（6 个技能）
│   ├── fastapi-api-security-authentication/        # SKILL + references/ + scripts/
│   ├── go-security-audit/                          # SKILL + references/
│   ├── golang-continuous-integration/              # SKILL + assets/ evals/ references/
│   ├── security-audit/                             # README + SKILL + NOTICE + references/ + scripts/
│   ├── spring-boot-testing/                        # SKILL + references/
│   └── spring-security/                            # SKILL + references/
├── 📁 research/
│   └── supervisor-skills/                          # 🔬 12 个科研技能（CC BY-NC-SA 4.0）
│       ├── README.zh-CN.md                         # 本仓库中文导读
│       ├── references/PROVENANCE.md                # 署名与许可声明
│       └── idea-evaluator/, deep-research/, ...    # 12 个技能目录
├── 📁 dsh-plugin-starter/                          # 🧩 DSH 插件起步项目生成技能
├── 📁 test/                                        # 🧪 技能生成示例与样例数据
│   ├── api_security_demo-20260717.sql
│   └── sql-to-{fastapi,flask,gin,springboot}-example/, page-design-showcase/
├── 📁 .codebuddy/skills/ · .agents/skills/         # 🧠 各 20 个 superpowers-zh 通用技能
├── 📁 .workbuddy/skills/                           # common-website-design / it-requirement-analysis / md-prd-to-html-prototype / diagnosing-superpowers
├── 📁 .cursor/skills/                              # it-requirement-analysis / prd-html-skill
├── 📁 .dsh/skills/                                 # common-website-design / diagnosing-superpowers / it-requirement-analysis / prd-html-skill
└── 📁 .superpowers/sdd/                            # SDD 工作流资源
```

---

## 快速开始

### 1️⃣ 配置技能到你的 AI 工具

> 根据你使用的 AI 编程助手，选择对应的配置指南：

| 🤖 AI 工具 | 📚 配置文档 |
| ----------- | ----------- |
| 🚀 **Trae IDE** | [配置指南](.docs/Trea中使用skill配置.md) |
| 💻 **Claude Code** | [配置指南](.docs/claude中使用skill配置.md) |
| ⚡ **GitHub Copilot** | [配置指南](.docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md) |
| 🧩 **CodeBuddy** | [配置指南](.docs/CodeBuddy中使用skill配置.md) |
| 🛠️ **WorkBuddy** | [原型转应用技能指南](.docs/workbuddy中使用原型转应用技能.md) |
| 🐋 **DSH（DeepSeek Harness）** | [superpowers 技能指南](.docs/dsh中使用superpowers技能.md) |
| 🧩 **DSH 插件开发** | [dsh-plugin-starter 使用指南](.docs/使用dsh-plugin-starter技能开发DSH插件.md) |
| 🌐 **现代 Web 前端指南** | [modern-web-guidance 使用指南](.docs/使用modern-web-guidance技能编写现代Web前端指南.md) |

> 📝 **提示**：详细配置说明请参考 `.docs/` 目录（另有 `plans/` 与 `specs/` 设计文档）。

---

### 2️⃣ 使用技能

本仓库技能分四类，输入方式不同。

#### A. 后端：从 SQL 生成接口脚手架

将包含 `CREATE TABLE` 的 SQL 输入给 AI，要求生成对应的项目脚手架。

**📥 示例输入**：

```sql
CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    age INT COMMENT '年龄',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除'
);
```

**📤 生成内容对照表**：

| ⚡ 技能 | 📥 输入 | 📤 生成内容 |
| -------- | -------- | ----------- |
| **FastAPI** | SQL CREATE TABLE | Model / Schema / Repository / Service / Resource + 测试骨架 |
| **Flask** | MySQL DDL | Model / Controller / Service / Resource + 项目骨架 |
| **Gin** | MySQL DDL | Model / DAO / Service / Resource + 项目骨架 |
| **Spring Boot** | SQL CREATE TABLE | Entity / Repository / DTO / Service / Controller + 项目骨架 |

表结构还没定时，先用 [database-schema-designer](design/database-schema-designer/README.md) 出 MySQL 脚本，再把 `schema.mysql.sql` 交给上表里的技能。那些技能不执行 DDL。PostgreSQL 脚本不要直接交给它们。

#### B. 前端：从原型生成应用工程

将**原型 HTML 代码**、**设计图截图**或 **PRD 页面清单**交给 AI，生成可运行的工程。

**📥 示例输入**：

```text
这是我们的原型页面（附 HTML 代码 / 设计图 / 页面清单）。
请用 prototype-to-flutter-app 技能，生成可运行的 Flutter 工程，
用 mock 数据还原页面布局与交互，后续我再对接后端接口。
```

**📤 生成内容对照表**：

| ⚡ 技能 | 📥 输入 | 📤 生成内容 |
| -------- | -------- | ----------- |
| **uni-app x** | 原型代码 / 图片 / PRD | `.uvue` 页面 + 组件 + services 分层 + mock 数据，可在 HBuilder 直接运行 |
| **Flutter** | 原型代码 / 图片 / PRD | features 分层 + Repository + mock 数据，`flutter pub get && flutter run` 即可运行 |
| **Nuxt UI Starter** | 原型代码 / 图片 / PRD | Nuxt 页面与组件工程，内置 mock 数据 |
| **Taro** | 原型代码 / 图片 / PRD | Taro 4 多端工程，Vue3 / React 双分支 |
| **iOS 原生** | 原型代码 / 图片 / PRD | SwiftUI 四页范本 + MVVM & Combine + SwiftData，`xcodegen generate` 后 Xcode 直接 Run |
| **Android 原生** | 原型代码 / 图片 / PRD | Compose 四页范本 + 单 Activity MVI + Hilt + Room，Android Studio 打开即运行 |
| **vben 后台** | 后台需求描述 | vue-vben-admin 路由菜单 / CRUD 页面 / 看板 / mock 数据 |

> 💡 上述技能都会生成**数据访问层接缝**：切换到真实后端只需改一个开关（`useMock` / `AppContainer` 装配），页面代码无需改动。

#### C. 参考型：编写代码前检索专家指南

`modern-web-guidance` 不「生成工程」，而是**在动手前注入专家指南**；Java / Go / 安全技能则提供各自领域的工程规范与评审清单。

**📥 示例输入**：

```text
请实现一个点击遮罩层关闭的确认对话框，要能用键盘 Esc 关闭、并避免背景页面滚动。
```

**📤 产出**：符合现代 Web 规范的实现代码 + 回复末尾 `### Modern Web Guidance` 披露用到的指南。

`modern-web-guidance` 可单独使用，也可在下列技能写浏览器界面时叠加（它们自己的目录、分层和组件库不变）：

- [prototype-to-web(Nuxt UI Starter)](<prototype-to/prototype-to-web(Nuxt UI Starter)/README.md>)、[requirements-to-vue_vben_admin](prototype-to/requirements-to-vue_vben_admin/README.md)：映射到各自的 UI 组件
- [common-website-design](.dsh/skills/common-website-design/README.md)、[prd-html-skill](.cursor/skills/prd-html-skill/README.md)、[md-prd-to-html-prototype](design/md-prd-to-html-prototype/README.md)：直接落进 HTML
- [prototype-to-taro-app](prototype-to/prototype-to-taro-app/README.md)、[prototype-to-app-uniappx](prototype-to/prototype-to-app-uniappx/README.md)：仅 H5
- [dsh-plugin-starter](dsh-plugin-starter/README.md)：仅双面型设置页

小程序、App、Flutter、iOS、Android 和后端脚手架不套用。对照见使用指南第 14 节。

```sh
# 也可直接当本地命令行工具用（在 design/modern-web-guidance/ 目录下）
python3 resources/tools/mwg.py search "light dismiss dialog"
python3 resources/tools/mwg.py retrieve "light-dismiss-a-dialog,dialog"
```

> 🌐 指南随仓库自带、完全离线、无遥测；检索前如更新过 `guides/`，先跑 `python3 resources/tools/build_index.py`。

#### D. 工程规范：Java / Go 与安全

这些技能不生成脚手架，而是在**写代码、评审或升级**时给出约定与清单：

- Java：新建项目用 `create-spring-boot-java-project`，已有项目写业务用 `java-springboot`，日常语法与构建用 `java-development`，版本迁移用 `java-upgrade`，按 OpenAPI 规约实现用 `openapi-to-application-java-spring-boot`
- Go：`golang-project-layout` 定目录，`go-api-design` 定 HTTP 接口，`golang-grpc` 定 RPC，`golang-testing` 定测试；CI 与依赖扫描见 `golang-continuous-integration`
- 安全：`security-audit` 审已有代码，`fastapi-api-security-authentication` 补 FastAPI 登录与权限，`spring-security` / `spring-boot-testing` 覆盖 Spring 安全与测试，`go-security-audit` 只读评审 Go 服务

---

## 🗺️ 未来规划

- [ ] 🔮 新增更多面向企业前后端的技能（脚手架、治理、工程化等）
- [ ] 🧪 完善技能验证样例与回归测试
- [ ] 📋 建立统一技能命名、版本与文档规范
- [ ] 🎯 补充 Flutter / uni-app x / iOS（Xcode）/ Android（Gradle）技能在真实 SDK 环境下的编译回归验证

---

## 🤝 贡献指南

欢迎提交新的 Skill 或改进现有 Skill！

**💡 建议流程**：

1. 🍴 Fork 本仓库并新建分支
2. 📁 在对应分类目录（`sql-to/`、`design/`、`prototype-to/`、`go/`、`java/`、`security/`、`research/`）中新建独立技能目录，包含 `SKILL.md`、`README.md`、`resources/`
3. 🧪 补充对应示例到 `test/`
4. 📝 更新根 README 的技能清单与仓库结构
5. 🔄 发起 Pull Request

---

## 📄 许可证

仓库根目录未声明统一许可证文件；各技能自带其许可（`database-schema-designer`、`security-audit`、`huashu-design` 等为 MIT，`modern-web-guidance` 见 `ATTRIBUTION.md`）。`research/supervisor-skills` 为 **CC BY-NC-SA 4.0**，不受 MIT 覆盖。对外分发前请核对每个技能的许可声明。
