# 架构约定（Nuxt UI Starter）

本文定义生成工程的分层规则，基于 Nuxt 4 的约定优于配置理念，结合 Nuxt UI 组件库，确保工程开箱即用且便于后续演进。

参考：
- <https://nuxt.com/docs/guide/concepts/auto-imports>
- <https://ui.nuxt.com/>
- <https://nuxt.com/docs/guide/directory-structure/app>

---

## 1. 分层职责

```text
UI 层（pages/ + components/）    ← 只负责展示与交互，调用 composables
       ↓ 调用
逻辑层（composables/）            ← 持有状态、调用 service、暴露响应式数据
       ↓ 依赖
数据层（services/）               ← Repository 抽象 + 数据源切换（mock/remote）
       ↓ 依赖
基础设施（types/ + utils/ + app.config.ts）
```

### UI 层

| 组成 | 职责 | 禁止 |
| --- | --- | --- |
| `app/pages/*.vue` | 页面组件、路由入口、SEO 元信息 | 直接发请求、写复杂业务规则 |
| `app/components/*.vue` | 可复用组件（自动导入） | 感知数据来源、直接调用 service |
| `app/layouts/` | 页面布局骨架 | 业务逻辑 |

**关键**：页面只调用 composables 获取数据与方法，不直接 `$fetch`。

### 逻辑层

| 组成 | 职责 |
| --- | --- |
| `app/composables/use*.ts` | 组合式函数，持有 `ref`/`reactive` 状态，调用 service，暴露给页面 |

**composable 是状态与逻辑的容器**，类似 Flutter 的 Controller，但更轻量。多个页面可共享同一 composable。

### 数据层

| 组成 | 职责 |
| --- | --- |
| `app/services/*Service.ts` | 定义数据获取方法，内部根据 `useMock` 开关决定走 mock 还是 remote |
| mock 数据 | 内联在 service 文件中或 `app/data/mock/` 下 |
| remote | 用 Nuxt 内置 `$fetch` 调用真实 API |

**Service 是唯一数据接缝**：页面与 composable 只依赖 service 的方法签名，不依赖具体数据源。

### 基础设施

| 组成 | 职责 |
| --- | --- |
| `app/types/` | TypeScript 接口与类型（自动导入） |
| `app/utils/` | 纯函数工具（自动导入） |
| `app/app.config.ts` | Nuxt UI 主题配置（颜色、组件默认 props） |
| `app/assets/css/main.css` | Tailwind 入口与全局样式 |
| `nuxt.config.ts` | Nuxt 模块、构建配置 |

### 服务端（Nitro）

| 组成 | 职责 |
| --- | --- |
| `server/api/` | Nitro API 路由（可选，对接后端时可在此做 BFF 代理） |
| `server/routes/` | Nitro 服务端路由（可选） |

**Nitro 是 Nuxt 4 的服务端引擎**，内置在 Nuxt 中无需额外安装。原型阶段通常用 mock 数据，无需写 server 端代码；对接真实后端时，可在 `server/api/` 中定义接口转发或直接由前端 `$fetch` 调用。

---

## 2. 依赖方向（严格单向）

```text
pages  →  composables  →  services  →  types/utils
  │           │              ↑
  └── components ←───────────┘
```

禁止：

- `services` 反向依赖 `pages` 或 `composables`
- `components` 直接调用 `services`（应通过 props/events 或 composables）
- 页面直接 `$fetch`（必须经过 service）

---

## 3. 目录结构

```text
app/
├── app.vue                    # 根组件：UApp + UHeader + UMain(NuxtPage) + UFooter
├── navigation.ts              # 顶栏栏目唯一登记处，供 UNavigationMenu 使用
├── app.config.ts              # Nuxt UI 主题（colors.primary / neutral）
├── assets/
│   └── css/main.css           # @import tailwindcss + @nuxt/ui
├── components/                # 自动导入组件
│   ├── AppLogo.vue
│   ├── SkillCard.vue
│   └── EmptyState.vue
├── composables/               # 自动导入组合式函数
│   └── useSkills.ts           # 列表状态：items / loading / error / load()
├── pages/                     # 文件路由
│   ├── index.vue              # /
│   └── detail.vue             # /detail
├── services/                  # 数据服务层（唯一接缝）
│   └── skillService.ts        # getSkills()：useMock ? mock : $fetch
├── types/                     # 自动导入类型
│   └── skill.ts               # interface Skill { ... }
└── utils/                     # 自动导入工具
    └── format.ts
server/                        # Nitro 服务端（可选，原型阶段通常不需要）
└── api/                       # Nitro API 路由
    └── skills.get.ts          # GET /api/skills
```

**注意**：Nuxt 4 推荐使用 `app/` 目录（而非根目录的 `pages/`/`components/`）。模板即采用 `app/` 结构。

---

## 4. 状态管理约定（Composables）

### 标准写法

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

<template>
  <div v-if="loading">加载中...</div>
  <UAlert v-else-if="error" :title="error" color="red" />
  <EmptyState v-else-if="!items.length" />
  <div v-else class="grid gap-4">
    <SkillCard v-for="item in items" :key="item.id" :item="item" />
  </div>
</template>
```

### 强制规则

1. **状态必须用 `ref` / `reactive`**，保证响应式
2. **异步操作必须处理 loading 与 error**，不能只有成功态
3. **不要在 `<script setup>` 顶层直接 `await`** 会阻塞组件初始化，用 `onMounted` 或 `useAsyncData`
4. **composable 内不引用组件实例**，保持纯逻辑

---

## 5. 路由约定（文件路由）

Nuxt 采用文件路由，无需手动注册：

| 文件 | 路由 |
| --- | --- |
| `app/pages/index.vue` | `/` |
| `app/pages/detail.vue` | `/detail` |
| `app/pages/skills/[id].vue` | `/skills/:id` |
| `app/pages/skills/index.vue` | `/skills` |

页面间跳转：

```vue
<NuxtLink to="/detail">详情</NuxtLink>
<!-- 或 -->
const router = useRouter()
router.push('/detail')
```

传参：

```ts
// 跳转
router.push({ path: '/detail', query: { id: skill.id } })

// 接收
const route = useRoute()
const id = computed(() => route.query.id as string)
```

---

## 6. 数据服务约定（Service 层）

```ts
// app/services/skillService.ts
const useMock = true // 对接后端时改 false

const mockSkills: Skill[] = [/* ... */]

export const skillService = {
  async getSkills(): Promise<Skill[]> {
    if (useMock) {
      await delay(300) // 模拟网络延迟
      return mockSkills
    }
    return await $fetch<Skill[]>('/api/skills')
  },

  async getSkillById(id: string): Promise<Skill | null> {
    if (useMock) {
      await delay(200)
      return mockSkills.find(s => s.id === id) ?? null
    }
    return await $fetch<Skill>(`/api/skills/${id}`)
  }
}
```

**对接后端三步**：

1. `useMock` 改为 `false`
2. 确认 `$fetch` 的 API 路径与返回结构
3. 页面与 composable 零改动

---

## 7. 错误处理约定

### Service 层

`$fetch` 失败时抛错，由 composable 捕获：

```ts
try {
  items.value = await skillService.getSkills()
} catch (e) {
  error.value = e instanceof Error ? e.message : '加载失败，请重试'
}
```

### UI 层

三态 + 错误重试：

```vue
<UButton v-if="error" @click="load">重试</UButton>
```

---

## 8. 样式约定

1. **优先用 Nuxt UI 组件**（`UButton`、`UCard`、`UInput` 等），保证一致性
2. **布局用 Tailwind 工具类**（`flex`、`grid`、`gap-*`、`p-*`）
3. **颜色走 Tailwind 语义色**（`text-primary`、`bg-primary`），不硬编码 hex
4. **暗色模式**：Nuxt UI 自动适配，无需手动写 `dark:` 前缀（除非需要微调）
5. **响应式**：用 `sm:`/`md:`/`lg:` 断点前缀

---

## 9. 测试约定

建议至少提供一个组件测试（可选，原型阶段不强制）：

```ts
// test/SkillCard.test.ts
import { mount } from '@vue/test-utils'
import SkillCard from '~/components/SkillCard.vue'

test('渲染技能标题', () => {
  const wrapper = mount(SkillCard, {
    props: { item: { id: '1', title: 'Vue 入门' } }
  })
  expect(wrapper.text()).toContain('Vue 入门')
})
```

注意：模板默认不含测试依赖，需要时再引入 `@vue/test-utils` + `vitest`。

---

## 10. 已有工程新增栏目与列表页

起步工程生成之后，用户用一张信息列表页原型图加栏目、加列表页时，按 `incremental_list_page.md` 执行。

- 栏目只追加到 `app/navigation.ts`
- 新列表页沿用本节的依赖方向：页面 → composable → service
- 不覆盖已有页面，不重跑整套模板复制
