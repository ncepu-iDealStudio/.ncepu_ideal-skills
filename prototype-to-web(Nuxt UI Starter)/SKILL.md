---
name: "prototype-to-web-nuxt-ui-starter"
description: "从原型（HTML/CSS 代码、设计图截图或 PRD 页面清单）生成基于 nuxt-ui-templates/starter 的开箱即用 Web 工程：Nuxt 4 + Vue 3 + TypeScript + Nuxt UI + Nitro + Tailwind CSS v4 + ESLint 已配好，含分层目录、文件路由、mock 数据驱动的页面还原、可直接 pnpm dev 的工程。用户提到「原型转 Web」「设计稿做网页」「照这个页面做 Nuxt」「生成 Nuxt 项目」「Nuxt UI」时使用。也用于已生成的工程：用户贴一张列表页原型图，说「加栏目」「新增信息列表页」「按这张图加一页」时，在现有工程上追加栏目和列表页，而不是重做项目。用户提供接口文档，说「接口文档对接」「按 Swagger / OpenAPI / Apifox 接真实数据」「把 mock 换成接口」时，只在 service 内对接真实数据，不重做页面。"
---

# Prototype-to-Web (Nuxt UI Starter) Skill

## 概述

把**原型**转换成**开箱即用的 Nuxt UI Starter 工程**。

基于开源模板 [nuxt-ui-templates/starter](https://github.com/nuxt-ui-templates/starter) 起步，已内置：

- **Nuxt 4** — 文件路由、自动导入、SSR/SSG、`$fetch`
- **Vue 3** — 组合式 API（`<script setup>`）
- **Nuxt UI** — 100+ 组件、暗色模式、Tailwind 集成
- **Nitro** — Nuxt 服务端引擎，提供 server API 路由与构建能力
- **Tailwind CSS v4** — 原子化 CSS
- **TypeScript** — 类型安全
- **ESLint** — 代码规范

核心目标：

1. 按**分层架构**（pages / composables / services / types）组织代码
2. 用 **mock 数据**驱动页面，还原布局、视觉与交互
3. 产出**能直接 `pnpm dev`** 的工程，无需再补脚手架
4. Service 层是唯一数据接缝。按接口文档对接时，字段映射和请求都留在 service，页面调用方式不变

**分层约定**（对齐 Nuxt 约定优于配置 + 清晰分层）：

```text
app/
├── app.vue                     # 入口：UApp + UHeader + UMain(NuxtPage) + UFooter
├── navigation.ts               # 顶栏栏目唯一登记处（UNavigationMenu 的数据源）
├── app.config.ts               # Nuxt UI 主题（颜色等）
├── assets/css/main.css         # Tailwind + Nuxt UI 样式入口
├── components/                 # 自动导入组件（U* 优先）
│   ├── AppLogo.vue
│   ├── SkillCard.vue
│   └── EmptyState.vue
├── composables/                # 自动导入组合式函数（状态 + 逻辑）
│   └── useSkills.ts
├── pages/                      # 文件路由（无需手动注册）
│   ├── index.vue               # /
│   └── detail.vue              # /detail
├── services/                   # 数据服务层（唯一接缝：mock/remote 切换）
│   └── skillService.ts
├── types/                      # TypeScript 类型（自动导入）
│   └── skill.ts
└── utils/                      # 工具函数（自动导入）
    └── format.ts
```

**强制约定**：

- **页面不直接发请求**，只调 composable
- **composable 不直接 `$fetch`**，只调 service
- **Service 是唯一数据接缝**。真实字段与页面类型不一致时，在 service 内映射；某个方法对接完成后，才关掉该方法的 `useMock`
- **优先用 Nuxt UI 组件**（`UButton`、`UCard`、`UInput` 等），自定义部分用 Tailwind 工具类
- **颜色走 Tailwind 语义色**（`text-primary`、`bg-primary`），不硬编码 hex

---

## 什么时候使用此技能

触发场景：

- 用户提供**原型 HTML/CSS**，要求转 Nuxt Web 项目
- 用户提供**设计图/截图**，要求照做网页
- 用户提供**PRD/页面清单**，要求生成 Nuxt 工程骨架
- 用户说"这个页面用 Nuxt 怎么写"、"生成一个 Nuxt UI 项目"
- 起步工程已经生成，用户再给一张**列表页原型图**，要求新增栏目或信息列表页
- 起步工程已经生成，用户提供**接口文档**（OpenAPI / Swagger / Apifox / Markdown / 粘贴的路径与响应示例），要求把 mock 换成真实数据

**不适用**：把任意既有 Nuxt 项目整体重构；纯 Vue 组件片段问答；实现后端接口。本技能生成的工程上追加栏目、列表页，以及按接口文档对接前端，都**适用**。对接不实现后端，也不按文档生成新页面。

---

## 输入形态

支持三类，可混合：

| 输入 | 提取方式 | 可靠性 |
| --- | --- | --- |
| **HTML/CSS 原型代码** | 解析 DOM 结构，映射 Nuxt UI 组件 + Tailwind | 最高 |
| **设计图 / 截图** | 视觉理解区域、层级、控件 | 中 |
| **PRD / 页面清单** | 抽取页面、字段、跳转 | 低，需补视觉决策 |

**优先级**：视觉以图片为准，结构以代码为准，业务规则以 PRD 为准。冲突时**停下来问**。

### 最小澄清清单

- 页面清单与主流程：首页、关键跳转
- 视觉基调：主色（Tailwind 色名，如 green/blue/violet）、是否深色模式
- 是否需要导航栏（顶部 Header / 侧边栏 Sidebar）
- 是否需要表单、表格等复杂交互

---

## 关键技术决策（直接影响开箱即用）

### 1. 零重型依赖（模板自带即够用）

模板已含 Nuxt + @nuxt/ui + Tailwind + ESLint + TS。**不额外引入**：

- 状态管理（Pinia）→ 用内置 composables
- HTTP 客户端（axios）→ 用内置 `$fetch`
- 路由库 → 用内置文件路由
- 工具库（lodash）→ 用 ES 内置或手写

**理由**：依赖越少，`pnpm install` 越不容易失败，开箱即用率越高。

### 2. 状态管理用 Composables

```ts
// app/composables/useSkills.ts
export const useSkills = () => {
  const items = ref<Skill[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function load() {
    loading.value = true
    error.value = null
    try {
      items.value = await skillService.getSkills()
    } catch (e) {
      error.value = e instanceof Error ? e.message : '加载失败'
    } finally {
      loading.value = false
    }
  }

  return { items, loading, error, load }
}
```

页面侧：

```vue
<script setup lang="ts">
const { items, loading, error, load } = useSkills()
onMounted(() => load())
</script>
```

### 3. 路由使用文件路由

无需手动注册，文件名即路由：

| 文件 | 路由 |
| --- | --- |
| `app/pages/index.vue` | `/` |
| `app/pages/detail.vue` | `/detail` |
| `app/pages/skills/[id].vue` | `/skills/:id` |

跳转用 `<NuxtLink to="/detail">` 或 `useRouter().push()`。

### 4. 数据服务层（Service）

```ts
// app/services/skillService.ts
const useMock = true  // 起步阶段用 mock。接口文档对接见 api_binding.md

export const skillService = {
  async getSkills(): Promise<Skill[]> {
    if (useMock) {
      await delay(300)
      return mockSkills
    }
    return await $fetch<Skill[]>('/api/skills')
  }
}
```

**Service 是唯一接缝**：composable 只调 service 方法，不关心数据来源。上面的 `$fetch<Skill[]>` 只表示起步工程的占位。真实文档的字段、包络与页面类型不一致时，按 `api_binding.md` 在 service 内映射，不能把原始响应直接当成 `Skill[]`。

### 5. 主题集中管理

颜色在 `app/app.config.ts` 声明，页面用 Tailwind 语义色：

```ts
// app/app.config.ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'green',
      neutral: 'slate'
    }
  }
})
```

页面中用 `text-primary`、`bg-primary`、`border-primary`，不写 hex。

---

## 已有工程：按原型图加栏目和信息列表页

用户已经有起步工程，又给了一张信息列表页设计图时，走增量，不走下面的全量步骤。

骨架已存在的判定：目录里同时有 `nuxt.config.ts`、`app/pages/`、`app/services/`。

操作契约：`resources/specifications/incremental_list_page.md`。执行时同时满足下面六条：

1. **不覆盖工程**。禁止再复制 `resources/templates/project_structure/`，禁止改主题色和已有页面、service、composable。
2. **栏目只追加**。登记处是 `app/navigation.ts` 的 `navItems`。`app.vue` 用 `UNavigationMenu` 渲染（桌面放在 `UHeader` 默认插槽，移动端放 `#body`）。文件还不存在时，先补首页一项，再追加新栏目，并只把导航接线补进现有 `UHeader`。
3. **一图一页**。只生成当前这张图的列表页。顶栏里其他没给页面图的栏目名写入待确认，不生成。
4. **成套文件**。每个新列表页都有 `app/types/{entity}.ts`、`app/services/{entity}Service.ts`、`app/composables/use{Entity}.ts`、`app/components/{Entity}Card.vue`、`app/pages/{kebab}.vue`。命名与起步工程的 Skill 列表一致。
5. **分层不变**。页面只调 composable，composable 只调 service，service 内 `useMock`。mock 至少 6 条，含超长标题和缺图。页面具备 loading / empty / error。没有第二张详情图时不生成详情页。
6. **路由冲突就停**。目标 `app/pages/*.vue` 已存在时先问用户，不覆盖。改完运行 `resources/tools/validate_project.py`。

图看不清的字段不要猜，列入输出里的「待确认」。

---

## 已有工程：按接口文档对接真实数据

用户已经有起步工程，并给出接口文档，要求页面显示真实数据时，走对接，不走全量生成，也不走加页。

骨架已存在的判定：目录里同时有 `nuxt.config.ts`、`app/services/`。没有 service 层就停，不要在页面里直接请求。

操作契约：`resources/specifications/api_binding.md`。执行时同时满足下面六条：

1. **文档对齐现有方法**。先列出 `*Service.ts` 里已有方法和页面真正用到的字段，再用文档去对。不按文档把工程重做成接口大全，也不生成文档里多出来的页面。
2. **适配只在 service**。`$fetch` 取文档中的原始结构，再映射成现有页面类型（如 `Skill`）。页面和 composable 的调用方式保持不变。
3. **包络在 service 解开**。响应是 `{ code, data, message }` 时在 service 解包；业务失败抛错，交给现有 `error` 态。
4. **鉴权只加文档写明的请求头**。不新做登录页，不写刷新令牌或通用拦截器。文档没写清鉴权方式时停下来问。
5. **按方法关 mock**。该方法的路径、字段和包络都对上之后，才关掉该方法的 `useMock`。没对上的方法继续走 mock。
6. **仍用 `$fetch`**。不引入 axios、Pinia，不改 `app.config.ts` 和无关页面。路径对不上、字段对不上、包络有歧义时停下来问，不猜。

分页和筛选只对接页面上已经有的交互。

---

## 使用流程

下面六步用于**从零生成**工程。目标目录已经是 Nuxt UI Starter 工程时：加栏目或列表页走「按原型图加栏目和信息列表页」；提供接口文档走「按接口文档对接真实数据」。

### 步骤 1：解析原型 → page inventory

产出页面清单：

| 字段 | 示例 |
| --- | --- |
| `page_name` | `index` |
| `route` | `/` |
| `file_path` | `app/pages/index.vue` |
| `layout_type` | `list` / `detail` / `form` / `grid` / `profile` / `landing` |
| `data_model` | `Skill` |
| `components` | `SkillCard`, `EmptyState` |
| `data_fields` | `id`, `title`, `userName`, `tags` |
| `interactions` | 跳转、加载更多 |

机器可读中间产物按 `resources/specifications/prototype_parser_contract.md` 输出 `proto_context.json`。HTML 输入可用 `resources/tools/parse_prototype.py` 生成初稿。

### 步骤 2：确认视觉与交互

问清楚：主色（Tailwind 色名）、是否深色模式、导航类型、表单校验规则。

### 步骤 3：生成工程骨架

从 `resources/templates/project_structure/` 复制，替换占位符：

```text
{{project_name}}        工程名（kebab-case，package.json name）
{{app_title}}           应用显示名
{{primary_color}}       主色（Tailwind 色名，如 green/blue）
{{neutral_color}}       中性色（如 slate）
```

必生成文件：

- `package.json`（含 Nuxt + @nuxt/ui + Tailwind + ESLint + TS）
- `nuxt.config.ts`（modules 含 @nuxt/ui、@nuxt/eslint）
- `tsconfig.json`、`eslint.config.mjs`
- `app/app.vue`、`app/navigation.ts`、`app/app.config.ts`
- `app/assets/css/main.css`
- `app/components/`（AppLogo + 业务组件）
- `app/composables/`
- `app/pages/`
- `app/services/`
- `app/types/`
- `app/utils/`
- `.gitignore`、`.editorconfig`
- `README.md`

### 步骤 4：生成页面与组件

按布局原型选 Nuxt UI 组件（详见 `resources/specifications/nuxt_ui_mapping_rules.md`）：

| 布局 | 核心组件 |
| --- | --- |
| 列表 | `v-for` + `UCard` |
| 详情 | `UCard` + 文本组件 |
| 表单 | `UForm` + `UFormField` + `UInput`/`USelect` |
| 宫格 | `grid grid-cols-*` + `UCard` |
| 个人中心 | `UAvatar` + `UList` |
| 落地页 | `UPageHero` + `UPageSection` |

### 步骤 5：填充 mock 数据

`app/services/*Service.ts` 中提供与真实接口**同形状**的数据：

- 列表至少 6 条，撑满一屏
- 含边界数据：超长标题、缺图、空列表
- 用 `setTimeout` 模拟网络延迟，让 Loading 态可见

### 步骤 6：实现交互

必须覆盖：

- 页面跳转与返回（`NuxtLink` / `useRouter`）
- 加载态（`loading` ref + 骨架屏 / `animate-pulse`）
- 空态（自定义 `EmptyState` 组件）
- 错误态（`UAlert` + 重试按钮）
- 点击反馈（`UButton` / `NuxtLink`）
- 轻提示（`useToast().add(...)`）
- 表单校验与提交反馈

### 步骤 7：自检

运行 `resources/tools/validate_project.py`：

- `package.json` 可解析、name 为 kebab-case、type 为 module
- `nuxt.config.ts` 含 `@nuxt/ui` 模块
- `app/app.vue` 含 `<NuxtPage />`
- `app/app.config.ts` 声明 `ui.colors.primary`
- `app/assets/css/main.css` 导入 tailwindcss 与 @nuxt/ui
- `postinstall` 为 `nuxt prepare`
- 页面不直接用原生 `fetch`（应用 service 层 + `$fetch`）
- 存在 `tsconfig.json`
- 建议建立 `services/` 与 `composables/` 层
- 未默认引入 Pinia
- `app/navigation.ts` 存在时，`app.vue` 用 `UNavigationMenu` 渲染，且每个站内栏目路由都有页面文件

---

## 文件结构（生成的目标工程）

```text
{{project_name}}/
├── package.json
├── nuxt.config.ts
├── tsconfig.json
├── eslint.config.mjs
├── .gitignore
├── .editorconfig
├── README.md
└── app/
    ├── app.vue
    ├── navigation.ts
    ├── app.config.ts
    ├── assets/css/main.css
    ├── components/
    │   ├── AppLogo.vue
    │   ├── SkillCard.vue
    │   └── EmptyState.vue
    ├── composables/
    │   └── useSkills.ts
    ├── pages/
    │   ├── index.vue
    │   └── detail.vue
    ├── services/
    │   └── skillService.ts
    ├── types/
    │   └── skill.ts
    └── utils/
        └── format.ts
```

---

## 对接后端 API

起步工程默认 `useMock = true`，页面先用 mock。用户提供接口文档之后，按 `resources/specifications/api_binding.md` 在对应 service 内映射字段并切换该方法的真实请求。

不要只把整个文件的 `useMock` 改成 `false` 就结束。远程结果往往不是页面类型本身，不能把 `$fetch` 的返回值直接当成 `Skill[]`。

数据流转：

```text
Page → useSkills() → skillService.getSkills()
                          ├── 该方法仍为 mock → mockSkills
                          └── 该方法已对接   → $fetch 原始响应 → 映射为 Skill[]
```

页面与 composable 的调用方式不变。映射、解包、文档要求的请求头都留在 service。

---

## 代码规范

### 命名

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 工程名 | kebab-case | `skill-swap-web` |
| 页面文件 | kebab-case + `.vue` | `index.vue`, `detail.vue` |
| 组件文件 | PascalCase + `.vue` | `SkillCard.vue` |
| composable | camelCase `use` 前缀 | `useSkills.ts` |
| service | camelCase + `Service` | `skillService.ts` |
| 类型文件 | camelCase | `skill.ts` |
| 类型/接口 | PascalCase | `Skill` |
| 变量 | camelCase | `skillList` |
| 常量 | UPPER_SNAKE_CASE | `API_BASE` |

### 组件规范

- **优先用 Nuxt UI 组件**：`UButton`、`UCard`、`UInput` 等
- **布局用 Tailwind 工具类**：`flex`、`grid`、`gap-*`、`p-*`
- **图标用 Iconify 语法**：`i-lucide-*`、`i-simple-icons-*`
- **颜色用语义色**：`text-primary`、`bg-primary`，不写 hex
- **响应式用断点前缀**：`sm:`、`md:`、`lg:`

### 注释

- 中文注释
- composable / service 顶部说明：用途、数据来源、主要方法
- 复杂交互处加行内注释

---

## 输出格式

```text
✅ 已生成 Nuxt UI Starter 工程：{{project_name}}

📁 结构
├── app/pages/          {{N}} 个页面（文件路由）
├── app/components/     组件
├── app/composables/    状态与逻辑
├── app/services/       数据服务层（mock/remote 切换）
└── app/types/          TypeScript 类型

🎨 已还原
- 页面：首页 / 详情（2 个）
- 组件：SkillCard、EmptyState
- 交互：加载态、空态、错误态、点击跳转、Toast 提示

▶️ 如何运行（开箱即用）
1. pnpm install
2. pnpm dev
（无需额外配置；mock 数据已内置）

🔌 如何对接后端
提供接口文档后，按 api_binding.md 只改对应 service：
映射字段、解开包络，再关掉该方法的 useMock。
页面与 composable 调用方式不变。

⚠️ 待确认
- 详情页评论区分页规则
- 空态文案
```

---

## 错误处理与边界

### 原型含 Web 专有特性

| 原型特性 | Nuxt UI / Tailwind 处理 |
| --- | --- |
| CSS Grid | `grid grid-cols-* gap-*` |
| 绝对定位 | `relative` + `absolute` |
| CSS 动画 | `transition-*` / `animate-*` |
| 渐变色 | `bg-gradient-to-r from-* to-*` |
| 复杂阴影 | `shadow-md` / `shadow-lg` |
| 图标字体 | `i-lucide-*` / `i-simple-icons-*` |

### 图片资源

原型图片链接**不可直接引用**。做法：

- 占位用 `UIcon` 或纯色背景块
- 网络图用 `<img loading="lazy">` + `@error` 回退
- 本地图片放 `public/` 目录，通过 `/images/xxx.png` 引用

### 无法推断时

不臆造。生成静态可看版本，把不确定项列入"待确认"，不要静默决定。

---

## 资源文件结构

```text
prototype-to-web(Nuxt UI Starter)/
├── SKILL.md
├── README.md
└── resources/
    ├── config/
    │   ├── naming_rules.json
    │   ├── design_tokens.json
    │   └── dependency_policy.json
    ├── specifications/
    │   ├── prototype_parser_contract.md
    │   ├── architecture_conventions.md
    │   ├── nuxt_ui_mapping_rules.md
    │   ├── incremental_list_page.md
    │   └── api_binding.md
    ├── templates/
    │   └── project_structure/
    │       ├── package.json
    │       ├── nuxt.config.ts
    │       ├── tsconfig.json
    │       ├── eslint.config.mjs
    │       ├── .gitignore
    │       ├── .editorconfig
    │       ├── README.md
    │       └── app/
    │           ├── app.vue
    │           ├── navigation.ts
    │           ├── app.config.ts
    │           ├── assets/css/main.css
    │           ├── components/
    │           ├── composables/
    │           ├── pages/
    │           ├── services/
    │           ├── types/
    │           └── utils/
    ├── tools/
    │   ├── parse_prototype.py
    │   ├── validate_project.py
    │   └── preview_plan.py
    └── demo_output/
        └── skill-swap-web/
```

---

## 重要提示

1. **基于 Nuxt UI Starter 模板** —— 以 [nuxt-ui-templates/starter](https://github.com/nuxt-ui-templates/starter) 为基线
2. **页面不碰 `$fetch`** —— 只调 composable，composable 调 service
3. **Service 是唯一接缝** —— 切换 mock/真实只改 service 内开关
4. **零重型依赖** —— 模板自带即够用，不引 Pinia/axios
5. **优先 Nuxt UI 组件** —— `U*` 组件保证一致性，自定义用 Tailwind
6. **颜色走语义色** —— `text-primary` 等，不写 hex
7. **三态齐全** —— Loading / Empty / Error 必须有，不能只有成功态
8. **mock 要像真数据** —— 有长度、有边界、有延迟
9. **`postinstall` 必须为 `nuxt prepare`** —— 否则类型与自动导入无法生成
10. **文件路由** —— `app/pages/index.vue` → `/`，无需手动注册
11. **已有工程加列表页** —— 按 `incremental_list_page.md` 追加 `app/navigation.ts` 与成套分层文件，不覆盖起步工程
12. **已有工程对接接口文档** —— 按 `api_binding.md` 在 service 内映射；不改页面调用，不实现后端
