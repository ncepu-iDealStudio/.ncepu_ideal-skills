# Swiss Minimal（瑞士极简）

纯白、无衬线、可见网格、单一强调色。国际主义平面风格的网页化：作品集、实验室、文档站、设计机构。

```yaml
id: swiss-minimal
version: 1
name: 瑞士极简

source:
  derived_from: "Ilm-Alan/frontend-design · Swiss anchor"
  repo: "https://github.com/Ilm-Alan/frontend-design"
  license: "MIT"
  attribution: "视觉体系改编自 Ilm-Alan/frontend-design（MIT）的 Swiss 锚点"
  local_changes: "中文语境下标题字体退回系统无衬线栈；补充列表/表单页令牌"

identity:
  mood: [rational, clean, editorial-neutral, confident]
  best_for: [作品集, 设计/研究实验室, 文档站, 建筑与工作室]
  not_for: [娱乐化、游戏、强情绪化品牌]

colors:
  background: "#FFFFFF"
  surface: "#F7F7F8"
  text: "#111111"
  muted: "#6E6E73"
  accent: "#E4002B"            # Swiss 红（可换 #FF4F00 国际橙 / #002FA7 克莱因蓝，全站仅一种）
  border: "#E5E5E7"

typography:
  heading: "'Helvetica Neue', 'PingFang SC', 'Noto Sans SC', Arial, sans-serif（单一字族，靠字重与字号分层）"
  body: "同 heading"
  scale: "1.428（大跨距：display 很大、正文很小）"
  numeric: "日期/页码/编号作为构图元素，可用 condensed 或 tabular"

geometry:
  radius: "0"
  border: "1px hairline（#E5E5E7 或文本色细线）"
  shadow: "none"

layout:
  density: airy
  max_width: "1280px"
  grid_tendency: "可见网格线/1px 分隔线；左对齐排版；不对称均衡；大量留白"

effects:
  texture: "无"
  image_treatment: "原色直出，精准裁切；不加滤镜"

motion:
  duration: "150–250ms"
  easing: "ease"

rules:
  prefer:
    - "标题左对齐；用字号对比制造层级，不用颜色"
    - "强调色全场克制：一个词、一条线、一个按钮，不超过 5% 面积"
    - "编号/日期/分类标签作为版面装饰元素（小号 mono 或 condensed）"
  avoid:
    - "居中排版、暖色纸底、纹理噪点"
    - "衬线 display 字体"
    - "圆角、阴影、多彩"

breaks_if:
  - "出现暖纸色、衬线大标题、居中构图、纹理，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：`accent`——保持高饱和单色族（Swiss 红 / 国际橙 / 伊夫·克莱因蓝 #002FA7 任选），全站只用一个强调色
- **锁定**：纯白/中性底、网格线、hairline 分隔（白底网格是本包身份）
- **冲突**：学生要多彩/渐变 → 不是改包，换 tech-aurora / glassmorphism

## 使用提示

- 层级全部来自排版：h1 巨大、正文 15–16px、muted 辅助信息小号
- 分隔线是这个包的"装饰"：用 1px 线组织信息，而不是卡片
- 强调色选定后全站唯一，禁止混用两种强调色
