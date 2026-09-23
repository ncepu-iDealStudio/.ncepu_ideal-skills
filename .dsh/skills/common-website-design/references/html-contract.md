# Core HTML Contract（HTML 硬性契约）

每个生成的页面必须同时满足：第一层标准 Web 语义（硬性）+ 第二层机器注释（可删除）。**删除全部 data-* 后，页面必须仍是一份完全正常、语义正确的 HTML。**

## 第一层 · 标准 Web 语义

### 文档骨架（每页必须）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>页面标题 - 站点名</title>
  <meta name="description" content="…">
</head>
```

### 结构标签

- 用 `header / nav / main / section / article / aside / footer` 表达结构，禁止 div 海洋
- `<main>` 每页恰一个；`<nav>` 必须带 `aria-label` 区分用途（主导航/面包屑/页脚导航）
- section 用 `aria-labelledby` 关联自己的标题 id

### Heading 层级

- 每页**恰一个 `<h1>`**（页面主题）
- h2/h3 表达**内容层级**而非字号；禁止跳级（h1→h3）
- 视觉大小交给 CSS，禁止为了字号选错级别

**四个必然踩到的跳级陷阱**（每次都是同一批位置，落笔前先安排好层级）：

| 位置 | 错误写法 | 正确写法 |
|---|---|---|
| 页脚栏目 | 直接 `<h4>产品</h4>`（前面最高只到 h2/h1 → 跳级） | 页脚先放 `<h2 class="sr-only">站点导航</h2>`，栏目标题用 `<h3>` |
| 卡片网格 | 页面 h1 之后直接是卡片的 `<h3>` | 网格前补 `<h2 class="sr-only">产品清单</h2>`，或给网格一个真实的 h2 小节标题 |
| `<dialog>` 标题 | `<h3 id="dlg-title">` 挂在只到 h1 的页面上 | 用 `<h2>`（dialog 是独立上下文，按所处文档的层级继续） |
| `<table>` 表头 | 用 `<th>` 冒充标题 | `th` 不是 heading，不参与层级；表说明放 `<caption>` |

> `h2 class="sr-only"` 是给读屏软件的大纲，视觉上隐藏。它解决的是"这一屏需要一个标题层级但我不需要它显示出来"——比把卡片标题降级或加边框更省事，也不破坏版式。

### Heading 层级之外：`<body>` 与容器闭合

模板拼接时最容易漏掉 `<body>` 开标签——浏览器会容错补回来，肉眼几乎看不出，但删掉 data-* 交给下游拆解时就是一份不合法的 HTML。`scripts/validate.py` 现在会检查 `<body>` 存在与结构性容器（div/section/article/header/footer/main/nav/ul/ol/dl/form/details/figure/blockquote/table/dialog）是否闭合。

### ARIA 原则：Native first

- 原生标签已表达的语义**禁止**再堆 ARIA：`<main>` 不加 `role="main"`，`<nav>` 不加 `role="navigation"`
- 仅在原生不足时使用：`aria-label`（区分同名导航）、`aria-current="page"`（当前页高亮）、`aria-expanded / aria-controls`（展开控件）、`aria-hidden="true"`（装饰图形）
- 图标一律 `aria-hidden` 或提供替代文本；不得用 unicode 字符（▣ ◊）冒充图标

### SEO 与内容语义

- `time datetime="2026-09-18"` 包裹日期；`img` 必有 alt 与 width/height
- 图片说明用 `figure + figcaption`；引用用 `blockquote + cite`
- 文章 detail 页加 Article JSON-LD；有面包屑时加 BreadcrumbList JSON-LD

## 第二层 · 机器注释（data-*）

三个属性，命名一律小写连字符 + 点号字段：

| 属性 | 含义 | 示例 |
|------|------|------|
| `data-component` | 可抽成组件/partial 的结构 | `data-component="post-card"` |
| `data-collection` | 重复内容的集合（循环区域） | `data-collection="posts"` |
| `data-slot` | 动态内容字段 | `data-slot="post.title"` |

```html
<section class="latest" data-component="post-list" data-collection="posts">
  <article data-component="post-card">
    <a href="article.html" data-slot="post.url">
      <h2 data-slot="post.title">多模态模型推理成本下降 40%</h2>
    </a>
    <p data-slot="post.summary">…</p>
    <time datetime="2026-09-18" data-slot="post.date">2026年9月18日</time>
  </article>
  <!-- 同结构卡片重复 ≥ 3 次以体现循环 -->
</section>
```

规则：

- `data-slot` 前缀是**模型名（单数，如 post）**，`data-collection` 是**集合名（复数，如 posts）**；manifest 的 collections 字段清单按 slot 的字段部分（点号后）比对
- site-header / site-footer 也标注 `data-component`
- manifest 的 `components` / `collections` 必须与页面中实际出现的 data-* 一致
- 集合区域至少渲染 3 条同构样例，让循环结构可辨认

## 交互模块：原生优先

**有原生模块的一律用原生标签，不要用 JS 重造：**

| 功能 | 原生实现 |
|------|---------|
| 模态/弹窗 | `<dialog>` + `showModal()` |
| 折叠/手风琴 | `<details>` + `<summary>` |
| 进度/度量 | `<progress>` / `<meter>` |
| 表单校验 | `required` / `pattern` / `type=email|tel|url` + `:invalid` 样式 |
| 下拉菜单 | `<select>`（简单场景）或 `<details>` |
| 搜索框 | `<search>` + `<input type="search">` |
| 图片画廊切换 | `<input type="radio">` hack 或 CSS scroll-snap |

原生确实无法实现（轮播、复杂 tab 联动）才写 JS：

1. 自写轻量实现优先；确需引库则选轻量库，允许 CDN 外联（登记进 manifest 的 `external.cdn`）
2. **每个交互功能必须在 manifest 的 `modules` 中注明实现方式**：`{ "feature": "移动菜单", "implementation": "details/summary + CSS" }`——让后续 Agent 能用目标框架的等价原生模块（如 Vue 的 Teleport、Hugo 的 partial）替换
3. JS 文件放 `template/js/main.js`，写清注释分块

## 资产策略（离线优先）

- CSS / 图片 / 字体：一律本地化到 `template/css|image|`；不引用远程占位图服务
- 字体优先系统字体栈；需要特色字体时下载 woff2 放本地，禁止直接 `@import` 远程字体
- JS 库可 CDN 外联，但须登记；核心浏览体验不得依赖 JS（渐进增强）
