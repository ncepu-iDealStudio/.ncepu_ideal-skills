# Industrial Dark（工业暗色）

黑底、等宽字体、单一信号色、全平面的**控制台审美**——像工程系统 / 仪表盘 / 开发者工具的内场界面，不是对外营销页。信息密度高，一切靠边框分区，不用阴影。

```yaml
id: industrial-dark
version: 1
name: 工业暗色

source:
  derived_from: "Ilm-Alan/frontend-design · Industrial anchor"
  repo: "https://github.com/Ilm-Alan/frontend-design"
  license: "MIT"
  attribution: "视觉体系改编自 Ilm-Alan/frontend-design（MIT）的 Industrial 锚点"
  local_changes: "补充 surface 层级色、muted 文字色与响应式断点"

identity:
  mood: [technical, precise, serious, console]
  best_for: [控制台/仪表盘界面, 开发者工具, 技术文档站, 工程系统页面, 用户明确要"工程控制台"气质的站点]
  not_for: [企业对外官网/品牌营销页, 传统企业门户, 面向消费者的温和品牌, 产品营销展示站, 儿童教育, 生活方式]

colors:
  background: "#0B0C0A"        # 暖黑
  surface: "#14160F"           # 卡片/面板底
  surface_alt: "#1B1E16"       # 次级面板/表头
  text: "#E8EAE6"
  muted: "#9AA096"
  accent: "#00E676"            # 单一信号色（可换 #FFB800 警示琥珀 / #FF3B30 危险红，语义场景）
  border: "#2A2D26"

typography:
  heading: "IBM Plex Mono, JetBrains Mono, ui-monospace, monospace"
  body: "IBM Plex Mono, ui-monospace, monospace"
  scale: "1.25（紧凑，小字号高密度）"
  numeric: "font-variant-numeric: tabular-nums（所有数据表格必须）"

geometry:
  radius: "0（一律直角）"
  border: "1px solid var(--border)（分区靠边框，不靠阴影）"
  shadow: "none"

layout:
  density: dense
  max_width: "1320px"
  grid_tendency: "强网格；表格式信息；hairline 分隔线；标签-值成对呈现"

effects:
  texture: "无（纯平面）"
  image_treatment: "去饱和或绿调 duotone；技术示意图优先于照片"

motion:
  duration: "120–200ms"
  easing: "linear（机械感，禁 ease-out 长尾）"

rules:
  prefer:
    - "状态色仅用于语义：运行/成功=绿、警告=琥珀、危险=红"
    - "元数据（时间戳、编号、单位）用 mono 小字 + muted 色"
    - "大数字/指标作为视觉锚点"
  avoid:
    - "圆角、装饰阴影、渐变、发光"
    - "衬线字体、手写体"
    - "彩色背景块（除语义状态）"

breaks_if:
  - "出现衬线字体、暖色纸底、圆角卡片、装饰阴影、多彩渐变，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：`accent` 信号色（绿 #00E676 / 琥珀 #FFB800 / 红 #FF3B30 / 酸橙 #C6FF4A 任选），保持高亮信号感、全站仅一色
- **锁定**：`background / surface / text` 与 mono 字体体系（黑底+等宽是本包身份）
- **冲突**：学生要白底 → **锚点破坏，换包**（corporate-clean / swiss-minimal），不得改包

## 使用提示

- **定位警告**：本包是控制台审美。电池/制造/能源企业的**对外官网**不是它的场景——那类需求应给 corporate-clean（白底稳重）或 tech-aurora（现代科技感）；领域词"能源/制造"≠ 控制台气质
- 禁止在营销型页面上伪造"产线状态/实时运行率"等遥测面板——那是控制台 UI，放营销页上就是 AI 味
- 适合的 hero：不是大图，而是"系统状态面板"——关键指标 + 信号色 + mono 大字
- 卡片 = 带边框的平面区块，标题行像终端表头
- CDN 字体可引 IBM Plex Mono（须登记），或直接退回 ui-monospace 栈保证离线可用
