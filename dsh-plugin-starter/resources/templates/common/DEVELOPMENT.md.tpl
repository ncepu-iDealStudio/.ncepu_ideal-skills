# {{DISPLAY_ZH}} 开发指南（初学者完整版）

> 这份文档是这个插件的「说明书 + 教材」。它假设你**没写过 DSH 插件**，也**没读过源码**，
> 只要求你会 TypeScript 基础语法、知道 `npm`/`pnpm` 是什么。
>
> 读完并照着做完，你能做到：改功能 → 构建 → 装进 DSH → 调试 → 打包发布。
>
> 生成时间：{{CREATED_AT}} ｜ 类型：`{{TYPE}}`（{{TYPE_HINT}}）｜ 包名：`{{PKG_NAME}}`

---

## 1. 你拿到了什么

```text
{{SLUG}}/
├── src/
│   ├── index.ts          # Host 半边：往 DSH 里「注册」能力（接线层，通常不用大改）
│   ├── capability.ts      # 业务实现：真正干活的地方（你主要改这里）
{{CLIENT_TREE}}├── cordis.patch.yml       # DSH 安装时用的 bundle patch
├── package.json            # 清单：dsh.bundle / dsh.client 声明，包名是唯一键
├── tsconfig.json          # tsc 类型检查配置
├── tsdown.config.ts       # 构建配置（Host/Client 双目标）
├── README.md              # 面向使用者：怎么装、怎么构建
└── DEVELOPMENT.md         # 就是本文件：面向开发者
```

**两句话理解这个工程**：

1. `src/index.ts` 负责「把自己挂到 DSH 上」，`src/capability.ts` 负责「挂上去之后做什么」。
2. 你写的是 **TypeScript 源码**，DSH 运行的是 **`lib/` 里的构建产物**。所以任何修改都必须重新 `pnpm build`。

---

## 2. 心智模型：DSH 插件到底是什么

DSH 的插件体系基于 Cordis（一个依赖注入 + 生命周期框架）。一个插件就是一个模块，导出两样东西：

| 导出 | 作用 | 时机 |
|---|---|---|
| `export const inject` | 声明「我要用哪些服务」（如 `tools` / `webServer`） | 加载时，DSH 等这些服务就绪后才调用 `apply` |
| `export function apply(ctx)` | 插件主体：注册工具 / 路由 / 事件 | 服务就绪后，只调用一次 |

三条必须记住的纪律：

1. **不要在 `apply` 里直接 `ctx.get('xxx')` 拿关键服务**。`ctx.get` 是「可选读取」，服务没就绪时会返回 `undefined`，于是你的插件静默失效。关键服务一律写进 `inject`。
2. **所有注册都要可回收**。定时器、路由、样式节点都要包在 `ctx.effect(() => { ... return () => 清理() }, '标签')` 里，否则插件卸载后会泄漏。`ctx.on(...)` 注册的事件监听器本身跟随生命周期，无需手动清理。
3. **插件的身份是包名**（`package.json.name`）。它同时出现在 4 个地方，必须完全一致（见第 6 节）。改包名等于换身份，已安装的 profile 会失效。

### 2.1 「双面」是什么意思

```text
┌─────────────────────────┐        HTTP (fetch)        ┌──────────────────────────┐
│  Host 半边（Node 进程）   │ ◄───────────────────────── │  Client 半边（浏览器）      │
│  src/index.ts           │      POST + JSON 信封       │  src/client/index.ts      │
│  产物 lib/index.mjs      │                            │  产物 lib/client.js       │
│  注册 tool / route / 事件 │                            │  往设置页注入 UI 区块       │
└─────────────────────────┘                            └──────────────────────────┘
```

- Host 与 Client **不共享内存**，也不走 Cordis 事件，唯一通道是 **HTTP**。
- 因此：Host 侧要用 `ctx.webServer.register()` 暴露路由，Client 侧用原生 `fetch()` 调用。
- 别用 Typert 的 `@Remote` 装饰器 —— 外部开发者用的生成器版本太旧，跑不通。

---

## 3. 环境准备

```bash
node -v            # 需要 ≥ 20.19，推荐 22+
pnpm -v            # 没装：npm i -g pnpm
dsh --version      # DSH 命令行；开发者预览版为 0.1.x，API 会变
```

安装依赖：

```bash
pnpm install
```

> 如果卡在网络上：`NODE_OPTIONS=--dns-result-order=ipv4first pnpm install`，或配置 HTTP 代理。
> 依赖版本说明：`package.json` 里 `@deepseek-ai/*` 固定在 `^0.1.0-rc.7`、`@deepseek-ai/cordis` 固定在 `^4.0.1`。
> 升级前先看官方 changelog —— 预览版 API 是**破坏性变更**。

---

## 4. 第一次改动：跑通「改 → 构建 → 装 → 验」闭环

### 4.1 改一行业务代码

打开 `src/capability.ts`，把 demo 实现换成你的逻辑。判断标准很简单：**这个文件不 import 任何 DSH API**，纯粹输入 → 输出，所以可以直接写单测。

### 4.2 类型检查 + 构建

```bash
pnpm typecheck      # tsc --noEmit，只检查类型不产出文件
pnpm build          # tsdown 产出 lib/index.mjs{{CLIENT_ARTIFACT}}
```

构建后你应该看到：

```text
lib/
├── index.mjs         # Host 半边（ESM，给 Node 进程用）
├── index.d.mts       # Host 类型声明
{{DEV_LIB_TREE}}
```

`lib/` 是**构建产物，别手改、别提交**（已在 `.gitignore`）。

### 4.3 装进 DSH

```bash
# 安装本地目录（开发期最常用）
dsh plugin --profile web add .

# 确认真的进了装配（不是「装了但没用」）
dsh --profile web --dump-config | grep {{SLUG}}

# 重启 DSH
dsh web --port 3081
```

{{VERIFY_STEPS}}
### 4.4 改完怎么看效果

| 改动位置 | 生效方式 |
|---|---|
| Host 半边（`src/index.ts`、`capability.ts`） | 必须 `pnpm build` + **重启 DSH 进程** |
| Client 半边（`src/client/index.ts`） | `pnpm build` + 刷新浏览器页面即可（dev 模式下可热更新） |
| `package.json` 的 `dsh.*` 声明 | `dsh plugin remove` 再 `add`，然后重启 |

---

## 5. 往下做功能：按类型扩展

{{DEV_TYPE_SECTION}}

---

## 6. 四个「一改就废」的坑（务必背下来）

### 6.1 包名是唯一键，四处必须一致

| 位置 | 字段 |
|---|---|
| `package.json` | `name` |
| `tsdown.config.ts` | `PLUGIN_ID` |
| `cordis.patch.yml` | `name`（以及 `id` 建议用插件 id） |
| `tsconfig.json` | `paths` 的键（仅带界面插件） |

再加一处运行期约束：Client 产物里的 `window.__ModuleLoader__.load({ id })` 必须等于包名，否则浏览器侧模块加载不到。

### 6.2 `dsh.bundle.patch` 不能省

```json
"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
```

漏了它，`dsh plugin add` 只把插件当普通依赖装进 `package.json`，**路由不注册、设置页不出现，而且不报错**。这是最难查的问题，`--dump-config` 一查就知道。

### 6.3 `output: { schema, render }` 是 defineTool 的必填项

```ts
output: {
  schema: { type: 'object', additionalProperties: false, properties: { ... } },
  render: (_args, value) => [{ type: 'text', text: String(value) }],
}
```

- 缺 `output` → 注册直接失败，模型看不到工具。
- `execute` 返回的是**规范的 JSON 值**（不是 `{content:[...]}` 消息形状），给模型看的文本由 `render` 生成。
- schema 里每个 object 的 `additionalProperties` 必须**显式**写 `true` 或 `false`，否则报 `JsonSchemaError`。

### 6.4 沙箱与 Windows

- 写 `DSH_HOME` 等非工作区目录：先 `ctx.get('sandboxPolicy').resolve({ mode: 'danger-full-access' })`，否则默认沙箱拒绝。
- 文件读写用 `ctx.get('fs')`（带沙箱与观测策略），不要直接 `import node:fs`。
- Windows 上不要靠 bash 执行器删文件，用 Node 原生 API（`fs.unlink`）。

---

## 7. 打包与发布

### 7.1 产物里到底要有什么

`package.json` 的 `files` 字段决定了发布内容：

```json
"files": ["lib/index.mjs", "lib/index.d.mts"{{DEV_FILES_EXTRA}}, "cordis.patch.yml"]
```

**必须**包含 `cordis.patch.yml`，否则别人装了你的包不会被插入 profile 的插件清单。

### 7.2 本地打包 / 自测安装

```bash
pnpm build
pnpm pack                    # 生成 {{SLUG}}-<version>.tgz
dsh plugin --profile web add ./{{SLUG}}-{{VERSION}}.tgz
```

### 7.3 发布到 npm（可选）

```bash
pnpm build
npm publish --access public   # 带 scope 的包默认 private，必须加 --access public
```

### 7.4 发布到 GitHub（社区分发的主渠道）

```bash
git init && git add . && git commit -m "feat: initial release"
git remote add origin git@github.com:<your-account>/{{SLUG}}.git
git push -u origin master
```

别人安装：

```bash
dsh plugin --profile web add github:<your-account>/{{SLUG}}
```

发布前请确认：

- [ ] `README.md` 里有一条能复制粘贴就能跑的安装命令
- [ ] 工具描述 / 设置页文案是写给「模型」和「用户」看的，不是写给开发者看的
- [ ] 出错路径返回结构化错误（`{ ok: false, error }`），不要裸抛异常
- [ ] 插件卸载后没有残留定时器 / 监听器 / 全局状态
- [ ] 仓库打了 `dsh-plugin` topic（社区入口）

---

## 8. 调试手册

### 8.1 三招定位

| 招式 | 命令 / 做法 | 能回答什么 |
|---|---|---|
| 看装配 | `dsh --profile web --dump-config \| grep {{SLUG}}` | 插件到底进没进当前组合？ |
| 看会话日志 | DSH 会话事件流（SessionEvent / Trajectory） | 工具被调用了吗？入参和返回值是什么？ |
| 事件探针 | 临时注册 `tools/pre-execute` / `tools/post-execute` 监听器打印日志 | 调用被谁拦了？ |

### 8.2 症状 → 根因速查

| 症状 | 优先怀疑 | 处理 |
|---|---|---|
| 模型看不到工具 | 缺 `output`、被 `restrict` 过滤、被同名 scope 遮蔽、`run_code` 保留名冲突 | 补齐 `output`；`ctx.tools.schemas(scope)` 查看当前可见工具 |
| 设置页没出现 | 缺 `dsh.bundle.patch`、`dsh.client` 未声明、Client bundle 不是 `__ModuleLoader__` 格式 | `--dump-config` 确认装配；看浏览器 console |
| 浏览器报 `__ModuleLoader__ is not defined` | Client 产物没被 tsdown 包上 `banner/footer/intro` | 检查 `tsdown.config.ts` 的 `outputOptions` |
| Client 报 `require` 找不到模块 | `neverBundle` 漏了 `react` / `@deepseek-ai/dsh-*`，或 `alwaysBundle` 没内联其余依赖 | 模块表只认 `react` 与 `@deepseek-ai/dsh-*`，其余必须内联 |
| `apply` 里拿到 `undefined` | 用 `ctx.get` 代替了 `inject` | 把服务名加进 `export const inject` |
| 路由注册直接抛错 | `(kind, path)` 重复（两个插件抢同一路径） | 换路径前缀 |
| 写文件被拒绝 | 沙箱默认策略 | `sandboxPolicy.resolve({ mode: 'danger-full-access' })` |
| 中文乱码 / JSON 解析失败 | 文件带 UTF-8 BOM | 用无 BOM 的 UTF-8 保存 |
| 运行期 cordis 类型不匹配 | `peerDependencies` 漏了 `@deepseek-ai/cordis` | 补上 `"@deepseek-ai/cordis": "^4.0.1"` |
| GitHub 推送 403 | token 权限不足 | 细粒度 token 需 `Contents: Read and write`；或 classic token（`repo`） |

### 8.3 开发期更快的路径：patch 覆盖层

不想每次 `plugin add` 时，可以绕过安装，直接把源码挂进 headless 进程：

```bash
# mock.patch.yml 里用相对 profile 目录的路径引你的插件
DSH_HOME="$PWD/.dsh-home" npx dsh --profile headless --patch ./dev.patch.yml "让 Agent 调一下 {{TOOL_NAME}}"
```

适合快速验证 Host 逻辑；Client 侧（设置页）仍建议走 `dsh web` 正常安装流程验证。

---

## 9. 升级与兼容

DSH 当前是开发者预览版（`0.1.x`），破坏性变更常见。升级前先做两件事：

1. 看官方 changelog / release notes；
2. 用你代码里的 `import` 去比对已安装包的 `lib/types/*.d.ts`，重点检查：
   - `ToolDefinition`（`output` 是否仍必填）
   - 工具事件签名（waterfall 决策对象，没有 `payload.deny()`）
   - `webServer.register` 的路由契约
   - `__ModuleLoader__` 的 id 是否仍等于包名

`{{PKG_NAME}}` 的依赖锁定在 `package.json`，升级时只改 `@deepseek-ai/*` 的版本号，不要顺手升级 `tsdown`/`typescript` 大版本。

---

## 10. 下一步可以做什么

- [ ] 把 `src/capability.ts` 的 demo 逻辑换成真实业务
- [ ] 补单元测试（`capability.ts` 是纯函数，用 `node:test` 或 vitest 都行）
- [ ] 给 `README.md` 补真实用法示例
- [ ] 加日志：`ctx.logger.info('[{{SLUG}}] ...')`，便于在会话日志里定位
- [ ] 需要配置项时，优先用环境变量起步，再考虑设置页持久化
- [ ] 对外发布时按第 7 节清单逐条过一遍

> 卡住时的通用顺序：**先 `--dump-config` 看装配 → 再看会话日志 → 最后才怀疑代码**。
> 90% 的「插件不生效」都发生在装配环节，而不是业务代码里。
