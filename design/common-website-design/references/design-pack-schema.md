# Design Pack Schema（设计包契约）

设计包 = 一份锁定视觉令牌的规范。**只换衣服，不改骨架**：设计包可控制颜色、字体、间距、圆角、阴影、密度、布局倾向、图片处理、动效；**禁止**规定 HTML 语义结构、heading 组织、ARIA、SEO、data-* 标注。

## 文件格式

`designs/<id>.md`，正文为一段说明 + 一个 YAML 代码块：

```yaml
id: industrial-dark
version: 1
name: 工业暗色

source:                      # 可追溯性，必填
  derived_from: "Ilm-Alan/frontend-design · Industrial anchor"
  repo: "https://github.com/Ilm-Alan/frontend-design"
  license: "MIT"
  attribution: "视觉体系改编自 Ilm-Alan/frontend-design（MIT）"
  local_changes: "补充了 surface 层级色与响应式断点"

identity:
  mood: [technical, precise, serious]
  best_for: [智能制造, 能源, 工程, 自动化, 网络安全]
  not_for: [面向消费者的温和品牌]

colors:
  background: "#0B0C0A"
  surface: "#14160F"
  text: "#E8EAE6"
  muted: "#9AA096"
  accent: "#00E676"          # 单一信号色
  border: "#2A2D26"

typography:
  heading: "IBM Plex Mono, JetBrains Mono, monospace"
  body: "IBM Plex Mono, monospace"
  scale: "1.25（紧凑）"

geometry:
  radius: "0"
  border: "1px solid var(--border)"
  shadow: "none（用边框替代阴影）"

layout:
  density: dense
  max_width: "1320px"
  grid_tendency: "强网格、表格化信息"

effects:
  texture: "无（平面）"
  image_treatment: "去饱和或 duotone"

motion:
  duration: "120–200ms"
  easing: "linear / steps"

rules:
  prefer:
    - "tabular-nums 表格数字"
    - "状态色仅用于语义（成功/警告/危险）"
  avoid:
    - "圆角、装饰阴影、渐变"
    - "衬线字体"

breaks_if:
  - "出现衬线字体、暖色纸底、圆角、装饰阴影即视为破坏锚点"
```

## 选择流程（候选确认制）

1. 学生明确指定 → 匹配 `designs/`；无精确匹配时找最接近的 2–3 个候选让学生选
2. 未指定 → 依内容领域与用途挑 2–3 个候选，展示 id / 名称 / 一句话定位 / 关键视觉特征
3. 学生无偏好 → 推荐一个并说明理由，经确认采用
4. 选定后复制到 `site/doc/design/<pack-id>.md`，学生定制在副本上修改并在 `local_changes` 中注明

## 学生自定义风格

学生描述的风格若与内置包均不匹配：以最接近的包为底，按其描述改写副本的 colors/typography 等字段，`derived_from` 注明"学生自定义 + 底包 id"。

## 常见选型误区（历史翻车记录）

- **领域词 ≠ 风格**："电池/能源/制造企业"是内容领域，不是视觉风格。企业**对外营销官网**默认从 corporate-clean / tech-aurora / flat-material 中给候选；industrial-dark 是控制台审美，仅当学生明确要"工程控制台/仪表盘"气质时给
- **强风格包谨慎推荐**：retro-futuristic、glassmorphism 气质强烈且易显廉价，只在学生描述明显匹配时进入候选，不作为"科技感"的默认答案
- **一个站点一个包**：禁止混搭（"Swiss 带一点 Brutalist"是类别错误）；差异表达应体现在页面结构，而非风格杂交

## 色彩偏好层（Palette Override）

学生可以指定色彩倾向（"主色要绿""深蓝一点""暖色系"）。色彩偏好**不是第四正交维度**，而是选定设计包之后的一层覆盖：直接改"包"会破坏锚点（industrial-dark 的身份就是黑底+信号色），完全不接又无视学生需求。

### 每包声明可变槽位

每个设计包文件含"色彩覆盖（Palette Override）"小节，声明：

- **可变**：可替换的色位（通常是 primary/accent）+ 替换约束（明度/饱和度/对比度底线）
- **锁定**：锚点身份色（背景/表面/文字等），不可动
- **冲突规则**：学生要求触碰锁定色位时，**不是改包，是重新选包**

### 冲突处理速查

| 学生要求 | 处理 |
|---------|------|
| "corporate-clean 主色改绿色" | 允许：替换 primary，遵守"保持深色系"约束 |
| "industrial-dark 但要白底" | 冲突：白底是锚点破坏项 → 回到候选，推荐 corporate-clean / swiss-minimal |
| "tech-aurora 渐变要青绿色" | 允许：渐变色相族内旋转，保持深色底+霓虹族 |
| "retro-futuristic 但要柔和浅色" | 冲突：该包身份就是黑底霓虹 → 重新选包 |
| "commerce-rich 促销红改品牌橙" | 允许：保持高唤醒度促销色约束即可 |

### 应用方式

1. 配色选项从 `references/palettes.md` 选取（自定配色区优先于通用方案），**不现场编造色值**；学生直接给了色值的，校验对比度后采用
2. 在 `site/doc/design/<pack-id>.md` 副本上直接改 colors 字段，`local_changes` 注明"学生指定：主色 #xxx"
2. `site/doc/README.md` 的 design 段记录最终色板
3. 生成时色彩集中在 `base.css` 的 `:root` 自定义属性替换，不散落各处
4. 替换后必须抽检对比度 ≥4.5:1（design-quality 的硬性要求）

## 新增设计包规则

- 一个包一个文件，id 唯一且与文件名一致
- 必须完整填写 source（自研也写 `derived_from: self`）
- license 不明或不可再分发的内容禁止进入 designs/
- 新包须通过 validate.py 对应检查（manifest 中 designPack 与落盘副本一致）
