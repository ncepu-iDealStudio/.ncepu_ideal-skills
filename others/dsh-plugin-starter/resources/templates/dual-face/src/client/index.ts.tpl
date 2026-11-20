/**
 * {{DISPLAY_ZH}} —— Client 半边（浏览器侧）
 *
 * 职责：往设置页注入一个区块（settings.section 插槽），用 fetch() 调 Host 半边的路由。
 * 本文件最终会被 tsdown 包成 window.__ModuleLoader__.load({ id, factory }) 格式，
 * 由 DSH 从 /plugins/<包名>/client.js 加载 —— 不要手写这层包装。
 *
 * 依赖约定：react 与 @deepseek-ai/dsh-client-* 由 DSH 模块表提供，不打包进产物。
 */
import * as React from 'react'
import type { ClientContext } from '@deepseek-ai/dsh-client-runtime/client'
import type {} from '@deepseek-ai/dsh-client-ui-settings/client'
import type {} from '@deepseek-ai/dsh-client-locale/client'

/** locale 命名空间 / 插槽 id / 日志标签，统一用插件 id，便于排查 */
const PLUGIN_ID = '{{SLUG}}'
const ROUTE_PREFIX = '{{ROUTE_PREFIX}}'

/** 统一的 Host 路由调用封装：POST + JSON + { ok, value | error } 信封 */
async function post(
  path: string,
  payload: unknown,
): Promise<{ ok: boolean; value?: unknown; error?: string }> {
  let response: Response
  try {
    response = await fetch(path, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload ?? {}),
    })
  } catch {
    return { ok: false, error: 'Host 路由不可用' }
  }
  try {
    const envelope: unknown = await response.json()
    if (typeof envelope !== 'object' || envelope === null) return { ok: false, error: '响应格式错误' }
    const record = envelope as { ok?: boolean; value?: unknown; error?: string }
    if (record.ok === true) return { ok: true, value: record.value }
    return { ok: false, error: record.error ?? 'Host 返回失败' }
  } catch {
    return { ok: false, error: '响应不是合法 JSON' }
  }
}

/** 样式一律走 --dsw-alias-* 设计令牌，硬编码颜色会在深色主题下失效 */
const STYLE_TEXT = `
.{{SLUG_UNDERSCORE}}-section { display: flex; flex-direction: column; gap: 8px; }
.{{SLUG_UNDERSCORE}}-row { display: flex; gap: 8px; align-items: center; }
.{{SLUG_UNDERSCORE}}-input { flex: 1; padding: 6px 8px; border: 1px solid var(--dsw-alias-border-default); border-radius: 6px; background: var(--dsw-alias-surface-default); color: var(--dsw-alias-label-primary); }
.{{SLUG_UNDERSCORE}}-button { padding: 6px 14px; border: none; border-radius: 6px; background: var(--dsw-alias-brand-primary); color: var(--dsw-alias-label-on-brand); cursor: pointer; }
.{{SLUG_UNDERSCORE}}-hint { font-size: 12px; color: var(--dsw-alias-label-secondary); white-space: pre-wrap; }
`

/** Client 硬依赖：slots（插槽系统）与 locale（多语言） */
export const inject = ['slots', 'locale']

export function apply(ctx: ClientContext): void {
  // 1. 注册中英双语文案（en 为兜底）
  ctx.effect(
    () => ctx.locale.register(PLUGIN_ID, 'zh', {
      title: '{{DISPLAY_ZH}}',
      placeholder: '{{PLACEHOLDER_ZH}}',
      submit: '执行',
      empty: '尚未执行',
      failed: '失败',
    }),
    `${PLUGIN_ID}: zh dict`,
  )
  ctx.effect(
    () => ctx.locale.register(PLUGIN_ID, 'en', {
      title: '{{DISPLAY_EN}}',
      placeholder: '{{PLACEHOLDER_EN}}',
      submit: 'Run',
      empty: 'Not run yet',
      failed: 'Failed',
    }),
    `${PLUGIN_ID}: en dict`,
  )

  // 2. 注入样式（ctx.effect 里创建，卸载时移除）
  ctx.effect(() => {
    const style = document.createElement('style')
    style.textContent = STYLE_TEXT
    document.head.appendChild(style)
    return () => { style.remove() }
  }, `${PLUGIN_ID}: settings styles`)

  // 3. 设置页区块组件（在闭包里定义，才能拿到 ctx 做 bind）
  function SettingsSection(): React.ReactElement {
    const t = ctx.locale.bind(PLUGIN_ID)
    const [text, setText] = React.useState('')
    const [result, setResult] = React.useState('')
    const [busy, setBusy] = React.useState(false)

    const run = React.useCallback(async () => {
      setBusy(true)
      const response = await post(`${ROUTE_PREFIX}/run`, { text })
      setBusy(false)
      setResult(response.ok ? JSON.stringify(response.value) : `${t('failed')}: ${response.error ?? ''}`)
    }, [text])

    return React.createElement(
      'div',
      { className: `{{SLUG_UNDERSCORE}}-section` },
      React.createElement('h3', null, t('title')),
      React.createElement(
        'div',
        { className: `{{SLUG_UNDERSCORE}}-row` },
        React.createElement('input', {
          className: `{{SLUG_UNDERSCORE}}-input`,
          value: text,
          placeholder: t('placeholder'),
          onChange: (event: React.ChangeEvent<HTMLInputElement>) => { setText(event.target.value) },
        }),
        React.createElement(
          'button',
          { className: `{{SLUG_UNDERSCORE}}-button`, onClick: run, disabled: busy },
          t('submit'),
        ),
      ),
      React.createElement('div', { className: `{{SLUG_UNDERSCORE}}-hint` }, result || t('empty')),
    )
  }

  // 4. 注入设置页区块（settings.section 是列表插槽，可与其他插件并存）
  ctx.slots.inject('settings.section', () => ctx.slots.register({
    name: 'settings.section',
    id: PLUGIN_ID,
    order: 50,
    label: () => ctx.locale.bind(PLUGIN_ID)('title'),
  }, SettingsSection))
}
