# {{app_title}}

基于 [Nuxt UI Starter](https://github.com/nuxt-ui-templates/starter) 生成的应用。技术栈是 Nuxt 4 + TypeScript + ESLint + Nuxt UI，官方起步仓库已经配好这几样。

本仓库是按原型长出来的业务页面。官方 starter 更短，适合对照它看页头、主题和 Nuxt UI 的默认写法：

- 仓库与说明：<https://github.com/nuxt-ui-templates/starter>
- 组件与语义色：<https://ui.nuxt.com/>

需要 Node 20 或以上。包管理用 pnpm。

## 快速开始

```bash
pnpm install
pnpm dev
```

浏览器打开终端里打印的本地地址。另外还有：

```bash
pnpm build      # 生产构建
pnpm preview    # 预览构建结果
pnpm lint       # ESLint
pnpm typecheck  # 类型检查
```

当前列表用的是 `app/services/skillService.ts` 里的 mock，不连后端也能看到数据。

## 目录怎么读

```text
app/
├── app.vue                 # 整站外壳：页头、页脚、NuxtPage
├── error.vue               # 404 / 500，使用 Nuxt UI 的 UError
├── navigation.ts           # 顶栏栏目。新增栏目只改这个数组
├── app.config.ts           # 主题色：primary / neutral
├── pages/                  # 文件名就是路由。index.vue → /
├── components/             # 自动导入，模板里直接写 <SkillCard>
├── composables/            # 自动导入。页面只调用这里
├── services/               # 唯一数据接缝：mock 或真实请求
├── types/                  # 页面用的类型
└── utils/
server/api/                 # Nitro 示例接口，形状与 Skill 类型相同
```

页面不直接请求。调用顺序是：页面 → composable（`useAsyncData`）→ service。

## 新增一个栏目

1. 打开 `app/navigation.ts`，在数组末尾加一项，例如 `{ label: '资讯', to: '/news', icon: 'i-lucide-newspaper' }`。
2. 栏目的 `to` 必须有对应页面，否则校验不通过。

不要在 `app.vue` 里再手写一组链接。顶栏已经绑定 `navItems`。

## 新增一个页面

以「资讯」列表为例。

1. 新建 `app/pages/news.vue`。文件名即路由 `/news`，不用注册路由。
2. 页面里只写：

```vue
<script setup lang="ts">
const { items, loading, error, load } = useNews()
</script>
```

不要再写 `onMounted(() => load())`。`useNews` 内部用 `useAsyncData` 取数，刷新用返回的 `load`。

3. `app/composables/useNews.ts` 照 `useSkills.ts`：取出 `useRequestFetch()` 和 `useRuntimeConfig().public.apiBase`，传给 service。
4. `app/services/newsService.ts` 照 `skillService.ts`：mock 与真实请求都返回同一个类型。真实请求使用传入的 fetcher，不要在页面里写 `$fetch`。
5. 卡片用 `UCard`、`UButton`、`USelect`。颜色用 `text-muted`、`bg-default`、`border-default`、`text-primary`，不要写 `bg-slate-*` 或 `bg-white`。
6. 需要一份能点的示例接口时，照 `server/api/skills.get.ts` 增加 `server/api/news.get.ts`。

按钮、筛选、下拉不要用原生 `<button>` / `<select>`。

## 对接一个接口

1. 看文档里的路径、字段和包络。字段名和页面类型不一致时，只在对应的 service 函数里映射。
2. 把该函数的 `useMock` 改为 `false`。还没对接的函数保持 `true`。
3. 同源示例接口不用改地址，直接请求 `/api/skills`（见 `server/api/skills.get.ts`）。外部接口把基地址写进 `.env`：

```bash
NUXT_PUBLIC_API_BASE=https://api.example.com
```

service 通过 `runtimeConfig.public.apiBase` 读取。不要在 service 里再硬编码另一份基地址。

4. 列表 composable 必须把 `useRequestFetch()` 传进 service，这样服务端渲染时才能带上请求头。页面代码不用改。

更完整的对接约定见技能里的 `resources/specifications/api_binding.md`。

## 改主题

`app/app.config.ts`：

```ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'green',
      neutral: 'slate'
    }
  }
})
```

改 `neutral` 后，语义色（`bg-default`、`text-muted`）会跟着变。手写的 `slate` 类不会跟着变，所以页面里不要写那些类。
