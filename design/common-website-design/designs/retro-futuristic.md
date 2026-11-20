# Retro-Futuristic（复古未来）

黑底霓虹、CRT 扫描线、时期字体。机器人实验室 / 前沿科技 / 太空主题 / 复古赛博的美学。气质强烈，只用于确实想要这种表达的学生。

```yaml
id: retro-futuristic
version: 1
name: 复古未来

source:
  derived_from: "Ilm-Alan/frontend-design · Retro-Futuristic anchor"
  repo: "https://github.com/Ilm-Alan/frontend-design"
  license: "MIT"
  attribution: "视觉体系改编自 Ilm-Alan/frontend-design（MIT）的 Retro-Futuristic 锚点"
  local_changes: "补充 surface/border 令牌；动效收敛为静态原型可用"

identity:
  mood: [futuristic, retro, experimental, cinematic]
  best_for: [机器人实验室, 前沿科技展示, 游戏/娱乐, 太空/天文主题]
  not_for: [企业官网, 政务, 金融, 医疗]

colors:
  background: "#0A0014"        # 深紫黑
  surface: "#12081F"
  text: "#EDE6FF"
  muted: "#8F82B8"
  accent_primary: "#FF006E"    # 霓虹品红
  accent_secondary: "#00FFFF"  # 霓虹青
  border: "#2E1F45"

typography:
  heading: "Orbitron, 'Press Start 2P', VT323, monospace（标题专用时期字体）"
  body: "'Space Mono', ui-monospace, monospace"
  scale: "1.4（display 与正文反差拉大）"

geometry:
  radius: "0–4px"
  border: "1px solid var(--border)；焦点元素可用 1px 霓虹描边"
  shadow: "霓虹 glow（text-shadow: 0 0 12px accent），克制用于标题与 CTA"

layout:
  density: medium
  max_width: "1160px"
  grid_tendency: "雷达/网格背景、终端窗口式面板、斜切角装饰"

effects:
  texture: "CRT 扫描线（::before repeating-linear-gradient 覆盖层，透明度 ≤ 8%）或色差（text-shadow 红青偏移 2px），二选一"
  image_treatment: "高对比 + 霓虹描边框；扫描线覆盖"

motion:
  duration: "150–300ms"
  easing: "steps(4) 或 linear（机械/数字感）"

rules:
  prefer:
    - "终端/控制台式面板：标题栏 + 状态点 + mono 内容"
    - "霓虹双色严格配对使用（品红+青），不引入第三色"
    - "扫描线是全页覆盖层，不作用于局部"
  avoid:
    - "现代无衬线（Inter/Segoe）作为 display 字体"
    - "白底、纸质感、扁平极简"
    - "发光堆满全页（焦点元素之外保持暗）"

breaks_if:
  - "出现现代 sans 字体、白底、无纹理平面，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：霓虹双色对（品红 #FF006E + 青 #00FFFF → 磷光绿 #00FF41 + 琥珀 #FFB000），保持"黑底 + 双霓虹对撞"结构
- **锁定**：深紫黑底、扫描线/glow 纹理、mono 字体（本包身份）
- **冲突**：学生要柔和浅色 → **锚点破坏，换包**，不得改包

## 使用提示

- 扫描线覆盖层必须 `pointer-events: none` 且透明度极低，不影响可读性
- Orbitron/VT323 等字体需 CDN 或本地 woff2，退回栈为 monospace 仍成立
- 长正文页（文章 detail）应减弱纹理强度，优先可读性
