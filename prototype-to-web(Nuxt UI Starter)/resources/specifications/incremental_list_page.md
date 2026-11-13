# 已有工程增量：按原型图新增栏目和信息列表页

适用：目标目录**已经是**本技能生成的 Nuxt UI Starter 工程（或同结构工程），用户再提供一张**信息列表页**原型图，要求新加栏目、新加列表页。

全量生成（从零复制 `templates/project_structure/`）不走本文。

---

## 1. 先判定，再动手

骨架已存在，当目录里**同时**有：

- `nuxt.config.ts`（modules 含 `@nuxt/ui`）
- `app/pages/`
- `app/services/`

| 场景 | 判定 | 动作 |
| --- | --- | --- |
| **新增列表页** | 目标路由对应的 `app/pages/*.vue` **不存在** | 按第 4 节成套新增，并在 `app/navigation.ts` **追加**一项 |
| **该页已存在** | 同名页面文件已在 | **停下来问**。用户没说“按新图改这一页”之前，不覆盖 |
| **图不是列表** | 画面主体是表单、详情、个人中心、落地页 | 停下来说明本路径只生成信息列表页，请用户确认是否改走别的 `layout_type` |

一次只落地**当前这张图对应的一个列表页**。图的顶栏里若还有别的栏目名，写进 `need_confirm`，不要顺手生成那些页面。

---

## 2. 禁止事项

- 禁止把 `resources/templates/project_structure/` 再复制进目标工程
- 禁止改 `package.json`、`nuxt.config.ts`、`app/app.config.ts`、`app/assets/css/main.css`（用户没要求换主色或依赖时）
- 禁止重写已有 `pages/`、`services/`、`composables/`、`types/`、`components/`
- 禁止删、改已有栏目文案。顶栏只追加
- 看不清的字段、跳转、筛选项不要猜。能看清的先做，其余列入「待确认」

`app.vue` 只允许补导航接线（第 3 节）。页头 Logo、页脚、SEO 元信息保持原样。

---

## 3. 栏目只有一个登记处

文件：`app/navigation.ts`

```ts
/** 顶栏栏目。新增栏目只在此数组末尾追加一项。 */
export const navItems = [
  { label: '首页', to: '/', icon: 'i-lucide-home' }
]
```

`app.vue` 的 `UHeader` 必须消费这份数组（Nuxt UI 4 组件名是 `UNavigationMenu`，不是 `UNavigation`）：

```vue
<script setup lang="ts">
import { navItems } from './navigation'
</script>

<template>
  <UHeader>
    <template #left>
      <!-- 保留已有 Logo，不要改 -->
    </template>

    <UNavigationMenu :items="navItems" />

    <template #right>
      <!-- 保留已有右侧按钮，不要改 -->
    </template>

    <template #body>
      <UNavigationMenu :items="navItems" orientation="vertical" class="-mx-2.5" />
    </template>
  </UHeader>
</template>
```

工程里还没有 `app/navigation.ts` 时：

1. 新建该文件，先写入**已经存在的首页**（`/` → `首页`），再追加本次新栏目
2. 按上面的插槽把 `UNavigationMenu` 接进现有 `UHeader`，不要整文件替换 `app.vue`

以后每次加栏目，只追加数组的一项：

```ts
{ label: '资讯', to: '/news', icon: 'i-lucide-newspaper' }
```

`label` 用图里高亮或页面标题上的栏目名。`to` 用 kebab-case 路径。`icon` 用能对上含义的 `i-lucide-*`；对不上就用 `i-lucide-layout-list`，不要留空字符串。

---

## 4. 从原型图读什么

按这个顺序看图，写进页面清单后再生成文件：

| 顺序 | 看什么 | 写到哪里 |
| --- | --- | --- |
| 1 | 页面主标题 | `pages/*.vue` 的 `h1` |
| 2 | 顶栏里本次要新增的栏目名 | `navItems[].label` |
| 3 | 重复出现的那一张卡片 | `*Card.vue` 的可见字段 |
| 4 | 卡片是单列还是多列 | 页面网格：单列 `grid gap-4`，多列再加 `md:grid-cols-2` 或 `lg:grid-cols-3` |
| 5 | 筛选项、搜索框、Tab | 有才做；没有不要补 |
| 6 | 卡片是否明显可点进详情 | 可点只记入待确认。**没有第二张详情图时不生成详情页** |

卡片字段只映射图上看得见的内容，例如标题、摘要、封面、作者、时间、标签。每条数据都要有 `id: string`。

---

## 5. 一个列表页的成套文件

下面用「资讯 / News / `/news`」举例。换成实际实体时保持同一套命名：页面与路径 kebab-case，组件与类型 PascalCase，composable 为 `use` + PascalCase，service 为 camelCase + `Service`。

### 5.1 `app/types/news.ts`

```ts
/** 资讯列表项。字段与列表卡片可见内容一致。 */
export interface News {
  id: string
  title: string
  summary: string
  cover: string
  author: string
  publishedAt: string
}
```

### 5.2 `app/services/newsService.ts`

```ts
/**
 * 资讯数据服务层（唯一数据接缝）
 * 对接后端时只改本文件：useMock=false，并核对 $fetch 路径。
 */

const useMock = true
const API_BASE = '/api'

function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

const mockNews: News[] = [
  { id: '1', title: '示例标题', summary: '摘要', cover: '', author: '张三', publishedAt: '2024-03-01' }
  // 至少 6 条。其中 1 条标题超长，1 条 cover 为空
]

export const newsService = {
  async getNews(): Promise<News[]> {
    if (useMock) {
      await delay(300)
      return mockNews
    }
    return await $fetch<News[]>(`${API_BASE}/news`)
  }
}
```

### 5.3 `app/composables/useNews.ts`

与 `useSkills` 相同：`items` / `loading` / `error` / `load()`，`load` 只调用 `newsService.getNews()`。页面文件里不要出现 `$fetch` 或 `fetch(`。

### 5.4 `app/components/NewsCard.vue`

- `defineProps<{ item: News }>()`
- 外层 `UCard`
- 封面缺省时用 `UIcon` 或纯色块，不引用原型图里的外链
- 颜色只用 `text-primary`、`bg-muted` 这类语义色

### 5.5 `app/pages/news.vue`

结构与起步工程的 `app/pages/index.vue` 相同，四段按这个顺序：

1. `loading`：三张 `UCard` + `animate-pulse`
2. `error`：`UAlert` + 重试按钮调用 `load`
3. 空列表：已有的 `EmptyState`
4. 有数据：`v-for` 渲染 `NewsCard`

`onMounted(() => load())`。页面不直接请求。

---

## 6. 改完必做

在技能目录执行：

```bash
python resources/tools/validate_project.py <目标工程目录>
```

通过标准：无 error；`app/navigation.ts` 里每个站内 `to` 都能落到 `app/pages/` 下的文件；新页面没有原生 `fetch(`。

向用户汇报时列出：新增栏目、新增文件、mock 字段、以及图里没看清所以没做的项。
