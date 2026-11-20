# Glassmorphism（毛玻璃）

半透明磨砂面板浮在彩色渐变背景上：backdrop-filter 模糊 + 白色半透明 + 细描边。常见于个人作品集与创意产品页。⚠ 本包极易用滥（个人开发者廉价感的重灾区），只用于确实合适的场景，且必须遵守用量纪律。

```yaml
id: glassmorphism
version: 1
name: 毛玻璃

source:
  derived_from: "self（自研；基于 CSS backdrop-filter 的通行实现，未复制任何第三方仓库代码）"
  repo: ""
  license: "本项目 MIT"
  attribution: "自研设计包"
  local_changes: ""

identity:
  mood: [airy, modern, layered, playful]
  best_for: [个人作品集, 创意/娱乐产品页, 天气/音乐类应用风格页面, 活动专题]
  not_for: [严肃企业官网, 政务/金融/医疗, 长文阅读内容站]

colors:
  background: |
    必须有"可被毛玻璃透出的"彩色背景：
    渐变天空 #7BC6FF → #A78BFA → #FF9BB3，或深色底 + 彩色光斑
  panel: "rgba(255,255,255,.45)（深色底用 rgba(255,255,255,.08)）"
  text: "#1C2B4A（浅色玻璃上）/ #FFFFFF（深色玻璃上）"
  muted: "rgba(28,43,74,.65)"
  accent: "#1A73E8 或从背景主色取（保持单色）"
  border: "rgba(255,255,255,.55)"

typography:
  heading: "'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif（字重 600–700）"
  body: "同 heading（400）"
  scale: "1.3"

geometry:
  radius: "16–20px"
  border: "1px solid rgba(255,255,255,.55)（浅色玻璃描边）"
  shadow: "0 8px 32px rgba(31,38,135,.12)（柔和投影，仅一层）"

layout:
  density: medium-low（毛玻璃需要呼吸空间）
  max_width: "1160px"
  grid_tendency: "大色块背景 + 居中玻璃面板；卡片间距大"

effects:
  texture: "backdrop-filter: blur(14–20px)；背景彩色 blob（radial-gradient 圆形色块）"
  image_treatment: "背景图即质感来源；玻璃面板内不再放重图"

motion:
  duration: "250–400ms"
  easing: "ease-out"

rules:
  prefer:
    - "毛玻璃只用于浮层/卡片/导航层，正文阅读区保持高对比实底"
    - "背景色块要有明暗差，玻璃面板的模糊才有意义"
    - "文字对比度必须 ≥4.5:1，低对比'透明感文字'一律禁止"
  avoid:
    - "全站每个元素都毛玻璃（个人开发者滥用信号，变廉价）"
    - "玻璃面板套玻璃面板"
    - "纯白/纯灰背景上用毛玻璃（无东西可透出，等于没效果）"

breaks_if:
  - "背景没有可透出的色彩、面板无 blur、文字低对比，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：`background` 渐变族（蓝紫粉 → 青绿橙 / 日落橙粉等），只要保持"有可透出的彩色背景"这一前提
- **锁定**：panel 透明度 + blur 规则、文字对比度规则（这些是毛玻璃成立的条件，不是风格）
- **冲突**：学生要实底严肃风 → 不是改包，换 corporate-clean

## 使用提示

- **用量纪律**：一页上毛玻璃元素 ≤ 3 处（导航 + hero 面板 + 一组卡片）；超过即降格为普通半透明
- backdrop-filter 需要浏览器支持，必须写 `-webkit-backdrop-filter` 兜底，并给不支持时的半透明实底 fallback
- 学生说"梦幻、轻盈、玻璃感"才选本包；企业/严肃需求一律不推
