## 5.1 加一条路由（route 型最常见的扩展）

当前 Host 注册的是 `{{ROUTE_PREFIX}}` 前缀路由，已实现两个端点：

| 方法 | 路径 | 作用 |
|---|---|---|
| POST | `{{ROUTE_PREFIX}}/ping` | 健康探针，确认 Host 半边已就绪 |
| POST | `{{ROUTE_PREFIX}}/run` | 业务端点，进入 `capability.ts` |

### 步骤 1：在 `capability.ts` 加一个纯函数

```ts
export async function {{CAMEL}}Detail(
  payload: Readonly<Record<string, unknown>>,
): Promise<{ ok: boolean; value?: unknown; error?: string }> {
  const id = payload.id
  if (typeof id !== 'string') return { ok: false, error: '缺少字符串参数 id' }
  return { ok: true, value: { id, title: 'demo' } }
}
```

### 步骤 2：在 `index.ts` 的 handler 里加一个分支

```ts
if (pathname === `${ROUTE_PREFIX}/detail`) {
  const payload = await readJsonBody(req)
  const result = await {{CAMEL}}Detail((payload ?? {}) as Readonly<Record<string, unknown>>)
  json(res, result)
  return
}
```

### 步骤 3：想拆成多个前缀时

`(kind, path)` 必须**全局唯一**，重复注册会直接抛错。需要第二组路径就再注册一次，并各自包 `ctx.effect`：

```ts
ctx.effect(() => {
  const dispose = ctx.webServer.register({ kind: 'prefix', path: '{{ROUTE_PREFIX}}-admin', handler: adminHandler })
  return () => { dispose() }
}, '{{SLUG}}: admin routes')
```

### 步骤 4：验证（无需界面）

```bash
pnpm build && dsh plugin --profile web add . && dsh web --port 3081

curl -X POST http://127.0.0.1:3081{{ROUTE_PREFIX}}/ping
curl -X POST http://127.0.0.1:3081{{ROUTE_PREFIX}}/run \
  -H 'content-type: application/json' -d '{"text":"hi"}'
```

### 写路由的纪律

| 纪律 | 原因 |
|---|---|
| 只接受 POST + JSON，返回 `{ ok, value }` / `{ ok, error }` 信封 | 与社区插件、将来的 Client 半边保持一致 |
| 读 body 要有体积上限（模板里 `BODY_CAP_BYTES`） | 防止超大 payload 打爆内存 |
| 业务异常转成 `{ ok: false, error }`，不要 500 裸抛 | 调用方（浏览器侧）能稳定拿到结构化错误 |
| 文件读写走 `ctx.get('fs')`，从 `index.ts` 注入进 capability | 保留沙箱与观测策略 |
| 处理完记得 `res.end()` | 否则连接挂住 |
