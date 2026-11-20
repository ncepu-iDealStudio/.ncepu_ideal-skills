# 🎯 ncepu_ideal-skills

> Enterprise Project Skills Collection | Code generation, design, engineering conventions, and security audits — driven by resources

![License](https://img.shields.io/badge/license-Multiple-blue)
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

[中文](./README.md) | 📝 English

---

## ✨ Key Features

- 🔄 **Resource-driven Architecture** - Templates + Configurations + Standards, completely driven by resource files
- 🚀 **One-click Scaffolding** - Complete project code from SQL schemas (backend) or prototypes (frontend)
- 🎨 **Multi-stack Support** - Go / Java / FastAPI / Flask / Gin / Spring Boot / uni-app x / Flutter / iOS / Android
- 📦 **Incremental Generation** - Full initial generation + incremental updates
- 🔒 **Built-in Security** - Soft/hard delete, sensitive data masking, input validation, plus dedicated audit skills
- 🧩 **Runs Out of the Box** - Generated frontend projects ship with mock data, no backend needed to preview
- 📚 **Reference Skills** - Modern Web guides and Java / Go engineering conventions inject expert knowledge without taking over your layout

---

## 🎯 Current Skills

Grouped by directory. **33 primary skills**, plus 4 IDE-specific copies and 20 superpowers-zh general skills.

### 🏭 SQL → Backend Scaffolds (`sql-to/`, 4)

| Skill | Input → Output |
| --- | --- |
| [`sql-to-fastapi-restfulapi-scaffold`](sql-to/sql-to-fastapi-restfulapi-scaffold/README.md) | SQL `CREATE TABLE` → layered FastAPI scaffold (Model / Schema / Repository / Service / Resource + test skeleton) |
| [`sql-to-flask-restfulapi-scaffold`](sql-to/sql-to-flask-restfulapi-scaffold/README.md) | MySQL DDL → Flask + Flask-RESTful API scaffold |
| [`sql-to-springboot-restfulapi-scaffold`](sql-to/sql-to-springboot-restfulapi-scaffold/README.md) | SQL `CREATE TABLE` → layered Spring Boot scaffold, exports `docs/openapi.json` / `docs/api.md` |
| [`sql-to-gin-restfulapi-scaffold`](sql-to/sql-to-gin-restfulapi-scaffold/README.md) | MySQL DDL → layered Gin + GORM scaffold, includes a one-command regression pipeline |

> If the tables are not designed yet, use [`database-schema-designer`](design/database-schema-designer/README.md) to produce a MySQL script first. These scaffold skills do not run DDL.

---

### 🎨 Design & Requirements (`design/`, 5)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `database-schema-designer` | Natural language or an existing schema → engine-correct DDL (PostgreSQL / MySQL first, SQLite / MongoDB secondary) + `database-design.md`; adapted from OneWave AI (MIT) | [README](design/database-schema-designer/README.md) |
| `frontend-design` | Visual design guidance: aesthetic direction, typography, avoiding templated defaults; framework-agnostic | [SKILL.md](design/frontend-design/SKILL.md) |
| `huashu-design` | One prompt → high-fidelity HTML prototypes, slides, animation, visualization, and design reviews; three directions first (MIT) | [README](design/huashu-design/README.md) |
| `md-prd-to-html-prototype` | Local Markdown PRD → single-file low-fidelity HTML prototype; fields come from the document, gaps are asked first | [README](design/md-prd-to-html-prototype/README.md) |
| `modern-web-guidance` | Reference skill: retrieve from 209 bundled modern Web guides before writing UI; offline, self-contained, Chinese-driven | [README](design/modern-web-guidance/README.md) |

> The guides are verbatim upstream English copies (CC-BY 4.0 / code Apache-2.0); credit in [ATTRIBUTION.md](design/modern-web-guidance/ATTRIBUTION.md). Web UI skills can overlay it while keeping their own layout, layers, and components.

---

### 📱 Prototype → App Projects (`prototype-to/`, 7)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `prototype-to-app-uniappx` | Prototype → uni-app x vapor-mode (TS) project with `.uvue` pages, layered services, and mock data | [README](prototype-to/prototype-to-app-uniappx/README.md) |
| `prototype-to-flutter-app` | Prototype → Flutter project with feature-first layers, Repository, and `ChangeNotifier`; no heavy dependencies | [README](prototype-to/prototype-to-flutter-app/README.md) |
| `prototype-to-web(Nuxt UI Starter)` | Prototype → Nuxt UI Starter project with pages, components, and mock data | [README](<prototype-to/prototype-to-web(Nuxt UI Starter)/README.md>) |
| `prototype-to-taro-app` | Prototype → Taro 4 multi-platform project, Vue3 / React branches confirmed by the user | [README](prototype-to/prototype-to-taro-app/README.md) |
| `prototype-to-ios-native-app(AwesomeSwift)` | Prototype → native SwiftUI iOS project (Swift 5.10 / XcodeGen / MVVM + Combine) | [README](<prototype-to/prototype-to-ios-native-app(AwesomeSwift)/README.md>) |
| `prototype-to-android-native-app(Fragmject)` | Prototype → native Jetpack Compose Android project (Kotlin 2.1 / single-Activity MVI / Hilt) | [README](<prototype-to/prototype-to-android-native-app(Fragmject)/README.md>) |
| `requirements-to-vue_vben_admin` | Admin requirements → runnable vue-vben-admin (vben5) scaffold with CRUD pages, dashboards, and mock data | [README](prototype-to/requirements-to-vue_vben_admin/README.md) |

> Every skill creates a data-access seam: switching to a real backend only flips one flag (`useMock` / `AppContainer` wiring). H5 UI may overlay [`modern-web-guidance`](design/modern-web-guidance/README.md); mini programs and native apps do not.

---

### ☕ Java Engineering (`java/`, 5)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `create-spring-boot-java-project` | Scaffold a new Spring Boot project from start.spring.io (Maven / Gradle) with sensible config, PostgreSQL, logging, security, testing, and Docker defaults | [SKILL.md](java/create-spring-boot-java-project/SKILL.md) |
| `java-development` | Framework-free daily Java: Maven / Gradle, JDK-version idioms (records / sealed / virtual threads), logging, null handling, concurrency, static analysis, packaging | [SKILL.md](java/java-development/SKILL.md) |
| `java-springboot` | Write and review application code in an existing Spring Boot 3/4 project: controllers, validation, ProblemDetail, JPA, RestClient, caching, scheduling | [SKILL.md](java/java-springboot/SKILL.md) |
| `java-upgrade` | Upgrade a Java project to a newer JDK (11→17→21→25), loading only the matching per-version guide | [SKILL.md](java/java-upgrade/SKILL.md) |
| `openapi-to-application-java-spring-boot` | OpenAPI 3 spec → Spring Boot app: openapi-generator produces interfaces and DTOs, then implement controllers, services, persistence, security, and tests | [SKILL.md](java/openapi-to-application-java-spring-boot/SKILL.md) |

---

### 🐹 Go Engineering (`go/`, 4)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `go-api-design` | HTTP/REST API design: handlers, ServeMux routing, middleware, validation, pagination, idempotency, health checks, error responses, graceful shutdown | [SKILL.md](go/go-api-design/SKILL.md) |
| `golang-grpc` | gRPC conventions: protobuf organization, interceptors, status codes, TLS/mTLS, bufconn tests, streaming RPCs | [SKILL.md](go/golang-grpc/SKILL.md) |
| `golang-project-layout` | Go layout: cmd / internal / pkg, module and package naming, go.work workspaces, multi-main CLI tools | [SKILL.md](go/golang-project-layout/SKILL.md) |
| `golang-testing` | Go testing: table-driven tests, testify, parallel tests, fuzzing, fixtures, goleak, snapshots, coverage, integration tests | [SKILL.md](go/golang-testing/SKILL.md) |

---

### 🔒 Security (`security/`, 6)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `fastapi-api-security-authentication` | Add allowlists, Bearer JWT, and role/object permissions to an existing FastAPI CRUD project; stops to ask when prerequisites fail | [SKILL.md](security/fastapi-api-security-authentication/SKILL.md) |
| `go-security-audit` | Read-only Go security review: input validation, SQL/command injection, SSRF, path traversal, auth, secrets, crypto, OWASP Top 10 | [SKILL.md](security/go-security-audit/SKILL.md) |
| `golang-continuous-integration` | Go CI/CD: GitHub Actions test / lint / SAST / coverage / dependency-scan jobs, Dependabot, Renovate, GoReleaser | [SKILL.md](security/golang-continuous-integration/SKILL.md) |
| `security-audit` | Audit existing code for broken access control, injection, XSS, SSRF, authentication and JWTs, secrets, deserialization, uploads, dependencies, and logs | [README](security/security-audit/README.md) |
| `spring-boot-testing` | Spring Boot test technique selection: slices, Testcontainers `@ServiceConnection`, Failsafe, MockitoBean, JUnit / AssertJ | [SKILL.md](security/spring-boot-testing/SKILL.md) |
| `spring-security` | Configure and review Spring Security 6/7: SecurityFilterChain lambda DSL, method security, OAuth2 resource server, CSRF/CORS, MockMvc security tests | [SKILL.md](security/spring-security/SKILL.md) |

> `security-audit` candidate scan: `python security/security-audit/scripts/scan_sinks.py <project-root>` — a hit is not a conclusion. Reports never include attack steps or raw secrets. Adapted from [developer-agent-skills/security-audit](https://github.com/reddygopalkrishna/developer-agent-skills/blob/main/skills/security-audit/SKILL.md) (MIT); see `NOTICE`.

---

### 🧰 Standalone & General Skills

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `dsh-plugin-starter` | Turn a one-line brief or prototype into a DSH plugin starter project for four plugin types, with a built-in developer guide | [README](dsh-plugin-starter/README.md) |
| `common-website-design` | Natural-language website brief → framework-agnostic static HTML design prototype (multi-page HTML + shared styles + `site-manifest.json`) | [README](.dsh/skills/common-website-design/README.md) |
| `it-requirement-analysis` | Business request → implementable PRD, user stories, functional and non-functional requirements, risks, and acceptance criteria | See directories below |
| `prd-html-skill` | PRD / requirement note / page list → clickable multi-page HTML prototype, including a single-file offline bundle | [README](.cursor/skills/prd-html-skill/README.md) |
| `supervisor-skills` | 12 research skills covering idea evaluation, literature review, paper writing, pre-submission review, and rebuttal | [Chinese guide](research/supervisor-skills/README.zh-CN.md) |

- `common-website-design` is installed in `.workbuddy/skills/` and `.dsh/skills/`; `it-requirement-analysis` in `.cursor/skills/`, `.dsh/skills/`, and `.workbuddy/skills/`; `prd-html-skill` in `.cursor/skills/` and `.dsh/skills/`
- The 12 research skills must be **installed as one group** (they reference each other); most are pure prompts, while `drawio-reconstruction` additionally needs Python scripts and the draw.io CLI
- ⚠️ `supervisor-skills` is **CC BY-NC-SA 4.0** (non-commercial, share-alike) and **not covered by this repository's MIT terms**. Read [`references/PROVENANCE.md`](research/supervisor-skills/references/PROVENANCE.md) before commercial use
- `.codebuddy/skills/` and `.agents/skills/` each contain 20 superpowers-zh general skills (brainstorming, TDD, systematic-debugging, writing-plans, etc.) for CodeBuddy / Agent workflows

---

## 🏗️ Repository Structure

```text
ncepu_ideal-skills/
├── 📄 README.md / README.en.md / CODEBUDDY.md
├── 📁 .docs/                                       # IDE setup guides + design notes + plans/ specs/ images/
├── 📁 sql-to/                                      # 🏭 SQL -> backend scaffolds (4 skills, README + SKILL + resources/)
│   ├── sql-to-fastapi-restfulapi-scaffold/         # ⚡ also docs/
│   ├── sql-to-flask-restfulapi-scaffold/           # 🐍
│   ├── sql-to-springboot-restfulapi-scaffold/      # ☕
│   └── sql-to-gin-restfulapi-scaffold/             # 🌀
├── 📁 design/                                      # 🎨 Design / requirements / database (5 skills)
│   ├── database-schema-designer/                   # README + SKILL + NOTICE + LICENSE + references/
│   ├── frontend-design/                            # SKILL.md
│   ├── huashu-design/                              # README(.en) + SKILL + assets/ demos/ references/ scripts/
│   ├── md-prd-to-html-prototype/                   # README + SKILL + references/ resources/ scripts/
│   └── modern-web-guidance/                        # README + SKILL + ATTRIBUTION + resources/ (209 guides)
├── 📁 prototype-to/                                # 📱 Prototype -> app projects (7 skills, all with resources/)
│   ├── prototype-to-app-uniappx/
│   ├── prototype-to-flutter-app/
│   ├── prototype-to-web(Nuxt UI Starter)/
│   ├── prototype-to-taro-app/
│   ├── prototype-to-ios-native-app(AwesomeSwift)/
│   ├── prototype-to-android-native-app(Fragmject)/
│   └── requirements-to-vue_vben_admin/
├── 📁 go/                                          # 🐹 Go engineering conventions (4 skills, SKILL + references/)
│   ├── go-api-design/
│   ├── golang-grpc/
│   ├── golang-project-layout/
│   └── golang-testing/
├── 📁 java/                                        # ☕ Java engineering conventions (5 skills, SKILL + references/)
│   ├── create-spring-boot-java-project/
│   ├── java-development/
│   ├── java-springboot/
│   ├── java-upgrade/
│   └── openapi-to-application-java-spring-boot/
├── 📁 security/                                    # 🔒 Security (6 skills)
│   ├── fastapi-api-security-authentication/        # SKILL + references/ + scripts/
│   ├── go-security-audit/                          # SKILL + references/
│   ├── golang-continuous-integration/              # SKILL + assets/ evals/ references/
│   ├── security-audit/                             # README + SKILL + NOTICE + references/ + scripts/
│   ├── spring-boot-testing/                        # SKILL + references/
│   └── spring-security/                            # SKILL + references/
├── 📁 research/
│   └── supervisor-skills/                          # 🔬 12 research skills (CC BY-NC-SA 4.0)
│       ├── README.zh-CN.md                         # Chinese guide in this repo
│       ├── references/PROVENANCE.md                # Credit and license notice
│       └── idea-evaluator/, deep-research/, ...    # 12 skill directories
├── 📁 dsh-plugin-starter/                          # 🧩 DSH plugin starter skill
├── 📁 test/                                        # 🧪 Generated samples and fixture data
│   ├── api_security_demo-20260717.sql
│   └── sql-to-{fastapi,flask,gin,springboot}-example/, page-design-showcase/
├── 📁 .codebuddy/skills/ · .agents/skills/         # 🧠 20 superpowers-zh general skills each
├── 📁 .workbuddy/skills/                           # common-website-design / it-requirement-analysis / md-prd-to-html-prototype / diagnosing-superpowers
├── 📁 .cursor/skills/                              # it-requirement-analysis / prd-html-skill
├── 📁 .dsh/skills/                                 # common-website-design / diagnosing-superpowers / it-requirement-analysis / prd-html-skill
└── 📁 .superpowers/sdd/                            # SDD workflow resources
```

---

## 🚀 Quick Start

### 1️⃣ Configure Skills in Your AI Tool

> Choose the configuration guide based on your AI coding assistant:

| 🤖 AI Tool | 📚 Documentation |
| ----------- | ----------- |
| 🚀 **Trae IDE** | [Configuration Guide](.docs/Trea中使用skill配置.md) |
| 💻 **Claude Code** | [Configuration Guide](.docs/claude中使用skill配置.md) |
| ⚡ **GitHub Copilot** | [Configuration Guide](.docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md) |
| 🧩 **CodeBuddy** | [Configuration Guide](.docs/CodeBuddy中使用skill配置.md) |
| 🛠️ **WorkBuddy** | [Prototype-to-App Guide](.docs/workbuddy中使用原型转应用技能.md) |
| 🐋 **DSH (DeepSeek Harness)** | [superpowers Guide](.docs/dsh中使用superpowers技能.md) |
| 🧩 **DSH plugins** | [dsh-plugin-starter Usage Guide](.docs/使用dsh-plugin-starter技能开发DSH插件.md) |
| 🌐 **Modern Web Guidance** | [modern-web-guidance Usage Guide](.docs/使用modern-web-guidance技能编写现代Web前端指南.md) |

> 📝 **Note**: See `.docs/` for detailed guides (also `plans/` and `specs/` design documents).

---

### 2️⃣ Use the Skill

Skills fall into four categories with different inputs.

#### A. Backend: generate API scaffolding from SQL

Provide SQL containing `CREATE TABLE` statements and request the corresponding project scaffolding.

**📥 Example Input**：

```sql
CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT 'Student ID',
    name VARCHAR(100) NOT NULL COMMENT 'Student Name',
    age INT COMMENT 'Age',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT 'Soft delete flag'
);
```

**📤 Skill Generators Reference**：

| ⚡ Skill | 📥 Input | 📤 Output |
| -------- | -------- | ----------- |
| **FastAPI** | SQL CREATE TABLE | Model / Schema / Repository / Service / Resource + test skeleton |
| **Flask** | MySQL DDL | Model / Controller / Service / Resource + project skeleton |
| **Gin** | MySQL DDL | Model / DAO / Service / Resource + project skeleton |
| **Spring Boot** | SQL CREATE TABLE | Entity / Repository / DTO / Service / Controller + project skeleton |

If the tables are not designed yet, use [database-schema-designer](design/database-schema-designer/README.md) to produce a MySQL script, then pass `schema.mysql.sql` to one of the skills above. Those skills do not run DDL. Do not pass a PostgreSQL script to them.

#### B. Frontend: generate a project from a prototype

Hand the AI a **prototype HTML code**, **design screenshot**, or **PRD page list** to produce a runnable project.

**📥 Example Input**：

```text
Here is our prototype (attached HTML code / design screenshot / page list).
Use the prototype-to-flutter-app skill to generate a runnable Flutter project,
restoring layout and interactions with mock data. I'll wire up the backend later.
```

**📤 Skill Generators Reference**：

| ⚡ Skill | 📥 Input | 📤 Output |
| -------- | -------- | ----------- |
| **uni-app x** | prototype code / image / PRD | `.uvue` pages + components + services layers + mock data, runnable in HBuilder |
| **Flutter** | prototype code / image / PRD | feature layers + Repository + mock data; `flutter pub get && flutter run` |
| **Nuxt UI Starter** | prototype code / image / PRD | Nuxt pages and components with mock data |
| **Taro** | prototype code / image / PRD | Taro 4 multi-platform project, Vue3 / React branches |
| **iOS native** | prototype code / image / PRD | SwiftUI four-page templates + MVVM & Combine + SwiftData; run in Xcode after `xcodegen generate` |
| **Android native** | prototype code / image / PRD | Compose four-page templates + single-Activity MVI + Hilt + Room; open in Android Studio |
| **vben admin** | admin requirements | vue-vben-admin routes / CRUD pages / dashboards / mock data |

> 💡 Each skill generates a **data-access seam**: switching to the real backend only requires flipping one flag (`useMock` / `AppContainer` wiring) — page code stays unchanged.

#### C. Reference: retrieve expert guidance before writing code

`modern-web-guidance` does not scaffold a project — it injects expert guides **before** implementation. The Java / Go / security skills provide engineering conventions and review checklists for their domains.

**📥 Example Input**：

```text
Implement a confirmation dialog that closes when the backdrop is clicked,
supports Esc to dismiss, and prevents the page behind from scrolling.
```

**📤 Output**: spec-compliant implementation code + a `### Modern Web Guidance` disclosure section.

`modern-web-guidance` works standalone and can also be overlaid when these skills write browser UI. Their own directories, layers, and component libraries stay in charge:

- [prototype-to-web(Nuxt UI Starter)](<prototype-to/prototype-to-web(Nuxt UI Starter)/README.md>) and [requirements-to-vue_vben_admin](prototype-to/requirements-to-vue_vben_admin/README.md): map the advice onto their existing UI components
- [common-website-design](.dsh/skills/common-website-design/README.md), [prd-html-skill](.cursor/skills/prd-html-skill/README.md), and [md-prd-to-html-prototype](design/md-prd-to-html-prototype/README.md): write the behavior into HTML
- [prototype-to-taro-app](prototype-to/prototype-to-taro-app/README.md) and [prototype-to-app-uniappx](prototype-to/prototype-to-app-uniappx/README.md): H5 only
- [dsh-plugin-starter](dsh-plugin-starter/README.md): dual-face settings pages only

Mini programs, native apps, Flutter, iOS, Android, and backend scaffolds do not use it. The map is section 14 of the usage guide.

```sh
# Also usable as a standalone local CLI (from the design/modern-web-guidance/ directory)
python3 resources/tools/mwg.py search "light dismiss dialog"
python3 resources/tools/mwg.py retrieve "light-dismiss-a-dialog,dialog"
```

> 🌐 Guides ship with the repo: fully offline, no telemetry. After updating `guides/`, run `python3 resources/tools/build_index.py` first.

#### D. Engineering conventions: Java, Go, and security

These skills do not scaffold projects; they provide conventions and checklists when you **write, review, or upgrade** code:

- Java: scaffold with `create-spring-boot-java-project`, write features with `java-springboot`, handle language/build details with `java-development`, migrate versions with `java-upgrade`, implement from OpenAPI with `openapi-to-application-java-spring-boot`
- Go: `golang-project-layout` for directories, `go-api-design` for HTTP APIs, `golang-grpc` for RPC, `golang-testing` for tests; CI and dependency scanning in `golang-continuous-integration`
- Security: `security-audit` for existing code, `fastapi-api-security-authentication` for FastAPI login and permissions, `spring-security` / `spring-boot-testing` for Spring, `go-security-audit` for read-only Go reviews

---

## 🗺️ Roadmap

- [ ] 🔮 Add more enterprise full-stack skills (scaffolding, governance, engineering, etc.)
- [ ] 🧪 Improve validation samples and regression tests
- [ ] 📋 Standardize naming/versioning/documentation conventions for all skills
- [ ] 🎯 Add compile-time regression for the Flutter / uni-app x / iOS / Android skills against real SDKs

---

## 🤝 Contribution

Contributions are welcome, especially new Skills or improvements to existing ones!

**💡 Recommended Workflow**：

1. 🍴 Fork this repository and create a feature branch
2. 📁 Implement the new Skill in its own directory under the matching category (`sql-to/`, `design/`, `prototype-to/`, `go/`, `java/`, `security/`, `research/`), including `SKILL.md`, `README.md`, `resources/`
3. 🧪 Add a runnable sample under `test/`
4. 📝 Update the root README skill list and repository structure
5. 🔄 Submit a Pull Request

---

## 📄 License

There is no single repository-wide LICENSE file at the root; individual skills carry their own licenses (`database-schema-designer`, `security-audit`, `huashu-design`, etc. are MIT; `modern-web-guidance` see `ATTRIBUTION.md`). `research/supervisor-skills` is **CC BY-NC-SA 4.0** and not covered by MIT. Check each skill's license before redistribution.
