---
name: "modern-web-guidance"
description: "编写或修改 Web 前端界面代码前，检索现代 Web 平台最佳实践指南。用户要处理 HTML/CSS 与客户端 JS 任务时必须使用：对话框/弹窗/Popover/模态框、抽屉、Tooltip、表格、暗色模式、容器查询、subgrid、锚点定位、视图过渡、滚动驱动动画、视差、轮播、标签页、表单校验/自动填充、自定义 select、无障碍与键盘操作、滚动条、字体与排版、色彩 oklch、Web 性能指标（LCP/INP/CLS）、图片优化、预加载、passkeys 与安全、HTML 清理、Web Components、日期时区、内置 AI、WebAssembly、框架里的原生 HTML/CSS/DOM 用法。后端 SQL/ORM/接口路由、CI/CD/Docker/脚本、纯构建工具配置（Vite/tsconfig/ESLint）不触发。"
---

# 现代 Web 平台指南（Modern Web Guidance）

## 概述

LLM 训练数据里有大量遗留前端代码，容易生成「用厚重 JavaScript 模拟本该由浏览器原生完成的行为」的写法。本技能把 Chrome / Edge / Firefox / MDN 团队维护的 **209 份现代 Web 平台指南**（随仓库自带、完全离线）注入实现前的上下文，让产出优先使用原生 API、平台级性能与无障碍能力，并按 Baseline 状态做轻量回退。

**核心原则：先检索，再实现；不凭记忆杜撰指南 id 或规则。**

指南是英文原文（CC-BY 4.0，见 [ATTRIBUTION.md](ATTRIBUTION.md)），本文件是中文的「路由器」。

## 何时使用

**触发（任一命中即先加载本技能）：**
- 要写/改任何 Web UI、CSS 布局与动画、客户端 JS 交互逻辑
- 涉及：模态框、对话框、Popover、抽屉、Tooltip、表格、暗色模式、表单校验与自动填充、无障碍、图片/字体加载、动画与过渡、安全与认证、日期时区、内置 AI、Web Components
- 即便用了 React / Vue / Nuxt / Tailwind —— 只要落到标准 HTML/CSS/DOM，仍触发
- 用户明确提到「现代写法」「Baseline」「别用旧写法」「按 Web 最佳实践」

**不触发：**
- 后端：SQL、ORM、API 路由、数据库
- 基建/脚本：CI/CD、Docker、GitHub Actions、Python/Go 脚本
- 纯工具链：Vite/tsconfig/ESLint/测试配置、复制重命名、第三方文档查询

## 工具位置

所有命令在 `modern-web-guidance/` 目录下执行（或用绝对路径指向 `resources/tools/mwg.py`）：

| 用途 | 命令 |
| :--- | :--- |
| 重建索引 | `python3 resources/tools/build_index.py` |
| 检索 | `python3 resources/tools/mwg.py search "<查询>"` |
| 取回全文 | `python3 resources/tools/mwg.py retrieve "<id>[,<id>]"` |
| 列目录 | `python3 resources/tools/mwg.py list [分类]` / `categories` |

完整契约见 [resources/specifications/local_search_contract.md](resources/specifications/local_search_contract.md)。

## 主工作流

### 第 1 步：检索（`search`）

用 **2–5 词、动作导向、单一** Web 平台能力或 UI 模式的查询：

```sh
python3 resources/tools/mwg.py search "light dismiss dialog"
python3 resources/tools/mwg.py search "responsive data table"
```

- **聚焦且通用**：`<动词> + <UI/平台对象>`，可带上已知的 HTML/CSS/JS 特性名。
- **省略**框架名（React/Vue/Tailwind）与业务名词（产品、路由、组件名/文件名）。
- **多特性拆开**：「深色模式下的响应式表格」拆成 `dark mode` 与 `responsive data table` 两次检索。
- **把意图翻译成 UI 原语**：「删除前确认」→ `"confirmation modal dialog"`；「选个日期」→ `"date picker input"`；「点外面关闭」→ `"light dismiss dialog"`。
- **中文可直接搜**：工具内置中文→英文同义词映射（`暗色`、`抽屉`、`通行密钥`、`滚动条`…）。

按返回的 `title` / `summary` 判断：
- **命中** → 直接 `retrieve`，**不要**再 `list`；
- **结果为空或不相关** → 用具体的 HTML/CSS/UI 名词（`dialog`、`modal`、`popover`、`table`、`form`）**改写一次**再搜；仍不中则用 `list` 浏览主题或判定该主题未被覆盖，不强取无关指南。

### 第 2 步：取回（`retrieve`）

```sh
python3 resources/tools/mwg.py retrieve "light-dismiss-a-dialog,dialog"
```

- 既取**具体用例指南**，也取适用的**学科总览指南**（`css` / `forms` / `html` / `accessibility` / `performance` / `security` / `color` …），多个 id 用逗号分隔。
- **全文输出、绝不截断**。若终端输出被截断，用文件读取工具按索引里的 `path` 直接读 `resources/guides/<path>`。
- 指南正文里的 `npx -y modern-web-guidance@latest retrieve "<id>"` 交叉引用，一律改成本地 `python3 resources/tools/mwg.py retrieve "<id>"`，**禁止联网调用 npx**。

### 第 3 步：实现并按指南核对

生成或修改代码后，逐条对照取回的指南：
- **现代模式与回退**：相关原生 API、必要的 fallback 是否已正确应用；不强行加入用户没要求的特性。
- **任务完成度**：是否完整满足用户诉求。
- **Baseline 与回退策略**：见下节。
- 不要运行 `legacy-scan`（本技能不提供，见契约文档第 6 节）。

### 第 4 步：披露

凡是本轮咨询了指南，在交付改动的回复末尾加 `### Modern Web Guidance` 小节：
- **指南确实影响了代码**：每个新应用的 `<id>` 写**一条**第一人称要点（1–2 句、≤75 字），说明那个非显而易见的 API / 覆盖 / 回退，以及它避免的坑，并附该规则的一小段**逐字引用**（不要引指南的概述段）：
  `- **`<id>`**：<应用了什么、避开了什么坑>（"<该条规则的逐字短引>"）。`
  - **绝不**凭记忆编造 id 或引用；上下文压缩后重新 `search`/`retrieve` 确认；只归属本轮真正用上的指南。
- **只检索但一条都没用上**：写一句第一人称说明查了哪些主题、为何都没适用（若有用上的指南则省略此句）。

## 浏览器支持与回退

- **默认**：指南假定 **Baseline Widely available** 特性无需回退。非 Widely available 特性**必须**遵循该指南「Fallback strategies」章节的回退建议，除非用户给了自定义浏览器支持策略。
- **自定义策略**：用户声明了目标（如 "Safari 17.4+"、"不要任何 polyfill"、"允许 Newly Available 但需特性检测降级"）时，用指南里的 Baseline 日期判断：特性的 "Baseline since" 日期 ≤ 目标年份即可省略回退。
- **轻量回退优先**：<50 行、按场景定制、条件加载；避免重型 polyfill 或遗留库。
- 若项目面向受限运行时（Electron/Tauri）、排除特定浏览器、或纠结 polyfill 体积，建议把策略写进 `AGENTS.md` / `CLAUDE.md`。

## 框架适配

指南用原生 HTML/CSS/JS，迁移时**保留现代特性**，不要退回旧写法：

- **类型**：新出的 HTML 属性用展开/断言补上（`{...({ popover: 'hint', interestfor: id, commandfor: id } as any)}`），不要删属性或去改 `@types/react`。
- **SSR / 打包器**：SSR 里守卫 `window` / `HTMLElement`；polyfill 用客户端 effect 里的裸 `import('<pkg>')`（或设 Vite `build.target: 'esnext'`）；**绝不**从 `node_modules` 拷贝文件。
- **DOM / ID / CSS**：`showModal()` / `moveBefore()` 通过 ref 在非 VDOM 托管节点上调用；用 `useId()` 生成每实例唯一的 `id` / `anchor-name`；`:root` 与 `@starting-style` 保持顶层、不被 scoped。

## 快速参考

| 任务 | 建议检索词 |
| :--- | :--- |
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

17 个分类共 209 份指南：`accessibility` / `built-in-ai` / `css` / `forms` / `html` / `js` / `performance` / `privacy` / `pwa` / `security` / `ui-atoms` / `ui-behaviors` / `ui-components` / `user-experience` / `visual-design` / `wasm` / `webmcp`。

## 常见错误

| 错误 | 正确做法 |
| :--- | :--- |
| 凭记忆直接写 `<dialog>` 用法、编造指南 id | 先 `search` → `retrieve`，按取回的原文实现 |
| 查询里塞框架名/业务名（"React 设置弹窗"） | 去掉噪声，用 `"light dismiss dialog"` |
| 一个查询塞多个特性（"深色模式响应式表格"） | 拆成多次 `search` |
| 命中后就直接开始写代码，不取全文 | `search` 只给摘要，必须 `retrieve` 拿到 gotchas 与回退 |
| 看到指南里的 npx 交叉引用就联网执行 | 一律映射为本地 `mwg.py`（契约文档第 4 节） |
| 给 Widely available 特性画蛇添足加重型 polyfill | 默认无需回退；非 Widely available 才按指南做轻量回退 |
| 落后于上游后忘记重建索引 | 更新 `guides/` 后重跑 `build_index.py` |

## 现有代码库现代化（替代流程）

仅当用户要求**宽泛、开放式**的全库现代化/遗留模式扫描（未点名具体特性或组件）时：
1. 用 `categories` / `list` 人工圈定相关指南范围；
2. 逐文件核对指南中的现代模式，按 `keepWhen` / `dropWhen` 思路剔除误报（回退、跨文件 helper、vendor 代码、形似代码）；
3. 汇总已核实的问题与现代化计划，说明本地工具**不提供** `legacy-scan` 的确定性规则库；
4. 用户要求实际改造时，逐条 `retrieve` 对应指南再应用替换，并对改动过的文件复核。

用户点名要「加/改/修/审某个具体特性或组件」时，走主工作流，**不要**做全库扫描。

## 许可与来源

指南原文来自 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) v1.0.0（commit `4dd9683`），
文档 CC-BY 4.0、代码 Apache-2.0。署名、许可与上游差异见 [ATTRIBUTION.md](ATTRIBUTION.md)。
