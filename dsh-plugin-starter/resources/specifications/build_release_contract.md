# 构建、打包与发布契约

---

## 1. 构建：tsdown 双目标

```ts
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
    deps: { neverBundle: (id) => id === '@deepseek-ai/cordis' || id.startsWith('@deepseek-ai/dsh-') },
  },
  {
    name: `${PLUGIN_ID}/client`,       // 仅带界面插件需要
    entry: { client: 'src/client/index.ts' },
    outDir: 'lib',
    format: 'cjs',
    platform: 'browser',
    target: 'es2022',
    dts: true,
    clean: false,
    deps: {
      neverBundle: (id) => id === 'react' || id.startsWith('@deepseek-ai/dsh-'),
      alwaysBundle: (id) => id !== 'react' && !id.startsWith('@deepseek-ai/dsh-'),
    },
    outputOptions: {
      entryFileNames: 'client.js',
      banner: `window.__ModuleLoader__.load({ id: ${JSON.stringify(PLUGIN_ID)}, factory: (require) => {`,
      footer: 'return module.exports; } });',
      intro: 'var module = { exports: {} }; var exports = module.exports;',
    },
  },
])
```

| 目标 | 入口 | 产物 | 关键配置 |
|---|---|---|---|
| host | `src/index.ts` | `lib/index.mjs` + `index.d.mts` | `esm` / `node` / `neverBundle` 排除 cordis 与 dsh-host-* |
| client | `src/client/index.ts` | `lib/client.js` | `cjs` / `browser` / 排除 react 与 dsh-client-* / 其余内联 / `__ModuleLoader__` 包装 |

---

## 2. 标准命令

```bash
pnpm install
pnpm typecheck          # tsc --noEmit
pnpm build              # tsdown 双目标
pnpm pack               # 生成 .tgz
```

`lib/` 是产物目录：**不提交、不手改**。

---

## 3. 安装与验证

```bash
dsh plugin --profile web add .                        # 本地目录
dsh plugin --profile web add ./xxx-0.1.0.tgz          # tgz
dsh plugin --profile web add github:user/repo         # GitHub
dsh plugin --profile web remove <包名>                 # 卸载
dsh --profile web --dump-config | grep <包名>          # 确认进了装配
dsh web --port 3081                                   # 重启验证
```

验证方式按类型不同：

| 类型 | 验证 |
|---|---|
| tool-only | 让 Agent 调工具，看入参与返回值 |
| route-only | `curl -X POST http://127.0.0.1:3081/<prefix>/ping` |
| dual-face | 设置页出现区块 → 操作 → 看到 `{ok:true}` |
| interceptor | 调非白名单工具 → 被拒绝；设环境变量放行 → 通过 |

---

## 4. 发布

### npm

```bash
pnpm build
npm publish --access public     # 带 scope 的包默认私有，必须加 --access
```

### GitHub（社区主渠道）

```bash
git init && git add . && git commit -m "feat: initial release"
git remote add origin git@github.com:<account>/<repo>.git
git push -u origin master
```

- 仓库打 `dsh-plugin` topic（社区插件入口）。
- 细粒度 token 需该仓库 `Contents: Read and write`；或 classic token（`ghp_` + `repo`）。

---

## 5. 版本与兼容

| 依赖 | 锁定值 | 说明 |
|---|---|---|
| `@deepseek-ai/cordis` | `^4.0.1` | 必须写进 `peerDependencies` |
| `@deepseek-ai/dsh-*` | `^0.1.0-rc.7` | 开发者预览版，**破坏性变更频繁** |
| Node | `>= 20.19`，推荐 22+ | |
| `tsdown` | `^0.22.x` | 不要随手升大版本 |
| `react` | `^18.2.x` | 仅带界面插件 |

升级流程：读 changelog → 比对已安装包 `lib/types/*.d.ts` → 只改 `@deepseek-ai/*` 版本 → `pnpm typecheck` → 重装并验证。

---

## 6. 发布前清单

- [ ] `pnpm typecheck && pnpm build` 通过
- [ ] `validate_plugin.py` 0 错误
- [ ] `--dump-config` 能看到插件行
- [ ] `files` 含 `cordis.patch.yml`
- [ ] README 有一条可复制即跑的安装命令
- [ ] 工具/设置页文案是给模型与用户看的
- [ ] 卸载后无残留定时器/监听器
