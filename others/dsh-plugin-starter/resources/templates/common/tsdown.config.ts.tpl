import { defineConfig } from 'tsdown'

/**
 * 插件唯一标识：必须与 package.json 的 name 完全一致（含 scope）。
 * DSH 用它在 /plugins/<id>/client.js 加载 Client 半边。
 */
const PLUGIN_ID = '{{PKG_NAME}}'

/**
 * Host 目标产出 lib/index.mjs（ESM / node），Client 目标产出 lib/client.js（CJS / browser）。
 * 纯 Host 插件只有第一个目标。
 */
export default defineConfig([
  {
    name: `${PLUGIN_ID}/host`,
    entry: { index: 'src/index.ts' },
    outDir: 'lib',
    format: ['esm'],
    platform: 'node',
    target: 'es2022',
    dts: true,
    clean: false,
    deps: {
      // cordis 与 @deepseek-ai/dsh-* 由宿主进程提供，绝不能打进产物
      neverBundle: (id) => id === '@deepseek-ai/cordis' || id.startsWith('@deepseek-ai/dsh-'),
    },
  },{{CLIENT_TARGET}}
])
