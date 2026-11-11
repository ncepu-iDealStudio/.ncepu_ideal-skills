# 使用 `dsh-plugin-starter` 技能开发 DSH 插件

> 面向第一次做 DSH（DeepSeek Harness）插件的同学。照着本文走完，你能把「我想要个插件，能……」变成
> **一个用 VSCode 打开就能开发、能构建、能装进 DSH、能打包发布**的工程。
>
> 全文以三个真实需求贯穿：一个**工具型**（让 AI 能查笔记）、一个**双面型**（设置页里管理笔记）、一个**拦截器型**（命令白名单）。

---

## 1. 这个技能做什么

一句话：**把需求或原型，初始化成 DSH 插件起步项目**，并把「接下来怎么写、怎么调、怎么发」写进工程自带的 `DEVELOPMENT.md`。

| 输入 | 输出 |
| --- | --- |
| 一句话需求（文字） | 一个可构建的插件工程 + 开发指南 |
| 插件原型（HTML / 截图 / PRD 功能清单） | 同上，界面结构按原型还原到设置页区块 |
| 已有插件目录 | 不重新生成，走「审计 + 改造」流程 |

它支持 **四类插件**：

| 类型 | 用户嘴里的说法 | 能力出口 | 有界面 |
| --- | --- | --- | --- |
| `tool-only` 工具型 | 「让 AI 能查/抓/算/写」 | `ctx.tools.register(defineTool(...))` | 否 |
| `route-only` 路由型 | 「给外部脚本提供接口」 | `ctx.webServer.register()` | 否 |
| `dual-face` 双面型 | 「设置页 / 面板 / 可视化配置」 | 路由 + `settings.section` 插槽 | 是 |
| `interceptor` 拦截器型 | 「白名单 / 审计 / 审批」 | `ctx.on('tools/pre-execute')` | 否 |

**分工**：脚本干确定性的事（目录、清单、双目标构建配置、四处命名一致）；模型干业务（`src/capability.ts` 里的真实逻辑）。

---

## 2. 安装与触发

### 2.1 安装位置

技能目录名必须与 `SKILL.md` 的 `name`（`dsh-plugin-starter`）一致：

| 工具 | 路径 |
| --- | --- |
| DSH（用户级） | `~/.dsh/skills/dsh-plugin-starter/`（`$DSH_HOME` 未设时默认 `~/.dsh`） |
| DSH（项目级） | `<项目根>/.dsh/skills/dsh-plugin-starter/` |
| CodeBuddy | `<项目根>/.codebuddy/skills/dsh-plugin-starter/` |
| Agent Skills 通用 | `<项目根>/.agents/skills/dsh-plugin-starter/` |
| Cursor | `<项目根>/.cursor/skills/dsh-plugin-starter/` |

```bash
# 例：装到 DSH 用户级
cp -r ncepu_ideal-skills/dsh-plugin-starter ~/.dsh/skills/dsh-plugin-starter
```

### 2.2 怎么触发

三种方式，效果等价：

1. **描述匹配**（最常用）：「帮我做一个 DSH 插件，能在设置页里管理我的笔记」
2. **点名**：「用 dsh-plugin-starter 技能，把这段原型做成 DSH 插件」
3. **显式手势**：DSH 会话里 `/dsh-plugin-starter`

触发后技能会走**六步**：澄清 → 类型判定 → 写 spec → 生成 → 补业务 → 验证交付。**不会跳过澄清直接写代码。**

---

## 3. 完整流程（对话 + 命令）

### 3.1 第一步：需求澄清（选择题）

你只要说一句模糊需求，技能会一次问 2-3 个选择题：

```text
📋 需要确认 3 件事

1. 谁使用这个能力？
   [A] 模型（让 Agent 自己调用）
   [B] 用户（在 DSH 设置页里操作）
   [C] 外部系统（HTTP 接口）
   [D] 限制已有工具的行为（白名单/审计）

2. 数据从哪来？
   [A] 本地文件（工作区 / DSH_HOME）
   [B] 远程 HTTP API
   [C] 当前会话上下文
   [D] 暂时只要骨架

3. 命名
   包名建议：@<你的scope>/dsh-notes，可用吗？
```

回答后，技能会给一份 5 行需求摘要（目标 / 能力出口 / 数据来源 / 命名 / 完成标准）让你确认。

> **为什么要这一步**：包名一旦定错（例如用了官方 `@deepseek-ai` 命名空间），后面每一步都要返工；插件类型一旦定错（该做界面却做成命令行），用户会直接认为「没做好」。

### 3.2 第二步：类型判定

技能按 `resources/config/plugin_types.json` 的判定表选型。你可以直接用这张表自查：

| 你的真实诉求 | 应选类型 | 不该选什么 |
| --- | --- | --- |
| 让 Agent 多一个能力 | `tool-only` | 别做界面，界面只会增加安装/调试成本 |
| 让别人（脚本/系统）能调我 | `route-only` | 别做成工具，模型并不需要它 |
| 我自己要能看见、能配置 | `dual-face` | 别只做路由，用户没有入口会以为没生效 |
| 限制/审计已有工具 | `interceptor` | 别重复实现一个工具 |

> **拿不准时**：只要有「配置 / 查看」的诉求，选 `dual-face`。

### 3.3 第三步：生成

技能会落一份 spec 再调生成器。你也可以手动跑（spec 格式见第 7 节）：

```bash
python dsh-plugin-starter/resources/tools/scaffold_plugin.py \
  --spec my-plugin.json --out ./dsh-notebook
```

或者完全不写 spec：

```bash
python dsh-plugin-starter/resources/tools/scaffold_plugin.py \
  --type dual-face \
  --name @me/dsh-notebook \
  --route /notebook \
  --display-zh "笔记本" --display-en "Notebook" \
  --desc-zh "在设置页里管理笔记" \
  --out ./dsh-notebook
```

想先看会生成哪些文件：

```bash
python .../scaffold_plugin.py --spec my-plugin.json --out ./x --dry-run
```

### 3.4 生成出来是什么

```text
dsh-notebook/
├── src/
│   ├── index.ts            # Host 半边：注册工具 / 路由 / 拦截事件（接线层）
│   ├── capability.ts        # 业务实现（纯函数，唯一需要你「填空」的文件）
│   └── client/index.ts      # 仅双面型：设置页 UI
├── package.json             # 清单：dsh.bundle（+ dsh.client）
├── tsconfig.json
├── tsdown.config.ts         # host +（可选）client 双目标
├── cordis.patch.yml          # 安装时插入 profile 插件清单
├── README.md                # 面向使用者：怎么装、怎么构建
├── DEVELOPMENT.md           # ★ 面向开发者：10 章完整教材
└── .gitignore
```

**四个文件各管一件事**（记住这个分工，后面就不会乱）：

| 文件 | 你在这里做什么 | 什么时候需要动 |
| --- | --- | --- |
| `package.json` | 声明包名、`dsh.bundle`/`dsh.client`、依赖 | 加依赖、改包名（尽量避免） |
| `tsdown.config.ts` | 构建目标与打包规则 | 几乎不用动 |
| `src/index.ts` | 把能力挂到 DSH 上 | 加第二个工具/路由时 |
| `src/capability.ts` | 真实业务逻辑 | **主要在这里写** |

### 3.5 第四步：补业务逻辑

`capability.ts` 的入参/出参形状按类型不同：

**工具型**（返回 `{ ok, value?, error? }`）

```ts
export interface NotesSearchInput {
  query: string
  limit?: number
}

export async function notesSearch(input: NotesSearchInput): Promise<{ ok: boolean; value?: string; error?: string }> {
  const limit = Math.min(input.limit ?? 10, 50)
  const hits = await searchNotes(input.query, limit)   // 你的真实实现
  return { ok: true, value: hits.map((h) => `- ${h.title}`).join('\n') }
}
```

**路由型 / 双面型**（入参是请求 JSON，出参就是 HTTP 信封）

```ts
export async function addNote(payload: Readonly<Record<string, unknown>>): Promise<{ ok: boolean; value?: unknown; error?: string }> {
  const text = payload.text
  if (typeof text !== 'string' || text.trim() === '') return { ok: false, error: '缺少非空字符串参数 text' }
  return { ok: true, value: { id: save(text) } }
}
```

**拦截器型**（返回放行 / 拒绝决策）

```ts
export function evaluatePolicy(toolName: string, args: Readonly<Record<string, unknown>>): { kind: 'allow' } | { kind: 'deny'; reason: string } {
  if (toolName === 'bash' && !ALLOWED.has(String(args.command ?? '').split(/\s+/)[0])) {
    return { kind: 'deny', reason: '命令不在白名单内' }
  }
  return { kind: 'allow' }
}
```

需要**第二个工具 / 路由 / 设置区块**时，看生成的 `DEVELOPMENT.md` 第 5 章——那里按类型给了完整代码块和验证步骤。

### 3.6 第五步：构建 + 自检

```bash
cd dsh-notebook
pnpm install
pnpm typecheck          # 类型检查
pnpm build              # 产出 lib/index.mjs（+ lib/client.js）

# 静态 18 项自检（零依赖，秒级）
python <skill>/resources/tools/validate_plugin.py .
```

`validate_plugin.py` 会逐项打印 `[ OK ] / [WARN] / [FAIL]`。**出现 `[FAIL]` 不要往下走**，按提示修：

| 失败项 | 典型原因 |
| --- | --- |
| `dsh.bundle.patch` | `package.json` 缺 `dsh.bundle.patch` |
| `cordis.patch.yml name` | 与包名不一致（大小写、scope） |
| `tsdown PLUGIN_ID` | 与包名不一致 |
| `Client 半边装配` | `dsh.client` / `exports['./client']` / tsdown client 目标 三者不一致 |
| `defineTool 契约` | 少了 `output: {schema, render}` |
| `路由生命周期` | `webServer.register` 没包在 `ctx.effect` |
| `编码 / 占位符` | 文件带 BOM、模板占位符没替换 |

### 3.7 第六步：装进 DSH 并验证

```bash
dsh plugin --profile web add .                          # 安装本地目录
dsh --profile web --dump-config | grep dsh-notebook     # 确认真的进了装配
dsh web --port 3081                                     # 重启
```

按类型验证：

| 类型 | 怎么验 |
| --- | --- |
| `tool-only` | 对 Agent 说「用 `notes_search` 搜一下 XX」，看调用入参与返回值 |
| `route-only` | `curl -X POST http://127.0.0.1:3081/notes-api/ping` |
| `dual-face` | 设置页出现新区块 → 操作 → 看到 `{ ok: true }` |
| `interceptor` | 调一个非白名单工具 → 收到拒绝原因；设环境变量放行 → 通过 |

> **90% 的「插件不生效」都发生在装配环节**，不在业务代码。所以 `--dump-config | grep` 是第一个动作，不是最后一个。

---

## 4. 工程自带教材：`DEVELOPMENT.md`

生成的项目里有一份约 15KB 的开发指南，专为初学者写。10 章结构：

| 章 | 内容 | 什么时候看 |
| --- | --- | --- |
| 1 | 你拿到了什么（每个文件职责） | 第一次打开项目 |
| 2 | 心智模型：`inject` → `apply` → `effect`；Host/Client 为什么必须走 HTTP | 不理解「为什么要写两半」时 |
| 3 | 环境准备（Node ≥ 20.19 / pnpm / dsh 版本） | 装依赖前 |
| 4 | 第一次改动闭环（改 → 构建 → 装 → 验；含「改哪里要重启」表） | 第一次跑通 |
| 5 | **按类型扩展功能**（加工具 / 加路由 / 加设置区块 / 加策略） | 加第二个能力时 |
| 6 | 四个必背坑（包名四一致 / `dsh.bundle.patch` / `output` 必填 / 沙箱与 Windows） | 踩坑前预习 |
| 7 | 打包与发布（`files` 字段、tgz、npm、GitHub） | 要发给别人时 |
| 8 | 调试手册（三招 + 11 条「症状 → 根因」表 + headless `--patch` 开发法） | 不生效时 |
| 9 | 升级与兼容（预览版 API 变动检查项） | 升级 `@deepseek-ai/*` 前 |
| 10 | 下一步清单 | 收尾 |

**这份文档是「可执行的」**：里面的每条命令、每段代码都能直接复制运行，不是概念介绍。

---

## 5. 打包与发布

```bash
# 1) 构建 + 打 tarball
pnpm build && pnpm pack        # → dsh-notebook-0.1.0.tgz

# 2) 本地自测安装
dsh plugin --profile web add ./dsh-notebook-0.1.0.tgz

# 3) 发 npm（可选，scope 包必须 --access public）
npm publish --access public

# 4) 发 GitHub（社区主渠道）
git init && git add . && git commit -m "feat: initial release"
git remote add origin git@github.com:<你的账号>/dsh-notebook.git
git push -u origin master
# 别人安装：
# dsh plugin --profile web add github:<你的账号>/dsh-notebook
```

发布前逐条过：

- [ ] `package.json` 的 `files` **必须包含 `cordis.patch.yml`**（漏了别人装了不生效）
- [ ] `pnpm typecheck && pnpm build` 通过、`validate_plugin.py` 0 错误
- [ ] README 有一条复制即跑的安装命令
- [ ] 工具描述 / 设置页文案是给模型和用户看的
- [ ] 仓库打了 `dsh-plugin` topic
- [ ] 版本号与 `@deepseek-ai/*` 依赖锁定值写清楚

---

## 6. 调试方法论

### 6.1 三招定位（顺序别反）

```bash
# 招式 1：看装配——插件到底进没进当前组合
dsh --profile web --dump-config | grep dsh-notebook

# 招式 2：看会话日志——工具被调用了吗？入参/返回值是什么
#   （DSH 会话事件流里含 SessionEvent / Trajectory）

# 招式 3：事件探针——临时注册监听器打印，不改业务代码
ctx.on('tools/pre-execute', async (exec, next) => { console.log(exec.name, exec.arguments); return next() })
```

### 6.2 症状 → 根因速查

| 症状 | 优先怀疑 | 修法 |
| --- | --- | --- |
| 什么都没发生，也不报错 | 缺 `dsh.bundle.patch` | 补上并重装 |
| 模型看不到工具 | 缺 `output`；被 `restrict` 过滤；被同名 scope 遮蔽 | 补 `output`；`ctx.tools.schemas(scope)` 排查 |
| 设置页白屏，console 报 `__ModuleLoader__ is not defined` | Client 产物没被 banner/footer 包装 | 检查 `tsdown.config.ts` 的 `outputOptions` |
| Client 报 `require` 找不到模块 | `neverBundle` 漏了 `react`/`dsh-*`；或 `alwaysBundle` 没内联 | 模块表只认 `react` 与 `@deepseek-ai/dsh-*` |
| `apply` 里 `ctx.get('x')` 是 `undefined` | 用 `ctx.get` 代替了 `inject` | 服务名写进 `export const inject` |
| 路由注册直接抛错 | `(kind, path)` 与别的插件重复 | 换唯一前缀 |
| 写 `DSH_HOME` 被拒 | 沙箱默认策略 | `sandboxPolicy.resolve({mode:'danger-full-access'})` |
| 中文乱码 / JSON 解析失败 | 文件带 UTF-8 BOM | 存成无 BOM |
| 深色主题下样式崩 | 客户端硬编码颜色 | 全换 `var(--dsw-alias-*)` |
| 运行期 cordis 类型不匹配 | `peerDependencies` 漏 `@deepseek-ai/cordis` | 补 `^4.0.1` |
| GitHub 推送 403 | token 权限不足 | 细粒度 `Contents: Read and write` 或 classic `repo` |

### 6.3 更快的开发环：headless `--patch`

不想每次都 `plugin add` 时，可把源码直接挂进 headless 进程（路径相对 profile 目录解析）：

```bash
DSH_HOME="$PWD/.dsh-home" npx dsh --profile headless --patch ./dev.patch.yml "调一下 notes_search"
```

适合快速验证 Host 逻辑；**Client（设置页）仍建议走 `dsh web` 正常安装流程**验证。

---

## 7. spec 速查

```json
{
  "plugin": {
    "packageName": "@your-scope/dsh-notebook",
    "slug": "dsh-notebook",
    "type": "dual-face",
    "version": "0.1.0",
    "license": "MIT",
    "author": "Your Name <you@example.com>",
    "repoUrl": "https://github.com/your-scope/dsh-notebook",
    "displayNameZh": "笔记本",
    "displayNameEn": "Notebook",
    "descriptionZh": "在 DSH 设置页里记录与管理笔记。",
    "descriptionEn": "Manage notes from a DSH settings section."
  },
  "capability": {
    "summary": "笔记的增删查",
    "toolName": "notes_search",
    "toolDescription": "在用户笔记里搜索关键词。当用户问『我之前记过什么』时使用。",
    "routePrefix": "/notebook",
    "parameters": [
      { "name": "query", "type": "string", "required": true, "description": "搜索关键词" },
      { "name": "limit", "type": "number", "required": false, "description": "返回条数，默认 10" }
    ]
  }
}
```

| 字段 | 必需性 | 规则 |
| --- | --- | --- |
| `packageName` | ✅ | `^@scope/dsh-xxx$`；禁用 `@deepseek-ai`；最后一段 = slug |
| `slug` | 建议 | `^dsh-[a-z0-9-]+$`；可由包名推导 |
| `type` | ✅ | `tool-only` / `route-only` / `dual-face` / `interceptor` |
| `capability.toolName` | `tool-only` 必填 | snake_case；`run_code` 禁用 |
| `capability.routePrefix` | 路由/双面必填 | 形如 `/notebook`，无尾斜杠 |
| `capability.parameters` | 可选 | 支持 `string` / `number` / `boolean` / `string[]` |

完整字段表：`dsh-plugin-starter/resources/specifications/scaffold_spec_reference.md`。

---

## 8. 三个实战示例

### 8.1 工具型：让 AI 能查内部文档

> **你**：帮我做个 DSH 插件，让 AI 能搜索我们项目里的 Markdown 文档，关键词匹配就行，先不要界面。

技能判定：`tool-only`。生成 `@me/dsh-doc-search` + 工具 `doc_search`（参数 `query`、`limit`）。
你只需把 `capability.ts` 换成「遍历 `docs/**/*.md` 做关键词匹配」。验证：对 Agent 说「用 `doc_search` 搜『部署』」。

### 8.2 双面型：设置页里管理笔记

> **你**：我想在 DSH 设置页里加个「笔记本」，能添加、查看、删除，数据先存内存就行。

技能判定：`dual-face`。生成路由 `/notebook`（`ping`/`list`/`add`/`remove` 骨架）+ 设置页区块。
参考成品：[`resources/demo_output/dsh-plugin-notebook`](../dsh-plugin-starter/resources/demo_output/dsh-plugin-notebook/README.md)（就是按这个需求做的）。

### 8.3 拦截器型：bash 命令白名单

> **你**：我担心 Agent 乱敲命令，想加个白名单，只允许 git / ls / cat / grep。

技能判定：`interceptor`。生成 `tools/pre-execute` 监听 + 策略函数，白名单可用环境变量 `DSH_TOOL_GUARD_ALLOW` 覆盖。
验证：让 Agent 敲一个非白名单命令 → 应看到拒绝原因；`DSH_TOOL_GUARD_ALLOW='*'` 重启后 → 放行。

---

## 9. 改造已有插件

不要重新生成，按「审计 → 保留包名 → 改 src → 重装」走：

1. `python validate_plugin.py <插件目录>` —— 按 `[FAIL]` 顺序修：装配 → 声明 → 产物 → 运行期。
2. **保留包名**（它是注册键：profile 依赖、patch 行、`PLUGIN_ID`、bundle id 全派生自它）。
3. 只改 `src/`，再 `pnpm typecheck && pnpm build`，**绝不手改 `lib/`**。
4. `dsh plugin --profile web remove <包名>` → `add <目录>` → 重启。
5. 常见改造：
   - 路由型 → 工具型：把 handler 体搬进 `defineTool.execute`，补 `output`，`inject` 改 `['tools']`。
   - 加界面：加 `src/client/index.ts` + tsdown client 目标 + `dsh.client` + `exports['./client']`。

---

## 10. 与其他技能的边界

| 你可能想做的事 | 该用什么 |
| --- | --- |
| 做 DSH 插件（工具/路由/设置页/拦截器） | **本技能** |
| 写 DSH 技能（`SKILL.md`） | 技能体系（本仓库的 `docs/dsh中使用superpowers技能.md`） |
| 从 SQL 生成后端接口工程 | `sql-to-*-restfulapi-scaffold` |
| 从原型生成前端 App | `prototype-to-*` |

> 本技能生成的是**插件工程**（跑在 DSH 的 Node 进程 + DSH Web GUI 里），不是独立应用。

---

## 11. 常见问题

**Q1：`pnpm install` 装不上 `@deepseek-ai/*`？**
预览版包可能未公开或需内部源。先确认 DSH 版本与包版本匹配；IPv6 卡住试 `NODE_OPTIONS=--dns-result-order=ipv4first pnpm install`。

**Q2：包名能不能不带 scope？**
不建议。`dsh plugin add` 与模块表都以包名为键，带 scope 才不会与别人的插件撞名；同时**绝对不能**用 `@deepseek-ai`。

**Q3：可以改包名吗？**
可以，但要同步改 4 处：`package.json.name`、`tsdown.config.ts` 的 `PLUGIN_ID`、`cordis.patch.yml` 的 `name`、`tsconfig.json` 的 `paths` 键；然后重装。`validate_plugin.py` 会帮你查漏。

**Q4：生成的工程能直接用 VSCode 打开吗？**
可以。建议装 ESLint/Prettier 扩展；仓库已配置 `tsconfig`，`pnpm typecheck` 就是最可靠的检查。

**Q5：为什么只有一个 `capability.ts`？我有 5 个功能怎么办？**
`capability.ts` 是业务入口不是上限：加函数即可；`index.ts` 里按 `DEVELOPMENT.md` 第 5 章的模式追加注册块（工具/路由分支/设置区块）。

**Q6：Windows 上要注意什么？**
用 Node 原生 API（`fs.unlink`）替代 bash 命令；文件存成**无 BOM 的 UTF-8**；终端 GBK 下别用 `console.log` 打 emoji。

**Q7：静态检查过了就等于能跑吗？**
不等于。`validate_plugin.py` 是静态约定检查；真正编译要 `pnpm typecheck && pnpm build`。技能在交付时会明确区分「静态通过」与「编译通过」。

---

## 12. 附录：资源索引

| 内容 | 路径（相对 `dsh-plugin-starter/`） |
| --- | --- |
| 技能主文件（六步工作流、硬约束、坑位表） | `SKILL.md` |
| 技能说明 | `README.md` |
| 四类型判定表 | `resources/config/plugin_types.json` |
| 命名与一致性规则 | `resources/config/naming_rules.json` |
| 清单契约 | `resources/specifications/plugin_manifest_contract.md` |
| Host 契约（工具/路由/事件/沙箱） | `resources/specifications/host_contract.md` |
| Client 契约（bundle/插槽/locale/令牌） | `resources/specifications/client_contract.md` |
| 构建发布契约 | `resources/specifications/build_release_contract.md` |
| spec 字段表 | `resources/specifications/scaffold_spec_reference.md` |
| 生成器 | `resources/tools/scaffold_plugin.py` |
| 自检器（18 项） | `resources/tools/validate_plugin.py` |
| 示例 spec ×4 | `resources/tools/example_specs/` |
| 示例产物（双面型） | `resources/demo_output/dsh-plugin-notebook/` |

### 外部参考

- `lansi-ai/dsh-plugin-starter`：双面架构、tsdown 双目标、`__ModuleLoader__` 包装、清单字段、坑位表
- `yanhua1010/dsh-harness-tutorial`：插件三形态、Cordis 五概念、事件模式、headless `--patch` 调试
