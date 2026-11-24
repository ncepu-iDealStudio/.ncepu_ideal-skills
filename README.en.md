# 🎯 ncepu_ideal-skills

> Enterprise Skills Collection | A repository solely for collecting, organizing, categorizing, and continuously improving skills

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

## ✨ Repository Purpose

This repository does **one thing**: collect, organize, categorize, and improve skills. It does not host skill testing, nor does it maintain installed skill copies for individual AI tools.

- 📁 **Categorized by domain**: skills live in `requirements_analysis/`, `design/`, `sql-to/`, `prototype-to/`, `go/`, `java/`, `security/`, `research/`, `others/`, one directory per skill (`SKILL.md` + resources)
- 🧪 **Testing is external**: no test directories or sample artifacts here; skill validation and regression run in a **separate project**
- 🔁 **No tool copies**: no skill copies under `.workbuddy/`, `.cursor/`, `.dsh/`, avoiding drift between duplicates
- 🧩 **Multi-stack**: requirements analysis, database design, backend scaffolds, prototype-to-app, Go / Java conventions, security audits, and research

---

## 🎯 Skill List

Grouped by directory: **38 skills** (`requirements_analysis` 3, `design` 5, `sql-to` 4, `prototype-to` 7, `java` 5, `go` 4, `security` 6, `research` 3, `ppt` 1, `others` 1), plus the `requirements_analysis/spec-kit` toolkit, 20 general workflow skills, and 1 research skill collection (`supervisor-skills`).

### 📋 Requirements Analysis & Design (`requirements_analysis/`, 3 skills)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `brainstorming` | Turn ideas into designs: classify as spike / bounded / architectural; architectural work produces a design spec and requires approval before implementation | [SKILL.md](requirements_analysis/brainstorming/SKILL.md) |
| `it-requirement-analysis` | Business request → PRD, user stories, acceptance criteria, AI solution proposals, feature lists, and implementation plans; choice-based, progressive output | [SKILL.md](requirements_analysis/it-requirement-analysis/SKILL.md) |
| `database-schema-designer` | Natural language or existing schema → engine-correct DDL (PostgreSQL / MySQL first) + `database-design.md` | [README](requirements_analysis/database-schema-designer/README.md) |

> These three form the requirements-side pipeline: `it-requirement-analysis` (business needs) → `brainstorming` (technical design spec) → `database-schema-designer` (data model). The same directory also holds the upstream toolkit `spec-kit/` (spec-driven pipeline, not a skill written in this repo). See [使用说明.md](requirements_analysis/使用说明.md).

---

### 🎨 Design & Frontend (`design/`, 5)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `common-website-design` | Natural-language website brief → framework-agnostic static HTML prototype (multi-page + shared styles + `site-manifest.json`) | [README](design/common-website-design/README.md) |
| `frontend-design` | Visual design guidance: aesthetic direction, typography, avoiding templated defaults; framework-agnostic | [SKILL.md](design/frontend-design/SKILL.md) |
| `huashu-design` | One prompt → high-fidelity HTML prototypes, slides, animation, visualization, design reviews; three directions first (MIT) | [README](design/huashu-design/README.md) |
| `md-prd-to-html-prototype` | Local Markdown PRD → single-file low-fidelity HTML prototype; fields come from the document, gaps are asked first | [README](design/md-prd-to-html-prototype/README.md) |
| `modern-web-guidance` | Reference skill: retrieve from 209 bundled modern Web guides before writing UI; offline, self-contained, Chinese-driven | [README](design/modern-web-guidance/README.md) |

> The guides are verbatim upstream English copies (CC-BY 4.0 / code Apache-2.0); credit in [ATTRIBUTION.md](design/modern-web-guidance/ATTRIBUTION.md). When overlaid with generator skills, those skills still own the layout, layers, and components.

---

### 🏭 SQL → Backend Scaffolds (`sql-to/`, 4)

| Skill | Input → Output | Documentation |
| --- | --- | --- |
| `sql-to-fastapi-restfulapi-scaffold` | SQL `CREATE TABLE` → layered FastAPI scaffold (Model / Schema / Repository / Service / Resource) | [README](sql-to/sql-to-fastapi-restfulapi-scaffold/README.md) |
| `sql-to-flask-restfulapi-scaffold` | MySQL DDL → Flask + Flask-RESTful API scaffold | [README](sql-to/sql-to-flask-restfulapi-scaffold/README.md) |
| `sql-to-springboot-restfulapi-scaffold` | SQL `CREATE TABLE` → layered Spring Boot scaffold, exports OpenAPI docs | [README](sql-to/sql-to-springboot-restfulapi-scaffold/README.md) |
| `sql-to-gin-restfulapi-scaffold` | MySQL DDL → layered Gin + GORM scaffold | [README](sql-to/sql-to-gin-restfulapi-scaffold/README.md) |

> These skills consume MySQL `CREATE TABLE` and do not execute DDL. Use [`database-schema-designer`](requirements_analysis/database-schema-designer/README.md) first when tables are not designed yet.

---

### 📱 Prototype / Requirements → App Projects (`prototype-to/`, 7)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `prototype-to-app-uniappx` | Prototype → uni-app x vapor-mode (TS) project with `.uvue` pages, layered services, mock data | [README](prototype-to/prototype-to-app-uniappx/README.md) |
| `prototype-to-flutter-app` | Prototype → Flutter project with feature layers, Repository, `ChangeNotifier` | [README](prototype-to/prototype-to-flutter-app/README.md) |
| `prototype-to-web(Nuxt UI Starter)` | Prototype → Nuxt UI Starter project | [README](<prototype-to/prototype-to-web(Nuxt UI Starter)/README.md>) |
| `prototype-to-taro-app` | Prototype → Taro 4 multi-platform project, Vue3 / React branches | [README](prototype-to/prototype-to-taro-app/README.md) |
| `prototype-to-ios-native-app(AwesomeSwift)` | Prototype → native SwiftUI iOS project (XcodeGen / MVVM + Combine) | [README](<prototype-to/prototype-to-ios-native-app(AwesomeSwift)/README.md>) |
| `prototype-to-android-native-app(Fragmject)` | Prototype → native Compose Android project (single-Activity MVI / Hilt) | [README](<prototype-to/prototype-to-android-native-app(Fragmject)/README.md>) |
| `requirements-to-vue_vben_admin` | Admin requirements → runnable vue-vben-admin (vben5) scaffold | [README](prototype-to/requirements-to-vue_vben_admin/README.md) |

---

### ☕ Java Engineering (`java/`, 5)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `create-spring-boot-java-project` | Scaffold a new Spring Boot project from start.spring.io (Maven / Gradle) | [SKILL.md](java/create-spring-boot-java-project/SKILL.md) |
| `java-development` | Framework-free daily Java: Maven / Gradle, JDK-version idioms, logging, concurrency, static analysis, packaging | [SKILL.md](java/java-development/SKILL.md) |
| `java-springboot` | Write and review application code in an existing Spring Boot 3/4 project | [SKILL.md](java/java-springboot/SKILL.md) |
| `java-upgrade` | Upgrade a Java project to a newer JDK (11→17→21→25) and adopt new features | [SKILL.md](java/java-upgrade/SKILL.md) |
| `openapi-to-application-java-spring-boot` | OpenAPI 3 spec → Spring Boot application (spec-first) | [SKILL.md](java/openapi-to-application-java-spring-boot/SKILL.md) |

---

### 🐹 Go Engineering (`go/`, 4)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `go-api-design` | HTTP/REST API design: handlers, routing, middleware, validation, idempotency, graceful shutdown | [SKILL.md](go/go-api-design/SKILL.md) |
| `golang-grpc` | gRPC conventions: protobuf organization, interceptors, status codes, TLS/mTLS, streaming RPCs | [SKILL.md](go/golang-grpc/SKILL.md) |
| `golang-project-layout` | Go layout: cmd / internal / pkg, module naming, go.work workspaces | [SKILL.md](go/golang-project-layout/SKILL.md) |
| `golang-testing` | Go testing: table-driven, testify, parallel, fuzzing, goleak, coverage | [SKILL.md](go/golang-testing/SKILL.md) |

---

### 🔒 Security (`security/`, 6)

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `fastapi-api-security-authentication` | Add allowlists, Bearer JWT, and role/object permissions to an existing FastAPI CRUD project | [SKILL.md](security/fastapi-api-security-authentication/SKILL.md) |
| `go-security-audit` | Read-only Go security review: injection, SSRF, auth, secrets, OWASP Top 10 | [SKILL.md](security/go-security-audit/SKILL.md) |
| `golang-continuous-integration` | Go CI/CD: GitHub Actions, Dependabot, GoReleaser | [SKILL.md](security/golang-continuous-integration/SKILL.md) |
| `security-audit` | Audit existing code: broken access control, injection, XSS, SSRF, JWTs, secrets, uploads, dependencies | [README](security/security-audit/README.md) |
| `spring-boot-testing` | Spring Boot test technique selection: slices, Testcontainers, Failsafe | [SKILL.md](security/spring-boot-testing/SKILL.md) |
| `spring-security` | Configure and review Spring Security 6/7: SecurityFilterChain, OAuth2, MockMvc security tests | [SKILL.md](security/spring-security/SKILL.md) |

---

### 🧩 Other Skills

| Skill | Purpose | Documentation |
| --- | --- | --- |
| `dsh-plugin-starter` (`others/`) | One-line brief or prototype → DSH plugin starter project for four plugin types, with a developer guide | [README](others/dsh-plugin-starter/README.md) |
| `gorden-ppt-skill` (`ppt/`) | 21 built-in Chinese PPTX templates + non-destructive text-only editing with python-pptx: work reports, job reviews, teaching slides, business proposals, data visualization | [SKILL.md](ppt/gorden-ppt-skill/SKILL.md) |
| `supervisor-skills` (`research/`) | 12 research skills (idea evaluation, literature review, paper writing, pre-submission review, rebuttal) | [Chinese guide](research/supervisor-skills/README.zh-CN.md) |
| `research-weave` (`research/`) | Paper prospecting: decide which papers deserve deep reading; Scout / Map / Update modes produce reading recommendations, a traceable evidence ledger, and search records | [SKILL.md](research/research-weave/SKILL.md) |
| `best-paper-writing` (`research/`) | Award-paper-style writing: abstract / intro / method / experiments / figures distilled from 60 CVPR / ICCV / NeurIPS papers, with a built-in draft checker | [SKILL.md](research/best-paper-writing/skills/bestpaper-writing/SKILL.md) · [upstream README](research/best-paper-writing/README.md) |
| `superpowers-zh` (`requirements_analysis/`) | 20 general workflow skills (brainstorming, writing-plans, executing-plans, subagent-driven-development, systematic-debugging, TDD, etc.), ready to install into any Skill-capable AI tool | Directory: `requirements_analysis/superpowers-zh/` |

- The 12 research skills must be **installed as one group** (they reference each other); most are pure prompts, while `drawio-reconstruction` also needs Python scripts and the draw.io CLI
- ⚠️ `supervisor-skills` is **CC BY-NC-SA 4.0** (non-commercial, share-alike) and **not covered by MIT**. Read [`references/PROVENANCE.md`](research/supervisor-skills/references/PROVENANCE.md) before commercial use
- `research-weave` is **MIT** licensed and self-contained (validation script uses only the Python standard library); it complements `supervisor-skills/deep-research`
- `best-paper-writing` is mainly **CC BY 4.0** (attribution required, commercial use allowed); short excerpted sentences in its exemplars are **not** licensed for copying into new papers, and the base skill is MIT. See [`references/PROVENANCE.md`](research/best-paper-writing/references/PROVENANCE.md)
- ⚠️ `gorden-ppt-skill` code is **MIT**, but the visual assets in `templates/` are **non-commercial and must not be redistributed** (copyright stays with the original template authors) — personal study and research only, **no commercial use**. Adapted for WorkBuddy (optional auto-update, Windows/dependency notes); see [`references/PROVENANCE.md`](ppt/gorden-ppt-skill/references/PROVENANCE.md)

---

## 🏗️ Repository Structure

```text
ncepu_ideal-skills/
├── 📄 README.md / README.en.md / CODEBUDDY.md
├── 📁 .docs/                                       # Setup guides + design notes + plans/ specs/ images/
├── 📁 requirements_analysis/                       # 📋 Requirements analysis & design (3 skills + spec-kit + superpowers-zh)
│   ├── brainstorming/                              # SKILL + spec-review prompt + scripts + visual-companion
│   ├── it-requirement-analysis/                    # SKILL + references/ (PRD / user stories / process)
│   ├── database-schema-designer/                   # README + SKILL + NOTICE + LICENSE + references/
│   ├── spec-kit/                                   # GitHub Spec Kit toolkit (not authored here)
│   ├── superpowers-zh/                             # 🧠 20 general workflow skills (single source of truth)
│   ├── 使用说明.md
│   └── 关于开源需求分析技能.md
├── 📁 design/                                      # 🎨 Design & frontend (5 skills)
│   ├── common-website-design/                      # README + SKILL + PLAN + designs/ references/ scripts/
│   ├── frontend-design/                            # SKILL.md
│   ├── huashu-design/                              # README(.en) + SKILL + assets/ demos/ references/ scripts/
│   ├── md-prd-to-html-prototype/                   # README + SKILL + references/ resources/ scripts/
│   └── modern-web-guidance/                        # README + SKILL + ATTRIBUTION + resources/ (209 guides)
├── 📁 sql-to/                                      # 🏭 SQL -> backend scaffolds (4 skills, README + SKILL + resources/)
│   ├── sql-to-fastapi-restfulapi-scaffold/
│   ├── sql-to-flask-restfulapi-scaffold/
│   ├── sql-to-springboot-restfulapi-scaffold/
│   └── sql-to-gin-restfulapi-scaffold/
├── 📁 prototype-to/                                # 📱 Prototype / requirements -> app projects (7 skills)
│   ├── prototype-to-app-uniappx/
│   ├── prototype-to-flutter-app/
│   ├── prototype-to-web(Nuxt UI Starter)/
│   ├── prototype-to-taro-app/
│   ├── prototype-to-ios-native-app(AwesomeSwift)/
│   ├── prototype-to-android-native-app(Fragmject)/
│   └── requirements-to-vue_vben_admin/
├── 📁 go/                                          # 🐹 Go engineering conventions (4 skills)
│   ├── go-api-design/ / golang-grpc/
│   └── golang-project-layout/ / golang-testing/
├── 📁 java/                                        # ☕ Java engineering conventions (5 skills)
│   ├── create-spring-boot-java-project/ / java-development/ / java-springboot/
│   └── java-upgrade/ / openapi-to-application-java-spring-boot/
├── 📁 security/                                    # 🔒 Security (6 skills)
│   ├── fastapi-api-security-authentication/ / go-security-audit/
│   ├── golang-continuous-integration/ / security-audit/
│   └── spring-boot-testing/ / spring-security/
├── 📁 research/
│   ├── best-paper-writing/                         # 🏆 Award-paper-style writing (CC BY 4.0, CVPR templates & corpus)
│   ├── research-weave/                             # 🧵 Paper prospecting skill (MIT, SKILL + references/ + scripts/)
│   └── supervisor-skills/                          # 🔬 12 research skills (CC BY-NC-SA 4.0)
├── 📁 ppt/                                         # 📊 PPT generation (1 skill)
│   └── gorden-ppt-skill/                           # 🎨 21 Chinese-template PPT generation (code MIT / templates non-commercial)
├── 📁 others/
│   └── dsh-plugin-starter/                         # 🧩 DSH plugin starter skill
```

> Note: this repository contains **no** `test/` sample directory and no `.codebuddy/`, `.agents/`, `.workbuddy/`, `.cursor/`, or `.dsh/` tool-specific skill copies. Those tests and installed copies have been moved out; validation happens in a separate project. The general workflow skills live solely in `requirements_analysis/superpowers-zh/` and are installed into each tool as needed.

---

## Quick Start

### 1️⃣ Load a skill into your AI tool

Refer to the setup guides for how each tool loads skills from this repository:

| 🤖 AI Tool | 📚 Documentation |
| ----------- | ----------- |
| 🚀 **Trae IDE** | [Configuration Guide](.docs/Trea中使用skill配置.md) |
| 💻 **Claude Code** | [Configuration Guide](.docs/claude中使用skill配置.md) |
| ⚡ **GitHub Copilot** | [Configuration Guide](.docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md) |
| 🧩 **CodeBuddy** | [Configuration Guide](.docs/CodeBuddy中使用skill配置.md) · [Taro skill guide](.docs/在Codebuddy插件中使用prototype-to-taro-app技能指南.md) |
| 🛠️ **WorkBuddy** | [Research skills guide](.docs/如何在workbuddy中使用科研技能集supervisor-skills.md) · [research-weave guide](.docs/如何在workbuddy中使用科学研究技能research-weave.md) |
| 🧠 **DSH + Superpowers** | [Requirements tutorial](.docs/dsh中使用superpowers技能.md) |
| 🧠 **Cursor + Superpowers** | [Requirements tutorial](.docs/如何在cursor中使用Superpowers技能进行项目的需求分析.md) |

> 📝 More notes in `.docs/` (including `plans/` and `specs/`). Point the tool directly at the skill directory in this repository — do not copy skills into tool folders to create duplicates.

---

### 2️⃣ Typical workflows

#### A. From business requirements to a runnable backend

```text
it-requirement-analysis (PRD / acceptance criteria)
   → brainstorming (technical design spec)
   → database-schema-designer (data model + MySQL DDL)
   → sql-to-* skills (generate FastAPI / Flask / Gin / Spring Boot scaffold)
```

#### B. From a prototype to a frontend project

Hand prototype HTML, design screenshots, or a PRD page list to a `prototype-to-*` skill to generate a uni-app x / Flutter / Nuxt / Taro / iOS / Android / vben admin project with mock data ready to preview; later switch the data-access seam to a real backend.

#### C. Conventions and reviews

- Before coding: `modern-web-guidance` (Web UI), `frontend-design` (visual), `java-*` / `go-*` (engineering conventions)
- After coding: `security-audit`, `go-security-audit`, `spring-security` for security review and hardening
- Requirements-side and engineering-side skills work standalone or in sequence; this repository does not execute tests

---

## 🗺️ Roadmap

- [ ] 🔮 Keep adding and refining skills by domain, with clear categorization
- [ ] 📋 Standardize naming, versioning, and documentation across all skills
- [ ] 🔄 Keep in sync with how AI tools load skills (without introducing copies)

---

## 🤝 Contribution

Contributions are welcome, especially new Skills or improvements to existing ones!

**💡 Recommended Workflow**：

1. 🍴 Fork this repository and create a feature branch
2. 📁 Add the new skill under the matching category (`requirements_analysis/`, `design/`, `sql-to/`, `prototype-to/`, `go/`, `java/`, `security/`, `research/`, `others/`), including `SKILL.md`, `README.md`, and needed resources
3. 📝 Update the root README skill list and repository structure
4. 🔄 Submit a Pull Request
5. 🧪 Run skill tests and regression in a separate testing project — do not add test directories or sample artifacts to this repository

---

## 📄 License

There is no single repository-wide LICENSE file at the root; individual skills carry their own licenses (`database-schema-designer`, `security-audit`, `huashu-design`, etc. are MIT; `modern-web-guidance` see `ATTRIBUTION.md`). `research/supervisor-skills` is **CC BY-NC-SA 4.0** and not covered by MIT. Check each skill's license before redistribution.
