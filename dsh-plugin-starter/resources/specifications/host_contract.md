# Host 半边契约

Host 半边跑在 DSH 的 Node 进程里，产物是 `lib/index.mjs`。它是 Cordis 插件：导出 `inject` 与 `apply`。

---

## 1. 生命周期

```ts
export const inject = ['tools']          // 硬依赖，服务就绪后才调用 apply
export function apply(ctx: Context): void {
  ctx.tools.register(...)                 // 注册能力
  ctx.effect(() => {                      // 可回收注册
    const dispose = ctx.webServer.register(...)
    return () => { dispose() }
  }, '标签')
  ctx.on('tools/pre-execute', handler)    // 事件监听，随生命周期自动清理
}
```

三条铁律：

1. **`ctx.get()` 是可选读取**，服务未就绪时返回 `undefined`；关键服务一律进 `inject`。
2. **有返回 disposer 的注册必须包 `ctx.effect`**：路由、定时器、样式节点、长连接。
3. **`ctx.on` 注册的监听器无需手动清理**，它已绑定上下文生命周期。

---

## 2. 能力出口

| 出口 | API | 面向 | 说明 |
|---|---|---|---|
| 工具 | `ctx.tools.register(defineTool(...))` | 模型 | 模型直接调用，最常用 |
| 路由 | `ctx.webServer.register({kind, path, handler})` | 浏览器/外部 | `kind` 为 `exact` 或 `prefix`；`(kind, path)` 重复即抛错 |
| 事件 | `ctx.on('tools/pre-execute', ...)` | 其他插件/系统 | 拦截、审计、埋点 |
| 服务 | `class Xxx extends Service` | 其他插件 | 通过 `ctx.get('xxx')` 被使用 |
| 文件 | `ctx.get('fs')` | —— | 带沙箱与观测策略的文件系统，不要用 `node:fs` |
| 沙箱 | `ctx.get('sandboxPolicy').resolve({mode:'danger-full-access'})` | —— | 写非工作区目录（如 `DSH_HOME`）前必须申请 |

---

## 3. 工具契约（`defineTool`）

```ts
ctx.tools.register(defineTool({
  name: 'notebook_search',                 // snake_case；run_code 为保留名
  description: '在用户笔记里搜索关键词。当用户问“我之前记过什么”时使用。',
  parameters: {
    query: { type: 'string', required: true, description: '搜索关键词' },
    limit: { type: 'number', description: '返回条数，默认 10' },
  },
  output: {                                 // 必填，缺失则注册失败
    schema: {
      type: 'object',
      additionalProperties: false,          // 必须显式 true/false
      properties: {
        ok: { type: 'boolean', required: true },
        value: { type: 'string' },
        error: { type: 'string' },
      },
    },
    render: (_args, value) => [{ type: 'text', text: String(value) }],
  },
  async execute(args, exec) {
    if (exec.signal.aborted) return { ok: false, error: '已取消' }
    return { ok: true, value: '...' }
  },
}))
```

要点：

- **`execute` 返回规范 JSON 值**（不是 `{content:[...]}` 消息形状）；给模型看的文本由 `render` 生成。
- **返回值被 `output.schema` 强制校验**；违反会抛 `ToolOutputError` 并附 `violations`。
- **不要用 `input_schema` 键**，原生 schema 只有 `{name, description, parameters}`。
- **异步工作要观察 / 透传 `exec.signal`**，支持协作式取消。
- 可选字段：`presentCall` / `presentResult`（UI 卡片）、`timeoutMs`、`isConcurrencySafe`、`finalizeContent`。

### 参数 schema 三条经验

1. 能枚举就用 `enum`；非字符串别用 `string` 兜着。
2. 能给 `default` 就别设必填。
3. 描述写「何时使用」，不是「这个函数做什么」。

### 工具可见性排查

`scope` 注册会遮蔽同名全局工具；`ctx.tools.restrict({allow, deny})` 会过滤全局工具。链路：`ctx.tools.schemas(scope)` → 检查 `restrict` / preset 作用域 → 检查注册是否失败（缺 `output`）。

---

## 4. 路由契约

```ts
ctx.effect(() => {
  const dispose = ctx.webServer.register({
    kind: 'prefix',
    path: '/notebook',                 // 绝对路径、无尾斜杠
    handler: async (req, res) => {
      if (req.method !== 'POST') { res.writeHead(405); res.end(); return }
      // 读 body → 分发到 capability → 统一信封
      res.writeHead(200, { 'content-type': 'application/json; charset=utf-8' })
      res.end(JSON.stringify({ ok: true, value }))
    },
  })
  return () => { dispose() }
}, 'dsh-notebook: /notebook routes')
```

社区约定：

- **只走 POST + JSON**，返回 `{ ok: true, value }` / `{ ok: false, error }` 信封。
- **body 要有体积上限**（模板里 `BODY_CAP_BYTES = 1 << 20`）。
- **业务失败返回结构化错误**，不要 500 裸抛。
- **不要用 Typert `@Remote`**：npm 上的生成器太旧，外部项目用不了；Host↔Client 通道就是 HTTP。

---

## 5. 事件契约（拦截器必读）

```text
tools/pre-execute (waterfall) → guard → tools/execute (waterfall)
  → 工具本体 → tools/post-execute (waterfall) → finalizeContent → tools/result (emit)
```

| 事件 | 模式 | 签名 |
|---|---|---|
| `tools/pre-execute` | waterfall | `(exec, next) => {kind:'allow'} \| {kind:'deny', reason} \| {kind:'ask', reason?}` |
| `tools/execute` | waterfall | `(exec, next) => Promise<ToolExecutionResult>` |
| `tools/post-execute` | waterfall | `(exec, result, next) => Promise<PostToolDecision>` |
| `tools/result` | emit | `(exec, result) => undefined`（`result` 深冻结，只读） |
| `tools/change` | emit | 工具集变化通知 |

拦截器正确写法：

```ts
ctx.on('tools/pre-execute', async (exec, next) => {
  if (exec.name === 'bash') {
    const args = exec.arguments as { command?: string }   // 已解析、已冻结
    if (!ALLOWED.has((args.command ?? '').split(/\s+/)[0] ?? '')) {
      return { kind: 'deny', reason: '命令不在白名单内' }
    }
  }
  return next()
})
```

**没有 `payload.deny()`**；字段是 `exec.name`（不是 `toolName`）与 `exec.arguments`（不是 `argv` 数组）。

---

## 6. 平台差异

| 议题 | 做法 |
|---|---|
| Windows 删文件 | 用 `fs.unlink` 等 Node 原生 API，别依赖 bash 执行器（可能找不到 bash） |
| 编码 | 一律 UTF-8 **无 BOM**；BOM 会让 JSON 解析与 curl 输出出错 |
| 中文日志 | 用 `ctx.logger`，不要 `console.log` 打 emoji（部分终端编码会崩） |
