# Output Contract（落盘结构契约）

## 目录结构（固定）

```
site/                        ← 默认输出根目录；学生可另指定（须写入 README 的 outputRoot）
├── doc/
│   ├── README.md            ← 设计综述：唯一状态恢复入口
│   └── design/
│       └── <pack-id>.md     ← 采用的设计包副本（含学生定制）
└── template/
    ├── index.html           ← 必须存在
    ├── article.html …        ← 其余页面（文件名按需求，type 登记进 manifest）
    ├── css/
    │   ├── base.css         ← reset + design tokens + 排版基线
    │   ├── components.css   ← site-header/footer/卡片等组件
    │   └── pages.css        ← 页面特定样式
    ├── js/
    │   └── main.js          ← 仅原生模块不足时存在
    ├── image/
    └── site-manifest.json   ← 必须存在
```

## site/doc/README.md（设计综述）

生成过程中**每完成一步就更新**。必须包含：

```markdown
# <站点名> 设计综述

- outputRoot: site/          ← 若学生指定了别的目录，改这里
- 状态: 进行中（已完成 3/6 页）  ← 恢复工作的进度标记

## 需求原文
（学生原话摘要）

## Requirement Model
- site: 名称/语言/用途/受众
- pages: home(index.html) ✓ / list(category.html) ✓ / detail(article.html) 待生成 / …
- content: 领域 + 内容模型清单
- design: 选定 industrial-dark（选择理由一句话）

## 设计包
site/doc/design/industrial-dark.md（含/不含学生定制）

## 页面进度
- [x] index.html
- [ ] article.html …

## 给后续拆解 Agent 的提示
组件清单见 manifest.components；循环区域看 data-collection；字段定义看 manifest.collections。
```

## site-manifest.json（schema）

```json
{
  "site": {
    "name": "示例站点",
    "language": "zh-CN",
    "description": "一句话站点说明",
    "designPack": "industrial-dark",
    "generatedAt": "2026-09-18"
  },
  "outputRoot": "site/",
  "pages": [
    { "file": "index.html", "type": "home", "title": "首页" },
    { "file": "article.html", "type": "detail", "title": "文章页" }
  ],
  "components": ["site-header", "site-footer", "post-card", "post-list"],
  "collections": {
    "posts": { "fields": ["title", "summary", "url", "date", "author", "category"], "sample": true }
  },
  "contentSample": { "generated": true, "note": "所有内容为演示用样例数据" },
  "modules": [
    { "feature": "移动菜单", "implementation": "details/summary + CSS" },
    { "feature": "联系表单校验", "implementation": "原生 required + :invalid" }
  ],
  "external": { "cdn": ["https://cdn.example.com/lib/1.0/lib.min.js"] }
}
```

字段规则：

- `pages[].type` 取值：home / list / detail / landing / about / contact / search / error
- `components` 与页面中出现的 `data-component` 完全一致
- `collections` 每个键对应页面中的 `data-collection`；`fields` 对应其下 `data-slot` 的字段部分
- 所有样例数据声明在 `contentSample`；所有 CDN 引用声明在 `external.cdn`

## 验证

```
python scripts/validate.py site/template
```

零错误才算完成。验证器检查项见脚本头部注释；渲染级验证（截图/溢出/遮挡）为 V1.1，届时可接入浏览器工具。
