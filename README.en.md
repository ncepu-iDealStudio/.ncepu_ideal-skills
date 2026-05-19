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
- 🎨 **Multi-framework Support** - FastAPI / Flask / Spring Boot three major frameworks
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

## 🏗️ Repository Structure

```
ncepu_ideal-skills/
├── 📄 README.md                                    # Project documentation
├── 📄 README.en.md                                 # English documentation
├── 📄 .gitignore
├── 📁 docs/                                        # Configuration guides
│   ├── Trea中使用skill配置.md
│   ├── claude中使用skill配置.md
│   └── GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md
├── 📁 sql-to-fastapi-restfulapi-scaffold/         # ⚡ FastAPI skill
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       └── templates/
├── 📁 sql-to-flask-restfulapi-scaffold/           # 🐍 Flask skill
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
├── 📁 sql-to-springboot-restfulapi-scaffold/      # ☕ Spring Boot skill
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
└── 📁 test/                                        # 🧪 Generated example projects
    ├── sql-to-fastapi-example/
    ├── sql-to-flask-exmaple.com/
    └── sql-to-springboot-example/
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

| ⚡ Skill | 📥 Input | 
|--------|-----------|
| **FastAPI** | SQL CREATE TABLE | Model / Schema / Resource / Service + Project Skeleton |
| **Flask** | MySQL DDL | Model / Controller / Service / Resource + Project Skeleton |
| **Spring Boot** | SQL CREATE TABLE | Entity / Repository / DTO / Service / Controller + Project Skeleton |

---

### 3️⃣ Run Generated Example Projects

After code generation, you can run the example projects for verification:

| ⚡ Skill | 📂 Example Directory | 🚀 Start Command |
|--------|-----------|-----------|
| **FastAPI** | `test/sql-to-fastapi-example/` | `uvicorn start:app --reload` |
| **Flask** | `test/sql-to-flask-exmaple.com/` | `python manage.py runserver` |
| **Spring Boot** | `test/sql-to-springboot-example/` | `mvn spring-boot:run` |

**🌐 Access URLs**：

- 📖 **Swagger UI**: `http://127.0.0.1:8000/docs`
- 📚 **ReDoc**: `http://127.0.0.1:8000/redoc`

---

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
