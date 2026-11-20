/**
 * {{DISPLAY_ZH}} —— Host 半边（tool 型，无界面）
 *
 * 模型可直接调用这里注册的工具。本文件只做「接线」：
 *   parameters 参数 schema → capability 入参 → output.schema 校验 → render 给模型看
 * 业务逻辑写在 src/capability.ts。
 */
import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'
import { {{CAMEL}}Capability, type {{PASCAL}}Input } from './capability'

/** 硬依赖：关键服务一律写进 inject，apply() 会在它们就绪后执行（不要用 ctx.get 代替） */
export const inject = ['tools']

export function apply(ctx: Context): void {
  ctx.tools.register(defineTool({
    name: '{{TOOL_NAME}}',
    // description 是写给「模型」看的：什么时候用它、参数怎么填
    description: '{{TOOL_DESCRIPTION}}',
    parameters: {
{{PARAMETERS_TS}}
    },
    // output 是必填项，缺了会注册失败；返回值会被 output.schema 强制校验
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
      render: (_args, value: { ok: boolean; value?: string; error?: string }) => [
        { type: 'text', text: value.ok ? (value.value ?? '') : `失败：${value.error ?? '未知错误'}` },
      ],
    },
    async execute(args, exec) {
      // args 已按 parameters 校验并冻结；耗时逻辑要透传 exec.signal 支持协作式取消
      return {{CAMEL}}Capability(args as {{PASCAL}}Input, exec.signal)
    },
  }))
}
