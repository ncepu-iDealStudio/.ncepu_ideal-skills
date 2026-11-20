/**
 * {{DISPLAY_ZH}} —— 业务实现（唯一需要你「填空」的文件）
 *
 * 这里是纯函数：不 import 任何 DSH API，方便单测与复用。
 * 把 demo 实现替换成真实逻辑即可，index.ts 不用改。
 */

export interface {{PASCAL}}Input {
{{INPUT_FIELDS}}
}

export interface {{PASCAL}}Result {
  ok: boolean
  value?: string
  error?: string
}

export async function {{CAMEL}}Capability(
  input: {{PASCAL}}Input,
  signal?: AbortSignal,
): Promise<{{PASCAL}}Result> {
  if (signal?.aborted === true) return { ok: false, error: '已取消' }

  // ---- demo 实现：把入参回显出来，替换成你的业务逻辑 ----
  const pairs = Object.entries(input).map(([key, value]) => `${key}=${String(value)}`)
  return { ok: true, value: `{{DISPLAY_ZH}} 收到参数：${pairs.length > 0 ? pairs.join('，') : '（无）'}` }
}
