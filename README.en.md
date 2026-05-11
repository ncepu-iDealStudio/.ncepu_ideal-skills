# ncepu_ideal-skills

A collection of reusable backend engineering skills for enterprise projects.  
The first production-ready skill is already implemented: `sql-to-fastapi-scaffold`, which generates layered FastAPI project code from SQL table definitions.

中文版: [README.md](README.md)

## Goals

- Build reusable backend skills for team-wide delivery.
- Package best practices as Skills using templates, configurations, and standards.
- Grow into a multi-skill repository (database, API, architecture, engineering productivity, etc.).

## Current Skills

### 1) sql-to-fastapi-scaffold (implemented)

Location: `sql-to-fastapi-scaffold/`

What it does:

- Parses SQL `CREATE TABLE` statements
- Generates layered FastAPI code (Model / Schema / Resource / Service)
- Produces full project skeleton on first run, then supports incremental table-based generation
- Supports automatic soft-delete / hard-delete strategy
- Includes type mapping, naming rules, validation rules, and sensitive data masking rules

Details:

- Skill guide: `sql-to-fastapi-scaffold/README.md`
- Skill definition: `sql-to-fastapi-scaffold/SKILL.md`

## Repository Structure

```text
ncepu_ideal-skills/
├── README.md
├── README.en.md
├── docs/
│   └── Trea中使用skill配置.md
├── sql-to-fastapi-scaffold/
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       │   ├── naming_rules.json
│       │   └── type_mappings.json
│       ├── specifications/
│       │   └── coding_standards.md
│       └── templates/
│           ├── project_structure/
│           └── layers/
└── test/
	└── sql-to-fastapi-example/
```

Notes:

- `sql-to-fastapi-scaffold/resources/`: core skill assets (templates, mapping rules, standards)
- `test/sql-to-fastapi-example/`: generated sample project for validation
- `docs/`: usage and integration notes

## Quick Start

### 1) Use the skill

Provide SQL containing `CREATE TABLE` statements and ask the skill to scaffold a FastAPI API project.

Example (simplified):

```sql
CREATE TABLE student (
	studentID VARCHAR(20) PRIMARY KEY COMMENT 'Student ID',
	name VARCHAR(100) NOT NULL COMMENT 'Student Name',
	age INT COMMENT 'Age',
	is_deleted BOOLEAN DEFAULT FALSE COMMENT 'Soft delete flag'
);
```

### 2) Run the generated sample project

Sample path: `test/sql-to-fastapi-example/`

```bash
cd test/sql-to-fastapi-example
pip install -r requirements.txt
uvicorn start:app --reload
```

Default endpoints:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 3) Configure skill in Trae

See: `docs/Trea中使用skill配置.md`

## Design Approach

This repository follows a resource-driven approach:

- Structure is generated from templates (`resources/templates/`)
- Rules are controlled by configs (`resources/config/`)
- Output quality is constrained by standards (`resources/specifications/`)

Benefits:

- Maintainable: centralized and traceable rules
- Extensible: new skills can be added independently
- Reusable: one skill can serve multiple project contexts

## Roadmap

- Add more enterprise backend skills
- Improve validation samples and regression checks
- Standardize naming/versioning/documentation conventions for all skills

## Contribution

Contributions are welcome, especially new Skills or improvements to existing ones.

Recommended workflow:

1. Fork and create a feature branch
2. Add your skill in an isolated folder (`SKILL.md`, `README.md`, `resources/`)
3. Add a runnable sample under `test/`
4. Update root README skill list
5. Submit a Pull Request

## License

No license file is currently declared. Add a `LICENSE` before external distribution.
