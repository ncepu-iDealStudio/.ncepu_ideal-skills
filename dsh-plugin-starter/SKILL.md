---
name: "dsh-plugin-starter"
description: "把用户的一句话需求或插件原型，初始化成可直接用 VSCode 打开开发的 DSH（DeepSeek Harness）插件起步项目：支持工具型（无界面）、路由型（无界面）、双面型（设置页界面）、拦截器型四类；生成清单声明、tsdown 双目标构建配置、Host/Client 骨架与内置《开发者指南》（扩展功能、调试、打包发布、装入 DSH）。用户提到「开发 DSH 插件」「做一个 DSH 插件」「dsh plugin」「给 DSH 加工具/设置页」「插件打包发布」时使用。"
---

# DSH 插件起步项目生成技能

把「我想要一个 DSH 插件，能……」（或用户给的插件原型）变成**能直接打开开发、能构建、能装进 DSH 的工程骨架**，并把「接下来怎么写、怎么调、怎么发」写进工程自带的 `DEVELOPMENT.md`。

**核心分工**：`resources/tools/scaffold_plugin.py` 负责确定性的机械部分（目录、清单、双目标构建配置、命名一致性）；模型负责需求理解与业务代码（`src/capability.ts`）。

---

## 1. 什么时候用

**用**：

- 「开发一个 DSH 插件」「做一个能给 Agent 加 XX 能力的插件」
- 「给 DSH 加一个设置页 / 面板 / 可视化配置」
- 「写一个拦截某些工具调用的插件」
- 用户给了原型（HTML 界面、截图、需求清单）要求做成 DSH 插件
- 已有插件要改造（加界面、路由改工具）

**不用**：

- 只是问 DSH 插件的概念（直接讲，别生成工程）
- 写 DSH 技能（`SKILL.md`，走 skills 体系，不是插件）
- 与本仓库其他技能重叠的纯前端/后端脚手架生成

---

## 2. 输入形态

| 输入 | 提取方式 | 可靠性 |
| --- | --- | --- |
| 一句话需求（文字） | 按第 3.1 节做澄清，落成 spec | 中，靠澄清补全 |
| 插件原型（HTML/CSS/截图） | 先抽界面元素与交互，再映射到 `settings.section` 区块 | 高（有界面时最准） |
| PRD / 功能清单 | 抽「能力 → 出口（tool/route/ui）」对照 | 中 |
| 已有插件目录 | 走第 9 节「改造流程」，不重新生成 | 高 |

冲突时：**能力边界以需求为准，界面结构以原型为准**。拿不准就问。

---

## 3. 工作流（六步，不可跳步）

### 3.1 需求澄清（选择题，一次问 2-3 个）

只问「只有用户知道」的事，能从输入里读出来的不要问：

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
   包名建议：@<你的scope>/dsh-<名字>，可用吗？（例：@acme/dsh-notebook）
```

澄清完写一份 **5 行需求摘要**（目标 / 能力出口 / 数据来源 / 命名 / 完成标准）让用户确认。

### 3.2 类型判定

| 用户诉求关键词 | 类型 | 能力出口 | 有界面 |
| --- | --- | --- | --- |
| 让 AI 能查/抓/算/写 | `tool-only` | `ctx.tools.register(defineTool(...))` | 否 |
| 提供 HTTP 接口 / 给外部脚本调 | `route-only` | `ctx.webServer.register()` | 否 |
| 设置页 / 面板 / 可视化配置 | `dual-face` | 路由 + `settings.section` 插槽 | 是 |
| 拦截 / 白名单 / 审计 / 审批 | `interceptor` | `ctx.on('tools/pre-execute')` | 否 |

细则见 `resources/config/plugin_types.json`（含每类的 `signals`、`antiPatterns`、验证方式）。
**拿不准且有「配置/查看」诉求时选 `dual-face`** —— 界面比命令行更不容易被用户认为「没做好」。

### 3.3 写 spec

按 `resources/specifications/scaffold_spec_reference.md` 的格式落一份 JSON（字段表、类型对应关系都在里面）。最小可用 spec：

```json
{
  "plugin": { "packageName": "@me/dsh-echo", "type": "tool-only",
              "displayNameZh": "回声工具", "descriptionZh": "回显文本" },
  "capability": { "toolName": "echo_run",
                  "toolDescription": "把文本回显。当需要验证工具链时使用。",
                  "parameters": [{ "name": "text", "type": "string", "required": true,
                                   "description": "要回显的文本" }] }
}
```

命名规则见 `resources/config/naming_rules.json`：包名带自己的 scope、最后一段等于插件 id、`@deepseek-ai` 命名空间禁用、工具名 snake_case 且不能叫 `run_code`。

### 3.4 生成

```bash
python <skill>/resources/tools/scaffold_plugin.py --spec <spec.json> --out <目标目录>
# 或纯命令行：
python <skill>/resources/tools/scaffold_plugin.py --type dual-face --name @me/dsh-notebook \
  --route /notebook --display-zh "笔记本" --desc-zh "在设置页管理笔记" --out ./dsh-notebook
# 只预览：
python <skill>/resources/tools/scaffold_plugin.py --spec <spec.json> --out ./x --dry-run
```

生成器会做：目录与源文件、`package.json`（含 `dsh.bundle` / `dsh.client`）、`tsconfig.json`、`tsdown.config.ts` 双目标、`cordis.patch.yml`、`README.md`、**`DEVELOPMENT.md` 初学者开发指南**、`.gitignore`。

### 3.5 填业务逻辑（模型的主要工作）

打开 `src/capability.ts` —— **唯一需要「填空」的文件**，它不 import 任何 DSH API（纯函数，便于单测）。

- `tool-only`：入参是工具参数对象，返回 `{ ok, value?, error? }`。
- `route-only` / `dual-face`：入参是请求 JSON，返回 HTTP 信封 `{ ok, value?, error? }`。
- `interceptor`：入参是 `(toolName, args)`，返回 `{ kind: 'allow' }` 或 `{ kind: 'deny', reason }`。

需要第二个工具/路由/设置区块时，按生成工程里 `DEVELOPMENT.md` 第 5 章的模式追加注册块（Host 侧 `inject` 记得补服务名）。
**界面文案一律走 `ctx.locale`，样式只许用 `var(--dsw-alias-*)` 令牌。**

### 3.6 验证并交付

```bash
# 静态自检（18 项，零依赖）
python <skill>/resources/tools/validate_plugin.py <目标目录>

# 真正的编译验证（需要网络装依赖）
cd <目标目录> && pnpm install && pnpm typecheck && pnpm build
```

只有 `pnpm typecheck && pnpm build` 真的通过，才可以对用户说「可以了」；没跑就说「静态检查通过，编译需你在本地跑 `pnpm install && pnpm build`」。

交付话术模板：

> 工程已生成在 `./dsh-notebook`，用 VSCode 打开即可开发。
> 先读 `DEVELOPMENT.md`（改代码 → 构建 → 装进 DSH → 调试 → 发布全流程）。
> 快速验证：`pnpm install && pnpm build`，然后 `dsh plugin --profile web add .`、`dsh web --port 3081`。

---

## 4. 生成物清单

```text
<slug>/
├── src/
│   ├── index.ts            # Host 半边：注册能力（接线层）
│   ├── capability.ts        # 业务实现（唯一填空处）
│   └── client/index.ts      # 仅 dual-face：设置页 UI
├── package.json             # dsh.bundle / dsh.client 声明
├── tsconfig.json
├── tsdown.config.ts         # host +（可选）client 双目标
├── cordis.patch.yml          # 安装时插入 profile 插件清单
├── README.md                # 怎么装、怎么构建
├── DEVELOPMENT.md           # ★ 初学者开发指南（内置，见下）
└── .gitignore
```

`DEVELOPMENT.md` 固定包含 10 章：拿到什么 / 心智模型（inject-apply-effect、双面通信）/ 环境准备 / 第一次改动闭环 / **按类型的功能扩展** / 四个必背坑 / 打包发布 / 调试手册（症状→根因表）/ 升级兼容 / 下一步清单。第四、五章按插件类型由 `resources/templates/sections/*.md.tpl` 渲染。

---

## 5. 硬约束（违反即「装了但不生效」）

1. **包名是唯一键**，必须同时等于：`package.json.name`、`tsdown.config.ts` 的 `PLUGIN_ID`、`cordis.patch.yml` 的 `name`、`tsconfig.json` 的 `paths` 键前缀、Client bundle 的 `__ModuleLoader__.load({id})`。
2. **`dsh.bundle.patch` 不能省**：缺了它 `dsh plugin add` 只当普通依赖，路由与设置页静默失效。
3. **`peerDependencies` 必须写 `@deepseek-ai/cordis`**，否则运行期 cordis 类型不匹配。
4. **`defineTool` 的 `output: {schema, render}` 必填**；`execute` 返回规范 JSON 值，模型看的文本由 `render` 产出。
5. **object schema 的 `additionalProperties` 必须显式 `true`/`false`**，否则 schema 编译器报错。
6. **关键服务写进 `export const inject`**，不要用 `ctx.get` 读关键服务（服务未就绪返回 `undefined`）。
7. **有 disposer 的注册必须包 `ctx.effect`**（路由/定时器/样式节点）。
8. **Client 产物只能是 tsdown 包装的 `window.__ModuleLoader__.load({id, factory})`**；模块表只认 `react` 与 `@deepseek-ai/dsh-*`，其余依赖必须内联。
9. **不用 Typert `@Remote`**，Host↔Client 只走 `webServer.register` + `fetch`。
10. **`run_code` 是保留传输名**，不可注册；不许占用官方 `@deepseek-ai` 命名空间。

---

## 6. 坑位速查（症状 → 根因 → 修法）

| 症状 | 根因 | 修法 |
| --- | --- | --- |
| 设置页/路由完全没生效且无报错 | 缺 `dsh.bundle.patch` | 补 `dsh.bundle.patch: "./cordis.patch.yml"` |
| 模型看不到工具 | 缺 `output`、被 `restrict` 过滤、被同名 scope 遮蔽 | 补 `output`；`ctx.tools.schemas(scope)` 排查 |
| 浏览器报 `__ModuleLoader__ is not defined` | Client 产物没被 banner/footer 包装 | 检查 `tsdown.config.ts` 的 `outputOptions` |
| Client 报 `require` 找不到模块 | `neverBundle` 漏 react/dsh-*，或 `alwaysBundle` 没内联 | 按第 8 条修正 deps 规则 |
| `apply` 里拿到 `undefined` | 用 `ctx.get` 代替 `inject` | 服务名加进 `inject` |
| 路由注册抛错 | `(kind, path)` 重复 | 换唯一前缀 |
| 写 DSH_HOME 被拒 | 沙箱默认策略 | `sandboxPolicy.resolve({mode:'danger-full-access'})` |
| 中文乱码 / JSON 解析失败 | UTF-8 **BOM** | 存成无 BOM |
| `JsonSchemaError: additionalProperties must be explicitly true or false` | schema 写法含糊 | 每个 object 显式声明 |
| 深色主题下样式崩 | 客户端硬编码颜色 | 全换 `var(--dsw-alias-*)` |
| GitHub 403 | token 权限不足 | 细粒度 `Contents: Read and write` 或 classic `repo` |

---

## 7. 验证命令

```bash
# 生成后立刻做：静态 18 项自检
python resources/tools/validate_plugin.py <dir>

# 编译验证
cd <dir> && pnpm install && pnpm typecheck && pnpm build

# 装配验证（最关键的一步）
dsh plugin --profile web add .
dsh --profile web --dump-config | grep <包名>
dsh web --port 3081

# 按类型验证
# tool-only   : 让 Agent 调工具，看 IN/OUT
# route-only  : curl -X POST http://127.0.0.1:3081/<prefix>/ping
# dual-face   : 设置页应有新区块，操作后有 {ok:true}
# interceptor : 调非白名单工具应被拒绝
```

---

## 8. 打包与发布

```bash
pnpm build && pnpm pack                  # 生成 .tgz
npm publish --access public              # npm（可选）
git init && git add . && git commit -m "feat: initial release"
git remote add origin git@github.com:<account>/<repo>.git && git push -u origin master
# 别人安装：dsh plugin --profile web add github:<account>/<repo>
```

发布前：`files` 必须包含 `cordis.patch.yml`；README 有一条可复制即跑的安装命令；仓库打 `dsh-plugin` topic。细节见 `resources/specifications/build_release_contract.md`。

---

## 9. 改造已有插件（不重新生成）

1. **先审计**：`validate_plugin.py` 跑一遍 → 按 [FAIL] 项逐条修（顺序：装配 → 声明 → 产物 → 运行期）。
2. **保留包名**：包名是注册键，改名等于换身份（profile 依赖、patch 行、`PLUGIN_ID`、bundle id 全要改）。
3. **只改 `src/`，再 `pnpm typecheck && pnpm build`**，绝不手改 `lib/`。
4. **重装**：`dsh plugin --profile web remove <包名>` → `add <目录>` → 重启。
5. **常见改造**：
   - 路由型 → 工具型：把 handler 体搬进 `defineTool.execute`，补 `output`，`inject` 改 `['tools']`。
   - 加 Client 半边：加 `src/client/index.ts` + tsdown client 目标 + `dsh.client` + `exports['./client']`。

---

## 10. 资源索引

| 路径 | 用途 |
| --- | --- |
| `resources/tools/scaffold_plugin.py` | 生成器（spec → 工程），支持 4 类型、`--dry-run`、`--force` |
| `resources/tools/validate_plugin.py` | 18 项静态自检，退出码 0/1 |
| `resources/tools/example_specs/*.json` | 四种类型的示例 spec，可直接改字段复用 |
| `resources/config/plugin_types.json` | 类型判定表（signals / peerDeps / verify / antiPatterns） |
| `resources/config/naming_rules.json` | 命名与一致性规则（正则） |
| `resources/specifications/plugin_manifest_contract.md` | 清单契约：包名唯一键、`dsh.bundle`/`dsh.client` |
| `resources/specifications/host_contract.md` | 生命周期、工具契约、路由契约、事件流水线、沙箱 |
| `resources/specifications/client_contract.md` | bundle 格式、插槽、locale、主题令牌、fetch 信封 |
| `resources/specifications/build_release_contract.md` | 双目标构建、安装、npm/GitHub 发布、版本兼容 |
| `resources/specifications/scaffold_spec_reference.md` | spec 字段表与类型对应关系 |
| `resources/templates/` | common / 四种类型 / sections（指南按类型分章） |
| `resources/demo_output/dsh-plugin-notebook/` | 生成产物示例（双面型，含真实笔记逻辑） |

---

## 11. 交付自检

- [ ] spec 里的包名带用户自己的 scope，且不等于任何已有插件
- [ ] 类型判定有依据（对上了 `plugin_types.json` 的 signals）
- [ ] `validate_plugin.py` 报 0 错误
- [ ] `capability.ts` 已替换 demo 逻辑（不是原样交付回声实现）
- [ ] 生成的 `DEVELOPMENT.md` 未改动、路径正确
- [ ] 已明确告知用户：下一步是 `pnpm install && pnpm build` 与 `dsh plugin --profile web add .`
- [ ] 只跑过静态检查时，明确说明「编译未验证」，不谎称通过
