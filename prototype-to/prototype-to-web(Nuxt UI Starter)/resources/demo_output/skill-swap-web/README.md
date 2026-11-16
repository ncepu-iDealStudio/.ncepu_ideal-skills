# 技能互换 (skill-swap-web)

基于 [Nuxt UI Starter](https://github.com/nuxt-ui-templates/starter) 生成的技能互换示例。技术栈是 Nuxt 4 + TypeScript + ESLint + Nuxt UI。

官方 starter 更短，适合对照页头、主题和 Nuxt UI 的默认写法：

- 仓库与说明：<https://github.com/nuxt-ui-templates/starter>
- 组件与语义色：<https://ui.nuxt.com/>

需要 Node 20 或以上，包管理用 pnpm。

## 快速开始

```bash
pnpm install
pnpm dev
```

当前首页用 `app/services/skillService.ts` 里的 mock。另外还有 `pnpm build`、`pnpm preview`、`pnpm lint`、`pnpm typecheck`。

## 目录怎么读

```text
app/
├── app.vue                 # 整站外壳
├── error.vue               # 404 / 500
├── navigation.ts           # 顶栏栏目，只在这里追加
├── pages/index.vue         # 路由 /
├── composables/useSkills.ts
├── services/skillService.ts
└── types/skill.ts
server/api/skills.get.ts    # 与 Skill 同形状的示例接口
```

页面 → composable（`useAsyncData`）→ service。页面里没有 `$fetch`。

## 新增一个栏目

在 `app/navigation.ts` 末尾追加，例如 `{ label: '资讯', to: '/news', icon: 'i-lucide-newspaper' }`。`to` 必须有对应的 `app/pages` 文件。

## 新增一个页面

新建 `app/pages/news.vue`，脚本里只调用 `useNews()`，不要写 `onMounted`。composable 照 `useSkills.ts`，把 `useRequestFetch()` 和 `useRuntimeConfig().public.apiBase` 传给 service。卡片用 Nuxt UI 组件和语义色（`text-muted`、`bg-default`），不要写 `bg-slate-*`。

## 对接一个接口

1. 字段映射只写在 `skillService.ts`。
2. 把要接通的函数的 `useMock` 改为 `false`。
3. 先用本仓库的 `server/api/skills.get.ts`（`GET /api/skills`）。外部接口时在 `.env` 设置 `NUXT_PUBLIC_API_BASE`，不要另写一份基地址。
4. 列表请求继续由 `useSkills` 传入 `useRequestFetch()`。

## 改主题

改 `app/app.config.ts` 的 `ui.colors.primary` / `neutral`。页面继续用语义色，这样换中性色和深色模式才会一起生效。
