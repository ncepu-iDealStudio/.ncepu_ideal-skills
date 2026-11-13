# 技能互换 (skill-swap-web)

基于 [Nuxt UI Starter](https://github.com/nuxt-ui-templates/starter) 生成的技能互换平台示例。

## 技术栈

- **Nuxt 4** — Vue 全栈框架，文件路由、自动导入、SSR/SSG
- **Nuxt UI** — 官方 UI 组件库（100+ 组件、暗色模式、Tailwind 集成）
- **Tailwind CSS v4** — 原子化 CSS
- **TypeScript** — 类型安全
- **ESLint** — 代码规范

## 快速开始

```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev

# 构建生产版本
pnpm build

# 预览生产构建
pnpm preview

# 代码检查
pnpm lint

# 类型检查
pnpm typecheck
```

## 目录结构

```text
app/
├── app.vue                    # 根组件（UApp + Header + NuxtPage + Footer）
├── navigation.ts              # 顶栏栏目，新增栏目只在此追加
├── app.config.ts              # Nuxt UI 主题配置（primary=green）
├── assets/css/main.css        # Tailwind + Nuxt UI 样式入口
├── components/                # 自动导入组件
│   ├── AppLogo.vue
│   ├── SkillCard.vue
│   └── EmptyState.vue
├── composables/               # 自动导入组合式函数（状态 + 逻辑）
│   └── useSkills.ts
├── pages/                     # 文件路由
│   └── index.vue
├── services/                  # 数据服务层（mock/remote 切换）
│   └── skillService.ts
├── types/                     # TypeScript 类型
│   └── skill.ts
└── utils/                     # 工具函数
    └── format.ts
```

## 架构分层

```text
pages  →  composables  →  services  →  types/utils
```

- **pages**：只负责展示与交互，调用 composables
- **composables**：持有响应式状态，调用 services
- **services**：唯一数据接缝，内部切换 mock / remote

## 对接后端 API

1. 打开 `app/services/skillService.ts`
2. 将 `useMock` 改为 `false`
3. 确认 `API_BASE` 与接口路径
4. 页面与 composable 无需改动

## 自定义主题

在 `app/app.config.ts` 中修改：

```ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: 'green',   // 主色
      neutral: 'slate'    // 中性色
    }
  }
})
```
