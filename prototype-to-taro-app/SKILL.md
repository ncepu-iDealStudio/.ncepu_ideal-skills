---
name: "prototype-to-taro-app"
description: "从原型（设计图截图、HTML/CSS 代码或 PRD 页面清单）生成符合 Taro 规范的多端小程序/App 工程骨架，支持 Vue3+TS 与 React+TS 两种技术栈（由用户确认后选用其一）。内置登录、权限路由、请求封装、分页列表、下拉刷新、暗黑模式、多环境等能力，用 mock 数据还原页面与交互。用户提到「Taro 小程序」「原型转小程序」「Taro 脚手架」「多端 App」「用 React/Vue 做小程序」时使用。"
---

# Prototype to Taro App（Vue3 / React 双框架）

## 概述

把**原型**转换成**可运行的 Taro 多端工程**，一次编写，编译到微信小程序、支付宝小程序、H5、React Native。

**核心特点：支持双框架，由用户选择。**

| 分支 | 技术栈 | 适合 |
| --- | --- | --- |
| **Vue3** | Taro 4 + Vue 3 + TS + Vant + Pinia | 团队熟悉 Vue；需要快速还原 UI |
| **React** | Taro 4 + React 18 + TS + Dva/Redux + taro-ui | 复杂业务系统、企业业务 App |

> 两者能力对等，**不存在默认值**，必须由用户选择。

> ⚠️ **第一步必须让用户确认框架**，不要自行假设。

---

## 前置决策（开工前必须确认）

### 1. 框架选择（必问）

```text
请确认用哪个框架生成：
[A] Vue3 + TS（推荐给熟悉 Vue 的团队，UI 还原快）
[B] React + TS（适合复杂业务、状态流较重的企业应用）
```

**必须由用户明确选择**，技能不设默认值；用户未说明时一定要问，不要自行假设。

### 2. 其他必确认项

- **目标平台**：微信小程序 / H5 / 支付宝小程序 / RN（可多选）
- **是否需要登录与权限路由**（默认生成）
- **UI 组件库**：Vue3 侧 Vant Weapp；React 侧 taro-ui（或按团队要求）
- **是否需要暗黑模式**（Vue3 分支内置）

---

## 技术基线（实测核对）

| 项 | Vue3 分支 | React 分支 |
| --- | --- | --- |
| Taro | **4.x** | **4.x** |
| 框架 | Vue 3.4+ | React 18 |
| 语言 | TypeScript | TypeScript |
| 状态 | **Pinia** | **Dva + Immer**（Redux 封装） |
| UI | **Vant**（H5）+ **Vant Weapp**（小程序） | **taro-ui** |
| 构建 | Webpack5（Taro 内置） | Webpack5（Taro 内置） |
| 包管理 | pnpm | pnpm |

> **重要说明**：参考资料 `RealCoolSnow/taro-vue3-ts` 仓库当前已 **404（不可访问）**，本技能按 **Taro 官方规范**自建 Vue3 模板；`didilinkin/elf-taro` 实际锁定 Taro 3.0-rc + React 16 + Dva，本技能把其**架构思路**（拦截器、异常捕获、多环境）适配到 **Taro 4 + React 18**。

---

## 工程结构

### Vue3 分支

```text
{{project_name}}/
├── config/
│   ├── index.ts            # 主配置（framework: 'vue3'）
│   ├── dev.ts / prod.ts    # 多环境
├── src/
│   ├── app.ts              # 应用入口（createApp）
│   ├── app.config.ts       # 全局配置：pages / tabBar / window
│   ├── app.scss
│   ├── pages/
│   │   └── <page>/
│   │       ├── index.vue
│   │       ├── index.config.ts   # 页面标题等
│   │       └── model.ts          # 页面状态（可选）
│   ├── components/         # 公共组件
│   ├── store/              # Pinia
│   │   ├── index.ts
│   │   └── modules/{user,app}.ts
│   ├── services/           # API 层
│   │   ├── request.ts      # Taro.request 封装
│   │   └── modules/<domain>.ts
│   ├── utils/              # 工具
│   ├── mock/               # mock 数据
│   └── types/              # 类型定义
└── project.config.json     # 小程序项目配置
```

### React 分支

```text
{{project_name}}/
├── config/                 # 同 Vue3，framework: 'react'
├── src/
│   ├── app.tsx             # Provider 包裹（Dva store）
│   ├── app.config.ts
│   ├── pages/<page>/index.tsx
│   ├── models/             # Dva models
│   ├── services/           # 请求封装 + 拦截器
│   ├── utils/
│   └── types/
└── project.config.json
```

---

## 使用流程

### 步骤 1：确认框架与目标平台

见上文"前置决策"。**先问再做**。

### 步骤 2：解析原型

从设计图／HTML／PRD 中提取页面清单：

| 字段 | 示例 |
| --- | --- |
| `page_name` | `home` |
| `path` | `pages/home/index` |
| `title` | `首页` |
| `is_tab` | `true` |
| `layout` | `list` / `detail` / `form` / `grid` |
| `components` | `Card` / `Tag` / `Empty` |
| `interactions` | 跳转、下拉刷新、加载更多 |

按 `resources/specifications/prototype_parser_contract.md` 输出 `proto_context.json`。HTML 输入可用 `resources/tools/parse_prototype.py`。

### 步骤 3：生成工程骨架

按选定框架，从 `resources/templates/{vue3|react}/` 复制，替换占位符：

```text
{{project_name}}      工程名（kebab-case）
{{app_title}}         小程序显示名
{{appid}}             小程序 appid
{{primary_color}}     主色
```

### 步骤 4：生成页面

**Vue3 侧**：`pages/<name>/index.vue` + `index.config.ts`
**React 侧**：`pages/<name>/index.tsx` + `index.config.ts`

每个页面必须：

- 有 `index.config.ts`（设置标题）
- 在 `app.config.ts` 的 `pages` 数组注册
- 三态渲染（loading / empty / 有数据）

### 步骤 5：接入状态与请求

**Vue3**：

```ts
// store/modules/user.ts
export const useUserStore = defineStore('user', () => {
  const token = ref('')
  async function login(payload) {
    const res = await authApi.login(payload)
    token.value = res.token
    Taro.setStorageSync('token', res.token)
  }
  return { token, login }
})
```

**React**：

```ts
// models/user.ts
export default {
  namespace: 'user',
  state: { token: '' },
  effects: {
    *login({ payload }, { call, put }) {
      const res = yield call(authApi.login, payload)
      yield put({ type: 'setToken', payload: res.token })
    },
  },
  reducers: {
    setToken(state, { payload }) { return { ...state, token: payload } },
  },
}
```

### 步骤 6：填充 mock 数据

`src/mock/` 下提供与真实接口同形状的数据，列表至少 10 条，含超长文本与空数组边界。

### 步骤 7：自检

运行 `resources/tools/validate_project.py`：

- `app.config.ts` 的 pages 与 `src/pages/` 目录一一对应
- 每个页面有 `index.config.ts`
- 框架配置正确（`framework: 'vue3'` 或 `'react'`）
- 页面文件扩展名与框架匹配（`.vue` vs `.tsx`）
- 未混用两套框架的写法

---

## 双框架关键差异（生成时最易出错）

| 维度 | Vue3 分支 | React 分支 |
| --- | --- | --- |
| 页面文件 | `index.vue` | `index.tsx` |
| 入口 | `app.ts`（createApp） | `app.tsx`（class/函数 + Provider） |
| 组件定义 | `<script setup>` | 函数组件 + Hooks |
| 状态 | Pinia `defineStore` | Dva `model`（namespace/state/effects/reducers） |
| 状态读取 | `storeToRefs(useUserStore())` | `useSelector((s) => s.user)` |
| 状态更新 | 直接改变量 | `dispatch({ type: 'user/setToken' })` |
| UI 库 | Vant / Vant Weapp | taro-ui |
| 生命周期 | `onShow`/`onLoad`（Taro 提供） | `useDidShow`/`useLoad`（Taro hooks） |

**禁止混用**：一个工程只能有一种页面文件后缀。

---

## 内置能力（生成时一并产出）

| 能力 | 说明 |
| --- | --- |
| **登录** | 登录页 + token 持久化（`Taro.setStorageSync`） |
| **权限路由** | 无 token 跳登录；白名单页面免登录 |
| **请求封装** | 统一 baseURL、超时、错误码、401 跳登录 |
| **分页列表** | 下拉刷新 + 上拉加载 + 到底提示 |
| **表单** | 输入校验 + 提交反馈 |
| **暗黑模式**（Vue3） | CSS 变量 + `Taro.getSystemInfoSync().theme` |
| **多环境** | `config/dev.ts` / `prod.ts` + `process.env` |
| **异常捕获** | `app.onError` + 请求层兜底 |

---

## 命名规范

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 页面目录 | kebab-case | `pages/order-list/` |
| 页面文件 | `index.vue` / `index.tsx` | |
| 页面配置 | `index.config.ts` | |
| 组件 | PascalCase 文件 | `OrderCard.vue` |
| Store（Vue3） | `use<Name>Store` | `useUserStore` |
| Model（React） | `<name>` 小写 | `user` |
| Service | camelCase 函数 | `getOrderList` |
| 类型 | PascalCase | `OrderItem` |

---

## 输出格式

```text
✅ 已生成 Taro 工程：{{project_name}}（{{Vue3 或 React}} 分支）

📁 结构
├── config/         多环境配置
├── src/pages/      {{N}} 个页面
├── src/store/      Pinia
├── src/services/   请求层
└── src/mock/       mock 数据

🎨 已还原
- 页面：首页 / 列表 / 详情 / 我的
- 交互：下拉刷新、上拉加载、tabBar 切换、登录跳转

▶️ 如何运行
1. pnpm install
2. pnpm dev:weapp     # 微信小程序
3. 用微信开发者工具打开 dist/ 目录
（H5：pnpm dev:h5）

⚠️ 待确认
- 小程序 appid
- 各列表页的真实字段
```

---

## 重要提示

1. **先问框架** —— 不存在默认值，必须让用户明确选择
2. **页面必须在 `app.config.ts` 注册** —— 否则不编译进包
3. **每个页面要有 `index.config.ts`** —— 否则标题不对
4. **`pages` 路径不带 `index`** —— 写 `pages/home/index`，但目录要完整
5. **不要混用框架写法** —— `.vue` 和 `.tsx` 不能混在一个工程
6. **请求统一走 `services/request.ts`** —— 便于切真实接口和统一鉴权
7. **mock 要像真数据** —— 有长度有边界，否则看不出布局问题
8. **小程序有包体积限制** —— 主包 2MB，注意静态资源
9. **appid 留占位** —— 让用户填自己的
10. **中文注释与文案**
