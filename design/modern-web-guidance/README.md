# modern-web-guidance（现代 Web 平台指南技能）

把 [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance)
移植成本仓库的一个**离线自包含、中文驱动**的技能项目：在 AI 编写/修改 Web 前端界面代码之前，
先从随仓库自带的 **209 份现代 Web 平台指南**里检索、取回对应的专家指南，让产出优先使用
浏览器原生 API、平台级性能与无障碍能力，并按 Baseline 状态做轻量回退，远离遗留模式。

> 由 Google Chrome、Microsoft Edge、Mozilla Firefox 与 MDN 团队联合 Web 社区维护。
> 本仓库仅对**驱动层**（`SKILL.md`、本 README、检索工具、规范文档）做了中文改写与本地化，
> `resources/guides/` 下的 209 份指南为上游英文原文的逐字副本。详见 [ATTRIBUTION.md](ATTRIBUTION.md)。

---

## 为什么需要它

编码智能体常因训练数据里大量遗留前端代码，默认生成「用厚重 JavaScript 模拟浏览器原生能力」的写法
——例如手写焦点管理、手写模态框、手写滚动监听、引入重型 polyfill。本技能把高密度的现代实现模式、
gotchas、Baseline 兼容数据与轻量回退策略，在**动手前**注入上下文，并校准到「模型本来不会、
但浏览器原生已能做得更好」的部分。

## 本仓库版本与上游的差异

| 项目 | 上游 | 本项目 |
| :--- | :--- | :--- |
| 指南检索 | `npx modern-web-guidance@latest search/retrieve`（联网拉 npm 包、离线语义模型、带 Google 遥测） | 本地 `python3 resources/tools/mwg.py`（零依赖、完全离线、无遥测、关键词加权 + 中文映射） |
| 路由器 | 英文 `SKILL.md` | 中文 `SKILL.md`，工作流对齐但面向本仓库 |
| 指南内容 | 随 npm 包分发 | 随仓库原样自带 209 份（2.4 MB），可审计、可 diff |
| 交叉引用 | 指南内的 `npx … retrieve "<id>"` | 阅读时映射为本地 `mwg.py retrieve`，见 [检索契约](resources/specifications/local_search_contract.md) |
| 遗留扫描 | `legacy-scan`（依赖上游未开源的规则库） | 不提供 |
| Chrome 扩展包 | `skills/chrome-extensions` | 不纳入（本次仅移植主技能） |
| 实验特性门禁 | `.mwgrc` 解锁 Origin Trial / volatile 特性 | 不提供门禁（分发的公开快照无被隐藏内容） |

选择本地自包含的理由：上游 CLI 源码不在仓库里、需要联网、且带遥测；本仓库的技能强调
**资源驱动、可离线复现、可审计**，因此用零依赖 Python 工具替代。

## 目录结构

```text
modern-web-guidance/
├── SKILL.md                                  # 中文路由器：触发条件 + 4 步工作流 + 快速参考
├── README.md                                 # 本文件
├── ATTRIBUTION.md                            # 来源、commit、许可（Apache-2.0 / CC-BY-4.0）
└── resources/
    ├── guides/                               # 209 份指南原文（17 个分类，CC-BY 4.0）
    │   ├── css/  forms/  html/  js/  performance/  security/  accessibility/
    │   ├── ui-components/  ui-behaviors/  ui-atoms/  visual-design/  …
    ├── guides_index.json                     # 派生索引（由 build_index.py 生成）
    ├── specifications/
    │   └── local_search_contract.md          # 本地检索工具契约 + 上游命令映射
    └── tools/
        ├── build_index.py                    # 扫描 guides/ 重建索引（stdlib）
        └── mwg.py                            # 本地检索 CLI：search/retrieve/list/categories
```

## 快速开始

> 前置：Python 3（仅标准库，无需 pip 安装）。所有命令在 `modern-web-guidance/` 目录下执行。

```sh
# 0) 首次使用/更新指南后：重建索引
python3 resources/tools/build_index.py

# 1) 看看有哪些主题（17 类、209 份）
python3 resources/tools/mwg.py categories

# 2) 按能力检索（2–5 词、单一 UI/平台能力；中文也可）
python3 resources/tools/mwg.py search "light dismiss dialog"
python3 resources/tools/mwg.py search "响应式表格"
python3 resources/tools/mwg.py search "optimize image loading performance" -n 5

# 3) 取回指南全文（可逗号分隔多个 id）
python3 resources/tools/mwg.py retrieve "light-dismiss-a-dialog,dialog"

# 4) 浏览某个分类
python3 resources/tools/mwg.py list ui-components
```

`search` 返回 `id / 分类 / 标题 / 摘要 / 相关度`；按标题与摘要判断命中后直接 `retrieve`，
`retrieve` 输出**完整原文**（不截断），开头带一行 `<!-- id | category | source -->` 便于溯源。

### 命令一览

| 命令 | 作用 |
| :--- | :--- |
| `mwg.py search "<查询>" [-n 8] [--json]` | 关键词加权检索，返回候选指南 |
| `mwg.py retrieve "<id>[,<id>]"` | 输出指南全文（多 id 逗号分隔） |
| `mwg.py list [分类] [--json]` | 列出全部或某分类的 `id → 标题` |
| `mwg.py categories` | 列出 17 个分类及计数 |
| `build_index.py` | 重建 `guides_index.json` |

退出码：`search` 无结果为 `2`（应改写查询再搜或浏览目录）；`retrieve` 的 id 不存在为 `1`。

## 在 AI 工具里使用

把本技能目录按你所用工具的技能配置方式加载（参见根仓库
[配置指南](../README.md#1️⃣-配置技能到你的-ai-工具)），然后在任务里直接描述 Web UI 需求，例如：

```text
请实现一个点击遮罩层关闭的确认对话框，要能键盘 Esc 关闭、并避免背景页面滚动。
```

AI 会按 `SKILL.md` 的工作流：先 `search` → `retrieve` 相关指南 → 按指南实现 → 在回复末尾
用 `### Modern Web Guidance` 小节披露用到的指南与关键规则。触发条件、完整工作流、框架适配、
浏览器支持与回退策略都写在 [SKILL.md](SKILL.md)。

## 指南覆盖范围

209 份指南，按 17 个分类组织（数量随上游版本变化）：

| 分类 | 份数 | 主要内容 |
| :--- | ---: | :--- |
| `ui-behaviors` | 40 | 视图过渡、滚动驱动动画、拖拽、动效、空间导航 |
| `performance` | 26 | LCP/INP/CLS、图片/脚本优先级、长任务拆分、预加载 |
| `ui-components` | 22 | 对话框、抽屉、轮播、标签页、菜单、进度、Toast |
| `visual-design` | 22 | 色彩、排版、暗色模式、WebGL/着色器、文字装饰 |
| `forms` | 19 | 语义表单、校验、自动填充、自定义 select、OTP |
| `css` | 18 | 布局、容器查询、subgrid、相对颜色、样式复用 |
| `security` | 17 | Passkeys、HTML 清理、Trusted Types、数字签名 |
| `ui-atoms` | 13 | 响应式表格、滚动条、Tooltip、图标、进度指示 |
| `html` | 8 | Web Components、Shadow DOM、自定义元素 |
| `js` | 5 | Temporal 日期/时区、高精度时间戳、全局事件 |
| `built-in-ai` | 5 | Prompt API、翻译、摘要、语言检测 |
| `accessibility` | 4 | 屏幕阅读器、键盘、错误播报、文字缩放 |
| `webmcp` | 3 | 面向智能体的表单与 JS 工具 |
| `user-experience` | 3 | 内容优先、形态适配、自然交互 |
| `pwa` | 2 | 安装 Web 应用、迁移源 |
| `privacy` / `wasm` | 1+1 | 隐私、WebAssembly |

每份指南通常包含：Overview、Implementation（含可直接适配的代码）、Baseline 兼容数据、
Fallback strategies 与 gotchas。示例见
[`guides/ui-components/navigation-drawer.md`](resources/guides/ui-components/navigation-drawer.md)。

## 许可

- 指南内容（文档）：**CC-BY 4.0**，代码：**Apache-2.0**，署名 GoogleChrome/modern-web-guidance
- 详见 [ATTRIBUTION.md](ATTRIBUTION.md)；上游许可见其 README 的 License 章节

## 更新指南

指南会随 Web 平台演进而更新。同步上游最新版：

```sh
# 1) 拿到上游新版（示例：浅克隆到临时目录）
git clone --depth 1 https://github.com/GoogleChrome/modern-web-guidance.git /tmp/mwg-upstream

# 2) 用新版 guides/ 覆盖本地（保持英文原文）
rm -rf resources/guides
cp -r /tmp/mwg-upstream/skills/modern-web-guidance/guides resources/guides

# 3) 重建索引并核对计数
python3 resources/tools/build_index.py
python3 resources/tools/mwg.py categories

# 4) 抽样验证
python3 resources/tools/mwg.py search "light dismiss dialog"
```

随后更新 [ATTRIBUTION.md](ATTRIBUTION.md) 顶部的 commit 与版本号，并评估上游
`SKILL.md` 工作流是否有变化需要同步本技能。若决定翻译/改写指南，**必须**在 ATTRIBUTION.md
声明「已修改」。

> 详细操作与验收清单见 [resources/specifications/local_search_contract.md 第 8–9 节](resources/specifications/local_search_contract.md)。

## 与本仓库其它技能叠加

本技能不生成工程。下列技能在写到浏览器界面时会先检索本技能，它们自己的目录、分层和组件库保持不变：

- `prototype-to-web(Nuxt UI Starter)`、`requirements-to-vue_vben_admin`：映射到各自的 UI 组件
- `common-website-design`、`prd-html-skill`、`md-prd-to-html-prototype`：直接落进 HTML
- `prototype-to-taro-app`、`prototype-to-app-uniappx`：仅 H5
- `dsh-plugin-starter`：仅 dual-face 设置页

后端脚手架和 Flutter / iOS / Android 技能不叠加。说明见 [docs/使用modern-web-guidance技能编写现代Web前端指南.md](../.docs/使用modern-web-guidance技能编写现代Web前端指南.md)。
