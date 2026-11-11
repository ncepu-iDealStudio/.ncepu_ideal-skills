## 5.1 加第二个工具（tool 型最常见的扩展）

工具是**给模型用的函数**。一个插件可以注册任意多个工具，`apply` 里多调几次 `ctx.tools.register` 即可。

### 步骤 1：在 `src/capability.ts` 写实现

```ts
export interface {{PASCAL}}SummaryInput {
  path: string
  maxLines?: number
}

export async function {{CAMEL}}Summary(input: {{PASCAL}}SummaryInput): Promise<string> {
  // 纯函数：不 import DSH API，便于单测
  return `summary of ${input.path}`
}
```

### 步骤 2：在 `src/index.ts` 追加注册块

```ts
ctx.tools.register(defineTool({
  name: '{{SLUG_UNDERSCORE}}_summary',          // snake_case，模型可见
  description: '统计指定文件的摘要。当用户想知道某个文件里大致写了什么时使用。',
  parameters: {
    path: { type: 'string', required: true, description: '文件路径，绝对路径或工作区相对路径' },
    maxLines: { type: 'number', description: '最多返回多少行（默认 20）' },
  },
  output: {
    schema: {
      type: 'object',
      additionalProperties: false,
      properties: {
        ok: { type: 'boolean', required: true },
        value: { type: 'string' },
        error: { type: 'string' },
      },
    },
    render: (_args, value: { ok: boolean; value?: string }) => [
      { type: 'text', text: value.value ?? '' },
    ],
  },
  async execute(args, exec) {
    // 长耗时操作要观察 exec.signal，支持协作式取消
    if (exec.signal.aborted) return { ok: false, error: '已取消' }
    return { ok: true, value: await {{CAMEL}}Summary(args) }
  },
}))
```

### 步骤 3：参数 schema 的三条硬经验

1. **能枚举就别用自由文本**：`{ type: 'string', enum: ['a', 'b'] }`；非字符串一定要用 `number` / `boolean`。
2. **能给默认值就别设必填**：必填字段越多，模型填错的概率越高。
3. **描述写「什么时候用」而不是「这个函数做了什么」**：模型的决策完全依赖 description。

### 步骤 4：验证

```bash
pnpm typecheck && pnpm build
dsh plugin --profile web remove {{PKG_NAME}} && dsh plugin --profile web add .
dsh web --port 3081
```

然后在会话里直接说「用 `{{SLUG_UNDERSCORE}}_summary` 看一下某个文件」。

### 常见错法

| 错法 | 后果 |
|---|---|
| 用 `input_schema` 键传参 | 注册失败（原生 schema 只有 `{name, description, parameters}`） |
| 忘记 `output` | 注册失败，模型看不到工具 |
| `execute` 里 `throw` 裸异常 | 直接把工具循环打崩；应返回 `{ ok: false, error }` |
| 注册名为 `run_code` | 保留名，注册抛错 |
| `additionalProperties` 写不写都行 | 错。object 类型必须显式 `true`/`false` |
