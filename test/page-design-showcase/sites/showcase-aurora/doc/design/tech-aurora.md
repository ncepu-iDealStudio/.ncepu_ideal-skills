# Tech Aurora（极光科技）

深色饱和渐变底、超大字号标题、mesh 渐变与霓虹光。当代 AI 创业公司 / SaaS 官网的主流气质。这是内置包中唯一允许（且要求）渐变与发光的包。

```yaml
id: tech-aurora
version: 1
name: 极光科技

source:
  derived_from: "Ilm-Alan/frontend-design · Aurora Maximalism anchor"
  repo: "https://github.com/Ilm-Alan/frontend-design"
  license: "MIT"
  attribution: "视觉体系改编自 Ilm-Alan/frontend-design（MIT）的 Aurora Maximalism 锚点"
  local_changes: "收敛了动效强度以适配静态原型；补充表单/列表页令牌"

identity:
  mood: [bold, futuristic, premium, energetic]
  best_for: [AI 公司, SaaS, 开发者工具, 数据平台, 科技发布会官网]
  not_for: [政务, 传统制造, 法律, 学术机构]

colors:
  background: "#0A0A12"        # 深底，上面铺渐变
  gradient_base: "linear-gradient(135deg, #5D34D0 0%, #FF006E 55%, #00F0FF 100%)"
  gradient_soft: "radial mesh（violet/magenta/cyan 低透明度铺底）"
  surface: "#13131E"
  text: "#F2F2F8"
  muted: "#9B9BB0"
  accent: "#7C5CFF"            # 主交互色
  accent_glow: "#00F0FF"       # 强调/发光色

typography:
  heading: "Inter Tight, Inter, -apple-system, sans-serif（超大 display：clamp(2.5rem, 6vw, 5rem)）"
  body: "Inter, -apple-system, sans-serif"
  scale: "1.333（大跨距层级）"

geometry:
  radius: "12–20px"
  border: "1px solid rgba(255,255,255,0.08)"
  shadow: "彩色弥散光晕（box-shadow 用 accent 低透明度），仅用于主 CTA"

layout:
  density: spacious
  max_width: "1200px"
  grid_tendency: "hero 超大标题 + 居中叙事；玻璃拟态面板（backdrop-filter: blur）"

effects:
  texture: "mesh 渐变为主视觉面；噪点 1–2% 可选"
  image_treatment: "渐变遮罩融合，或 duotone"
  glow: "accent 文字/按钮可加 text-shadow/box-shadow 发光（克制，仅焦点元素）"

motion:
  duration: "300–500ms"
  easing: "cubic-bezier(0.22, 1, 0.36, 1)（spring 感，禁 bounce）"

rules:
  prefer:
    - "hero：超大字 + 渐变高亮关键词 + 单一主 CTA"
    - "深底上的卡片用玻璃拟态（半透明 + blur + 细边框）"
    - "渐变集中在 hero 与结尾 CTA，中段保持克制"
  avoid:
    - "大面积亮色平铺（破坏深底沉浸）"
    - "全页到处发光；渐变按钮套渐变背景"
    - "紫蓝渐变之外再混入第三种渐变方向"

breaks_if:
  - "变成纯平白底、hairline 极简、或衬线字体，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：渐变色相族（紫→品红→青 可旋转为其他霓虹三色族，如青→绿→蓝紫），保持深色底 + 高饱和发光族
- **锁定**：`background` 深色底、玻璃卡 rgba 体系、glow 效果（"深色底上的饱和渐变"是本包身份）
- **冲突**：学生要白底浅色 → 不是改包，换 flat-material / corporate-clean

## 使用提示

- 列表/详情页收敛：渐变退到页面顶部，正文区回到深底面板，保证可读性
- 无障碍注意：发光文字对比度必须仍达标，宁可加深底色
- Inter 可退回系统栈；渐变用 CSS 实现，不依赖图片
