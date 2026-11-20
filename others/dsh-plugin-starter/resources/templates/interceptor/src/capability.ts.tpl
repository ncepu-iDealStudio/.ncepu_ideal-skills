/**
 * {{DISPLAY_ZH}} —— 策略实现（唯一需要你「填空」的文件）
 *
 * 纯函数：给定工具名与参数，返回放行 / 拒绝。不 import 任何 DSH API。
 *
 * 环境变量：{{ENV_PREFIX}}_ALLOW（逗号分隔的工具名白名单）
 * 未设置时使用下面的内置白名单；设为 `*` 表示全部放行。
 */

export type PolicyDecision = { kind: 'allow' } | { kind: 'deny'; reason: string }

const DEFAULT_ALLOW = ['read_file', 'list_files', 'grep', 'search_content']

function readAllowList(): string[] {
  const raw = process.env.{{ENV_PREFIX}}_ALLOW
  if (raw === undefined || raw.trim() === '') return DEFAULT_ALLOW
  return raw.split(',').map((item) => item.trim()).filter((item) => item !== '')
}

export function evaluatePolicy(
  toolName: string,
  args: Readonly<Record<string, unknown>>,
): PolicyDecision {
  const allow = readAllowList()
  if (allow.includes('*')) return { kind: 'allow' }

  // ---- demo 策略：只放行白名单内的工具，替换成你的业务规则 ----
  if (allow.includes(toolName)) return { kind: 'allow' }
  const argKeys = Object.keys(args).join(',')
  return {
    kind: 'deny',
    reason: `工具 ${toolName} 不在白名单内（请求参数：${argKeys || '无'}）。如需放行，设置环境变量 {{ENV_PREFIX}}_ALLOW。`,
  }
}
