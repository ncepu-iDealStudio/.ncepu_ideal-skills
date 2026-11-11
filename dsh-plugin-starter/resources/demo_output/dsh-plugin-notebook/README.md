# 笔记本 (@demo/dsh-notebook)

> **这是 `dsh-plugin-starter` 技能的示例产物。**
> 它由 `scaffold_plugin.py` 生成骨架，再按 `DEVELOPMENT.md` 第 5 章把 `capability.ts` 与客户端 UI 补齐，
> 用来展示「一个刚生成出来的工程，长成能用的插件」是什么样。
> 想看纯生成结果，把 `resources/tools/example_specs/dual-face.json` 换掉 `--out` 重新生成即可。

在 DSH 设置页里记录与管理笔记，Host 侧提供笔记读写路由。

- 插件类型：`dual-face`（Host 路由 + Client 设置页）
- 插件 id（注册键）：`dsh-notebook`
- 包名：`@demo/dsh-notebook`

## 功能

Host 侧暴露 `/notebook` 前缀下的 POST 路由（统一 `{ ok, value | error }` 信封）：

| 路由 | 入参 | 作用 |
|---|---|---|
| `POST /notebook/ping` | —— | 健康探针，确认 Host 半边就绪 |
| `POST /notebook/list` | —— | 列出全部笔记（新→旧） |
| `POST /notebook/add` | `{ text: string }` | 新增一条笔记 |
| `POST /notebook/remove` | `{ id: string }` | 删除一条笔记 |

Client 侧在设置页注入「笔记本」区块：输入框 + 添加按钮 + 笔记列表（可删除），文案走 `ctx.locale` 中英双语，样式只用 `var(--dsw-alias-*)` 令牌。

## 目录结构

```text
dsh-notebook/
├── src/
│   ├── index.ts            # Host 半边：注册 HTTP 路由（业务在 capability.ts）
│   ├── capability.ts       # 业务实现：进程内 Map 存储的笔记增删查
│   └── client/
│       └── index.ts        # Client 半边：设置页区块（settings.section）
├── cordis.patch.yml       # DSH 安装配置（bundle patch）
├── package.json            # dsh.bundle / dsh.client 声明
├── tsconfig.json
├── tsdown.config.ts        # 双目标构建配置
├── README.md               # 本文件
└── DEVELOPMENT.md          # 开发指南：扩展功能、调试、打包发布
```

## 构建

```bash
pnpm install
pnpm typecheck            # tsc --noEmit
pnpm build                # tsdown → lib/index.mjs + lib/client.js
```

## 安装到 DSH 并验证

```bash
dsh plugin --profile web add .                          # 本地目录安装
dsh --profile web --dump-config | grep dsh-notebook     # 确认进了装配
dsh web --port 3081                                     # 重启后在设置页验证
```

验证清单：

1. 设置页出现「笔记本」区块；
2. 输入文字点「添加」→ 列表出现该条；
3. 点「删除」→ 该条消失；
4. 直接打路由（不经过界面）：

```bash
curl -X POST http://127.0.0.1:3081/notebook/ping
curl -X POST http://127.0.0.1:3081/notebook/add  -H 'content-type: application/json' -d '{"text":"first note"}'
curl -X POST http://127.0.0.1:3081/notebook/list -H 'content-type: application/json' -d '{}'
```

## 相对「纯生成结果」改了哪三处

| 文件 | 改动 | 对应 `DEVELOPMENT.md` |
|---|---|---|
| `src/capability.ts` | 回声实现 → 进程内 `Map` 笔记存储（list/add/remove） | 第 5.1 节「Host 侧加端点」 |
| `src/index.ts` | 增加 `/list`、`/add`、`/remove` 三个分支 | 第 5.1 节 |
| `src/client/index.ts` | 单个输入框 → 输入 + 列表 + 删除按钮 | 第 5.1 节「Client 侧加 UI」 |

> 换成真实持久化（写 `DSH_HOME` 下的 JSON 文件）时：在 `index.ts` 里把 `ctx.get('fs')` 与
> `ctx.get('sandboxPolicy').resolve({ mode: 'danger-full-access' })` 注入给 `capability.ts`，
> 页面与路由都不用改。

## 关键约束（改代码前先看一眼）

1. **包名是唯一键**：`package.json.name` = `tsdown.config.ts` 的 `PLUGIN_ID` = `cordis.patch.yml` 的 `name` = `tsconfig.json` 的 `paths` 键前缀。
2. **`dsh.bundle.patch` 不能删**，否则 `dsh plugin add` 不生效且不报错。
3. **Client 产物必须由 tsdown 包成 `window.__ModuleLoader__.load({id, factory})`**，别手写。

生成时间：2026-11-11
