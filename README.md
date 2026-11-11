# 🎯 ncepu_ideal-skills

> 企业级项目技能（Skills）集合仓库 | 基于资源驱动设计，从 SQL 生成后端脚手架、从原型生成前端应用

![License](https://img.shields.io/badge/license-MIT-green)
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
- 🎨 **多技术栈支持** - FastAPI / Flask / Gin / Spring Boot / uni-app x / Flutter / iOS / Android
- 📦 **增量生成** - 支持首次全量生成和后续增量更新
- 🔒 **安全内置** - 自动软删除/硬删除、敏感数据脱敏、输入验证
- 🧩 **开箱即用** - 生成的前端工程内置 mock 数据，无需后端即可运行预览

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

### 9️⃣ prototype-to-app-uniappx

从**原型**（HTML/CSS 代码、设计图截图、PRD 页面清单）生成**可运行的 uni-app x 工程**：用 mock 数据还原页面布局、视觉与交互，产出可直接在 HBuilder 运行的多端工程。

- 默认输出**蒸汽模式（TS）**，同时说明 uts 写法的切换
- 强制规避 uni-app x 与 uni-app 的差异坑（`.uvue`、flex 默认竖向、文字须在 `<text>` 内、`manifest.json` 需 `"uni-app-x": {}`）
- 分层：页面 / 组件 / `services/api`（唯一数据接缝）/ `services/mock`
- 校验脚本 10 项，示例产物 `resources/demo_output/skill-swap-demo/`

📖 **详细说明**：[查看文档](prototype-to-app-uniappx/README.md)

---

### 🔟 prototype-to-flutter-app

从**原型**生成符合 Flutter 官方架构指南与最佳实践的**开箱即用工程**：分层目录、路由、主题、mock 数据驱动的页面还原，`flutter pub get && flutter run` 即可看到效果。

- 按功能切分目录（`features/`），UI 层 / 数据层分离，Repository 模式
- 状态管理用官方推荐的 `ChangeNotifier` + `ListenableBuilder`，**零重型依赖**（仅 `http`）
- 强制规避硬编码颜色、`features` 层直连 HTTP 等反模式
- 校验脚本 11 项，示例产物 `resources/demo_output/skill_swap_app/`

📖 **详细说明**：[查看文档](prototype-to-flutter-app/README.md)

---

### 1️⃣1️⃣ requirements-to-vue_vben_admin

把**后台管理需求描述**转换成基于 [vue-vben-admin](https://github.com/vbenjs/vue-vben-admin)（vben5）的**可运行后台管理脚手架**：自动划分功能模块、生成路由菜单、CRUD 页面、API 层与图表看板，内置 mock 数据可直接运行。

- 输入一段中文需求（如"系统管理模块包括：用户管理、角色管理、权限管理"）即可
- 自动判定页面类型：`crud` / `dashboard`（图表看板）/ `tree`（权限菜单）/ `form`
- 覆盖 vben5 的三个易错点：`ant-design-vue` 与 `antdv-next` 之别、`VbenTableAction` 导入来源、路由 glob 自动收集
- 校验脚本 14 项，示例产物 `resources/demo_output/demo-admin/`（3 模块 8 页面）
- 已在**真实 vben 仓库**中生成并验证：0 错误 0 警告

📖 **详细说明**：[查看文档](requirements-to-vue_vben_admin/README.md)

---

### 1️⃣2️⃣ prototype-to-taro-app

从**原型**生成符合 Taro 规范的**多端工程**（微信/支付宝小程序、H5、RN），一套代码多端运行。

- **支持两种技术栈，由用户确认后选用**：
  - Vue3 分支：Taro 4 + Vue 3 + TS + Vant + Pinia
  - React 分支：Taro 4 + React 18 + TS + Dva + Immer
- 内置登录、401 跳登录、多环境请求封装、分页列表、下拉刷新、空态/加载态
- 解析工具强制要求 `--framework` 参数，不设默认框架
- 校验脚本 12 项；两个分支各有示例产物 `resources/demo_output/skill-swap-{vue3,react}/`

> 说明：参考仓库 `RealCoolSnow/taro-vue3-ts` 已 404，Vue3 分支按 Taro 官方规范自建；
> `elf-taro` 为 Taro3.0-rc + React16，本技能把其架构思路适配到 Taro 4 + React 18。

📖 **详细说明**：[查看文档](prototype-to-taro-app/README.md)

---

### 1️⃣3️⃣ prototype-to-ios-native-app

从**原型**（HTML/CSS 代码、设计图截图、PRD 页面清单）生成**能用 Xcode 直接 Run** 的**原生 iOS 工程**，范式对齐开源项目 [AwesomeSwift](https://github.com/JoeyBling/AwesomeSwift)。

- 技术基线：Swift 5.10 + SwiftUI（iOS 17.0+）+ MVVM & Combine + SwiftData + Alamofire + Kingfisher，SPM 依赖管理
- 不手写 `.xcodeproj`：用 XcodeGen 从 `project.yml` 生成工程，开箱即用且可版本管理
- 内置列表/详情/表单/个人中心四个页面范本，新页面**复制改造**对应范本
- 数据访问层留接缝：切真实后端只改 `AppContainer` 装配，页面代码不动
- 校验脚本 22 项（不需要 macOS / Xcode），示例产物 `resources/demo_output/skill-swap-ios/`

📖 **详细说明**：[查看文档](prototype-to-ios-native-app/README.md)

---

### 1️⃣4️⃣ prototype-to-android-native-app

从**原型**生成**可直接用 Android Studio 打开并运行**的**原生 Android 工程**，范式对齐开源项目 [Fragmject](https://github.com/miaowmiaow/fragmject)。

- 技术基线：Kotlin 2.1 / AGP 8.7.3 / JDK 17，Jetpack Compose + Material3（BOM 2024.12.01）
- 单 Activity + MVI（`UiState` / `Event` / `StateFlow`），Hilt（KSP）注入、Navigation Compose 路由
- 本地存储 Room + DataStore，网络 Retrofit + OkHttp + kotlinx.serialization，图片 Coil
- 内置四个页面范本；`Navigation3` 仍在实验期，默认用 Navigation Compose，用户要求时才切换
- 校验脚本 21 项，示例产物 `resources/demo_output/skill-swap-android/`

📖 **详细说明**：[查看文档](<prototype-to-android-native-app(Fragmject)/README.md>)

---

### 1️⃣5️⃣ dsh-plugin-starter

从**一句话需求或插件原型**生成**可直接用 VSCode 打开开发**的 **DSH（DeepSeek Harness）插件起步项目**，并在工程里内置一份面向初学者的《开发者指南》。

- 支持四类插件：`tool-only`（工具型，无界面）/ `route-only`（路由型，无界面）/ `dual-face`（双面型，设置页界面）/ `interceptor`（工具拦截器）
- 生成即对齐 DSH 插件规范：`dsh.bundle.patch` 装配声明、`dsh.client` 双面声明、tsdown 双目标构建（`lib/index.mjs` + `lib/client.js`）、包名四处一致
- 内置 `DEVELOPMENT.md`：改代码 → 构建 → 装进 DSH → 调试 → 打包发布的完整闭环，含按类型的扩展代码与「症状 → 根因」调试表
- 零依赖工具链：`scaffold_plugin.py`（spec → 工程）、`validate_plugin.py`（18 项静态自检）
- 示例产物：`resources/demo_output/dsh-plugin-notebook/`（双面型：路由 + 设置页 + 笔记增删查）
- 📘 使用指南：[docs/使用dsh-plugin-starter技能开发DSH插件.md](docs/使用dsh-plugin-starter技能开发DSH插件.md)

📖 **详细说明**：[查看文档](dsh-plugin-starter/README.md)

---

## 🏗️ 仓库结构

```text
ncepu_ideal-skills/
├── 📄 README.md                                    # 项目说明
├── 📄 README.en.md                                 # 英文说明
├── 📄 CODEBUDDY.md                                 # CodeBuddy 技能说明
├── 📄 .gitignore
├── 📁 docs/                                        # 配置指南与设计方法
│   ├── Trea中使用skill配置.md
│   ├── claude中使用skill配置.md
│   ├── CodeBuddy中使用skill配置.md
│   ├── GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md
│   ├── 生成企业级脚手架项目的混合SKILL设计方法.md
│   ├── dsh中使用superpowers技能.md
│   ├── workbuddy中使用原型转应用技能.md
│   └── images/                                     # 配置截图
├── 📁 sql-to-fastapi-restfulapi-scaffold/          # ⚡ FastAPI 项目生成技能
│   ├── README.md
│   ├── SKILL.md
│   ├── docs/                                       # 本技能的 IDE 配置说明
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       └── tools/                                  # check_skill_consistency.py（自洽校验）
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
├── 📁 prototype-to-app-uniappx/                    # 📱 原型转 uni-app x 工程技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       └── demo_output/
├── 📁 prototype-to-flutter-app/                    # 🐦 原型转 Flutter 工程技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       └── demo_output/
├── 📁 requirements-to-vue_vben_admin/              # 🧩 需求转 vben 后台管理技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       └── demo_output/
├── 📁 prototype-to-taro-app/                       # 📦 原型转 Taro 多端工程技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       └── demo_output/
├── 📁 prototype-to-ios-native-app/                 # 🍎 原型转原生 iOS 工程技能（SwiftUI）
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       ├── demo_input/
│       └── demo_output/
├── 📁 prototype-to-android-native-app(Fragmject)/   # 🤖 原型转原生 Android 工程技能（Compose）
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       ├── specifications/
│       ├── templates/
│       ├── tools/
│       ├── demo_input/
│       └── demo_output/
├── 📁 dsh-plugin-starter/                          # 🧩 DSH 插件起步项目生成技能
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/                                 # 四类型判定表 + 命名规则
│       ├── specifications/                         # 清单/Host/Client/构建发布 契约
│       ├── templates/                              # common + 四类型 + 指南分章
│       ├── tools/                                  # scaffold_plugin.py / validate_plugin.py
│       └── demo_output/                            # 示例产物 dsh-plugin-notebook
├── 📁 .codebuddy/skills/                           # 🧠 通用技能（CodeBuddy，20 个 superpowers-zh）
├── 📁 .agents/skills/                              # 🧠 通用技能（Agent Skills，20 个 superpowers-zh）
├── 📁 .workbuddy/skills/                           # common-website-design、it-requirement-analysis、md-prd-to-html-prototype、diagnosing-superpowers
├── 📁 .cursor/skills/                              # it-requirement-analysis、prd-html-skill
├── 📁 .dsh/skills/                                 # common-website-design、it-requirement-analysis、prd-html-skill、diagnosing-superpowers
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

## 快速开始

### 1️⃣ 配置技能到你的 AI 工具

> 根据你使用的 AI 编程助手，选择对应的配置指南：

| 🤖 AI 工具 | 📚 配置文档 |
| ----------- | ----------- |
| 🚀 **Trae IDE** | [配置指南](docs/Trea中使用skill配置.md) |
| 💻 **Claude Code** | [配置指南](docs/claude中使用skill配置.md) |
| ⚡ **GitHub Copilot** | [配置指南](docs/GitHub%20Copilot中使用sql-to-flask-restfulapi-scaffold技能.md) |
| 🧩 **CodeBuddy** | [配置指南](docs/CodeBuddy中使用skill配置.md) |
| 🛠️ **WorkBuddy** | [原型转应用技能指南](docs/workbuddy中使用原型转应用技能.md) |
| 🐋 **DSH（DeepSeek Harness）** | [superpowers 技能指南](docs/dsh中使用superpowers技能.md) |
| 🧩 **DSH 插件开发** | [dsh-plugin-starter 使用指南](docs/使用dsh-plugin-starter技能开发DSH插件.md) |

> 📝 **提示**：详细配置说明请参考 `docs/` 目录

---

### 2️⃣ 使用技能

本仓库技能分两大类，输入方式不同。

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
| **FastAPI** | SQL CREATE TABLE | Model / Schema / Resource / Service + 项目骨架 |
| **Flask** | MySQL DDL | Model / Controller / Service / Resource + 项目骨架 |
| **Gin** | MySQL DDL | Model / DAO / Service / Resource + 项目骨架 |
| **Spring Boot** | SQL CREATE TABLE | Entity / Repository / DTO / Service / Controller + 项目骨架 |

#### B. 前端：从原型生成应用工程

将**原型 HTML 代码**、**设计图截图**或 **PRD 页面清单**交给 AI，生成可运行的移动端工程。

**📥 示例输入**：

```text
这是我们的原型页面（附 HTML 代码 / 设计图 / 页面清单）。
请用 prototype-to-flutter-app 技能，生成可运行的 Flutter 工程，
用 mock 数据还原页面布局与交互，后续我再对接后端接口。
```

**📤 生成内容对照表**：

| ⚡ 技能 | 📥 输入 | 📤 生成内容 |
| -------- | -------- | ----------- |
| **uni-app x** | 原型代码 / 图片 / PRD | `.uvue` 页面 + 组件 + services 分层 + mock 数据，可在 HBuilder 直接运行的多端工程 |
| **Flutter** | 原型代码 / 图片 / PRD | features 分层 + Repository + mock 数据，`flutter pub get && flutter run` 即可运行的工程 |
| **iOS 原生** | 原型代码 / 图片 / PRD | SwiftUI 四页范本 + MVVM & Combine + SwiftData + mock 数据，`xcodegen generate` 后 Xcode 直接 Run |
| **Android 原生** | 原型代码 / 图片 / PRD | Compose 四页范本 + 单 Activity MVI + Hilt + Room + mock 数据，Android Studio 打开即运行 |

> 💡 上述技能都会生成**数据访问层接缝**：切换到真实后端只需改一个开关（`useMock` / `AppContainer` 装配），页面代码无需改动。

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
2. 📁 在独立目录中实现新 Skill（包含 `SKILL.md`、`README.md`、`resources/`）
3. 🧪 补充对应示例到 `test/`
4. 📝 更新根 README 的技能清单
5. 🔄 发起 Pull Request

---

## 📄 许可证

当前仓库未声明许可证文件。建议补充 `LICENSE` 后再对外分发。
