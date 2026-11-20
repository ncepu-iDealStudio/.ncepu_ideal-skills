/**
 * 笔记本 —— 业务实现（唯一需要你「填空」的文件）
 *
 * 纯函数：不 import 任何 DSH API，便于直接单测。
 * 这里用一个进程内 Map 做存储示例；接真实持久化时，把 Map 换成
 * ctx.get('fs') 注入进来的读写函数即可，index.ts 与 client 都不用改。
 */

export interface Note {
  id: string
  text: string
  createdAt: string
}

export interface NotebookEnvelope {
  ok: boolean
  value?: unknown
  error?: string
}

const notes = new Map<string, Note>()
let sequence = 0

function nextId(): string {
  sequence += 1
  return `n${sequence}`
}

function readText(payload: Readonly<Record<string, unknown>>): string | null {
  const text = payload.text
  return typeof text === 'string' && text.trim() !== '' ? text.trim() : null
}

/** 列出全部笔记（新→旧） */
export async function listNotes(): Promise<NotebookEnvelope> {
  const items = [...notes.values()].sort((left, right) => (left.createdAt < right.createdAt ? 1 : -1))
  return { ok: true, value: { items, total: items.length } }
}

/** 新增一条笔记 */
export async function addNote(payload: Readonly<Record<string, unknown>>): Promise<NotebookEnvelope> {
  const text = readText(payload)
  if (text === null) return { ok: false, error: '缺少非空字符串参数 text' }
  if (notes.size >= 200) return { ok: false, error: '笔记已达示例上限 200 条，接入真实存储前先清理' }

  const note: Note = { id: nextId(), text, createdAt: new Date().toISOString() }
  notes.set(note.id, note)
  return { ok: true, value: note }
}

/** 删除一条笔记 */
export async function removeNote(payload: Readonly<Record<string, unknown>>): Promise<NotebookEnvelope> {
  const id = payload.id
  if (typeof id !== 'string' || id === '') return { ok: false, error: '缺少字符串参数 id' }
  const existed = notes.delete(id)
  if (!existed) return { ok: false, error: `笔记不存在：${id}` }
  return { ok: true, value: { id } }
}
