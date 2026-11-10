---
name: "prototype-to-app-uniappx"
description: "从原型（HTML/CSS 代码、设计图截图或 PRD 页面清单）生成符合 uni-app x 最佳实践的脚手架项目：用 mock 数据还原页面布局、视觉与交互，产出可直接在 HBuilder 运行的多端工程。用户提到「原型转 uniappx」「截图转 App」「照这个设计稿做小程序/App」「把原型做成可以点的应用」时使用。完成后可基于分层 mock 适配层平滑对接后端 API。"
---

# Prototype-to-App（uni-app x）Skill

## 概述

本技能把**原型**转换成**可运行的 uni-app x 脚手架工程**。

核心目标不是"生成一堆页面文件"，而是：

1. 还原原型的**页面布局与视觉层级**
2. 用 **mock 数据**驱动页面，让界面"有内容可看"
3. 还原**交互效果**（跳转、切换、弹层、下拉刷新、加载态）
4. 产出**规范分层**的工程，后续只需替换数据层即可对接真实 API

**分层约定**：

```text
pages/*.uvue          → 页面（只做编排：取数据、组合组件、绑定事件）
components/           → 可复用 UI 组件（无业务数据逻辑）
store/                → 页面级状态（可选，简单页面不必引入）
services/api/*.ts     → 数据访问层（唯一需要改造成真实请求的地方）
services/mock/*.ts    → mock 数据与模拟延迟
types/*.ts            → 数据模型类型定义
utils/                → 纯函数工具（格式化、校验）
```

**强制约定**：

- 页面**不直接写死**业务数据，必须从 `services/api` 取（哪怕当前返回的是 mock）
- `services/api` 是**唯一**对接后端的接缝，改造时只动这一层
- 组件**不感知**数据来源，只接收 props、抛出事件

---

## 什么时候使用此技能

触发场景：

- 用户提供**原型 HTML/CSS 代码**，要求转成 uni-app x 工程
- 用户提供**设计图/截图**，要求照着做 App / 小程序
- 用户提供**PRD 或页面清单**，要求生成可点原型
- 用户说"把这个页面做成 uni-app x"、"原型转 App"、"截图转小程序"

**不适用**：已有 uni-app（非 x）工程要迁移 —— 请参考官方升级指南；纯原生开发；后端接口实现。

---

## 输入形态与处理策略

技能支持三类输入，**可混合使用**：

| 输入 | 提取方式 | 可靠性 |
| --- | --- | --- |
| **HTML/CSS 原型代码** | 解析 DOM 结构与样式，机械映射组件 | 最高，结构明确 |
| **设计图 / 截图** | 视觉理解：识别区域、层级、控件类型 | 中，需人工确认细节 |
| **PRD / 页面清单** | 从文字描述抽取页面、字段、跳转 | 低，需补充视觉决策 |

### 输入优先级与冲突处理

1. 多种输入并存时，**视觉以图片为准，结构以代码为准，业务规则以 PRD 为准**
2. 三者矛盾时**停下来问**，不要自行决定
3. 信息不足时按第 3 节"澄清清单"补齐，不要臆造

### 输入信息不足时的最小澄清清单

在开始生成前，必须能回答：

- **目标平台**：App（Android/iOS）/ 小程序 / H5 / 全都要？
- **页面清单与主流程**：首页是哪个？关键跳转路径是什么？
- **视觉基调**：主色、圆角风格、是否深色模式
- **输入类型**：提供的材料是代码、图还是文字？
- **是否需要 tabBar**：几个 tab、分别是什么

---

## 关键框架事实（必须遵守，否则生成的代码在 App 端跑不起来）

uni-app x 与 uni-app 有**实质差异**，以下是最容易踩的坑：

### 1. 页面文件是 `.uvue`

```
pages/index/index.uvue     ✅
pages/index/index.vue      ❌（uni-app x 不认 .vue 页面）
```

### 2. App 端 CSS 是 Web CSS 的**子集**

| 限制 | 说明 | 正确做法 |
| --- | --- | --- |
| **flex 默认方向是竖向** | `flex-direction` 默认 `column`，不是 `row` | 横向布局必须显式写 `flex-direction: row` |
| **样式不继承** | 父级 `color`/`font-size` 不会传给子级 | 每个 `<text>` 自己写样式 |
| **文字必须在 `<text>` 内** | 裸文字不会渲染 | `<text>内容</text>` |
| **无 `display: inline`** | 不支持 Web 的 inline 流式布局 | 一律用 flex |
| 部分选择器不支持 | 复杂后代选择器、伪类可能失效 | 用 class，避免深层嵌套选择器 |

### 3. `pages.json` 必须注册所有页面

未注册的页面**不会被打包**。新增页面后必须同步更新 `pages.json` 的 `pages` 数组。

### 4. `manifest.json` 需带 uni-app x 标记

```json
{
  "name": "my-app",
  "appid": "__UNI__XXXXXXX",
  "versionName": "1.0.0",
  "versionCode": "100",
  "uni-app-x": {}
}
```

缺少 `"uni-app-x": {}` 节点，HBuilder 会把它当成普通 uni-app 项目。

### 5. 两种编译模式

| 模式 | 语言 | 脚本文件 | 说明 |
| --- | --- | --- | --- |
| **蒸汽模式**（默认） | js / ts | `main.ts` / `main.js` | 2026 年推出，性能反超原生，**推荐新项目使用** |
| VDOM 模式（旧） | uts 强类型 | `main.uts` | 编译为 kotlin/swift/ets，存量项目用 |

**本技能默认输出蒸汽模式（ts）**。若用户明确要求 uts 写法，见第 9 节"双模式切换"。

### 6. 组件与 API

- 基础组件沿用 uni-app / 小程序规范：`view`、`text`、`image`、`scroll-view`、`swiper` 等
- 全局 API 用 `uni.xxx`，如 `uni.navigateTo`、`uni.showToast`
- 页面生命周期：`onLoad`、`onShow`、`onReady`、`onPullDownRefresh`、`onReachBottom`

---

## 使用流程

### 步骤 1：识别输入并解析原型

读取用户提供的材料，产出一份**页面清单（Page Inventory）**：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `page_name` | 页面标识 | `index` |
| `page_path` | 文件路径 | `pages/index/index.uvue` |
| `route` | 路由 | `/pages/index/index` |
| `title` | 导航标题 | `技能互换` |
| `layout_type` | 布局原型 | `list` / `detail` / `form` / `grid` |
| `components` | 需要的 UI 组件 | `card`、`tag`、`avatar` |
| `data_fields` | 页面所需数据字段 | `title`、`price`、`avatar` |
| `interactions` | 交互行为 | `点击进入详情`、`下拉刷新` |

**机器可读的中间产物**：按 `resources/specifications/prototype_parser_contract.md` 定义的 schema 输出 `proto_context.json`。若用户提供的是 HTML，可直接用 `resources/tools/parse_prototype.py` 生成初稿。

### 步骤 2：确认视觉与交互决策

解析出清单后，向用户确认**无法从材料推断**的部分：

- tabBar 结构
- 主色 / 圆角 / 间距基调
- 列表是否分页、是否下拉刷新
- 空态 / 加载态 / 错误态的样式

用**选择题**提问，避免开放式提问。

### 步骤 3：生成工程骨架

从 `resources/templates/project_structure/` 复制骨架，并替换占位符：

```text
{{project_name}}      工程名（kebab-case）
{{app_title}}         应用显示名
{{appid}}             __UNI__ 开头
{{primary_color}}     主色
```

生成的文件：

- `README.md`（**必备说明文档**，从 `resources/templates/project_structure/README.md` 模板生成，见步骤 7）
- `jsconfig.json`（声明 `@/*` 别名，保证 VS Code 里 `@/services/api/*` 导入可跳转）
- `.vscode/settings.json`（把 `*.uvue` 关联为 Vue 语法，Volar 才生效）
- `manifest.json`（**必须含 `"uni-app-x": {}`**）
- `pages.json`（注册全部页面 + tabBar + globalStyle）
- `App.uvue`（全局样式与生命周期）
- `main.ts`（Vue 应用入口）
- `uni.scss`（设计 token 变量）
- `pages/*/*.uvue`
- `components/*.uvue`
- `services/api/*.ts` + `services/mock/*.ts`
- `types/*.ts`
- `package.json`（蒸汽模式下的依赖与脚本，可选）

### 步骤 4：生成页面与组件

按 `resources/templates/pages/` 下的布局原型模板生成：

| 布局原型 | 模板 | 适用 |
| --- | --- | --- |
| 列表页 | `list_page_template.uvue` | 信息流、商品列表、动态 |
| 详情页 | `detail_page_template.uvue` | 内容详情、商品详情 |
| 表单页 | `form_page_template.uvue` | 编辑、新建、提交 |
| 宫格页 | `grid_page_template.uvue` | 功能入口、分类导航 |
| 个人中心 | `profile_page_template.uvue` | 用户信息 + 设置项 |

**还原规则**（详见 `resources/specifications/visual_restoration_rules.md`）：

- 间距使用 `uni.scss` 中的 token，不写魔法数字
- 圆角、阴影、字号统一取自 token
- 每个页面的数据来自 `services/api`
- 加载态、空态必须有，不能只有"有数据"一种情况

### 步骤 5：填充 mock 数据

`services/mock/*.ts` 提供与真实接口**形状一致**的数据：

```ts
// services/mock/skill.mock.ts
export const mockSkillList: Skill[] = [
  { id: 1, title: '摄影入门', ... }
]
```

要点：

- 数据量要**足够撑满一屏**，否则看不出布局效果
- 包含**边界数据**：超长标题、无图片、零条数据
- 用 `mockDelay()` 模拟网络延迟，让加载态真实可见

### 步骤 6：实现交互

至少覆盖：

- 页面跳转（`uni.navigateTo` / `switchTab` / `navigateBack`）
- 点击反馈（`:active` 样式或 `hover-class`）
- 列表下拉刷新（`onPullDownRefresh` + `uni.stopPullDownRefresh`）
- 上拉加载更多（`onReachBottom`）
- 轻提示（`uni.showToast`）、确认弹窗（`uni.showModal`）
- 表单校验与提交反馈

### 步骤 7：生成配套说明文档（README.md）

生成的工程**必须**自带一份 `README.md` 说明文档，放在工程根目录，不得遗漏。

- 以 `resources/templates/project_structure/README.md` 为模板，替换占位符后写入工程根目录
- 必须包含以下小节（缺一不可）：
  1. **一句话项目简介**：来源原型、应用定位、主要功能
  2. **技术栈**：uni-app x（蒸汽模式/TS）+ 运行端（App/小程序/H5）
  3. **如何运行**：HBuilder 5.25+ 打开 → 运行到浏览器/手机；提示检查 `manifest.json` 的 `uni-app-x` 标记
  4. **在 VS Code 中开发**：说明 VS Code 只负责编辑、运行仍需 HBuilderX；推荐扩展；`jsconfig.json` 与 `.vscode/settings.json` 的作用；明确本工程非 CLI 工程，禁止 `npm run dev`
  5. **目录结构**：用代码块呈现真实生成的目录树
  6. **页面清单**：表格列出每个页面的路由与用途
  7. **对接后端 API**：`USE_MOCK` 开关 + `BASE_URL` + 函数签名对齐，强调页面代码零改动
  8. **注意事项**：`.uvue` 后缀、flex 默认竖向、文字须在 `<text>` 内、新页面须注册 `pages.json`
- 文档内容必须与工程实际一致（页面数量、目录树、组件名等以真实生成为准），不要照抄模板占位符
- Markdown 排版约定：表格分隔行统一写成 `| --- | --- |`（竖线两侧各一个空格），**不要**写成 `|---|---|`，否则 markdownlint 的 MD060 会报表格风格不一致

### 步骤 8：自检与输出

运行 `resources/tools/validate_project.py` 做静态检查：

- 工程根目录是否含 `README.md` 说明文档
- `pages.json` 中注册的页面文件是否都存在
- 是否存在 `.vue` 页面（应为 `.uvue`）
- `manifest.json` 是否含 `"uni-app-x"`
- 页面是否直接写死业务数据（应走 services）
- 是否存在 App 端不支持的 CSS 用法

> Windows 下 GBK 控制台直接运行该脚本可能因输出 emoji 报 `UnicodeEncodeError`，可先设置 `$env:PYTHONIOENCODING='utf-8'`（PowerShell）或 `set PYTHONIOENCODING=utf-8`（cmd）再运行。

生成完成后输出文件清单与**"如何对接真实接口"**的说明。

---

## 文件结构（生成的目标工程）

```text
{{project_name}}/
├── README.md                   # 工程说明文档（必备：运行方式/结构/对接后端/注意事项）
├── App.uvue                    # 全局样式、应用生命周期
├── main.ts                     # Vue 应用入口（蒸汽模式）
├── pages.json                  # 页面注册 + tabBar + globalStyle
├── manifest.json               # 应用配置（必须含 "uni-app-x": {}）
├── uni.scss                    # 设计 token
├── pages/
│   ├── index/index.uvue
│   ├── detail/detail.uvue
│   └── ...
├── components/
│   ├── nav-bar.uvue
│   ├── empty-state.uvue
│   ├── list-card.uvue
│   └── ...
├── services/
│   ├── api/
│   │   ├── request.ts          # 请求封装（含 mock 开关）
│   │   └── skill.ts            # 业务接口
│   └── mock/
│       ├── skill.mock.ts
│       └── delay.ts
├── store/                      # 可选
├── types/
│   └── skill.ts
├── utils/
│   ├── format.ts
│   └── validate.ts
└── static/
    └── logo.png
```

---

## 对接后端 API（本技能的收尾目标）

生成的工程天然预留了接缝。对接真实接口时**只需三步**：

### 1. 切换数据源开关

`services/api/request.ts` 中：

```ts
export const USE_MOCK = true   // 改成 false 即切到真实请求
```

### 2. 配置 baseURL

```ts
const BASE_URL = 'https://api.your-domain.com'
```

### 3. 对齐接口返回结构

`services/api/*.ts` 中的函数签名保持不变，只改内部实现：

```ts
// 改造前（mock）
export async function getSkillList(page: number): Promise<Skill[]> {
  await mockDelay()
  return mockSkillList
}

// 改造后（真实请求）
export async function getSkillList(page: number): Promise<Skill[]> {
  return request<Skill[]>({ url: '/skills', method: 'GET', data: { page } })
}
```

**页面代码一行都不用改** —— 这是分层设计的价值。

---

## 代码规范

### 命名

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 页面目录 | kebab-case | `pages/skill-detail/` |
| 页面文件 | kebab-case | `skill-detail.uvue` |
| 组件文件 | kebab-case | `skill-card.uvue` |
| 组件引用 | PascalCase | `<SkillCard />` |
| 类型 | PascalCase | `SkillDetail` |
| 函数/变量 | camelCase | `getSkillList` |
| 常量 | UPPER_SNAKE | `USE_MOCK` |
| CSS class | kebab-case | `.skill-card__title` |

### 样式

- 使用 BEM 风格的 class 命名：`.block__element--modifier`
- **必须显式声明** `flex-direction: row`（App 端默认是 column）
- 每个 `<text>` 自带样式，不依赖继承
- 尺寸优先用 `rpx`（响应式），固定 1px 边框可用 `px`

### 注释

- 中文注释
- 每个页面顶部说明：页面用途、数据来源、主要交互

---

## 输出格式

生成完成后，向用户展示：

```text
✅ 已生成 uni-app x 工程：{{project_name}}

📁 结构
├── pages/            {{N}} 个页面
├── components/       {{M}} 个组件
├── services/api/     数据接口层（对接后端的唯一接缝）
└── services/mock/    mock 数据

🎨 已还原
- 页面：首页 / 详情 / 我的（3 个）
- 组件：卡片、标签、空态、导航栏
- 交互：列表下拉刷新、点击跳转详情、加载态

▶️ 如何运行
1. 用 HBuilder 打开本目录（5.25+，默认蒸汽模式）
2. 运行 → 运行到浏览器（最快）或 运行到手机
3. 若提示非 uni-app x 项目，检查 manifest.json 是否含 "uni-app-x": {}

🔌 如何对接后端
1. services/api/request.ts 中 USE_MOCK 改为 false
2. 设置 BASE_URL
3. 按 services/api/*.ts 中的函数签名对齐接口
（页面代码无需改动）

⚠️ 待确认
- 详情页的评论区分页规则
- 空态文案是否用占位图
```

---

## 双模式切换（蒸汽模式 ↔ UTS）

用户要求 uts 写法时，改动点有限：

| 项 | 蒸汽模式（默认） | UTS 模式 |
| --- | --- | --- |
| 入口文件 | `main.ts` | `main.uts` |
| 脚本块 | `<script setup lang="ts">` | `<script setup>`（不上 lang，或 `lang="uts"`） |
| 类型定义 | `types/*.ts` | `types/*.uts` |
| 类型标注 | 可省略 | **必须**显式标注（强类型） |
| 接口定义 | TS `interface` | UTS `type` |

**注意**：两种模式**不要混用**。一个工程里要么全是 ts，要么全是 uts。

---

## 错误处理与边界

### 原型不足以还原时

不要臆造复杂交互。做法：

1. 生成**静态可看**的版本（布局 + mock 数据）
2. 在输出里明确标注："以下交互为占位，需你确认：…"
3. 列出待确认清单

### 原型含 Web 专有特性时

如 `<div>` 绝对定位复杂叠层、CSS Grid、动画库、canvas 图表：

- CSS Grid → 用 flex 嵌套模拟
- 复杂绝对定位 → 保留，但说明 App 端可能有差异
- JS 动画库 → 改用 uni-app x 的 CSS transition / animation
- 图表 → 建议引入 uts 插件或降级为静态图

### 图片资源

原型里的图片链接**不能直接引用**（跨域/失效）。做法：

- 占位图放 `static/`
- 或使用可访问的 CDN 地址（需用户确认可用）
- 在 `types` 或配置中集中管理图片 URL

---

## 资源文件结构

```text
prototype-to-app-uniappx/
├── SKILL.md
├── README.md
├── docs/
│   └── {{IDE}}中使用skill配置.md
└── resources/
    ├── config/
    │   ├── naming_rules.json        # 命名规则
    │   ├── design_tokens.json       # 默认设计 token
    │   └── mock_policy.json         # mock 数据生成策略
    ├── specifications/
    │   ├── prototype_parser_contract.md   # 原型 → context 的契约
    │   ├── page_mapping_rules.md          # 原型结构 → 组件的映射
    │   └── visual_restoration_rules.md    # 视觉还原规则
    ├── templates/
    │   ├── project_structure/       # 工程骨架
    │   ├── pages/                   # 页面布局模板
    │   └── layers/                  # 分层代码模板
    ├── tools/
    │   ├── parse_prototype.py       # HTML 原型 → proto_context.json
    │   ├── validate_project.py      # 生成工程自检
    │   └── preview_plan.py          # 预览生成计划
    └── demo_output/                 # 示例产物
```

---

## 重要提示

1. **`.uvue` 不是 `.vue`** —— 页面文件后缀写错，整个工程跑不起来
2. **flex 默认竖向** —— 横向布局必须显式 `flex-direction: row`
3. **样式不继承，文字必须在 `<text>` 内** —— 这是 App 端最常见的白屏原因
4. **`pages.json` 必须注册** —— 漏注册的页面不会被打包
5. **`manifest.json` 必须含 `"uni-app-x": {}`** —— 否则被识别为普通 uni-app
6. **页面不写死数据** —— 一律走 `services/api`，否则无法对接后端
7. **mock 要像真数据** —— 有长度、有边界、有延迟，否则看不出布局问题
8. **默认输出蒸汽模式（ts）** —— 旧项目要 uts 时按第 9 节切换，不要混用
9. **不要臆造交互** —— 原型没体现的，列进待确认清单
10. **中文注释与文案** —— 与团队习惯保持一致
11. **工程必须带 README.md** —— 生成后根目录必须含说明文档（运行/结构/页面清单/对接后端/注意事项），内容与实际工程一致
