# common-website-design

把自然语言描述的网站需求，转成一套**框架无关的静态 HTML 设计原型**。

产出终点是**设计中间层**：可直接用浏览器打开浏览，也带有足够的语义与机器注释，供后续拆成 Vue / Hugo / Hexo / EJS 等具体框架模板。本 skill 自身不生成任何框架项目代码。

## 它产出什么

一个站点目录，固定两大部分：

```
<站点名>/
├── doc/
│   ├── README.md            ← 设计综述与进度，也是上下文重置后的恢复入口
│   └── design/<pack-id>.md  ← 本次采用的设计包副本（含定制记录）
└── template/
    ├── *.html               ← 各页面
    ├── css/  js/  image/    ← 全部本地化，断网可浏览
    └── site-manifest.json   ← 页面、组件、集合、模块、外部依赖的结构登记
```

页面是双层语义：标准 HTML 语义标签（`header / nav / main / section / article / aside / footer`、每页恰一个 h1、ARIA 原生优先、SEO 基线）之上，叠加一层可删除的 `data-component / data-collection / data-slot` 机器注释。**删掉全部 data-* 后，仍然是一份完全正常的语义 HTML。**

## 三个正交维度

| 维度 | 决定什么 | 内容 |
|---|---|---|
| Page Archetype | 页面怎么组织 | 8 种原型：home / list / detail / landing / about / contact / search / error |
| Content Model | 页面装什么 | 预置 article / product / person / notice，其余按需求现建字段 |
| Design Pack | 页面长什么样 | 9 个内置包，采用候选确认制 |

三者独立组合。领域词不等于风格——“电池/能源/制造”是内容不是视觉，企业对外官网的候选应从 corporate-clean / tech-aurora / flat-material 中给。

### 内置设计包

| id | 名称 | 适用 |
|---|---|---|
| corporate-clean | 企业净白 | 传统企业、机构、学校官网 |
| flat-material | 扁平质感 | SaaS / App / 工具产品官网 |
| tech-aurora | 极光科技 | AI / SaaS / 科技公司发布页 |
| commerce-rich | 电商丰富 | 商城、旗舰店、促销专题 |
| editorial | 报纸编辑 | 新闻、资讯、学术媒体 |
| swiss-minimal | 瑞士极简 | 作品集、实验室、文档站 |
| industrial-dark | 工业暗色 | 控制台、仪表盘、开发者工具（不用于对外官网） |
| glassmorphism | 毛玻璃 | 个人作品集、创意页（强风格，慎用） |
| retro-futuristic | 复古未来 | 机器人、实验室、前沿科技（强风格，慎用） |

色彩偏好是设计包之上的**覆盖层**，不是第四个维度：每份设计包都声明了可变色位与锁定色位，学生要求触碰锁定色位时不是改包，而是重新选包。

## 目录结构

```
common-website-design/
├── SKILL.md            ← 工作流与路由（生成站点时以此为准）
├── PLAN.md             ← V1 设计规格书（开发依据，非操作指南）
├── README.md           ← 本文件
├── designs/            ← 9 个设计包，每份含 source / license / attribution
├── references/         ← 9 份契约文档
├── assets/             ← style-tile.html（样式确认页模板）
└── scripts/validate.py ← 输出验证器（Python 标准库，零依赖）
```

### references/ 契约文档

| 文件 | 内容 |
|---|---|
| intake-questions.md | 需求采集清单：6 项必问、含糊词追问表、视觉证据与色彩候选怎么给、确认回执模板 |
| page-archetypes.md | 8 种页面原型的必备区块与结构要求 |
| content-models.md | 预置内容模型与按需建模规则 |
| design-pack-schema.md | 设计包 YAML 契约、选择流程、色彩覆盖与选型误区 |
| palettes.md | 三色配色库（通用 6 系 11 套 + 自定配色区） |
| html-contract.md | 语义 HTML / ARIA / SEO / data-* / 原生模块清单 |
| output-contract.md | 落盘目录、manifest schema、资产策略 |
| motion.md | 6 种可复用动效模式（独立于设计包） |
| design-quality.md | 设计质量与反 AI 味纪律 |

## 几条贯穿全程的纪律

- **禁止凭空选**：任何要学生做的视觉取舍，先给看得见的证据——打开设计包画廊、候选预览页或样式确认页。只用形容词要求他做决定，等于让他猜
- **含糊词不许猜**：听到"要效果""要有设计感"，先追问**位置 · 目的 · 参照 · 强度**，以及"不能接受什么"，不要自行补全
- **默认值要摊开**：学生没答的项可以替他定，但必须标出哪些是默认的，并与"学生亲口定的"分列在 README 里
- **设计包只换衣服不改骨架**：视觉服从设计包，结构与无障碍服从 HTML 契约，冲突时以后者为准
- **交互原生优先**：`<dialog>`、`<details>/<summary>`、`<progress>`、原生表单校验；原生做不到才写轻量 JS，且必须在 manifest 的 `modules` 里登记实现方式
- **离线可用**：CSS、图片、字体全部本地化；只有已登记的 CDN JS 允许外联
- **诚实标注**：样例数据、外部依赖、模块实现方式都在 manifest 中如实登记，不把演示内容伪装成真实数据；资质/证书类内容不得伪造真实机构
- **防 AI 味**：禁止 Inter 一把梭、紫蓝渐变、卡片套卡片、伪造遥测面板、`//` 注释式 kicker 等八类高频特征；生成前需先写一段可判定的设计陈述（position / focus / device / banned），验证时逐条对照

## 验证

```
python scripts/validate.py <输出根目录>/template
```

纯标准库实现，检查 DOCTYPE / lang / title / viewport / description、每页恰一个 h1 与 heading 不跳级、重复 id、img alt、内部链接与本地资源是否存在、data-* 命名与 manifest 双向吻合、远程引用是否已登记。零错误视为通过。

## 设计包来源与许可

`designs/` 中 tech-aurora、swiss-minimal、industrial-dark、retro-futuristic 改编自 [Ilm-Alan/frontend-design](https://github.com/Ilm-Alan/frontend-design)（MIT）；其余五个为自研。每份设计包文件内均记录 `source` / `license` / `attribution` 与本地改动说明。仓库中不 vendor 任何大型第三方设计库。

## 成品示例

`../../../test/page-design-showcase/` 是本 skill 的产出示例，含设计包画廊与四个端到端生成的站点。
