/**
 * {{DISPLAY_ZH}} —— 业务实现（唯一需要你「填空」的文件）
 *
 * 纯函数：入参是请求 JSON，出参直接就是 HTTP 信封 { ok, value } | { ok, error }。
 * 需要读写文件时，应把 ctx.get('fs') 的实例从 index.ts 传进来，而不是在本文件里 import node:fs。
 */

export interface {{PASCAL}}Envelope {
  ok: boolean
  value?: unknown
  error?: string
}

export async function {{CAMEL}}Capability(
  payload: Readonly<Record<string, unknown>>,
): Promise<{{PASCAL}}Envelope> {
  // ---- demo 实现：回显请求体，替换成你的业务逻辑 ----
  const keys = Object.keys(payload)
  if (keys.length === 0) return { ok: false, error: '请求体为空：请以 JSON 形式 POST 参数' }
  return { ok: true, value: { echo: payload, receivedKeys: keys } }
}
