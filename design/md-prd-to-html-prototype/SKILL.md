---
name: md-prd-to-html-prototype
description: >
  读取本地 Markdown 格式 PRD 或需求文档，提取角色、页面、字段和交互，输出单文件 HTML 低保真原型。
  用户说「md 生成 html 原型」「根据 prd 文档生成原型」「把需求文档转为 html 原型」「把需求做成能点的单页」时使用。
  信息不足时先提问，不编造业务字段。
---

# MD-PRD 转 HTML 交互原型

读取用户指定的本地 `.md`，生成**一个**可在浏览器直接打开的后台低保真原型。样式和交互规则以 [resources/specifications/html-contract.md](resources/specifications/html-contract.md) 为准，从 [resources/templates/admin-shell.html](resources/templates/admin-shell.html) 起笔，不要另起一套布局。

## 执行流程

### 1. 读取需求

1. 向用户要本地 md 的路径，例如 `./prd/报修系统需求.md`。
2. 读全文。按 [resources/specifications/prd-extract.md](resources/specifications/prd-extract.md) 提取系统名称、角色、页面、字段、按钮和交互。
3. 页面或字段缺失时，列出待确认问题并停止。不要补造字段后再生成。

### 2. 套壳写文件

1. 以 `admin-shell.html` 为起点，把 md 里的页面做成侧栏视图，把新增/编辑做成弹窗。
2. 假数据只允许使用 md 里已经出现的字段。行里的示例值可以编，字段名不可以编。
3. 写入与源 md 同目录的 `原型-{系统名称}.html`。连字符用普通 `-`。
4. 用户明确要求多文件时才拆页。默认仍然是单文件内切换视图。

### 3. 交付摘要

写完文件后说明：

- 原型路径
- 已实现的页面
- 已模拟的交互
- 仍待确认、因而没做进原型的业务点

并告诉用户：可以改源 md 后重新生成，也可以直接指出要改的页面、字段或交互。

## 禁止

- 只在对话里贴代码块就结束。必须把 HTML 写到本地文件。
- 拆出本地 `.css` / `.js`，或再引入 Tailwind 以外的 CDN、字体、图片 URL。
- 做成高保真视觉稿，或接真实后端。
- 在 md 没写页面和字段时硬生成。

## 与 modern-web-guidance 叠加

单文件、低保真、字段以 md 为准，这些不变。写弹窗、表单、表格或键盘操作前，先查阅仓库里的 `modern-web-guidance`，再把行为写进同一个 HTML 的内联脚本。

```sh
python modern-web-guidance/resources/tools/mwg.py search "<2-5 词的单一 UI 能力>"
python modern-web-guidance/resources/tools/mwg.py retrieve "<id>"
```

不要因为指南再增加 CDN 或外部文件。Tailwind 这一处例外只写在 `html-contract.md`。没有这类界面任务时不要调用它。
