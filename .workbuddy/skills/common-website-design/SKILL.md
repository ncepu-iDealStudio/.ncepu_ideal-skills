---
name: common-website-design
description: 根据自然语言需求生成框架无关的语义化静态网站设计原型（多页面 HTML + 统一样式 + site-manifest.json）。当用户要求设计网站、博客、企业官网、落地页、资讯/门户/作品集页面原型，或需要一套可后续拆解为 Vue/Hugo/Hexo/EJS 模板的通用 HTML 页面时，使用本技能。不生成任何具体框架的项目代码。
---

# Common Website Design（通用网站设计原型生成）

## 目标与边界

将自然语言网站需求转换为一套**框架无关、可直接浏览、可机器拆解**的静态 HTML 设计原型。产出终点是设计中间层；转换为 Vue/Hugo/Hexo/EJS 属于后续其他 Agent 的职责，本技能不做。

三个正交维度决定产出：

- **Page Archetype**（页面怎么组织）— 8 种原型，见 `references/page-archetypes.md`
- **Content Model**（页面装什么）— 预置 4 种 + 按需建模，见 `references/content-models.md`
- **Design Pack**(页面长什么样) — 候选确认制，见 `references/design-pack-schema.md` 与 `designs/`

## 第零步：状态恢复（每次必须先做）

生成任何内容之前，先检查工作区是否已有进行中的站点：

1. 读取 `<工作区>/site/doc/README.md`（若学生指定过其他输出目录，以 README 中记录的 `outputRoot` 为准）
2. 若存在：按其中记录的需求模型、页面清单、设计选择与进度状态**继续未完成的工作**，不要重新提问
3. 若不存在：走下方全新流程

## 工作流（全新站点）

### 第 1 步：需求采集（一次性问全）

先解析出 Requirement Model：

```
site:     名称 / 语言（默认 zh-CN）/ 用途 / 受众
pages:    页面清单（type + 备注）
content:  内容领域 + 涉及的内容模型
design:   明确的视觉要求（若有）
```

**但这解析完不能直接动手。** 学生给的自然语言里，"要有设计感""要有效果"这类句子不是需求而是情绪，照着做等于双方各猜一半。动工前必须补齐下面两组问题，详细清单见 `references/intake-questions.md`。

**必问 6 项**（照 let meitu pitching 一次发完，不允许逐轮追问）：

| 问什么 | 不答怎么办 |
|---|---|
| 站名 / 一句话用途 / 主要给谁看 | 从需求推断，回执标注 |
| **页面清单**（列出你的建议让他增删） | 用建议版作默认；skill 硬性要求清单确认后才动手 |
| 底色偏好：**白底 / 浅色 / 深色** | 默认白底（这一条能砍掉一半设计包，性价比最高） |
| 品牌主色，或**明确不要的颜色** | 用包默认色（颜色是头号返工项） |
| **有没有参考**：见过的站 / PV / 截图 / 竞品 | 有参照时几乎不会返工；无参照则第 2 步的可视化候选不可跳过 |
| 内容**你提供**还是**我用占位样例**；资质/数据/证书用真还是假 | 一律用明显虚构的占位样例并标注，**绝不伪造真实机构** |

**听到这些词必须停下来追问**（不听 Szent：学生在索要某个你还没见过的东西）：

- **效果 / 动效 / 炫酷 / 高级感 / 有冲击力** → 追四件：**在哪里** + **起什么作用** + **有没有参照** + **强度（点缀 ←→ 满屏都动）**，外加"不能接受什么"
- **独特 / 有设计感 / 特别 / 别太普通** → 追四件：**哪个部分** + **想传达什么** + **参照** + **绝对不能接受什么**
- **简洁 / 干净** → 是**信息少**还是**视觉干净**？两者做法完全不同
- **高大上 / 像大厂** → 具体哪个公司；"廉价感"在他心里具体是什么

> **优先问"不能接受什么"。** 学生往往说不清想要什么，但能立刻说出讨厌什么——负面清单比正面描述可靠得多。

完整追问话术与判断表见 `references/intake-questions.md`。

允许根据需求**补充建议页面**（如学生只说"新闻网站"，建议补 list/detail/about）。完整页面清单必须列给学生**确认后**才继续。

### 第 2 步：设计包与配色选择（可视化候选）

> **硬性规则：每个候选都必须附"看得见的证据"。只甩一段文字描述让学生凭空想象 = 违规。**
> 这是整套流程里最容易偷懒、也最容易导致返工的一环：学生对"SaaS 扁平"没有画面，我们却在要他为这个画面负责。

执行：

1. 学生明确指定风格 → 直接匹配 `designs/` 中的包
2. 未指定 → 根据内容领域与用途挑选 **2–3 个候选**（给 9 个让人选等于没选）
3. **展示证据**，按此优先级：
   - **打开画廊**：用 Glob 找 `**/gallery/index.html`（本仓库为 `/test/page-design-showcase/gallery/index.html`）。它是**同一套内容 × 9 种视觉**的对照，最适合比选；让学生看完直接报号
   - **画廊不存在**：逐个打开候选包的预览文件（文件名稳定，见下表"预览文件"列，Glob 定位）
   - **两条路都不通**：**必须先告诉学生"我现在没法给你看图"**，并把每个候选写成可识别的**具象特征**——写"深蓝实底 banner + 三栏产能数字"，不许写"稳重大气"
4. 学生表示无偏好 → 推荐一个并说明理由，经确认后采用
5. **同时捕获色彩偏好**（若有）。色彩候选同样禁止甩三个等大色块——**观感由面积决定**：必须按 60/30/10 的实际比例摆开标明角色，或展示该配色的实际渲染页面。取值从 `references/palettes.md`（自定配色区优先）；若要求触碰该包锁定色位（如 industrial-dark 要白底），说明包选错了，回到候选重选

内置设计包一览（**预览文件名稳定，跨仓库可用 Glob 定位**）：

| id | 名称 | 一句话定位 | 预览文件 |
|----|------|-----------|---------|
| corporate-clean | 企业净白 | 传统企业/机构官网，白底稳重专业（企业对外官网首选候选） | `corporate-clean.html` |
| flat-material | 扁平质感 | Material/Apple 式扁平，阴影分层非边框，SaaS/App/工具产品官网 | `flat-material.html` |
| tech-aurora | 极光科技 | 深色渐变大标题霓虹，当代 AI/SaaS 官网气质 | `tech-aurora.html` |
| commerce-rich | 电商丰富 | 促销色+大图商品网格+角标，商城/旗舰店/促销专题 | `commerce-rich.html` |
| editorial | 报纸编辑 | 衬线大标题分栏排版，新闻/资讯/学术媒体 | `editorial.html` |
| swiss-minimal | 瑞士极简 | 纯白网格单强调色，作品集/实验室/文档站 | `swiss-minimal.html` |
| industrial-dark | 工业暗色 | 黑底等宽字体单信号色的**控制台审美**；仅用于工程系统/开发者向页面，不用于对外企业官网 | `industrial-dark.html` |
| glassmorphism | 毛玻璃 | 彩色底上半透明磨砂浮层，个人作品集/创意页（强风格，慎用） | `glassmorphism.html` |
| retro-futuristic | 复古未来 | 黑底霓虹 CRT 扫描线，机器人/实验室/前沿科技（强风格，慎用） | `retro-futuristic.html` |

> **选型警告**：领域词 ≠ 风格。"电池/能源/制造"是内容不是视觉——企业对外官网从 corporate-clean / tech-aurora / flat-material 中给候选；industrial-dark、retro-futuristic、glassmorphism 是强风格包，仅当学生描述明显匹配时使用。详见 `references/design-pack-schema.md` 的"常见选型误区"。

选定后**复制**该包文件到 `site/doc/design/<pack-id>.md`；学生有定制意见时在副本上修改并注明。

### 第 3 步：样式确认页（3 页以上站点必做）

防返工闸门：**先做一张单页确认方向，再去做全站。** 见 `references/intake-questions.md` 的 R1.5。

直接复制 `assets/style-tile.html` 改其中的 `:root` 令牌即可，它已按此结构准备好：三色 60/30/10 实际比例排布、真实文案的 hero、卡片/数据模块、排版层级（h1–h3 / 正文 / 链接 / 按钮）。做完给学生看，只问一件事："**这个方向对吗？**" 改这张页的成本是全站返工的几十分之一。

- **必做**：3 页及以上
- **可跳过**：1–2 页，或学生明确说"按你的判断来"；跳过要记进 README 的理由
- 被推翻时回到第 2 步重选，**不要直接改已经写好的页面**
- 这张页**不进最终交付目录**，放在 `site/doc/` 下留档即可（它是确认凭据，不是页面）

### 第 4 步：设计落盘

创建 `site/doc/README.md`（设计综述，唯一恢复入口），写入：需求原文摘要、Requirement Model、页面清单（含确认记录）、选定的设计包与理由、**`design_statement` 设计陈述（第 5 步产出）**、进度状态（逐页勾选）。**每完成一步就更新此文件。**

> **确认记录必须分清两类**：哪些是**学生亲口定的**，哪些是**你替他默认的**。上下文重置后接手的人靠这行区分："用户的决定"要认真执行，"上次的默认"可以被推翻。原文见 `references/intake-questions.md` 的确认回执模板。

### 第 5 步：设计陈述（stated direction，生成前必做）

写第一行业 HTML 之前，先用 3–5 句**把隐式的审美判断显式化**，写进 `doc/README.md` 的 `design_statement` 字段：

```
design_statement:
  position:  一句话定位 — 这站是什么气质，以及"不是什么"
  focus:     视觉主角 — 首屏第一眼落在哪（具体元素，不是"标题"这种空话）
  device:    差异化手法 — 与 AI 默认输出的区别在哪（如"用深蓝 banner + 真实产能数字背书，不用渐变卡片墙"）
  banned:    本页明确不做的事（如"不做浮动装饰球、不做等宽大写 kicker、不做假数据仪表盘"）
```

**为什么必须写**：模糊 prompt 下模型会收敛到训练分布的均值（AI 味）。陈述把"选哪个"的品味决策外置成可对照的约束：写页面时按它执行，第 10 步验证时按它逐条自检（视觉是否落在 `focus`、是否踩了 `banned`）。**没写陈述就开始排版 = 违规。**

陈述必须具体可判定（"沉稳专业"不合格，"深蓝实底 banner + 三栏产能数字，无渐变无插画"合格）。

### 第 6 步：设计令牌与站点骨架

- 依据设计包的 colors/typography/geometry/layout 确定 CSS 自定义属性（design tokens）
- 先建立所有页面共用的 site chrome：`site-header`（含 `<nav aria-label>`）、`site-footer`、面包屑（若有）

### 第 7 步：逐页生成

按 `references/page-archetypes.md` 中各原型的结构要求生成 HTML，全程遵守 `references/html-contract.md`：

- 语义标签 + 单 h1 不跳级；ARIA 仅在原生语义不足时使用
- 每页 head 必须含 lang/charset/viewport/title/meta description
- 重复内容区域加 `data-component` / `data-collection` / `data-slot` 机器注释
- 内容用**真实感样例数据**（假标题假摘要要像真的），占位图用本地 SVG/纯色图形
- CSS、图片、字体全部本地化到 `site/template/css|image|`

### 第 8 步：交互模块与动效（原生优先）

1. 有 HTML 原生模块的一律用原生：`<dialog>`（模态/弹窗）、`<details>+<summary>`（折叠/手风琴）、`<progress>/<meter>`、原生 form 校验
2. 原生无法实现才写轻量 JS（自写优先，引库须轻量且可 CDN 引入并登记）
3. **动效从 `references/motion.md` 的模式库挑选 1–2 种组合**（如企业站默认 fade-up-reveal + hover-lift），模式继承设计包的 duration/easing；首屏内容禁止 reveal；必须尊重 prefers-reduced-motion
4. 每个交互功能与动效都在 site-manifest.json 的 `modules` 中注明实现方式，例如 `{ "feature": "移动菜单", "implementation": "details/summary + CSS" }`、`{ "feature": "区块滚动淡入", "implementation": "IntersectionObserver + CSS transition（fade-up-reveal）" }`

### 第 9 步：site-manifest.json

按 `references/output-contract.md` 中的 schema 生成，登记 pages / components / collections（含字段与 sample 标记）/ modules / external CDN。

### 第 10 步：验证与修复

运行：

```
python scripts/validate.py <输出根目录>/template
```

修复所有错误后重跑至零错误。然后做两轮人工自检：

1. **对照 `design_statement`** — 视觉主角是否落在 `focus`？有没有踩 `banned`？对不上就改页面，不是改陈述
2. **对照 `references/design-quality.md`** — 反 AI 味纪律（禁止 Inter 一把梭、紫蓝渐变、卡片套卡片、彩底灰字、伪造遥测面板、`//` 代码注释式 kicker 等）

若具备视觉能力，用浏览器打开首页与详情页截图自查布局，发现溢出/遮挡即修复。

## 输出结构（固定）

```
site/
├── doc/
│   ├── README.md            ← 设计综述 + 状态恢复入口
│   └── design/<pack-id>.md  ← 采用的设计包副本
└── template/
    ├── index.html …          ← 各页面
    ├── css/                  ← base.css / components.css / pages.css
    ├── js/                   ← main.js（仅原生不足时存在）
    ├── image/
    └── site-manifest.json
```

学生可指定其他输出根目录名；指定后必须写入 site/doc/README.md 的 `outputRoot` 字段。

## 关键纪律（生成全程有效）

1. **禁止凭空选**：任何要学生做的视觉取舍，先给看得见的证据（画廊 / 预览页 / 样式确认页）。只用形容词要求他做决定，等于让他猜，返工由我方负责
2. **含糊词不许猜**：听到"要效果/要有设计感"，按第 1 步追问位置·目的·参照·强度，不要自行补全
3. **默认值要摊开**：学生没答的项你替他定可以，但必须在确认回执里标出哪些是默认的，并在 README 里与"学生亲口定的"分列
4. **设计包只换衣服不改骨架**：视觉服从设计包，HTML 结构/ARIA/SEO/data-* 服从 html-contract，两者冲突时以后者为准
5. **删除全部 data-* 后页面仍须是合法语义 HTML**
6. **离线可用**：断网双击 HTML 可完整浏览（已登记的 CDN JS 除外）
7. **诚实标注**：所有样例数据、CDN 依赖、模块实现方式都在 manifest 中如实登记；资质/证书类内容不得伪造真实机构
8. **每完成一步更新 site/doc/README.md 的进度状态**

## 资源索引

- `references/intake-questions.md` — **需求采集清单**：6 项必问、含糊词追问表、视觉证据怎么给、色彩候选怎么给、样式确认页、确认回执模板
- `references/page-archetypes.md` — 8 种页面原型的结构与必备区块
- `references/content-models.md` — 预置内容模型与按需建模规则
- `references/design-pack-schema.md` — 设计包契约（YAML schema）、选择流程、Palette Override 与常见选型误区
- `references/palettes.md` — 三色配色选项库（含自定配色区，展示时优先；自定配色名字常带出处梗，须先查母题再出页）
- `references/html-contract.md` — 语义 HTML / ARIA / SEO / data-* / 原生模块清单
- `references/output-contract.md` — 落盘目录、site-manifest schema、资产策略
- `references/motion.md` — 动效模式库（fade-up-reveal 等 6 种，独立于设计包）
- `references/design-quality.md` — 设计质量与反 AI 味纪律
- `designs/` — 9 个内置设计包
- `assets/style-tile.html` — 样式确认页模板（第 3 步用，复制后只改 `:root` 令牌）
- `scripts/validate.py` — 输出验证器
