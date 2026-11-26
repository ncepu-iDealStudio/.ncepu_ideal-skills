# 🎯 ncepu_ideal-skills

> 由华北电力大学iDeal工作室开发管理并维护
> 企业级技能（Skills）集合仓库 | 这是一个收集、整理、分类存放的仓库，包含工作室自己创建的与软件开发生命周期相关的技能仓库，按领域分门别类存放：

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

## ✨ 仓库定位

本仓库**只做一件事**：收集、整理、分类存放并持续优化各种技能。它不承载技能在AI工具中的测试与验证，技能测试可以由用户自行，参照帮助文档在独立项目中进行。

- 📁 **按领域分类**：技能按用途归入 `requirements_analysis/`、`design/`、`sql-to/`、`prototype-to/`、`go/`、`java/`、`security/`、`ppt/`、`research/`、`info-research/`、`others/` 等目录，每个技能一个独立目录（`SKILL.md` + 资源）
- 🧪 **测试外置**：本仓库不含测试目录与样例产物；技能的验证与回归测试在**独立项目**中进行
- 🔁 **无工具副本**：不再向 `.workbuddy/`、`.cursor/`、`.dsh/` 等 AI 工具目录拷贝技能副本，避免多份副本不同步
- 🧩 **多技术栈**：覆盖需求分析、数据库设计、后端脚手架、前端原型转工程、Go / Java 工程规范、安全审计与科研等场景

---

## 🎯 技能清单

技能按目录分类，下文列出主要技能与合集，另有 `requirements_analysis/spec-kit` 工具包、20 个通用工作流技能、1 组科研技能集（`supervisor-skills`）与 1 组计算机科研实证精选集（`auto-empirical-research`，6 项技能）。

### 📋 需求分析与设计（`requirements_analysis/`，3 个技能）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `brainstorming` | 把想法转成设计：先按探路 / 有界 / 架构级分类，架构级产出设计规格并经用户批准后才进入实现 | [SKILL.md](requirements_analysis/brainstorming/SKILL.md) |
| `it-requirement-analysis` | 业务诉求 → PRD、用户故事、验收标准、AI 方案建议、功能清单与实施计划；选择题式交互、渐进式输出 | [SKILL.md](requirements_analysis/it-requirement-analysis/SKILL.md) |
| `database-schema-designer` | 自然语言或已有库结构 → 分引擎 DDL（PostgreSQL / MySQL 为主）+ `database-design.md` | [README](requirements_analysis/database-schema-designer/README.md) |

> 这三个技能串起来就是需求侧主流程：`it-requirement-analysis`（业务需求）→ `brainstorming`（技术设计规格）→ `database-schema-designer`（数据模型设计）。同目录还有开源工具包 `spec-kit/`（规格驱动流水线，不是本仓库自写技能）。用法见 [使用说明](requirements_analysis/使用说明.md)。

---

### 🎨 设计与前端（`design/`，5 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `common-website-design` | 自然语言网站需求 → 框架无关的静态 HTML 设计原型（多页面 + 统一样式 + `site-manifest.json`） | [README](design/common-website-design/README.md) |
| `frontend-design` | 前端视觉设计指导：审美方向、排版、避免模板化默认样式，与具体框架无关 | [SKILL.md](design/frontend-design/SKILL.md) |
| `huashu-design` | 花叔 Design：一句话产出高保真 HTML 原型、幻灯片、动画、可视化与专家评审；先出三方向初稿供选择（MIT） | [README](design/huashu-design/README.md) |
| `md-prd-to-html-prototype` | 读取本地 Markdown PRD → 单文件 HTML 低保真原型；字段以文档为准，信息不足先提问 | [README](design/md-prd-to-html-prototype/README.md) |
| `modern-web-guidance` | 参考型：编写 Web 前端前检索随仓库自带的 209 份现代平台指南，离线自包含、中文驱动 | [README](design/modern-web-guidance/README.md) |

> `modern-web-guidance` 的指南为上游英文原文（CC-BY 4.0 / 代码 Apache-2.0），署名见 [ATTRIBUTION.md](design/modern-web-guidance/ATTRIBUTION.md)。它与具体生成技能叠加时，后者仍决定目录、分层与组件库。

---

### 🏭 SQL → 后端脚手架（`sql-to/`，4 个）

| 技能 | 输入 → 输出 | 文档 |
| --- | --- | --- |
| `sql-to-fastapi-restfulapi-scaffold` | SQL `CREATE TABLE` → FastAPI 分层脚手架（Model / Schema / Repository / Service / Resource） | [README](sql-to/sql-to-fastapi-restfulapi-scaffold/README.md) |
| `sql-to-flask-restfulapi-scaffold` | MySQL DDL → Flask + Flask-RESTful 接口项目脚手架 | [README](sql-to/sql-to-flask-restfulapi-scaffold/README.md) |
| `sql-to-springboot-restfulapi-scaffold` | SQL `CREATE TABLE` → Spring Boot 分层脚手架，导出 OpenAPI 文档 | [README](sql-to/sql-to-springboot-restfulapi-scaffold/README.md) |
| `sql-to-gin-restfulapi-scaffold` | MySQL DDL → Gin + GORM 分层脚手架 | [README](sql-to/sql-to-gin-restfulapi-scaffold/README.md) |

> 这些技能消费 MySQL `CREATE TABLE`，不执行 DDL。表结构未定时先用 [`database-schema-designer`](requirements_analysis/database-schema-designer/README.md) 出脚本。

---

### 📱 原型 / 需求 → 应用工程（`prototype-to/`，7 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `prototype-to-app-uniappx` | 原型 → uni-app x 蒸汽模式（TS）工程，`.uvue` 页面 + services 分层 + mock 数据 | [README](prototype-to/prototype-to-app-uniappx/README.md) |
| `prototype-to-flutter-app` | 原型 → Flutter 工程，features 分层 + Repository + `ChangeNotifier` | [README](prototype-to/prototype-to-flutter-app/README.md) |
| `prototype-to-web(Nuxt UI Starter)` | 原型 → Nuxt UI Starter 工程 | [README](<prototype-to/prototype-to-web(Nuxt UI Starter)/README.md>) |
| `prototype-to-taro-app` | 原型 → Taro 4 多端工程，Vue3 / React 双分支由用户确认 | [README](prototype-to/prototype-to-taro-app/README.md) |
| `prototype-to-ios-native-app(AwesomeSwift)` | 原型 → SwiftUI 原生 iOS 工程（XcodeGen / MVVM + Combine） | [README](<prototype-to/prototype-to-ios-native-app(AwesomeSwift)/README.md>) |
| `prototype-to-android-native-app(Fragmject)` | 原型 → Compose 原生 Android 工程（单 Activity MVI / Hilt） | [README](<prototype-to/prototype-to-android-native-app(Fragmject)/README.md>) |
| `requirements-to-vue_vben_admin` | 后台需求 → vue-vben-admin（vben5）可运行脚手架 | [README](prototype-to/requirements-to-vue_vben_admin/README.md) |

---

### ☕ Java 工程（`java/`，5 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `create-spring-boot-java-project` | 从 start.spring.io 脚手架新 Spring Boot 项目（Maven / Gradle） | [SKILL.md](java/create-spring-boot-java-project/SKILL.md) |
| `java-development` | 无框架日常 Java：Maven / Gradle、JDK 版本习惯用法、日志、并发、静态分析与打包 | [SKILL.md](java/java-development/SKILL.md) |
| `java-springboot` | 在已有 Spring Boot 3/4 项目中写和评审业务代码 | [SKILL.md](java/java-springboot/SKILL.md) |
| `java-upgrade` | 升级 Java 项目到更高 JDK（11→17→21→25）并采用新特性 | [SKILL.md](java/java-upgrade/SKILL.md) |
| `openapi-to-application-java-spring-boot` | OpenAPI 3 规约 → Spring Boot 应用（spec-first） | [SKILL.md](java/openapi-to-application-java-spring-boot/SKILL.md) |

---

### 🐹 Go 工程（`go/`，4 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `go-api-design` | HTTP/REST API 设计：handler、路由、中间件、校验、幂等、优雅关闭 | [SKILL.md](go/go-api-design/SKILL.md) |
| `golang-grpc` | gRPC 规范：protobuf 组织、拦截器、状态码、TLS/mTLS、流式 RPC | [SKILL.md](go/golang-grpc/SKILL.md) |
| `golang-project-layout` | Go 项目布局：cmd / internal / pkg、模块命名、go.work | [SKILL.md](go/golang-project-layout/SKILL.md) |
| `golang-testing` | Go 测试实践：表驱动、testify、并行、fuzz、goleak、覆盖率 | [SKILL.md](go/golang-testing/SKILL.md) |

---

### 🔒 安全（`security/`，6 个）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `fastapi-api-security-authentication` | 给已有 FastAPI CRUD 项目补白名单、Bearer JWT 与角色/对象权限 | [SKILL.md](security/fastapi-api-security-authentication/SKILL.md) |
| `go-security-audit` | Go 应用安全评审：注入、SSRF、认证、密钥、OWASP Top 10（只读报告） | [SKILL.md](security/go-security-audit/SKILL.md) |
| `golang-continuous-integration` | Go 项目 CI/CD：GitHub Actions、Dependabot、GoReleaser | [SKILL.md](security/golang-continuous-integration/SKILL.md) |
| `security-audit` | 审计已有代码：越权、注入、XSS、SSRF、JWT、密钥、上传与依赖 | [README](security/security-audit/README.md) |
| `spring-boot-testing` | Spring Boot 测试技术选型：测试切片、Testcontainers、Failsafe | [SKILL.md](security/spring-boot-testing/SKILL.md) |
| `spring-security` | Spring Security 6/7 配置与评审：SecurityFilterChain、OAuth2、MockMvc 安全测试 | [SKILL.md](security/spring-security/SKILL.md) |

---

### 🎓 教学（[`education/`](education/README.md)）

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `lesson-prep-assistant`（备课辅助助手） | 计算机专业教师备课技能：输入知识点 + 教学目标 → 先出教学内容提纲供审阅，确认后再生成按五段认知逻辑（是什么/为什么/发展历程/应用现状/如何开始使用）展开的 Markdown 讲义 + 可运行示例代码 + 配图，成品为可在 VSCode 中打开自学的材料包（原创） | [SKILL.md](education/lesson-prep-assistant/SKILL.md) · [中文导读](education/lesson-prep-assistant/README.md) |
| `teaching-pptx` | 教学知识点 → 逐页提纲 → 教师确认 → 可编辑的 16:9 PPTX 与演讲者备注 | [SKILL.md](education/teaching-pptx/SKILL.md) · [使用指南](education/teaching-pptx/README.md) |
| `prepkit` | 信息学竞赛备课与课堂质量参照 | [SKILL.md](education/prepkit/SKILL.md) |
| `TeachAnyHE` | 高校互动课件、仿真与知识图谱 | [中文导读](education/TeachAnyHE/README.md) |

---

### 🧩 其他技能

| 技能 | 说明 | 文档 |
| --- | --- | --- |
| `dsh-plugin-starter`（`others/`） | 一句话需求或插件原型 → DSH 插件起步项目，四类插件 + 内置开发者指南 | [README](others/dsh-plugin-starter/README.md) |
| `last30days`（`info-research/`） | 全网信息调研：拉取 Reddit/X/YouTube/HN/Polymarket/小红书等最近 30 天帖文与互动，综合生成带引用的调研报告 | [SKILL.md](info-research/last30days/SKILL.md) |
| `gorden-ppt-skill`（`ppt/`） | 21 套中文 PPTX 模板 + python-pptx 非破坏性纯文字编辑：工作汇报、述职竞聘、教学课件、商务提案、数据可视化等成品 PPT | [SKILL.md](ppt/gorden-ppt-skill/SKILL.md) |
| `supervisor-skills`（`research/`） | 12 个科研全流程技能（Idea 评估、文献调研、论文写作、投稿审核、Rebuttal） | [中文导读](research/supervisor-skills/README.zh-CN.md) |
| `research-weave`（`research/`） | 论文淘金：决定哪些论文值得精读，Scout/Map/Update 三模式产出阅读建议、可追溯证据账本与检索记录 | [SKILL.md](research/research-weave/SKILL.md) |
| `best-paper-writing`（`research/`） | 最佳论文风格写作：60 篇 CVPR/ICCV/NeurIPS 获奖论文提炼的摘要/引言/方法/实验/配图写作技能，自带草稿检查器 | [SKILL.md](research/best-paper-writing/skills/bestpaper-writing/SKILL.md) · [上游 README](research/best-paper-writing/README.md) |
| `auto-empirical-research`（`research/`） | 计算机科研实证精选 6 项：idea-discovery（找 idea 全流程）、experiment-plan（主张倒推实验）、dblp-api / openalex / bibliometrix-guide（文献检索与计量）、check-citations（引用真实性核查，自带脚本） | [PROVENANCE](research/auto-empirical-research/references/PROVENANCE.md) |
| `agentero-skills`（`research/`） | Agentero 工作台技能精选 2 项（已独立化改造）：中英文论文精读 `paper-reader`（可选讲义式笔记，已去 CLI 绑定）、论文写作规范 `research-paper-writing`（含 37 个写作示例） | [PROVENANCE](research/agentero-skills/references/PROVENANCE.md) |
| `superpowers-zh`（`requirements_analysis/`） | 20 个通用工作流技能（brainstorming、writing-plans、executing-plans、subagent-driven-development、systematic-debugging、TDD 等），供支持 Skill 的 AI 工具加载使用 | 目录：`requirements_analysis/superpowers-zh/` |

- 12 个科研技能需**作为一组整体安装**（技能间相互引用），多数为纯提示词；`drawio-reconstruction` 额外依赖 Python 脚本与 draw.io CLI
- ⚠️ `supervisor-skills` 整体为 **CC BY-NC-SA 4.0**（非商业 + 相同方式共享），**不受 MIT 覆盖**，商用前请阅读 [`references/PROVENANCE.md`](research/supervisor-skills/references/PROVENANCE.md)
- `research-weave` 为 **MIT** 许可，技能自包含（校验脚本仅依赖 Python 标准库），与 `supervisor-skills/deep-research` 定位互补
- `best-paper-writing` 主体为 **CC BY 4.0**（需署名，可商用），exemplars 中的论文短句引用**不在许可范围内、严禁复制进新论文**，基础技能部分为 MIT；详见 [`references/PROVENANCE.md`](research/best-paper-writing/references/PROVENANCE.md)
- ⚠️ `gorden-ppt-skill` 代码为 **MIT**，但 `templates/` 模板视觉资产**非商业 + 上游禁止二次分发**（版权归原模板作者），仅限个人学习研究，**严禁商用**；已为 WorkBuddy 做环境适配（自动更新改可选、Windows/依赖注记）；详见 [`references/PROVENANCE.md`](ppt/gorden-ppt-skill/references/PROVENANCE.md)
- `last30days` 为 **MIT** 许可；自带 Python 调研引擎（需 Python 3.12+），多数据源凭据**可选**（首次使用有 setup wizard 引导，亦有 keyless 模式）；调研境外平台需网络可达；详见 [`references/PROVENANCE.md`](info-research/last30days/references/PROVENANCE.md)
- `auto-empirical-research` 合集为 **CC BY-SA 4.0**，选择性收录 6 项科研技能。`experiment-plan` 和 `check-citations` 支持单独安装；`idea-discovery` 仍依赖未收录的上游组件，`openalex` 和 `bibliometrix-guide` 有外部运行要求。见[科研技能安装指南](research/README.md)和[来源与许可](research/auto-empirical-research/references/PROVENANCE.md)。
- `agentero-skills` 为 **MIT**（源自 Agentero 应用）。`paper-reader` 不依赖 Agentero CLI 或 Vault，默认在对话交付，配图提取可选；`research-paper-writing` 可独立使用。见[改造说明](research/agentero-skills/references/PROVENANCE.md)。

---

## 🏗️ 仓库结构

```text
ncepu_ideal-skills/
├── 📄 README.md / README.en.md / CODEBUDDY.md
├── 📁 docs/                                        # 配置指南 + 设计方法 + plans/ specs/ images/
├── 📁 requirements_analysis/                       # 📋 需求分析与设计（3 个技能 + spec-kit + superpowers-zh）
│   ├── brainstorming/                              # SKILL + 规格评审提示 + 脚本 + visual-companion
│   ├── it-requirement-analysis/                    # SKILL + references/（PRD / 用户故事 / 流程分析）
│   ├── database-schema-designer/                   # README + SKILL + NOTICE + LICENSE + references/
│   ├── spec-kit/                                   # GitHub Spec Kit 工具包（非本仓库自写技能）
│   ├── superpowers-zh/                             # 🧠 20 个通用工作流技能（唯一本体）
│   ├── 使用说明.md
│   └── 关于开源需求分析技能.md
├── 📁 design/                                      # 🎨 设计与前端（5 个技能）
│   ├── common-website-design/                      # README + SKILL + PLAN + designs/ references/ scripts/
│   ├── frontend-design/                            # SKILL.md
│   ├── huashu-design/                              # README(.en) + SKILL + assets/ demos/ references/ scripts/
│   ├── md-prd-to-html-prototype/                   # README + SKILL + references/ resources/ scripts/
│   └── modern-web-guidance/                        # README + SKILL + ATTRIBUTION + resources/（209 份指南）
├── 📁 sql-to/                                      # 🏭 SQL → 后端脚手架（4 个技能，README + SKILL + resources/）
│   ├── sql-to-fastapi-restfulapi-scaffold/
│   ├── sql-to-flask-restfulapi-scaffold/
│   ├── sql-to-springboot-restfulapi-scaffold/
│   └── sql-to-gin-restfulapi-scaffold/
├── 📁 prototype-to/                                # 📱 原型 / 需求 → 应用工程（7 个技能，均含 resources/）
│   ├── prototype-to-app-uniappx/
│   ├── prototype-to-flutter-app/
│   ├── prototype-to-web(Nuxt UI Starter)/
│   ├── prototype-to-taro-app/
│   ├── prototype-to-ios-native-app(AwesomeSwift)/
│   ├── prototype-to-android-native-app(Fragmject)/
│   └── requirements-to-vue_vben_admin/
├── 📁 go/                                          # 🐹 Go 工程规范（4 个技能）
│   ├── go-api-design/ / golang-grpc/
│   ├── golang-project-layout/ / golang-testing/
├── 📁 java/                                        # ☕ Java 工程规范（5 个技能）
│   ├── create-spring-boot-java-project/ / java-development/ / java-springboot/
│   └── java-upgrade/ / openapi-to-application-java-spring-boot/
├── 📁 security/                                    # 🔒 安全（6 个技能）
│   ├── fastapi-api-security-authentication/ / go-security-audit/
│   ├── golang-continuous-integration/ / security-audit/
│   └── spring-boot-testing/ / spring-security/
├── 📁 education/                                   # 🎓 备课与课件制作
│   ├── lesson-prep-assistant/                      # 自学讲义与材料包
│   ├── teaching-pptx/                             # 审批逐页提纲后生成教学 PPTX
│   ├── prepkit/                                   # 竞赛备课框架
│   └── TeachAnyHE/                                # 高校互动课件
├── 📁 research/
│   ├── best-paper-writing/                         # 🏆 最佳论文风格写作（CC BY 4.0，含 CVPR 模板与语料）
│   ├── agentero-skills/                            # 🖥️ Agentero 技能精选 2 项（MIT：中英文精读/写作规范，已独立化改造）
│   ├── auto-empirical-research/                    # 🧪 实证科研精选 6 技能（CC BY-SA 4.0：idea/实验/文献计量/引用核查）
│   ├── research-weave/                             # 🧵 论文淘金技能（MIT，SKILL + references/ + scripts/）
│   └── supervisor-skills/                          # 🔬 12 个科研技能（CC BY-NC-SA 4.0）
├── 📁 info-research/                               # 📰 全网信息调研（1 个技能）
│   └── last30days/                                 # 🗞️ 最近 30 天全网舆情调研（MIT，自带 Python 引擎）
├── 📁 ppt/                                         # 📊 PPT 生成（1 个技能）
│   └── gorden-ppt-skill/                           # 🎨 21 套中文模板 PPT 生成（代码 MIT / 模板非商业）
├── 📁 others/
│   └── dsh-plugin-starter/                         # 🧩 DSH 插件起步项目生成技能
```

> 说明：仓库中**不含** `test/` 样例目录，也不含 `.codebuddy/`、`.agents/`、`.workbuddy/`、`.cursor/`、`.dsh/` 等工具专用技能副本。这些测试与安装副本已移出本仓库，验证工作在独立项目中进行。通用工作流技能以 `requirements_analysis/superpowers-zh/` 为唯一本体，按需安装到具体工具。

---

## 快速开始

### 1️⃣ 选择技能并加载到你的 AI 工具

各工具如何把本仓库的技能加载为可用 Skill，参考对应配置指南：

| 🤖 AI 工具 | 📚 配置文档 |
| ----------- | ----------- |
| 🚀 **Trae IDE** | [配置指南](.docs/Trea中使用skill配置.md) |
| 💻 **Claude Code** | [配置指南](.docs/claude中使用skill配置.md) |
| ⚡ **GitHub Copilot** | [配置指南](.docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md) |
| 🧩 **CodeBuddy** | [配置指南](.docs/CodeBuddy中使用skill配置.md) · [Taro 技能指南](.docs/在Codebuddy插件中使用prototype-to-taro-app技能指南.md) |
| 🛠️ **WorkBuddy** | [科研技能集指南](.docs/如何在workbuddy中使用科研技能集supervisor-skills.md) · [research-weave 指南](.docs/如何在workbuddy中使用科学研究技能research-weave.md) |
| 🧠 **DSH + Superpowers** | [需求分析教程](.docs/dsh中使用superpowers技能.md) |
| 🧠 **Cursor + Superpowers** | [需求分析教程](.docs/如何在cursor中使用Superpowers技能进行项目的需求分析.md) |

> 📝 更多说明见 `.docs/`（含 `plans/` 与 `specs/` 设计文档）。加载时直接指向本仓库对应技能目录，不再复制到工具目录形成副本。

---

### 2️⃣ 典型使用链路

#### A. 从业务需求到可运行后端

```text
it-requirement-analysis（PRD / 验收标准）
   → brainstorming（技术方案与设计规格）
   → database-schema-designer（数据库设计 + MySQL DDL）
   → sql-to-* 技能（生成 FastAPI / Flask / Gin / Spring Boot 脚手架）
```

#### B. 从原型到前端工程

把原型 HTML 代码、设计图截图或 PRD 页面清单交给 `prototype-to-*` 技能，生成 uni-app x / Flutter / Nuxt / Taro / iOS / Android / vben 后台工程，内置 mock 数据可直接预览，后续改数据访问接缝对接真实后端。

#### C. 代码规范与评审

- 写代码前：`modern-web-guidance`（Web UI）、`frontend-design`（视觉）、`java-*` / `go-*`（工程规范）
- 写完代码：`security-audit`、`go-security-audit`、`spring-security` 等做安全评审与加固
- 需求侧技能与工程侧技能可独立使用，也可串联；本仓库不负责执行测试

---

## 🗺️ 未来规划

- [ ] 🔮 按领域继续补充与优化技能，保持分类目录清晰
- [ ] 📋 建立统一的技能命名、版本与文档规范
- [ ] 🔄 与各 AI 工具的加载方式保持同步（不引入技能副本）

---

## 🤝 贡献指南

欢迎提交新的 Skill 或改进现有 Skill！

**💡 建议流程**：

1. 🍴 Fork 本仓库并新建分支
2. 📁 在对应分类目录（`requirements_analysis/`、`design/`、`sql-to/`、`prototype-to/`、`go/`、`java/`、`security/`、`research/`、`others/`）中新建技能目录，包含 `SKILL.md`、`README.md` 及必要资源
3. 📝 更新根 README 的技能清单与仓库结构
4. 🔄 发起 Pull Request
5. 🧪 技能测试与回归请在独立测试项目中进行，不要在本仓库添加测试目录或样例产物

---

## 📄 许可证

仓库根目录未声明统一许可证文件；各技能自带其许可（`database-schema-designer`、`security-audit`、`huashu-design` 等为 MIT，`modern-web-guidance` 见 `ATTRIBUTION.md`）。`research/supervisor-skills` 为 **CC BY-NC-SA 4.0**，不受 MIT 覆盖。对外分发前请核对每个技能的许可声明。
