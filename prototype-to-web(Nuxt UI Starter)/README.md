# prototype-to-web(Nuxt UI Starter)

## 1. 这个技能是干嘛的

`prototype-to-web(Nuxt UI Starter)` 是一个面向 AI 开发场景的 Skill，用于把**原型**（HTML/CSS 代码、设计图截图、PRD 页面清单）转换成**开箱即用的 Nuxt UI Starter Web 工程**。

基于开源模板 [nuxt-ui-templates/starter](https://github.com/nuxt-ui-templates/starter) 起步，已内置 Nuxt 4 + Vue 3 + TypeScript + Nuxt UI + Nitro + Tailwind CSS v4 + ESLint。

与"给几个 Vue 组件示例"不同，它产出的是**完整可运行的脚手架**：

- 按分层架构组织代码（pages / composables / services / types）
- 文件路由，无需手动注册
- 内置 mock 数据，无需后端即可看到完整界面与交互
- Service 模式预留数据接缝，对接后端只改一处

核心价值：

1. **开箱即用** —— `pnpm install && pnpm dev` 即可看到效果
2. **还原度高** —— 布局、视觉层级、交互效果按原型还原
3. **可持续演进** —— 分层清晰，后续对接真实 API 无需重构

## 2. 适用场景

- 拿到设计稿/原型，要快速搭出 Nuxt Web 工程骨架
- 需要给客户演示"能点"的网页，但后端还没好
- 新项目起手，需要一套符合规范的目录与分层
- 起步工程已经生成，再拿一张信息列表页原型图，要加栏目、加列表页

**不适用**：把任意既有 Nuxt 项目整体重构；纯 Vue 组件片段问答；后端接口实现。本技能已经生成的工程上追加栏目和列表页是支持的，见第 10 节。

## 3. 技术栈与关键决策

| 项 | 选择 | 理由 |
| --- | --- | --- |
| 框架 | Nuxt 4 | 文件路由、自动导入、SSR/SSG、$fetch |
| 视图层 | Vue 3 | 组合式 API（`<script setup>`），响应式系统 |
| UI 库 | @nuxt/ui | 官方组件库，100+ 组件、暗色模式、Tailwind 集成 |
| 服务端 | Nitro | Nuxt 内置服务端引擎，server API 路由、构建部署 |
| 样式 | Tailwind CSS v4 | 原子化 CSS，与 Nuxt UI 深度集成 |
| 状态管理 | Composables | Nuxt 自动导入，原型阶段无需 Pinia |
| 网络 | `$fetch`（内置） | Nuxt 内置，基于 ohmyfetch，支持拦截器/重试 |
| 路由 | 文件路由 | `app/pages/` 下文件即路由，无需注册 |
| 类型 | TypeScript | 类型安全 |
| Lint | @nuxt/eslint | 官方 ESLint 模块，开箱即用 |

**默认零重型依赖**，最大化 `pnpm install` 成功率 —— 这是"开箱即用"的前提。

## 4. 技能项目结构

```text
prototype-to-web(Nuxt UI Starter)/
├── SKILL.md                                # 技能定义与工作流（AI 读取）
├── README.md                               # 本文件
└── resources/
    ├── config/
    │   ├── naming_rules.json               # 命名规则（Nuxt/Vue/TS 约定）
    │   ├── design_tokens.json              # 设计 token（Tailwind 颜色/间距/字号）
    │   └── dependency_policy.json          # 依赖策略（模板基线 + 拒绝项）
    ├── specifications/
    │   ├── prototype_parser_contract.md    # 原型 → context 契约
    │   ├── architecture_conventions.md     # 分层架构与依赖方向
    │   ├── nuxt_ui_mapping_rules.md        # HTML → Nuxt UI 组件映射
    │   └── incremental_list_page.md        # 已有工程上按原型图加栏目和列表页
    ├── templates/
    │   └── project_structure/              # 完整工程骨架（可直接复制）
    │       ├── package.json
    │       ├── nuxt.config.ts
    │       ├── tsconfig.json
    │       ├── eslint.config.mjs
    │       ├── .gitignore
    │       ├── .editorconfig
    │       ├── README.md
    │       └── app/
    │           ├── app.vue
    │           ├── app.config.ts
    │           ├── assets/css/main.css
    │           ├── components/
    │           ├── composables/
    │           ├── pages/
    │           ├── services/
    │           ├── types/
    │           └── utils/
    ├── tools/
    │   ├── parse_prototype.py              # HTML 原型 → proto_context.json
    │   ├── validate_project.py             # 生成工程静态自检
    │   └── preview_plan.py                 # 预览生成计划
    └── demo_output/
        └── skill-swap-web/                 # 示例：技能互换 Web 应用
```

## 5. 工具用法

### 5.1 从 HTML 原型生成 context 初稿

```bash
python resources/tools/parse_prototype.py 原型.html \
  --out proto_context.json \
  --project skill-swap-web \
  --title "技能互换"
```

输出 `proto_context.json`，包含识别的布局类型、组件、字段、交互。**这是初稿**，需核对 `diagnostics.need_confirm`。

### 5.2 预览生成计划

```bash
python resources/tools/preview_plan.py proto_context.json
```

输出页面清单与将要生成的文件列表，确认无误再生成。

### 5.3 校验生成结果

```bash
python resources/tools/validate_project.py ./skill-swap-web
```

检查 13 项：package.json 合法性、必备文件、nuxt.config 含 @nuxt/ui、app.vue 含 NuxtPage、app.config 声明 primary、页面无原生 fetch、main.css 导入、postinstall 为 nuxt prepare、无 Pinia、tsconfig 存在、services 层、composables 层、`app/navigation.ts` 的栏目都能落到页面文件。

加 `--json` 输出机器可读结果。

## 6. 生成的目标工程

```text
skill-swap-web/
├── package.json                  # 依赖：nuxt + @nuxt/ui + tailwindcss + eslint + ts
├── nuxt.config.ts                # modules: @nuxt/eslint, @nuxt/ui
├── tsconfig.json
├── eslint.config.mjs
├── .gitignore
├── .editorconfig
├── README.md
└── app/
    ├── app.vue                   # UApp + UHeader + NuxtPage + UFooter
    ├── navigation.ts             # 顶栏栏目，供 UNavigationMenu 使用
    ├── app.config.ts             # ui.colors.primary = 'green'
    ├── assets/css/main.css       # @import tailwindcss + @nuxt/ui
    ├── components/
    │   ├── AppLogo.vue
    │   ├── SkillCard.vue
    │   └── EmptyState.vue
    ├── composables/
    │   └── useSkills.ts          # 列表状态 + load()
    ├── pages/
    │   └── index.vue             # /
    ├── services/
    │   └── skillService.ts       # getSkills()：useMock ? mock : $fetch
    ├── types/
    │   └── skill.ts
    └── utils/
        └── format.ts
```

## 7. 对接后端 API

三步，**页面代码零改动**：

```ts
// 1. app/services/skillService.ts
const useMock = false
const API_BASE = 'https://api.your-domain.com'

// 2. 核对 $fetch 的接口路径与返回结构

// 3. composable 与页面自动切换数据源（无需改）
```

数据流转：

```text
Page → useSkills() → skillService.getSkills()
                        ├── useMock=true  → mockSkills（setTimeout 延迟）
                        └── useMock=false → $fetch('/api/skills')
```

## 8. 示例产物

`resources/demo_output/skill-swap-web/` 是完整示例（技能互换 Web 应用），已通过 `validate_project.py` 全部检查。

## 9. 与其他 prototype-to-* 技能的关系

本技能与 `prototype-to-flutter-app`、`prototype-to-app-uniappx` 等是姊妹技能，共享同一套原型解析契约设计思路：

| 项 | Flutter 版 | uni-app x 版 | Nuxt UI 版（本技能） |
| --- | --- | --- | --- |
| 目标 | Android/iOS/Web/桌面 | App/小程序/H5 | Web |
| 语言 | Dart | Vue + TS/UTS | Vue + TS |
| 状态 | ChangeNotifier | reactive/ref | composables |
| 数据接缝 | Repository | service | service |
| 输入 | 同样支持三类原型 | 同样支持三类原型 | 同样支持三类原型 |

可按团队技术栈选择对应技能。

## 10. 起步之后加栏目和信息列表页

起步工程生成之后，可以把一张**信息列表页原型图**交给 AI，并说明要新增的栏目。技能按 `resources/specifications/incremental_list_page.md` 在现有工程上追加，不重做项目。

会新增或补齐：

- `app/navigation.ts`：只在末尾追加一个栏目，并用 `UNavigationMenu` 显示在顶栏
- 一套列表页文件：`types`、`services`（mock）、`composables`、卡片组件、`pages/*.vue`
- 加载、空列表、失败重试三种状态

已经存在的页面、主题色和依赖不会被覆盖。同一路由的页面文件如果已经在，会先停下来问，而不是直接改。图里看不清的字段会列入待确认；没有单独的详情图时，不会顺便生成详情页。
