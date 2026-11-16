# md-prd-to-html-prototype

读取一份本地 Markdown 需求，生成一个能在浏览器里点的后台低保真原型。页面、字段和按钮以文档为准；文档没写清楚就先问，不编造字段。

## 产物

- 与源 md 同目录的 `原型-{系统名称}.html`
- 默认单文件：侧栏切换视图，新增和编辑用弹窗
- 样式只允许 Tailwind 这一处 CDN，其余 CSS 和 JS 写在同一个 HTML 里

## 目录

本体在仓库根目录 `md-prd-to-html-prototype/`。`.workbuddy/skills/md-prd-to-html-prototype/` 是整份测试副本，文件与本体保持一致。目录名与 `SKILL.md` 的 `name` 一致。

```text
md-prd-to-html-prototype/
├── SKILL.md
├── README.md
├── resources/
│   ├── specifications/
│   │   ├── prd-extract.md      # 从 md 抽什么，何时停下来问
│   │   └── html-contract.md    # 单文件、命名、外链边界、交互
│   ├── templates/
│   │   └── admin-shell.html    # 后台壳，生成时从这里改
│   └── demo_output/
│       ├── 校园报修需求.md
│       └── 原型-校园报修.html
├── references/                 # 多端、多页草稿，当前流程不读取
│   ├── output-contract.md
│   ├── interaction-contract.md
│   └── intake-and-state.md
└── scripts/                    # 上述草稿的校验器，当前流程不运行
    ├── validate_prototype.py
    └── test_validate_prototype.py
```

当前 `SKILL.md` 只使用 `resources/`。`references/` 和 `scripts/` 仍随本体整份同步到测试副本，避免两处文件集合不一致。

## 和 prd-html-skill 的差别

本技能吃一份已经写好的 md，直接出单文件原型。`prd-html-skill` 会先在项目里建导航地图和逐页规格，再逐页生成。不要把两套流程叠在同一次生成里。
