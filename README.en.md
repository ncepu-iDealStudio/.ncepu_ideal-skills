# 🎯 ncepu_ideal-skills

> Enterprise Backend Engineering Skills Collection | Resource-driven design for rapid scaffolding of standardized project code

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.100%2B-orange)
![Flask](https://img.shields.io/badge/Flask-v2.0%2B-purple)
![SpringBoot](https://img.shields.io/badge/Spring%20Boot-2.7%2B-green)

[中文](./README.md) | 📝 English

---

## ✨ Key Features

- 🔄 **Resource-driven Architecture** - Templates + Configurations + Standards, completely driven by resource files
- 🚀 **One-click Scaffolding** - Auto-generate complete project code from SQL table definitions
- 🎨 **Multi-framework Support** - FastAPI / Flask / Gin / Spring Boot four major frameworks
- 📦 **Incremental Generation** - Full initial generation + incremental updates
- 🔒 **Built-in Security** - Auto soft-delete/hard-delete, sensitive data masking, input validation

---

## 🎯 Current Skills

### 1️⃣ sql-to-fastapi-restfulapi-scaffold

Generate complete FastAPI RESTful API project scaffolding from SQL `CREATE TABLE` statements

📖 **Details**：[View Documentation](sql-to-fastapi-restfulapi-scaffold/README.md)

---

### 2️⃣ sql-to-flask-restfulapi-scaffold

Generate Flask + Flask-RESTful enterprise API project scaffolding from MySQL DDL scripts

📖 **Details**：[View Documentation](sql-to-flask-restfulapi-scaffold/README.md)

---

### 3️⃣ sql-to-springboot-restfulapi-scaffold

Generate complete Spring Boot RESTful API project scaffolding from SQL `CREATE TABLE` statements

📖 **Details**：[View Documentation](sql-to-springboot-restfulapi-scaffold/README.md)

---

### 4️⃣ sql-to-gin-restfulapi-scaffold

Generate Gin + GORM enterprise API project scaffolding from MySQL DDL scripts

Status: ✅ Production-ready workflow with one-command regression (context generation, template rendering, router merge, snapshot checks)

Quick command:

```bash
python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py
```

📖 **Details**：[View Documentation](sql-to-gin-restfulapi-scaffold/README.md)

---

### 5️⃣ common-website-design

Turn a natural-language website brief into a framework-agnostic static HTML design prototype (multi-page HTML, shared styles, and `site-manifest.json`). It does not generate Vue, Hugo, Hexo, or EJS project code.

- Installed at `.workbuddy/skills/common-website-design/` and `.dsh/skills/common-website-design/`
- Sample output: [test/page-design-showcase](test/page-design-showcase/README.md)

---

### 6️⃣ it-requirement-analysis

Turn a business request into an implementable IT specification: PRD, user stories, functional and non-functional requirements, risks, and acceptance criteria.

- Installed at `.cursor/skills/it-requirement-analysis/`, `.dsh/skills/it-requirement-analysis/`, and `.workbuddy/skills/it-requirement-analysis/`

---

### 7️⃣ prd-html-skill

Turn a PRD, requirement note, or page list into a clickable multi-page HTML prototype, including a single-file offline HTML bundle.

- Installed at `.cursor/skills/prd-html-skill/` and `.dsh/skills/prd-html-skill/`

---

### 8️⃣ md-prd-to-html-prototype

Read a local Markdown PRD and emit a self-contained single-file HTML prototype (inlined CSS and JS, no external assets).

- Installed at `.workbuddy/skills/md-prd-to-html-prototype/`

---

## 🏗️ Repository Structure

```
ncepu_ideal-skills/
├── 📄 README.md                                    # Project documentation
├── 📄 README.en.md                                 # English documentation
├── 📄 CODEBUDDY.md                                 # CodeBuddy skill notes
├── 📄 .gitignore
├── 📁 docs/                                        # Guides and design notes
│   ├── Trea中使用skill配置.md
│   ├── claude中使用skill配置.md
│   ├── GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md
│   ├── 生成企业级脚手架项目的混合SKILL设计方法.md
│   └── images/                                     # Setup screenshots
├── 📁 sql-to-fastapi-restfulapi-scaffold/          # ⚡ FastAPI skill
│   ├── README.md
│   ├── SKILL.md
│   ├── docs/
│   └── resources/
│       ├── config/
│       ├── specifications/
│       └── templates/
├── 📁 sql-to-flask-restfulapi-scaffold/            # 🐍 Flask skill
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       ├── static/
│       └── demo_output/
├── 📁 sql-to-springboot-restfulapi-scaffold/       # ☕ Spring Boot skill
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       └── templates/
├── 📁 sql-to-gin-restfulapi-scaffold/              # 🌀 Gin skill
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       ├── static/
│       └── demo_output/
├── 📁 .codebuddy/skills/                           # 20 superpowers-zh skills
├── 📁 .agents/skills/                              # 20 superpowers-zh skills
├── 📁 .workbuddy/skills/                           # common-website-design, it-requirement-analysis, md-prd-to-html-prototype
├── 📁 .cursor/skills/                              # it-requirement-analysis, prd-html-skill
├── 📁 .dsh/skills/                                 # common-website-design, it-requirement-analysis, prd-html-skill
└── 📁 test/                                        # Generated samples and fixture SQL
    ├── api_security_demo-20260717.sql
    ├── sql-to-fastapi-example/
    ├── sql-to-flask-example/
    ├── sql-to-gin-example/
    ├── sql-to-springboot-example/
    └── page-design-showcase/
        ├── gallery/
        └── sites/
```

---

## 🚀 Quick Start

### 1️⃣ Configure Skills in Your AI Tool

> Choose the configuration guide based on your AI coding assistant:

| 🤖 AI Tool | 📚 Documentation | ✨ Features |
|-----------|-----------|--------|
| 🚀 **Trae IDE** | [Configuration Guide](docs/Trea中使用skill配置.md) |
| 💻 **Claude Code** | [Configuration Guide](docs/claude中使用skill配置.md) |
| ⚡ **GitHub Copilot** | [Configuration Guide](docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md) |

> 📝 **Note**: Please refer to the `docs/` directory for detailed configuration guides

---

### 2️⃣ Use the Skill

After configuring the skill, provide SQL containing `CREATE TABLE` statements and request generation of the corresponding project scaffolding.

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
|--------|-----------|-----------|
| **FastAPI** | SQL CREATE TABLE | Model / Schema / Resource / Service + Project Skeleton |
| **Flask** | MySQL DDL | Model / Controller / Service / Resource + Project Skeleton |
| **Gin** | MySQL DDL | Model / DAO / Service / Resource + Project Skeleton |
| **Spring Boot** | SQL CREATE TABLE | Entity / Repository / DTO / Service / Controller + Project Skeleton |


## 🗺️ Roadmap

- [ ] 🔮 Add more enterprise backend skills (scaffolding, governance, engineering, etc.)
- [ ] 🧪 Improve validation samples and regression tests
- [ ] 📋 Standardize naming/versioning/documentation conventions for all skills

---

## 🤝 Contribution

Contributions are welcome, especially new Skills or improvements to existing ones!

**💡 Recommended Workflow**：

1. 🍴 Fork this repository and create a feature branch
2. 📁 Implement new Skill in an isolated folder (`SKILL.md`, `README.md`, `resources/`)
3. 🧪 Add a runnable sample under `test/`
4. 📝 Update root README skill list
5. 🔄 Submit a Pull Request

---

## 📄 License

No license file is currently declared. Add a `LICENSE` before external distribution.
