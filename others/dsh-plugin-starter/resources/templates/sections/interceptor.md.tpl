## 5.1 加策略（interceptor 型最常见的扩展）

拦截器不提供新能力，而是**改变已有工具的行为**：放行、拒绝、加审计、加限流。

### 5.1.1 工具执行流水线（先记住这张图）

```text
tools/pre-execute   (waterfall)  ← 你现在的插件在这一层
  → guard（ctx.tools.guard，单调 deny）
  → tools/execute   (waterfall，超时/重试/埋点)
  → 工具本体 execute()
  → tools/post-execute (waterfall，可替换结果或阻塞)
  → finalizeContent
  → tools/result     (emit，只读观测)
```

waterfall 的规则只有一条：**返回决策对象表示「我不放行」；`return next()` 表示「交给下一环」**。

```ts
// 拒绝
return { kind: 'deny', reason: '命令不在白名单内' }

// 放行
return next()
```

不存在 `payload.deny()` 这种写法；字段是 `exec.name`（不是 `toolName`）与 `exec.arguments`（已解析并冻结的对象，不是 `argv` 数组）。

### 5.1.2 换一套策略

改 `src/capability.ts` 的 `evaluatePolicy`。三个可直接落地的方向：

**A. 参数级校验**（只允许读、不允许写）

```ts
const WRITE_TOOLS = new Set(['write_file', 'edit_file', 'delete_file'])

export function evaluatePolicy(toolName: string, args: Readonly<Record<string, unknown>>) {
  if (READ_ONLY && WRITE_TOOLS.has(toolName)) {
    return { kind: 'deny', reason: `只读模式：${toolName} 被禁止` }
  }
  return { kind: 'allow' }
}
```

**B. 路径白名单**（把工具限制在工作区内）

```ts
const path = args.path
if (typeof path === 'string' && !path.startsWith(process.cwd())) {
  return { kind: 'deny', reason: '只能访问工作区内的路径' }
}
```

**C. 审计 + 放行**（不拦截，只记录）

```ts
process.stderr.write(`[audit] ${toolName} args=${JSON.stringify(args)}\n`)
return { kind: 'allow' }
```

### 5.1.3 需要「问一下用户」时

`tools/pre-execute` 也能返回 `{ kind: 'ask', reason }`，由 DSH 弹出确认。适合高风险的写操作。

### 5.1.4 验证

```bash
pnpm build && dsh plugin --profile web add . && dsh web --port 3081

# 放行全部（便于先确认链路通）
{{ENV_PREFIX}}_ALLOW='*' dsh web --port 3081
```

先让 Agent 调一个**不在白名单**里的工具，应看到拒绝原因；再设 `{{ENV_PREFIX}}_ALLOW` 放行后重试。两次都符合预期，才算真的通了。

### 拦截器纪律

| 纪律 | 原因 |
| --- | --- |
| 只做判定，不做耗时 IO | 它挡在每一次工具调用前面，慢一点全场都慢 |
| 拒绝必须给 `reason` | 模型会读这个原因自我纠正 |
| 不要 `throw` | 抛异常会让工具循环崩掉，而不是优雅拒绝 |
| 判定要幂等 | 同一次调用可能被多次评估（重试、子 Agent） |
| 别抢 `tools/execute` 的活 | 那是加超时/重试的地方，语义不同 |
