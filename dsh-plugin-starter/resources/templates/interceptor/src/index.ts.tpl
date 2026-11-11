/**
 * {{DISPLAY_ZH}} —— Host 半边（interceptor 型，无界面）
 *
 * 监听工具执行前的拦截事件（tools/pre-execute，waterfall）：
 * 返回 { kind: 'deny', reason } 拒绝；返回 next() 放行。
 * 策略逻辑写在 src/capability.ts，本文件只做事件接线。
 */
import type { Context } from '@deepseek-ai/cordis'
import { evaluatePolicy } from './capability'

export function apply(ctx: Context): void {
  // ctx.on 注册的监听器跟随插件生命周期，卸载时自动清理
  ctx.on('tools/pre-execute', async (exec, next) => {
    const decision = evaluatePolicy(exec.name, exec.arguments as Readonly<Record<string, unknown>>)
    if (decision.kind === 'deny') return decision
    return next()
  })
}
