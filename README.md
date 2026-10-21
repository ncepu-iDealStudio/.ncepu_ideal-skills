# 🎯 ncepu_ideal-skills

> 企业级服务端接口项目技能（Skills）集合仓库 | 基于资源驱动设计，快速生成符合团队标准的项目脚手架

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.100%2B-orange)
![Flask](https://img.shields.io/badge/Flask-v2.0%2B-purple)
![SpringBoot](https://img.shields.io/badge/Spring%20Boot-2.7%2B-green)

[English](./README.en.md) | 📝 中文

---

## ✨ 特性亮点

- 🔄 **资源驱动架构** - 模板 + 配置 + 规范，完全由资源文件驱动代码生成
- 🚀 **一键生成脚手架** - 从 SQL 表结构自动生成完整项目代码
- 🎨 **多框架支持** - FastAPI / Flask / Gin / Spring Boot 四大主流框架
- 📦 **增量生成** - 支持首次全量生成和后续增量更新
- 🔒 **安全内置** - 自动软删除/硬删除、敏感数据脱敏、输入验证

---

## 🎯 当前技能清单

### 1️⃣ sql-to-fastapi-restfulapi-scaffold

从 SQL `CREATE TABLE` 语句生成完整的 FastAPI RESTful API 项目脚手架

📖 **详细说明**：[查看文档](sql-to-fastapi-restfulapi-scaffold/README.md)

---

### 2️⃣ sql-to-flask-restfulapi-scaffold

从 MySQL DDL 脚本生成 Flask + Flask-RESTful 风格的企业级接口项目脚手架

📖 **详细说明**：[查看文档](sql-to-flask-restfulapi-scaffold/README.md)

---

### 3️⃣ sql-to-springboot-restfulapi-scaffold

从 SQL `CREATE TABLE` 语句生成完整的 Spring Boot RESTful API 项目脚手架

📖 **详细说明**：[查看文档](sql-to-springboot-restfulapi-scaffold/README.md)

---

### 4️⃣ sql-to-gin-restfulapi-scaffold

从 MySQL DDL 脚本生成 Gin + GORM 风格的企业级接口项目脚手架

状态：✅ 已具备一键回归能力（含 context 生成、模板渲染、路由合并、快照校验）

快速命令：

```bash
python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py
```

📖 **详细说明**：[查看文档](sql-to-gin-restfulapi-scaffold/README.md)

---

### 5️⃣ common-website-design

通用网站设计原型生成技能：把自然语言网站需求转成**框架无关的静态 HTML 设计原型**（多页面 HTML + 统一样式 + `site-manifest.json`），可后续拆解为 Vue / Hugo / Hexo / EJS 模板。本技能自身不生成任何框架项目代码。

- 三个正交维度：8 种页面原型 × 内容模型 × 9 个内置设计包（候选确认制）
- 内置验证器 `scripts/validate.py`（Python 标准库，零依赖）
- 成品示例：[test/page-design-showcase](test/page-design-showcase/README.md)
- 安装位置：`.workbuddy/skills/common-website-design/`、`.dsh/skills/common-website-design/`

---

### 6️⃣ it-requirement-analysis

IT 需求分析专家技能：把业务诉求转化为可落地、可验收、可开发的 IT 系统标准，输出 PRD、用户故事、功能/非功能需求、风险依赖与验收标准。AI 应用优先、渐进式输出、选择题式交互。

- 安装位置：`.cursor/skills/it-requirement-analysis/`、`.dsh/skills/it-requirement-analysis/`、`.workbuddy/skills/it-requirement-analysis/`

---

### 7️⃣ prd-html-skill

PRD 驱动的 HTML 交互原型方案（spec 驱动简化版）：MD 规划 + HTML 交付，把 PRD / 需求文档 / 页面清单转成可交互的多页面原型，并支持打包成单文件离线 HTML。

- 安装位置：`.cursor/skills/prd-html-skill/`、`.dsh/skills/prd-html-skill/`

---

### 8️⃣ md-prd-to-html-prototype

读取本地 Markdown 格式 PRD，提取角色、页面、字段与交互逻辑，输出**完全独立的单文件 HTML 原型**（内联全部 CSS/JS，无外部资源，双击即可打开）。

- 安装位置：`.workbuddy/skills/md-prd-to-html-prototype/`

---

## 🏗️ 仓库结构

```
ncepu_ideal-skills/
├── 📄 README.md                                    # 项目说明
├── 📄 README.en.md                                 # 英文说明
├── 📄 CODEBUDDY.md                                 # CodeBuddy 技能说明
├── 📄 .gitignore
├── 📁 docs/                                        # 配置指南与设计方法
│   ├── Trea中使用skill配置.md
│   ├── claude中使用skill配置.md
│   ├── GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md
│   ├── 生成企业级脚手架项目的混合SKILL设计方法.md
│   └── images/                                     # 配置截图
├── 📁 sql-to-fastapi-restfulapi-scaffold/          # ⚡ FastAPI 项目生成技能
│   ├── README.md
│   ├── SKILL.md
│   ├── docs/                                       # 本技能的 IDE 配置说明
│   └── resources/
│       ├── config/
│       ├── specifications/
│       └── templates/
├── 📁 sql-to-flask-restfulapi-scaffold/            # 🐍 Flask 接口项目生成技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       ├── static/
│       └── demo_output/
├── 📁 sql-to-springboot-restfulapi-scaffold/       # ☕ Spring Boot 项目生成技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       └── templates/
├── 📁 sql-to-gin-restfulapi-scaffold/              # 🌀 Gin 接口项目生成技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       ├── static/
│       └── demo_output/
├── 📁 .codebuddy/skills/                           # 🧠 通用技能（CodeBuddy，20 个 superpowers-zh）
├── 📁 .agents/skills/                              # 🧠 通用技能（Agent Skills，20 个 superpowers-zh）
├── 📁 .workbuddy/skills/                           # common-website-design、it-requirement-analysis、md-prd-to-html-prototype
├── 📁 .cursor/skills/                              # it-requirement-analysis、prd-html-skill
├── 📁 .dsh/skills/                                 # common-website-design、it-requirement-analysis、prd-html-skill
└── 📁 test/                                        # 🧪 技能生成示例与样例数据
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

##  快速开始

### 1️⃣ 配置技能到你的 AI 工具

> 根据你使用的 AI 编程助手，选择对应的配置指南：

| 🤖 AI 工具 | 📚 配置文档 
|-----------|-----------|
| 🚀 **Trae IDE** | [配置指南](docs/Trea中使用skill配置.md) |
| 💻 **Claude Code** | [配置指南](docs/claude中使用skill配置.md) |
| ⚡ **GitHub Copilot** | [配置指南](docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md) |
| 🧩 **CodeBuddy** | [配置指南](docs/CodeBuddy中使用skill配置.md) |

> 📝 **提示**：详细配置说明请参考 `docs/` 目录

---

### 2️⃣ 使用技能

在配置好技能后，将包含 `CREATE TABLE` 的 SQL 输入给 AI，要求生成对应的项目脚手架。

**📥 示例输入**：

```sql
CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    age INT COMMENT '年龄',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除'
);
```

**📤 技能生成器对照表**：

| ⚡ 技能 | 📥 输入 | 📤 生成内容 |
|--------|--------|-----------|
| **FastAPI** | SQL CREATE TABLE | Model / Schema / Resource / Service + 项目骨架 |
| **Flask** | MySQL DDL | Model / Controller / Service / Resource + 项目骨架 |
| **Gin** | MySQL DDL | Model / DAO / Service / Resource + 项目骨架 |
| **Spring Boot** | SQL CREATE TABLE | Entity / Repository / DTO / Service / Controller + 项目骨架 |

## 🗺️ 未来规划

- [ ] 🔮 新增更多面向企业后端的技能（脚手架、治理、工程化等）
- [ ] 🧪 完善技能验证样例与回归测试
- [ ] 📋 建立统一技能命名、版本与文档规范

---

## 🤝 贡献指南

欢迎提交新的 Skill 或改进现有 Skill！

**💡 建议流程**：

1. 🍴 Fork 本仓库并新建分支
2. 📁 在独立目录中实现新 Skill（包含 `SKILL.md`、`README.md`、`resources/`）
3. 🧪 补充对应示例到 `test/`
4. 📝 更新根 README 的技能清单
5. 🔄 发起 Pull Request

---

## 📄 许可证

当前仓库未声明许可证文件。建议补充 `LICENSE` 后再对外分发。