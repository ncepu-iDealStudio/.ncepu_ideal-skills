# Editorial（报纸编辑）

衬线大标题、分栏排版、首字下沉、期刊/报纸的编辑部气质。新闻资讯、科技媒体、学术内容站的阅读优先选择。

```yaml
id: editorial
version: 1
name: 报纸编辑

source:
  derived_from: "self（自研；基于经典报刊排印传统，未复制任何第三方仓库代码）"
  repo: ""
  license: "本项目 MIT"
  attribution: "自研设计包"
  local_changes: ""

identity:
  mood: [literary, credible, serious, reading-first]
  best_for: [新闻/资讯站, 科技媒体, 学术内容, 评论/深度阅读, 文化杂志]
  not_for: [工具型产品官网, 控制台, 娱乐化落地页]

colors:
  background: "#FCFBF8"        # 微暖纸白（非纯白）
  surface: "#F4F2EC"
  text: "#1A1815"
  muted: "#6B6558"
  primary: "#8C2F1B"           # 报刊红（标题下划线、栏目题花）
  link: "#1A1815"              # 正文链接用下划线区分，不依赖颜色
  border: "#DDD8CC"

typography:
  heading: "'Noto Serif SC', 'Source Han Serif SC', Georgia, 'Songti SC', serif（display 字重 700–900）"
  body: "'Noto Sans SC', 'PingFang SC', sans-serif（正文阅读用无衬线，与标题形成衬线/非衬线对比）"
  scale: "1.38（标题很大，正文 17px/1.8 行高优先阅读）"
  meta: "栏目名、日期、作者用小号字 + 字距拉开（letter-spacing: 0.08em）"

geometry:
  radius: "0"
  border: "1px solid var(--border)；分隔用双细线（报纸题花风）"
  shadow: "none"

layout:
  density: medium-dense
  max_width: "正文栏 720px；页面网格 1200px（含侧栏）"
  grid_tendency: "首页多栏报纸网格（头条大块 + 次要新闻小卡）；文章页单栏正文 + 侧栏目录"

effects:
  texture: "无（或纸感 ≤1%，可省）"
  image_treatment: "黑白或低饱和照片；图片说明（figcaption）必须有"

motion:
  duration: "150–250ms"
  easing: "ease"

rules:
  prefer:
    - "头条文章占首页最大块：大衬线标题 + 摘要 + 继续阅读"
    - "栏目体系清晰：栏目名（科技/评论/深度）作为导航与卡片标签"
    - "文章页：面包屑 + 作者/日期行 + 正文 + 相关阅读；首段可首字下沉"
    - "日期与作者信息用 time datetime + data-slot 完整标注"
  avoid:
    - "卡片圆角阴影堆砌（用分隔线和留白组织信息）"
    - "无衬线大标题（本包的 display 必须衬线）"
    - "霓虹、渐变、发光等科技感元素"

breaks_if:
  - "标题改为无衬线、出现卡片化 SaaS 风格或强渐变，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：`primary` 报刊红 → 墨绿/藏青/深棕等（保持低饱和、沉稳的报刊题花色）
- **锁定**：微暖纸白底、衬线 display 体系、正文文字色（阅读性是本包身份）
- **冲突**：学生要科技感/霓虹 → 不是改包，换 tech-aurora

## 使用提示

- 中文衬线字体优先系统栈（宋体/Songti SC/Noto Serif SC），无需下载字体文件即可成立
- 分栏布局在移动端退化为单栏，头条优先
- 与 swiss-minimal 的区别：editorial 是"内容优先的阅读体验"，swiss 是"形式优先的构成主义"——学生说"像报纸/杂志"选本包，说"极简/工作室"选 swiss
