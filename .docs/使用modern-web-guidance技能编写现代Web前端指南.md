# 使用 `modern-web-guidance` 技能编写现代 Web 前端

> 面向所有会写/改 Web 界面的人。照着本文走完，你能让 AI 在动手写 HTML/CSS/客户端 JS 之前，先查
> 随仓库自带的 **209 份现代 Web 平台专家指南**，把「用厚重 JS 模拟浏览器原生能力」的遗留写法，
> 换成 `<dialog>`、容器查询、视图过渡、原生表单校验这类**浏览器已经帮你做好**的现代做法。
>
> 移植自 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) v1.0.0，
> 由 Chrome / Edge / Firefox / MDN 团队维护。本文是**使用说明**，技能本体见
> [`modern-web-guidance/`](../modern-web-guidance/README.md)，工具契约见
> [`local_search_contract.md`](../modern-web-guidance/resources/specifications/local_search_contract.md)。

---

## 1. 一句话：它解决什么问题

编码智能体的训练数据里有大量遗留前端代码，容易默认生成这种写法：

- 手写 `role="dialog"` + `aria-modal` + 焦点陷阱 + Esc 监听 + `body.style.overflow='hidden'`
- 用 `window.innerWidth` 媒体查询硬套响应式
- 引入重型 polyfill 或第三方 UI 库做一件浏览器原生就能做的事

`modern-web-guidance` 在**实现之前**把高密度的现代实现模式、隐藏的 gotchas、Baseline 兼容数据和
轻量回退策略注入上下文。它**不生成工程**，是一个「参考型 / 路由器」技能。

| 输入 | 输出 |
| --- | --- |
| 一句 Web UI 需求（「做个点遮罩关闭的确认框」） | 符合现代规范的实现代码 + 用了哪些指南的披露 |
| 已有的前端代码要改 | 按指南修正后的代码 + 差异说明 |
| 一个命令行查询 | 相关指南 id + 全文（也可当独立 CLI 用） |

**与上游的关键差异**（决定了下面的用法）：上游靠 `npx modern-web-guidance@latest …` 联网拉包、
带遥测、且 CLI 源码不随仓库开源；本技能改成**随仓库自带的零依赖本地 Python 工具**——
完全离线、可审计、无遥测。所以你**不需要装 npm 包、不需要联网**。

---

## 2. 安装与配置

### 2.1 前置条件

- **Python 3**（仅标准库，无需 `pip install`）——本地检索工具需要。
- 一个支持 Skills 的 AI 编码工具（见下表），或干脆只用命令行。

### 2.2 安装位置

技能目录名必须与 `SKILL.md` 的 `name`（`modern-web-guidance`）一致。整个目录一起复制：

| 工具 | 路径 |
| --- | --- |
| DSH（用户级） | `~/.dsh/skills/modern-web-guidance/`（`$DSH_HOME` 未设时默认 `~/.dsh`） |
| DSH（项目级） | `<项目根>/.dsh/skills/modern-web-guidance/` |
| Claude Code | `~/.claude/skills/` 或 `<项目根>/.claude/skills/` |
| CodeBuddy | `<项目根>/.codebuddy/skills/modern-web-guidance/` |
| Agent Skills 通用 | `<项目根>/.agents/skills/modern-web-guidance/` |
| Cursor | `<项目根>/.cursor/skills/modern-web-guidance/` |
| WorkBuddy | `<项目根>/.workbuddy/skills/modern-web-guidance/` |

```bash
# 例：装到 Claude Code 全局目录
cp -r ncepu_ideal-skills/modern-web-guidance ~/.claude/skills/

# 例：装到当前项目的 DSH 项目级目录
mkdir -p .dsh/skills && cp -r /path/to/ncepu_ideal-skills/modern-web-guidance .dsh/skills/
```

> 💡 指南、索引、工具都在这个目录里（约 2.7 MB / 216 个文件），**整个目录一起复制**，
> 不要只拷 `SKILL.md`，否则 `retrieve` 会找不到 `resources/guides/`。

### 2.3 首次初始化（生成索引）

索引文件 `resources/guides_index.json` 是随仓库提交的派生文件，开箱即用。
只有当你**更新过 `guides/`** 或想校验一致性时才重建：

```bash
cd modern-web-guidance
python3 resources/tools/build_index.py
# 输出：指南数 209，分类数 17
```

### 2.4 验证安装

```bash
cd modern-web-guidance
python3 resources/tools/mwg.py categories      # 应列出 17 类、209 份
python3 resources/tools/mwg.py search "light dismiss dialog"
```

在支持技能列表的工具里（如 Claude Code 输入 `/skills`），应能看到 `modern-web-guidance`。

---

## 3. 怎么触发（三种方式，效果等价）

1. **描述匹配（最常用）**：直接说 Web UI 需求，例如「帮我做个确认删除的对话框，点遮罩能关、Esc 能关、背景别滚动」。
2. **点名**：「用 modern-web-guidance 技能，检查一下这个表格在手机上的响应式写法」。
3. **显式手势**：部分工具支持 `/modern-web-guidance`。

**会触发**：HTML/CSS、Web UI、客户端 JS 交互；对话框/弹窗/Popover/抽屉/Tooltip、表格、暗色模式、
容器查询、视图过渡、滚动动画、表单校验与自动填充、无障碍、图片/字体、性能（LCP/INP/CLS）、
安全与 Passkeys、Web Components、日期时区、内置 AI；即使用了 React/Vue/Nuxt/Tailwind，只要落到
标准 HTML/CSS/DOM 仍触发。

**不会触发**：后端 SQL/ORM/接口路由、CI/CD/Docker/脚本、纯构建配置（Vite/tsconfig/ESLint）、
复制重命名、查第三方文档。

---

## 4. 完整工作流：四步

技能被触发后，`SKILL.md` 要求它严格走下面四步。**核心纪律：先检索，再实现；不凭记忆杜撰指南 id 或规则。**

### 第 1 步 `search` —— 检索相关指南

```bash
python3 resources/tools/mwg.py search "light dismiss dialog"
```

查询写成 **2–5 词、动作导向、单一**能力或 UI 模式：

| ✅ 好查询 | ❌ 坏查询 | 为什么 |
| --- | --- | --- |
| `light dismiss dialog` | `dialog` | 太泛，召回一堆 |
| `responsive data table` | `responsive table dark mode` | 复合特性，要拆成两次 |
| `confirmation modal dialog` | `close React settings modal on outside click` | 带了框架名/业务名词噪声 |
| `container queries` | `选个日期` | 领域意图要翻译成 UI 原语：→ `date picker input` |

- 省略框架名（React/Vue/Tailwind）与业务名词（产品、路由、文件名）。
- 多特性任务**拆成多次** `search`。
- 把隐含意图翻译成 UI 原语：「删除前确认」→ `confirmation modal dialog`。
- **中文可直接搜**：工具内置中文→英文同义词映射（`暗色`、`抽屉`、`通行密钥`、`滚动条`…）。

按返回的 `title` / `summary` 判断：
- **命中** → 直接进第 2 步 `retrieve`，**不要**再 `list`；
- **结果为空/不相关** → 用具体名词（`dialog`/`modal`/`popover`/`table`/`form`）**改写一次**再搜；
- 仍不中 → 用 `list` 浏览主题，或判定该主题未被覆盖，**不强取无关指南**。

### 第 2 步 `retrieve` —— 取回全文

```bash
python3 resources/tools/mwg.py retrieve "light-dismiss-a-dialog,dialog,accessibility"
```

- 既取**具体用例指南**，也取适用的**学科总览指南**（`css`/`forms`/`html`/`accessibility`/
  `performance`/`security`/`color`…），多个 id 用逗号分隔。
- 输出**完整原文、不截断**，开头有一行 `<!-- id | category | source: 相对路径 -->` 便于溯源。
- 若终端输出被截断，用文件读取工具直接读 `resources/guides/<path>`（`path` 来自索引），
  **不要**用 `head`/`cat` 截断后臆断。
- ⚠️ 指南正文里出现的 `npx -y modern-web-guidance@latest retrieve "<id>"` 交叉引用，
  **一律改成本地命令**，禁止联网调用 npx（映射表见契约文档第 4 节）。

### 第 3 步 实现并按指南核对

生成/修改代码后逐条对照取回的指南：

- 相关现代 API、必要的 fallback 是否正确应用；
- 是否完整满足用户诉求，且**没有强行加入用户没要的特性**；
- Baseline 与回退策略（见第 6 节）。

### 第 4 步 披露

凡是本轮咨询了指南，回复末尾加 `### Modern Web Guidance` 小节：

```markdown
### Modern Web Guidance

- **`dialog`**：用 `showModal()` + `<dialog closedby="any">`，不手写焦点陷阱/Esc/ARIA，
  省去重建原生语义（"DON'T add role="dialog", aria-modal, a focus trap…"）。
- **`light-dismiss-a-dialog`**：声明式 `closedby="any"`，并为不支持的浏览器加按坐标判定的
  pointer 回退，避免拖拽误关（"MANDATORY: Use closedby="any"…"）。
```

- 每个**新应用**的 `<id>` 一条第一人称要点（1–2 句、≤75 字），说明非显而易见的 API/覆盖/回退
  与它避免的坑，附该条规则的**逐字短引**（不要引指南的概述段）。
- **绝不**凭记忆编造 id 或引用；上下文压缩后重新 `search`/`retrieve` 确认；只归属本轮真正用上的指南。
- 若只检索但一条都没用上：写一句第一人称说明查了哪些主题、为何都没适用。

---

## 5. 命令行速查（也能脱离 AI 单独用）

所有命令在 `modern-web-guidance/` 目录下执行（`mwg.py` 也可用绝对路径调用）：

| 命令 | 作用 |
| --- | --- |
| `python3 resources/tools/mwg.py search "<查询>" [-n 8] [--json]` | 关键词加权检索，返回候选 id/标题/摘要 |
| `python3 resources/tools/mwg.py retrieve "<id>[,<id>]"` | 输出指南全文，多 id 逗号分隔 |
| `python3 resources/tools/mwg.py list [分类] [--json]` | 列出全部或某分类的 `id → 标题` |
| `python3 resources/tools/mwg.py categories` | 列出 17 个分类及计数 |
| `python3 resources/tools/build_index.py` | 重建 `guides_index.json` |

```bash
# 看主题
python3 resources/tools/mwg.py categories

# 英文 / 中文检索
python3 resources/tools/mwg.py search "optimize image loading performance" -n 5
python3 resources/tools/mwg.py search "响应式表格" -n 5
python3 resources/tools/mwg.py search "暗色模式"

# 取全文（可多个）
python3 resources/tools/mwg.py retrieve "dialog,forms"

# 浏览某分类
python3 resources/tools/mwg.py list ui-components
```

**退出码**：`search` 无结果为 `2`（应改写查询或浏览目录）；`retrieve` 的 id 不存在为 `1`。
`--json` 便于脚本消费。检索**完全离线、零依赖、无遥测**。

---

## 6. 浏览器支持与回退策略

- **默认**：指南假定 **Baseline Widely available** 特性无需回退。非 Widely available 特性
  **必须**遵循该指南「Fallback strategies」章节的回退建议，除非用户给了自定义策略。
- **自定义策略**：用户声明目标（如 `Safari 17.4+`、`不要任何 polyfill`、`允许 Newly Available
  但需特性检测降级`）时，用指南里的 Baseline 日期判断：特性的 "Baseline since" 日期 ≤ 目标年份
  即可省略回退。
- **轻量回退优先**：<50 行、按场景定制、条件加载；避免重型 polyfill 或遗留库。
- 面向受限运行时（Electron/Tauri）、排除特定浏览器、或纠结 polyfill 体积时，建议把策略写进
  `AGENTS.md` / `CLAUDE.md`，例如：
  `**Browser Support:** Allow Newly Available features, but only adopt custom fallback code that
  adds <= 20 lines and no external dependencies`。

> 📌 上游对 Origin Trial / volatile 特性有 `retrieve` 门禁（`.mwgrc` 解锁），本技能**不做门禁**：
> 分发的是上游公开快照，不含被门禁隐藏的内容。仍须遵守上面的通用 Baseline 规则。

---

## 7. 框架适配（别把现代特性改回旧写法）

指南用原生 HTML/CSS/JS，迁移到框架时**保留现代特性**：

- **类型**：新出的 HTML 属性用展开/断言补上
  （`{...({ popover: 'hint', interestfor: id, commandfor: id } as any)}`），不要删属性或去改 `@types/react`。
- **SSR / 打包器**：SSR 里守卫 `window` / `HTMLElement`；polyfill 用客户端 effect 里的裸
  `import('<pkg>')`（或设 Vite `build.target: 'esnext'`）；**绝不**从 `node_modules` 拷贝文件。
- **DOM / ID / CSS**：`showModal()` / `moveBefore()` 通过 ref 在非 VDOM 托管节点上调用；用 `useId()`
  生成每实例唯一的 `id` / `anchor-name`；`:root` 与 `@starting-style` 保持顶层、不被 scoped。

---

## 8. 实战示例

### 8.1 你给 AI 的输入

```text
请实现一个点击遮罩层关闭的确认对话框，要能用键盘 Esc 关闭、
避免背景页面滚动，关闭后焦点回到触发按钮。
```

### 8.2 AI 内部实际执行的命令与输出（节选）

```bash
$ python3 resources/tools/mwg.py search "light dismiss dialog" -n 5
查询「light dismiss dialog」→ 5 条结果（共 209 份指南）：

  [ 88.0] light-dismiss-a-dialog  (ui-behaviors)
          Light-Dismiss a Dialog
  [ 64.0] platform-controls-dismiss-dialog  (ui-behaviors)
          Platform Controls Dismiss Dialog
  [ 36.0] dialog  (ui-components)
          Dialog
  [ 32.0] declarative-dialog-popover-control  (ui-behaviors)
  [ 32.0] prevent-page-scroll-under-modal-dialog  (ui-behaviors)

$ python3 resources/tools/mwg.py retrieve "dialog,light-dismiss-a-dialog,prevent-page-scroll-under-modal-dialog,accessibility"
<!-- id: dialog | category: ui-components | source: ui-components/dialog.md -->
# Dialog
Use the native <dialog> element for modal and non-modal dialogs…
...（全文，不截断）
```

### 8.3 产出的关键代码（对照：不用技能时通常手写一大堆 JS）

```html
<dialog id="confirm" closedby="any" aria-labelledby="confirm-title">
  <h2 id="confirm-title">确认删除？</h2>
  <form method="dialog">
    <button value="cancel" autofocus>取消</button>
    <button value="confirm">删除</button>
  </form>
</dialog>
<button id="trigger" commandfor="confirm" command="show-modal">删除</button>
```

```css
/* 原生顶层 + 背景锁滚动：无需 body overflow 技巧 */
dialog::backdrop { overflow: hidden; }   /* 让 ::backdrop 成为滚动容器 */
dialog:modal { overscroll-behavior: contain; }
```

```js
const dialog = document.getElementById('confirm');
// showModal() 原生负责 Esc、焦点返回触发按钮、页面 inert
// closedby="any" 原生负责点遮罩关闭；仅对不支持的浏览器加轻量坐标判定回退
```

**差异一览**（来自真实对照验证）：

| 能力 | 不用技能（手写遗留写法） | 用技能（现代原生） |
| --- | --- | --- |
| 模态语义 | `role="dialog"` + `aria-modal` + `aria-hidden` | 原生 `<dialog>` + `showModal()` |
| Esc 关闭 | 文档级 `keydown` + 焦点陷阱 | 浏览器原生 |
| 点遮罩关闭 | `pointerdown`/`click` 判定 | `closedby="any"`（+轻量回退） |
| 背景不滚动 | `body.style.overflow='hidden'` + 补滚动条 | `overscroll-behavior` + `::backdrop` |
| 焦点返回 | 手动存触发按钮 | `showModal()` 原生 |

### 8.4 回复末尾的披露（技能强制）

```markdown
### Modern Web Guidance

- **`dialog`**：用 `showModal()` + 原生 `<dialog>`，不手写焦点陷阱/Esc/ARIA，
  省去重建原生语义（"DON'T add role="dialog", aria-modal, a focus trap…"）。
- **`prevent-page-scroll-under-modal-dialog`**：用 `overscroll-behavior: contain` +
  `::backdrop` 的 `overflow: hidden` 锁滚动，不用 html/body 的 overflow 技巧（"…"）。
```

---

## 9. 常见任务 → 检索词速查

| 任务 | 建议检索词 |
| --- | --- |
| 模态框 / 点外关闭 | `dialog`、`light dismiss dialog`、`confirmation modal` |
| 抽屉 / 导航 | `navigation drawer`、`navbar` |
| 弹出层 / Tooltip | `popover`、`tooltip`、`anchor positioning` |
| 表格 | `responsive data table`、`sortable table` |
| 表单 | `form validation`、`autofill`、`user-invalid` |
| 暗色 / 颜色 | `dark mode`、`color oklch`、`contrast-color` |
| 布局 | `container queries`、`subgrid`、`css layout` |
| 动画 / 过渡 | `view transitions`、`scroll-driven animations`、`entry exit animation` |
| 性能 | `optimize image priority`、`INP`、`break up long tasks`、`preload` |
| 安全 / 认证 | `passkey`、`sanitize untrusted html`、`trusted types` |
| 无障碍 | `accessibility`、`focus-visible`、`error announcement` |
| Web Components | `custom elements`、`shadow dom` |
| 日期时区 | `Temporal`、`calendar`、`timezone` |
| 内置 AI | `prompt api`、`translator`、`summarizer` |

17 个分类共 209 份：`accessibility` / `built-in-ai` / `css` / `forms` / `html` / `js` /
`performance` / `privacy` / `pwa` / `security` / `ui-atoms` / `ui-behaviors` /
`ui-components` / `user-experience` / `visual-design` / `wasm` / `webmcp`。

---

## 10. 现有代码库现代化（另一种流程）

仅当用户要求**宽泛、开放式**的全库现代化/遗留扫描（未点名具体特性或组件）时：

1. `categories` / `list` 人工圈定相关指南范围；
2. 逐文件核对现代模式，剔除误报（回退、跨文件 helper、vendor 代码、形似代码）；
3. 汇总已核实问题与计划，说明本地工具**不提供** `legacy-scan` 的确定性规则库；
4. 用户要求实际改造时，逐条 `retrieve` 对应指南再应用替换，并复核改动文件。

> 用户点名「加/改/修/审某个具体特性或组件」时走第 4 节主工作流，**不要**做全库扫描。

---

## 11. 常见问题（FAQ）

| 问题 | 解答 |
| --- | --- |
| 需要联网 / 装 npm 包吗？ | **不需要**。工具随仓库自带、零依赖、完全离线；刻意不调用 `npx`。 |
| 会上传我的代码或查询吗？ | **不会**。无网络请求、无遥测。 |
| 指南是中文吗？ | 指南是**上游英文原文逐字副本**（CC-BY 4.0），中文在 `SKILL.md`/README/工具里；中文可直接检索。 |
| 为什么 `retrieve` 里还写着 `npx …`？ | 是指南正文的交叉引用，一律按第 4 节映射成本地 `mwg.py retrieve`。 |
| `search` 没结果怎么办？ | 用具体 UI 名词改写**一次**再搜；仍不中则 `list` 浏览，或判定主题未覆盖，不强取。 |
| `retrieve` 输出被终端截断？ | 用文件读取工具读 `resources/guides/<path>`，别用 `head`/`cat` 截断后臆断。 |
| 用 React/Vue/Tailwind 还有用吗？ | 有。只要落到标准 HTML/CSS/DOM 就触发，按第 7 节保留现代特性。 |
| 更新/改了 `guides/` 后要做什么？ | 重跑 `python3 resources/tools/build_index.py`，再抽样验证。 |
| 支持 `legacy-scan` / Chrome 扩展包吗？ | 本次不移植（前者依赖上游未开源规则库，后者是独立技能包）。 |
| 许可？ | 文档 CC-BY 4.0、代码 Apache-2.0，署名见 [`ATTRIBUTION.md`](../modern-web-guidance/ATTRIBUTION.md)。 |

---

## 12. 更新指南

指南随 Web 平台演进而更新，同步上游最新版：

```bash
git clone --depth 1 https://github.com/GoogleChrome/modern-web-guidance.git /tmp/mwg-upstream
rm -rf modern-web-guidance/resources/guides
cp -r /tmp/mwg-upstream/skills/modern-web-guidance/guides modern-web-guidance/resources/guides

cd modern-web-guidance
python3 resources/tools/build_index.py          # 重建索引
python3 resources/tools/mwg.py categories        # 核对计数
python3 resources/tools/mwg.py search "light dismiss dialog"   # 抽样验证
```

随后更新 `ATTRIBUTION.md` 顶部的 commit 与版本号，并评估上游 `SKILL.md` 工作流是否需要同步。
若决定翻译/改写指南，**必须**在 `ATTRIBUTION.md` 声明「已修改」。详见契约文档第 8–9 节。

---

## 13. 验收清单

- [ ] 整个技能目录（含 `resources/guides/`）已复制到 AI 工具的 skills 目录，目录名 = `modern-web-guidance`
- [ ] `python3 resources/tools/mwg.py categories` 显示 17 类、209 份
- [ ] `search "light dismiss dialog"` 首条为 `light-dismiss-a-dialog`
- [ ] `retrieve "dialog"` 输出含 `# Dialog` 且非空
- [ ] 中文查询（「暗色」「响应式表格」「通行密钥」）能返回相关结果
- [ ] 让 AI 做一次 Web UI 任务，回复末尾出现 `### Modern Web Guidance` 披露段且 id 真实存在
- [ ] 全程无网络请求、无遥测、无 `npx` 调用

---

## 14. 与本仓库其它技能叠加

叠加是同一次任务里两份技能一起生效，不是把本技能嵌进对方的生成步骤。对方技能仍决定目录、分层和组件库。只有写到浏览器里的 HTML/CSS/DOM 时，才按第 4 节检索。

| 技能 | 何时查阅 | 说明 |
| --- | --- | --- |
| [prototype-to-web(Nuxt UI Starter)](../prototype-to/prototype-to-web(Nuxt%20UI%20Starter)/README.md) | 对话框、表格、表单、暗色、滚动、焦点、图片优先级，映射到 Nuxt UI | 该技能 README 第 11 节 |
| [requirements-to-vue_vben_admin](../requirements-to-vue_vben_admin/README.md) | 同上，映射到 VxeGrid / Vben 表单 / Ant Design Vue | 该技能 README 第 10 节 |
| [common-website-design](../.dsh/skills/common-website-design/README.md) | 写静态 HTML 的语义、焦点、对话框、滚动、动效 | `.dsh` 与 `.workbuddy` 两份说明相同 |
| [prd-html-skill](../.cursor/skills/prd-html-skill/README.md) | 逐页写可点原型的对话框、表单、表格 | `.cursor` 与 `.dsh` 两份说明相同 |
| [md-prd-to-html-prototype](../.workbuddy/skills/md-prd-to-html-prototype/SKILL.md) | 单文件原型里的弹窗、表单、表格；仍全部内联 | 无单独 README，规则写在 `SKILL.md` |
| [prototype-to-taro-app](../prototype-to/prototype-to-taro-app/README.md) | 仅 H5 | 该技能 README 第 11 节；CodeBuddy 指南见 [在 CodeBuddy 中使用](在Codebuddy插件中使用prototype-to-taro-app技能指南.md) |
| [prototype-to-app-uniappx](../prototype-to/prototype-to-app-uniappx/README.md) | 仅 H5；App 端约束优先 | 该技能 README 第 11 节；WorkBuddy 指南见 [原型转应用](workbuddy中使用原型转应用技能.md) |
| [dsh-plugin-starter](../dsh-plugin-starter/README.md) | 仅 dual-face 设置页 | 该技能 README 第 11 节；插件指南见 [开发 DSH 插件](使用dsh-plugin-starter技能开发DSH插件.md) |

后端脚手架、Flutter、iOS、Android 不叠加。没有上述界面任务时，不要调用本技能。

## 相关文件

- 技能本体：[`modern-web-guidance/README.md`](../modern-web-guidance/README.md)
- 路由器：[`modern-web-guidance/SKILL.md`](../modern-web-guidance/SKILL.md)
- 工具契约：[`local_search_contract.md`](../modern-web-guidance/resources/specifications/local_search_contract.md)
- 来源与许可：[`ATTRIBUTION.md`](../modern-web-guidance/ATTRIBUTION.md)
- 各工具配置 skill 目录：[Claude](claude中使用skill配置.md) · [CodeBuddy](CodeBuddy中使用skill配置.md) · [Trea](Trea中使用skill配置.md) · [DSH](dsh中使用superpowers技能.md)
