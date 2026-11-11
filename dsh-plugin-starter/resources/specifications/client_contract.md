# Client 半边契约

Client 半边跑在浏览器里（DSH Web GUI），产物是 `lib/client.js`。它只做两件事：**往插槽里注入 UI**、**用 fetch 调 Host 路由**。

---

## 1. bundle 格式（最硬的约束）

产物必须是 `window.__ModuleLoader__.load({id, factory})`：

```js
window.__ModuleLoader__.load({
  id: "@your-scope/dsh-notebook",      // = 包名，注册键
  factory: (require) => {
    /* bundle 主体 */
    return module.exports
  },
})
```

- 这层包装**由 tsdown 的 `banner/footer/intro` 生成**，绝不手写。
- `load()` 只**登记** factory；模块体副作用（含样式注入）在首次 import 物化时执行。
- `require` 解析顺序：种子词 → shell 实例 → 记忆化记录 → 图行（注册依赖 factory）→ 已注册 factory → 其余抛错。
- 加载路径：`/plugins/<包名>/client.js`。

---

## 2. 依赖规则（两个最常见的打包事故）

模块表**只认识 `react` 与 `@deepseek-ai/dsh-client-*`**。

| 规则 | 漏了会怎样 |
| --- | --- |
| `neverBundle` 排除 `react`、`@deepseek-ai/dsh-*` | 被打进产物 → 模块表没有行 → 运行期 `require` 抛错 |
| `alwaysBundle` 内联其余所有依赖 | 模块表同样没有 → 同样抛错 |

---

## 3. 服务注入

```ts
export const inject = ['slots', 'locale']    // 服务名
export function apply(ctx: ClientContext): void { ... }
```

注意与 `package.json.dsh.client.inject`（**包名**）区分 —— 两个都存在，语义不同。

---

## 4. 插槽与设置页

```ts
ctx.slots.inject('settings.section', () => ctx.slots.register({
  name: 'settings.section',
  id: 'dsh-notebook',                    // 用包名保证唯一，避免与其他插件打架
  order: 50,                             // 排序
  label: () => ctx.locale.bind('dsh-notebook')('title'),   // 跟随界面语言
}, SettingsSection))
```

`settings.section` 是**列表槽**，可与其他插件并存。`id` 重复会导致区块冲突。

---

## 5. 多语言

**中英都要注册**，`en` 是兜底：

```ts
ctx.effect(() => ctx.locale.register('dsh-notebook', 'zh', { title: '笔记本' }), 'zh dict')
ctx.effect(() => ctx.locale.register('dsh-notebook', 'en', { title: 'Notebook' }), 'en dict')

// 组件内取词（bind 放在渲染时，不要放在注册时）
const t = ctx.locale.bind('dsh-notebook')
t('title')
```

---

## 6. 样式与主题

只允许用设计令牌：

```text
✅ var(--dsw-alias-surface-default)   ✅ var(--dsw-alias-label-primary)
✅ var(--dsw-alias-border-default)    ✅ var(--dsw-alias-brand-primary)
❌ #ffffff   ❌ rgba(0,0,0,.8)         // 深色主题下必失效
```

注入方式：在 `ctx.effect` 里 `document.createElement('style')` 追加到 `document.head`，清理函数里 `style.remove()`。

---

## 7. 与 Host 通信

```ts
async function post(path: string, payload: unknown) {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload ?? {}),
  })
  const envelope = await response.json()          // { ok, value } | { ok, error }
  return envelope
}
```

- 只用原生 `fetch`，不用 Typert `@Remote`。
- 统一解包 `{ ok, value | error }` 信封，失败也要有可读文案。
- 组件里所有异步请求要防「组件已卸载仍 setState」：用 `let active = true` + 清理函数，或 `AbortController`。

---

## 8. 构建产物验收

```bash
pnpm build
head -c 60 lib/client.js      # 应看到 window.__ModuleLoader__.load({
grep -o '"@your-scope/dsh-notebook"' lib/client.js | head -1
```

`validate_plugin.py` 第 7、16 项会自动做这两件事。
