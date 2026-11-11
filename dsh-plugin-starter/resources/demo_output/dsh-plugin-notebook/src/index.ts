/**
 * 笔记本 —— Host 半边（dual-face）
 *
 * 注册 /notebook 前缀下的 HTTP POST 路由，供 src/client 的设置页用 fetch() 调用。
 * 约定：POST + JSON，统一返回 { ok: true, value } | { ok: false, error } 信封。
 */
import type { IncomingMessage, ServerResponse } from 'node:http'
import type { Context } from '@deepseek-ai/cordis'
import type {} from '@deepseek-ai/dsh-host-webserver'
import { addNote, listNotes, removeNote } from './capability'

/** 硬依赖：webServer 就绪后才执行业务注册 */
export const inject = ['webServer']

const ROUTE_PREFIX = '/notebook'
const BODY_CAP_BYTES = 1 << 20

function json(res: ServerResponse, body: unknown, status = 200): void {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' })
  res.end(JSON.stringify(body))
}

/** 读 POST JSON body（带体积上限，超大请求直接丢弃） */
async function readJsonBody(req: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = []
  let total = 0
  for await (const chunk of req) {
    const part = chunk as Buffer
    total += part.length
    if (total > BODY_CAP_BYTES) {
      req.destroy()
      return null
    }
    chunks.push(part)
  }
  const text = Buffer.concat(chunks).toString('utf8')
  if (text === '') return null
  try {
    return JSON.parse(text)
  } catch {
    return null
  }
}

export function apply(ctx: Context): void {
  // 路由必须包在 ctx.effect 里：返回 disposer，插件卸载时自动注销
  ctx.effect(() => {
    const dispose = ctx.webServer.register({
      // (kind, path) 必须全局唯一，重复注册会直接抛错
      kind: 'prefix',
      path: ROUTE_PREFIX,
      handler: async (req: IncomingMessage, res: ServerResponse): Promise<void> => {
        if (req.method !== 'POST') {
          res.writeHead(405)
          res.end()
          return
        }
        const pathname = new URL(req.url ?? '/', 'http://localhost').pathname

        if (pathname === `${ROUTE_PREFIX}/ping`) {
          // 健康探针：客户端用来确认 Host 半边已就绪
          json(res, { ok: true, value: { pong: true } })
          return
        }

        if (pathname === `${ROUTE_PREFIX}/list`) {
          json(res, await listNotes())
          return
        }

        if (pathname === `${ROUTE_PREFIX}/add`) {
          json(res, await addNote((await readJsonBody(req) ?? {}) as Readonly<Record<string, unknown>>))
          return
        }

        if (pathname === `${ROUTE_PREFIX}/remove`) {
          json(res, await removeNote((await readJsonBody(req) ?? {}) as Readonly<Record<string, unknown>>))
          return
        }

        res.writeHead(404)
        res.end()
      },
    })
    return () => { dispose() }
  }, 'dsh-notebook: /notebook routes')
}
