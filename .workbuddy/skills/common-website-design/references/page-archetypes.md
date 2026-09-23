# Page Archetypes（8 种页面原型）

原型是**信息布局模式**，与内容无关。同一个 detail 原型可承载文章、产品、人物。每个原型定义必备区块与结构要求；具体区块内部内容由 Content Model 决定。

通用要求（所有页面）：完整 site chrome（`site-header` 含 `<nav aria-label="主导航">`、`site-footer`）、每页恰一个 `<h1>`、heading 不跳级。

---

## home（index.html）

信息密度最高的组合页，按需求从下列区块中选择组合（顺序可调）：

```
header
main
├── hero（站点定位/头条，h1 所在）
├── featured（焦点内容，data-collection）
├── latest / 分类入口
├── 价值介绍 / 服务概览（企业站）
└── 行动引导（订阅/联系）
footer
```

- hero 的 h1 是站点或头条标题，不得与站点名重复堆砌

## list（list.html / category.html / archive.html）

```
main
├── 页头（h1 = 列表名，如"人工智能"分类）
├── 筛选/子分类导航（nav 或 details 折叠）
└── 内容网格（≥ 6 条样例，data-collection + data-component 卡片）
```

- 卡片内链接指向对应 detail 页
- 有分页需求时渲染静态分页导航（链接可为 # 占位但须注明 sample）
- **heading 不跳级**：页头是 h1、卡片标题是 h3，中间缺 h2。处理二选一：卡片标题降级为合法层级，或在列表主体区加一个（可 `visually-hidden` 的）h2 作为集合标题。validate.py 会检出 h1→h3 跳级

## detail（article.html / product.html / person.html …）

```
main
├── 面包屑（nav aria-label="面包屑"）
├── 内容头（h1 + 元信息：作者/日期/分类，data-slot）
├── 正文（长内容；文章用 time datetime、figure+figcaption）
├── 侧栏（可选：目录/相关内容，aside）
└── 相关推荐（data-collection）
```

- 文章类 detail 可加 Article JSON-LD 与 BreadcrumbList JSON-LD

## landing（landing.html）

```
main
├── hero（单一主张，h1 + 行动按钮）
├── 痛点/价值区块（≥ 2 个 section）
├── 功能/亮点网格
├── 数据背书或用户评价
└── 结尾行动区（重复主行动按钮）
```

- 单页纵向滚动叙事；每个 section 用 `aria-labelledby` 关联自己的 h2

## about（about.html）

```
main
├── 简介（h1 + 组织说明）
├── 里程碑/时间线（可用 ol）
└── 团队（人物卡片，data-collection + person 模型）
```

## contact（contact.html）

```
main
├── h1 + 联系说明
├── 联系表单（form，原生校验：label+for、required、type=email/tel）
└── 联系信息（address；地图仅占位不引远程服务）
```

- 表单提交按钮用原生 `<button type="submit">`；不写真实后端，action 留 # 并注明 sample

## search（search.html）

```
main
├── h1 + 搜索表单（role="search" 的 form 或 search 元素）
└── 结果列表（样例结果，data-collection）或空结果态（含建议）
```

## error（404.html）

```
main
├── h1 = 404 说明
├── 返回首页/推荐内容链接
```

- 必须简洁可用；不得只有一行字
- **heading 不跳级**：若 main 内除 h1 外无 h2，而 site-footer 含 h3 列标题，validate.py 会检出 h1→h3 跳级。处理：footer 内加一个 `visually-hidden` h2（如"页脚"），或 main 内补 h2
