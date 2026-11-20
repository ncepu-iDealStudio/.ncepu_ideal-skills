## 5.1 带界面插件怎么长功能（Host 路由 + Client UI）

双面插件的扩展永远是**成对**的：Host 加一个端点 → Client 加一块 UI。

### 步骤 1：Host 侧加端点（`src/index.ts`）

```ts
if (pathname === `${ROUTE_PREFIX}/history`) {
  json(res, { ok: true, value: { items: [] } })
  return
}
```

### 步骤 2：Client 侧加 UI（`src/client/index.ts`）

```ts
const [items, setItems] = React.useState<unknown[]>([])

const loadHistory = React.useCallback(async () => {
  const response = await post(`${ROUTE_PREFIX}/history`, {})
  if (response.ok) setItems((response.value as { items?: unknown[] }).items ?? [])
}, [])

React.useEffect(() => { void loadHistory() }, [loadHistory])
```

渲染时把 `items` 映射成列表即可，样式继续用 `{{SLUG_UNDERSCORE}}-*` 类名。

### 步骤 3：文案一律走 locale

**不要在组件里写死中文**，否则切英文界面时会出现半中半英：

```ts
ctx.effect(() => ctx.locale.register(PLUGIN_ID, 'zh', { history: '历史记录' }), `${PLUGIN_ID}: zh`)
ctx.effect(() => ctx.locale.register(PLUGIN_ID, 'en', { history: 'History' }), `${PLUGIN_ID}: en`)

// 组件内
const t = ctx.locale.bind(PLUGIN_ID)
React.createElement('h4', null, t('history'))
```

`en` 是兜底语言，两套字典都要注册。

### 步骤 4：样式只允许用设计令牌

```text
✅ background: var(--dsw-alias-surface-default)
✅ color: var(--dsw-alias-label-primary)
✅ border: 1px solid var(--dsw-alias-border-default)
❌ background: #ffffff        // 深色主题下必炸
❌ color: rgba(0,0,0,.8)
```

令牌由 DSH 主题系统提供，`--dsw-alias-*` 是唯一合法来源。

### 步骤 5：验证

```bash
pnpm typecheck && pnpm build
dsh plugin --profile web remove {{PKG_NAME}} && dsh plugin --profile web add .
dsh web --port 3081
```

打开设置页 → 应该看到「{{DISPLAY_ZH}}」区块 → 点「执行」→ 结果区出现 `{ ok: true, value: ... }`。
如果区块出现但操作报「Host 路由不可用」，说明 Host 半边没加载或路由路径写错 —— 先 `--dump-config` 看装配。

### 双面插件的额外坑

| 现象 | 原因 | 修法 |
| --- | --- | --- |
| 设置页整块空白，console 报 `__ModuleLoader__ is not defined` | Client 产物没用 tsdown 的 `banner/footer/intro` 包装 | 检查 `tsdown.config.ts` 的 client 目标 |
| `require is not defined` / 找不到 `react` | `neverBundle` 没排除 `react`、`@deepseek-ai/dsh-*` | 模块表只认这两类，其余全部内联（`alwaysBundle`） |
| 切换语言后标签没变 | `label` 没用 `ctx.locale.bind(...)`，而是在注册时就取了值 | `label: () => ctx.locale.bind(PLUGIN_ID)('title')` |
| 页面刷新后样式丢失 | 样式节点没在 `ctx.effect` 里创建 | 用 `document.createElement('style')` + 清理函数 |
| 换主题后颜色不跟着变 | 用了硬编码颜色 | 全部换成 `var(--dsw-alias-*)` |
| 两个插件设置区块打架 | `slots.register` 的 `id` 重复 | `id` 用包名（`{{SLUG}}`）保证唯一 |
