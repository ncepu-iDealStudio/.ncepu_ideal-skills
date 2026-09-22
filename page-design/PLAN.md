# 页面生成 Skill（page-design）V1 设计规格书

> **给正在执行站点生成任务的 Agent：本文档是开发规格书，不是操作指南。生成站点请直接遵循 `.workbuddy/skills/page-design/SKILL.md` 的工作流，无需阅读本文档。**

> 版本：V1.0 草案（2026-09-18）
> 状态：架构冻结，七个关键问题已全部拍板，本文档为实现依据
> 目标读者：实现本 Skill 的 Agent / 开发者，以及课程老师

---

## 第 1 章 项目综述

### 1.1 背景与定位

学生能够用自然语言描述想要的网站（"一个深色科技风的 AI 资讯站，要首页、文章页、分类页"），但不理解 Vue component / Hugo template / Hexo layout / EJS partial 这些框架概念。

因此本 Skill **不生成任何具体框架的项目**，而是生成一套：

> **框架无关、可直接浏览、结构清晰、可被机器拆解的静态网站设计原型（HTML 设计中间层）。**

流水线位置：

```
学生自然语言需求
      ↓
  page-design Skill          ← 本项目
      ↓
框架无关 HTML 原型
      ↓
学生 / 后续 Agent 拆解
      ↓
Vue / Hugo / Hexo / EJS / ...
```

### 1.2 核心设计哲学：三个正交维度

```
Page Archetype   决定"页面怎么组织"
Content Model    决定"页面装什么内容"
Design Pack      决定"页面长什么样"
```

三者独立组合，统一落入 **Core HTML Contract** 生成 HTML。
"科技""工业"等是**内容属性**而非设计属性：科技站可以做报纸 Editorial 风，工业站可以做 Neo-Brutalist 风。

**Design Pack 只换衣服，不改骨架**：设计包只控制视觉（字体、颜色、间距、边框、阴影、密度、布局倾向、动效），不允许触碰 HTML 语义结构、ARIA 规则、SEO 规则、data-* 标注。

### 1.3 为什么用 HTML 作为中间表示

同一份产出同时服务四个对象：

| 对象 | 得到什么 |
|------|---------|
| 人类 | 直接打开浏览器即可浏览的完整原型 |
| 学生 | 语义化 HTML / CSS / 无障碍 / SEO 的教学范例 |
| 浏览器 / 搜索引擎 | 可解析的结构化页面 |
| 后续 Agent | 语义标签 + data-* 注释 + site-manifest，无需猜结构即可拆解 |

关键性质：**即使删掉全部 data-* 注释，产出依然是一份完全正常、语义正确的 HTML。**

---

## 第 2 章 V1 目标与职责边界

### 2.1 V1 做什么

- 接收自然语言网站需求，解析为标准化 Requirement Model
- 规划页面清单（可向学生补充建议，须经确认）
- 选择设计包（未指定时提供候选让学生选）
- 将需求与设计决策**落盘为文档**（支持上下文重置后恢复）
- 生成多个静态语义化 HTML 页面 + 统一 CSS + 轻量 JS
- 交互优先使用 HTML 原生模块（`<dialog>`、`<details>` 等）
- 生成站点结构描述 site-manifest.json
- 运行脚本化验证并修复问题

### 2.2 V1 明确不做什么

- × 不生成 Vue / Hugo / Hexo / EJS 项目或模板
- × 不做后端、数据库、CMS、业务 API
- × 不做浏览器渲染级验证（V1.1，接口预留）
- × 不内置大型设计数据库（外部库仅作参考来源，不 vendor）

---

## 第 3 章 总体架构与执行流程

```
学生自然语言需求
      ↓
Requirement Analysis（需求解析）
      ↓
Requirement Model（落盘 site/doc/README.md）
      ↓
┌─────────────┬─────────────┬─────────────┐
│ Page        │ Content     │ Design      │
│ Archetype   │ Model       │ Pack        │
│ 8 种页面原型 │ 预置+按需建模 │ 候选确认制   │
└─────────────┴─────────────┴─────────────┘
      ↓
Page Generator（按 Core HTML Contract 逐页生成）
      ↓
输出包（site/template/ 下 HTML/CSS/JS + site-manifest.json）
      ↓
Validator（scripts/validate.py 确定性检查）
      ↓
框架无关设计原型（设计中间层交付物）
```

**LLM 与脚本的分工**：LLM 负责设计、布局、语义、信息架构；脚本负责结构、链接、资源、契约一致性等确定性检查。不允许"我自己仔细检查过了"式的口头验证。

---

## 第 4 章 Requirement Model

### 4.1 输入

不要求结构化输入，接受自然语言。Agent 从中解析出四个部分：

```json
{
  "site":  { "name": "", "language": "zh-CN", "purpose": "", "audience": "" },
  "pages": [ { "type": "home", "notes": "头条+最新文章" } ],
  "content": { "domain": "technology-news", "models": ["article"] },
  "design": { "explicit": "深色科技风", "pack": "tech-aurora" }
}
```

### 4.2 规则

- 页面清单允许 Agent 补充建议（如学生只说"新闻网站"，建议补 `list + detail`），但必须**列出完整清单让学生确认后**才开始生成
- 解析结果必须写入 `site/doc/README.md`（见第 9 章），这是上下文恢复的唯一入口

---

## 第 5 章 Page Archetype（已确认：8 种）

| 原型 | 文件名约定 | 说明 |
|------|-----------|------|
| home | index.html | 首页：信息密度最高的组合页 |
| list | list.html / category.html | 列表/分类/归档页 |
| detail | article.html / product.html | 内容详情页（文章/产品/人物……） |
| landing | landing.html | 专题/落地页 |
| about | about.html | 关于页 |
| contact | contact.html | 联系页（含表单） |
| search | search.html | 搜索结果页 |
| error | 404.html | 错误页 |

- 原型是**信息布局模式**，不是内容：新闻详情 = detail + article 内容模型；教师介绍 = detail + person
- 具体文件名可按需求调整，但每页必须在 site-manifest.json 中登记 type
- 详细结构见 `skill/references/page-archetypes.md`

---

## 第 6 章 Content Model

### 6.1 预置内容模型（V1 少量预置）

- **article**：title, summary, author, publishedAt, cover, body, category, tags
- **product**：name, model, summary, image, specifications, certifications
- **person**：name, title, avatar, bio, affiliation, links
- **notice**：title, publisher, publishedAt, category, body

预置之外，Agent 按需求即时建立字段模型（如论文 paper：title, authors, venue, year, abstract, doi），并记录进 site-manifest.json 的 collections。

### 6.2 样例数据（已确认：真实感假数据是必要的）

- 生成真实感较强的样例内容用于展示（假标题、假摘要、假日期要像真的）
- 所有样例数据在 site-manifest.json 中标记 `"contentSample": {"generated": true}`
- 目的：原型演示效果 + 后续拆解时有真实结构可参照

---

## 第 7 章 Design Pack

### 7.1 设计包契约

每个设计包是 `designs/` 下一个独立 Markdown 文件，内含 YAML 规范（id、来源与许可证、identity、colors、typography、geometry、layout、effects、motion、rules）。完整 schema 见 `references/design-pack-schema.md`。

**硬性边界**：设计包只管视觉，禁止规定 HTML 结构、ARIA、SEO、data-*。

### 7.2 选择机制（已确认：候选确认制）

1. 学生明确指定 → 直接采用
2. 未指定 → Agent 依据内容领域与用途从 `designs/` 挑 **2–3 个候选**，向学生展示（id、名称、定位一句话、关键视觉特征），**并且必须同时给出该候选的实际渲染效果**，学生看过之后再选定
3. 学生表示无偏好 → Agent 推荐一个并说明理由，经学生确认
4. 色彩候选禁止只给等大色卡：须按 60/30/10 的实际面积比例呈现，或展示该配色的实际渲染页面

> **V1.1 修订（2026-09-22）**：原第 2 条只要求展示"id / 名称 / 一句话定位 / 关键视觉特征"，即**纯文字描述**。实测暴露的问题：学生对"SaaS 扁平""控制台审美"没有画面，被要求为一个看不见的东西负责，结果只能靠猜；做完才发现颜色与气质不对，返工成本落在生成之后。现改为**强制可视化候选**——优先打开设计包画廊（同一内容 × 9 种视觉的对照），画廊不可用时逐个打开候选预览页，两条路都不通时必须先声明"我现在没法给你看图"再退化为具象特征描述。配套新增 `references/intake-questions.md`（需求采集与追问清单）与 `assets/style-tile.html`（样式确认页模板，多页站点动手前先确认方向）。

选定后**复制**该设计包到 `site/doc/design/<pack-id>.md`（若学生有定制，在副本上修改）。

### 7.3 V1 内置 9 个设计包

| id | 名称 | 覆盖方向 | 来源 |
|----|------|---------|------|
| corporate-clean | 企业净白 | 传统企业/机构/学校官网 | 自研 |
| flat-material | 扁平质感 | SaaS/App/工具产品官网（Material/Apple 扁平） | 自研 |
| tech-aurora | 极光科技 | AI/SaaS/成熟科技公司 | 改编自 Ilm-Alan Aurora Maximalism (MIT) |
| commerce-rich | 电商丰富 | 商城/旗舰店/促销专题（大图高密度） | 自研 |
| editorial | 报纸编辑 | 新闻/资讯/学术媒体 | 自研 |
| swiss-minimal | 瑞士极简 | 作品集/实验室/文档站 | 改编自 Ilm-Alan Swiss (MIT) |
| industrial-dark | 工业暗色 | 控制台/仪表盘/开发者工具（⚠ 非对外官网） | 改编自 Ilm-Alan Industrial (MIT) |
| glassmorphism | 毛玻璃 | 个人作品集/创意页（强风格慎用） | 自研 |
| retro-futuristic | 复古未来 | 机器人/实验室/前沿科技（强风格慎用） | 改编自 Ilm-Alan Retro-Futuristic (MIT) |

**动效独立于设计包**：`references/motion.md` 提供 6 种可复用动效模式（fade-up-reveal 滚动淡入、stagger-reveal、hover-lift、scroll-snap-deck、accordion、parallax），生成时按需求挑 1–2 种组合，继承设计包 duration/easing，并登记 manifest.modules。设计包自身只保留 duration/easing 气质参数。

### 7.4 外部设计库策略（已定：不 vendor 大库）

- **Ilm-Alan/frontend-design**（MIT，仅 3 文件）：作为 V1 设计包的主要改编来源，逐包记录 source/license/attribution
- **UI/UX Pro Max**：**不 vendor**。体量过大（超过 200 文件上限、含 CLI/npm 发布/semantic-release），且存在许可证声明不一致 issue 与 Basic/Premium 商业分层。仅借鉴其数据组织思路，留作 V2 扩展的候选数据源（待许可证澄清）
- **Impeccable**（Apache-2.0）：不 vendor；其反 AI 味设计纪律被提炼为本 Skill 自研的 `references/design-quality.md`；其 CLI（`npx impeccable detect`，61 条确定性规则）可作为 V1.1 渲染级验证的候选工具
- **tiny521 预览库**：不需要（后续 Agent 具备视觉能力，可自行渲染检查）

### 7.5 可追溯性

每个设计包文件必须记录：`id / version / source / license / attribution`。更新外部来源时按版本对照，避免不知道生成结果依据哪一版。

---

## 第 8 章 Core HTML Contract

### 8.1 双层语义

**第一层 · 标准 Web 语义（硬性契约）**

- 结构标签：`header / nav / main / section / article / aside / footer`，禁止 div 海洋
- heading 层级表达内容层级（每页恰好一个 h1，不跳级）
- ARIA 原则：**Native HTML semantics first**。禁止 `role="main"` 之类冗余标注；仅在原生语义不足时使用 `aria-label / aria-current / aria-expanded / aria-controls`
- SEO 基线：`lang`、`charset`、`viewport`、`title`、`meta description`、`img alt`、`time datetime`；文章页可加 JSON-LD（Article / BreadcrumbList）

**第二层 · 机器注释（可删除）**

```html
<article data-component="post-card">
  <a href="article.html" data-slot="post.url">
    <h2 data-slot="post.title">…</h2>
  </a>
  <p data-slot="post.summary">…</p>
  <time datetime="2026-09-18" data-slot="post.date">2026年9月18日</time>
</article>
```

- `data-component`：可被抽成组件/partial 的结构
- `data-collection`：重复内容的数据集合（循环区域）
- `data-slot`：动态内容字段

### 8.2 交互模块：原生优先（已确认）

1. **有原生模块的一律用原生标签**：`<dialog>`（弹窗/模态）、`<details>/<summary>`（折叠/手风琴）、`<progress>/<meter>`、原生 `<form>` 校验（required/pattern）等
2. 原生确实无法实现（如轮播、复杂 tab）才引入轻量 JS，**自写实现优先于引库**，引库必须选择轻量、可 CDN 引入的库
3. **每个交互功能必须注明实现方式**（写进 site-manifest.json 的 `modules` 字段），方便其他 Agent 用其目标框架的等价模块替换

### 8.3 资产策略（已确认：离线优先）

- CSS、图片、字体：**一律本地化**，放在 `site/template/css|image|` 下；字体优先系统字体栈，需要特色字体时下载 woff2 到本地
- JS 库：**允许 CDN 外联引入**（需网络可用），但必须在 site-manifest.json 的 `external` 中登记 URL
- 图片占位：本地生成的纯色/SVG 图形，不依赖远程占位图服务
- 目标：断网状态下双击 HTML 仍可完整浏览（除已登记的 CDN JS）

---

## 第 9 章 输出结构与 Validation

### 9.1 落盘结构（已确认：设计落盘、可恢复）

```
site/                        ← 固定输出根目录（学生可另指定，须记录）
├── doc/
│   ├── README.md            ← 最终设计综述（唯一恢复入口，见 9.2）
│   └── design/
│       └── <pack-id>.md     ← 采用的设计包副本（含学生定制）
└── template/
    ├── index.html
    ├── article.html
    ├── …（其余页面）
    ├── css/                 ← base.css / components.css / pages.css
    ├── js/                  ← main.js（仅原生不足时）
    ├── image/
    └── site-manifest.json
```

### 9.2 site/doc/README.md（设计综述，状态恢复入口）

必须包含：需求原文摘要、Requirement Model（页面清单+内容模型+设计选择及理由）、进度状态（哪些页已生成/待生成）、后续 Agent 拆解提示。**SKILL.md 中写明：每次激活先读本文件，存在则恢复上下文续作，不存在则走全新流程。**

### 9.3 site-manifest.json

```json
{
  "site": { "name": "", "language": "zh-CN", "designPack": "tech-aurora", "generatedAt": "" },
  "outputRoot": "site/",
  "pages": [ { "file": "index.html", "type": "home", "title": "" } ],
  "components": ["site-header", "post-card"],
  "collections": { "posts": { "fields": ["title", "summary", "url", "date"], "sample": true } },
  "contentSample": { "generated": true, "note": "所有内容为演示用样例数据" },
  "modules": [ { "feature": "移动菜单", "implementation": "details/summary + CSS" } ],
  "external": { "cdn": [] }
}
```

### 9.4 Validator（scripts/validate.py，Python 标准库）

检查项：index.html 与 manifest 存在；HTML 可解析；lang/title/viewport/description 齐全；每页恰一个 h1 且不跳级；无重复 ID；内部链接与本地资源路径有效；data-* 命名合法；manifest 的 pages/components/collections 与实际文件互相吻合；CDN 引用已登记。输出问题清单，非零退出码表示有错误。

V1.1 预留：浏览器渲染级验证（桌面/移动截图、横向溢出、遮挡），候选工具 Impeccable CLI 或 Playwright。

---

## 第 10 章 V1 实施路线与验收标准

### 10.1 实施顺序（契约先行）

| 阶段 | 内容 | 状态 |
|------|------|------|
| Phase 1 | 六个契约文档（本 PLAN 第 4–9 章对应 references/ 全部文件） | ✅ 本轮完成 |
| Phase 2 | SKILL.md 工作流 + designs/ 6 个设计包 | ✅ 本轮完成 |
| Phase 3 | scripts/validate.py | ✅ 本轮完成 |
| Phase 4 | 端到端测试：用 2–3 个真实学生需求跑通全流程 | ⬜ 下一步 |
| Phase 5 | 迭代设计包、补充内容模型 | ⬜ |
| Phase 6 | V1.1 渲染级验证 + 框架拆解 adapter（独立 Skill） | ⬜ |

### 10.2 验收标准

1. 输入一句自然语言需求，产出 `site/doc/` + `site/template/` 完整结构
2. 所有页面浏览器直接打开可正常浏览，断网可用（除登记 CDN）
3. validate.py 零错误通过
4. 删除全部 data-* 后页面仍是合法语义 HTML
5. 上下文重置后仅凭 site/doc/README.md 可恢复继续工作
6. 每个交互功能在 manifest 的 modules 中有实现方式标注

### 10.3 Skill 安装位置

项目级：`.workbuddy/skills/page-design/`（随本项目分发，与老师 MIT 开源库合并时保持同等许可证纪律）。
