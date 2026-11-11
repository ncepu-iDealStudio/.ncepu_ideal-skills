# dsh-plugin-starter

> 把「一句话需求 / 一份插件原型」初始化成**可直接打开开发的 DSH（DeepSeek Harness）插件起步项目**，
> 并内置一份写给初学者的《开发者指南》——从改代码、调试，到打包发布、装进 DSH。

- 支持 **四类插件**：工具型（无界面）、路由型（无界面）、双面型（设置页界面）、拦截器型
- 生成的工程**自带 `DEVELOPMENT.md`**：10 章，含「按类型扩展功能」与「症状 → 根因」调试表
- 自带两个零依赖 Python 工具：`scaffold_plugin.py`（生成）、`validate_plugin.py`（18 项自检）

---

## 1. 它解决什么问题

DSH 插件的第一道门槛不是写业务代码，而是**一堆静默失败**：

- 少写 `dsh.bundle.patch` → 装了不生效，不报错
- 包名与 `PLUGIN_ID` / `cordis.patch.yml` 不一致 → 装了不生效，不报错
- Client 产物没被 tsdown 包成 `__ModuleLoader__.load({id, factory})` → 设置页白屏
- `defineTool` 少了 `output` → 工具注册失败，模型看不到
- `ctx.get` 代替 `inject` → `apply` 里拿到 `undefined`

本技能把这些约定**固化进模板与校验器**，让生成出来的工程默认就是对的；同时把「为什么」写进工程自带的 `DEVELOPMENT.md`，让初学者能自己往下走。

---

## 2. 四种插件类型

| 类型 | 能力出口 | 消费者 | 有界面 | 典型需求 |
| --- | --- | --- | --- | --- |
| `tool-only` | `ctx.tools.register(defineTool(...))` | 模型 | 否 | 「让 AI 能查/抓/算/写」 |
| `route-only` | `ctx.webServer.register()` | 外部脚本 / 浏览器 | 否 | 「提供 HTTP 接口给别人调」 |
| `dual-face` | 路由 + `settings.section` 插槽 | 用户（GUI） | 是 | 「设置页 / 面板 / 可视化配置」 |
| `interceptor` | `ctx.on('tools/pre-execute')` | 其他工具调用链 | 否 | 「白名单 / 审计 / 审批」 |

判定表（含触发词、peerDeps、验证方式、反模式）见 [`resources/config/plugin_types.json`](resources/config/plugin_types.json)。

---

## 3. 目录结构

```text
dsh-plugin-starter/
├── SKILL.md                          # 技能主文件（六步工作流 + 硬约束 + 坑位表）
├── README.md                         # 本文件
└── resources/
    ├── config/
    │   ├── plugin_types.json         # 四类型判定表
    │   └── naming_rules.json         # 包名 / 插件 id / 工具名 / 路由 的命名正则
    ├── specifications/
    │   ├── plugin_manifest_contract.md   # 清单契约：包名唯一键、dsh.bundle / dsh.client
    │   ├── host_contract.md              # 生命周期、工具契约、路由契约、事件流水线、沙箱
    │   ├── client_contract.md            # bundle 格式、插槽、locale、主题令牌、fetch 信封
    │   ├── build_release_contract.md     # 双目标构建、安装验证、npm / GitHub 发布
    │   └── scaffold_spec_reference.md    # 生成器 spec 字段表
    ├── templates/
    │   ├── common/                   # package.json / tsconfig / tsdown / cordis.patch.yml / README / DEVELOPMENT.md
    │   ├── tool-only/  route-only/  dual-face/  interceptor/   # 各类型的 src 模板
    │   └── sections/                 # 《开发指南》第 5 章，按类型渲染
    ├── tools/
    │   ├── scaffold_plugin.py        # 生成器（spec → 工程）
    │   ├── validate_plugin.py        # 18 项静态自检
    │   └── example_specs/            # 四类插件的示例 spec
    └── demo_output/
        └── dsh-plugin-notebook/      # 示例产物：双面型插件（路由 + 设置页 + 真实笔记逻辑）
```

---

## 4. 安装为技能

技能目录名必须与 `SKILL.md` 的 `name` 一致，把整个 `dsh-plugin-starter/` 放进任意技能根：

```bash
# DSH（用户级 / 项目级）
cp -r dsh-plugin-starter ~/.dsh/skills/dsh-plugin-starter
cp -r dsh-plugin-starter <项目根>/.dsh/skills/dsh-plugin-starter

# CodeBuddy / Agent Skills / Cursor
cp -r dsh-plugin-starter <项目根>/.codebuddy/skills/dsh-plugin-starter
cp -r dsh-plugin-starter <项目根>/.agents/skills/dsh-plugin-starter
```

安装后，对 AI 说「帮我做一个 DSH 插件，能……」即可触发；也可以点名「用 dsh-plugin-starter 技能」。

---

## 5. 快速开始

### 步骤 1：澄清需求

技能会一次问 2-3 个选择题（谁使用 / 数据从哪来 / 命名）。回答后得到一份 5 行需求摘要。

### 步骤 2：生成

```bash
# spec 驱动（推荐，模型会自动写好这份 spec）
python resources/tools/scaffold_plugin.py --spec my-plugin.json --out ./dsh-notebook

# 命令行直给
python resources/tools/scaffold_plugin.py \
  --type dual-face --name @me/dsh-notebook --route /notebook \
  --display-zh "笔记本" --display-en "Notebook" \
  --desc-zh "在设置页管理笔记" --out ./dsh-notebook

# 只预览将生成的文件
python resources/tools/scaffold_plugin.py --spec my-plugin.json --out ./x --dry-run
```

### 步骤 3：开发与验证

```bash
cd dsh-notebook
pnpm install && pnpm typecheck && pnpm build
python <skill>/resources/tools/validate_plugin.py .
dsh plugin --profile web add . && dsh web --port 3081
```

生成的工程里，**`DEVELOPMENT.md` 是主教材**，`src/capability.ts` 是唯一需要填业务逻辑的文件。

---

## 6. 生成物清单

```text
<slug>/
├── src/
│   ├── index.ts            # Host 半边：注册工具 / 路由 / 拦截事件
│   ├── capability.ts        # 业务实现（纯函数，唯一填空处）
│   └── client/index.ts      # 仅 dual-face：设置页 UI
├── package.json             # dsh.bundle（+ dsh.client）
├── tsconfig.json
├── tsdown.config.ts         # host +（可选）client 双目标
├── cordis.patch.yml          # 安装时插入 profile 插件清单
├── README.md                # 怎么装、怎么构建
├── DEVELOPMENT.md           # ★ 初学者开发指南（10 章）
└── .gitignore
```

### `DEVELOPMENT.md` 的 10 章

1. 你拿到了什么（文件职责）
2. 心智模型（`inject` → `apply` → `effect`、Host/Client 双面通信）
3. 环境准备（Node / pnpm / dsh 版本）
4. 第一次改动闭环（改 → 构建 → 装 → 验，含「改哪里要重启」对照表）
5. **按类型扩展功能**（加工具 / 加路由 / 加设置区块 / 加策略，各含完整代码）
6. 四个必背坑（包名四一致、`dsh.bundle.patch`、`output` 必填、沙箱与 Windows）
7. 打包与发布（files 字段、tgz、npm、GitHub）
8. 调试手册（三招定位 + 11 条「症状 → 根因」表 + patch 覆盖层开发法）
9. 升级与兼容（预览版 API 变动检查项）
10. 下一步清单

---

## 7. 校验器：18 项

```bash
python resources/tools/validate_plugin.py <插件目录>
# 退出码 0 = 通过（可能有警告）；1 = 存在错误
```

| 组 | 检查内容 |
| --- | --- |
| 装配 | 必需文件齐全、`package.json` 可解析、`main`/`exports` 指向、**`dsh.bundle.patch` 存在**、`cordis.patch.yml` 的 `id`/`name`/`insert` |
| 声明 | `tsdown` 的 `PLUGIN_ID` 与包名一致、`dsh.client` ↔ `src/client/index.ts` ↔ `exports['./client']` ↔ tsdown client 目标双向一致、`tsconfig` paths、`peerDependencies` 含 cordis |
| 产物 | `lib/client.js` 若是 `__ModuleLoader__.load` 格式且 id 等于包名（未构建则仅警告） |
| 运行期 | 未用 `input_schema`、未注册 `run_code`、`defineTool` 有 `output.schema/render`、`webServer.register` 包在 `ctx.effect`、有 `inject`、无硬编码颜色、结构化错误、无 BOM、无残留 `{{...}}` 占位符 |

---

## 8. 示例产物

[`resources/demo_output/dsh-plugin-notebook`](resources/demo_output/dsh-plugin-notebook/README.md)：双面型插件，展示「生成骨架 → 补齐业务」后的样子。

- Host：`/notebook` 下的 `ping` / `list` / `add` / `remove`
- Client：设置页「笔记本」区块（输入 + 列表 + 删除），中英双语，主题令牌
- 静态自检 0 错误

---

## 9. 参考来源

| 来源 | 本技能吸收了它什么 |
| --- | --- |
| [`lansi-ai/dsh-plugin-starter`](https://github.com/lansi-ai/dsh-plugin-starter) | 双面架构、tsdown 双目标与 `__ModuleLoader__` 包装、`package.json` 的 `dsh.bundle`/`dsh.client` 声明、17 条坑位、改名清单 |
| [`yanhua1010/dsh-harness-tutorial`](https://github.com/yanhua1010/dsh-harness-tutorial) | 插件三形态与 Cordis 生命周期、事件模式（waterfall / emit）、headless `--patch` 覆盖层调试、工具流水线五阶段 |
| 本仓库 `sql-to-*` / `prototype-to-*` 技能 | 分层组织方式：`config` / `specifications` / `templates` / `tools` / `demo_output`，规范先于实现、产物可校验 |

---

## 10. 注意

- DSH 仍是**开发者预览版**（`0.1.x`），`@deepseek-ai/*` 的 API 会破坏性变更。模板锁定 `^0.1.0-rc.7` / cordis `^4.0.1`，升级前先读 changelog。
- 本技能的静态校验**不能替代真实编译**：交付时若未跑 `pnpm typecheck && pnpm build`，应明确说明「编译未验证」。
