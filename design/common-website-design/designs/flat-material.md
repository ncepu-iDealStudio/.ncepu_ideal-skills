# Flat Material（扁平质感）

Google Material / Apple 扁平的现代感：白底、层级靠"高度"（阴影分层）而非边框、单一大胆强调色、圆角适中、克制无渐变。SaaS 产品、App、工具类官网的通用选择。

```yaml
id: flat-material
version: 1
name: 扁平质感

source:
  derived_from: "self（自研；参考 Material Design 3 / Apple HIG 公开设计原则，未复制任何第三方仓库代码）"
  repo: ""
  license: "本项目 MIT"
  attribution: "自研设计包"
  local_changes: ""

identity:
  mood: [modern, friendly, structured, clean]
  best_for: [SaaS 产品官网, App/工具产品页, 教育/开放平台, 企业产品子站, 移动优先的官网]
  not_for: [严肃报刊/学术, 强个性实验风, 控制台/仪表盘]

colors:
  background: "#FFFFFF"
  surface: "#F5F5F7"           # Apple 系浅灰底
  text: "#1D1D1F"
  muted: "#6E6E73"
  primary: "#1A73E8"           # Material 蓝（可按品牌替换，保持高饱和单色）
  primary_dark: "#1558B0"
  border: "#E0E0E5"

typography:
  heading: "Roboto, 'SF Pro Display', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif"
  body: "同 heading"
  scale: "1.3（标题层级清楚，不夸张）"

geometry:
  radius: "8–12px（按钮/卡片圆角）"
  border: "极少使用；分区靠阴影分层"
  shadow: |
    分层阴影（Material 高度）：
    卡片默认 0 1px 3px rgba(0,0,0,.08)；
    hover/浮层 0 4px 14px rgba(0,0,0,.12)；
    模态/抽屉 0 8px 30px rgba(0,0,0,.16)

layout:
  density: medium
  max_width: "1140px"
  grid_tendency: "卡片化分区（每卡一个主题，禁止卡片套卡片）；大面积留白；主 CTA 高对比实心按钮"

effects:
  texture: "无"
  image_treatment: "真实产品图/截图，卡片顶部整幅；禁止渐变遮罩下的假图"

motion:
  duration: "200–250ms"
  easing: "cubic-bezier(0.2, 0, 0, 1)（Material standard）"

rules:
  prefer:
    - "层级用阴影高度表达（raised card > flat card > 背景），不用边框堆叠"
    - "单一强调色贯穿（CTA/链接/图标），不引入第二强调色"
    - "按钮：实心主按钮 + 文字型次按钮（ghost）"
  avoid:
    - "渐变、霓虹、发光、扫描线"
    - "直角硬边框、双线框装饰"
    - "衬线 display 字体"

breaks_if:
  - "出现渐变主视觉、直角硬边框分区、霓虹色，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：`primary`——保持高饱和单色（Material 蓝 → 品牌绿/紫/橙均可），hover 态同族加深
- **锁定**：`background / surface / text` 与阴影分层体系（白底 + 灰阶阴影是本包身份）
- **冲突**：学生要深色渐变底 → 不是改包，换 tech-aurora

## 使用提示

- 与 corporate-clean 的区别：两者都"白底专业"，但 corporate-clean 靠边框/分隔线组织（传统门户感），flat-material 靠阴影高度分层（现代产品感）——学生说"像 App/产品官网"选本包
- 适合搭配 fade-up-reveal 动效（企业/产品站的默认动效组合）
- 阴影全部用 rgba(0,0,0,·) 灰阶，禁止彩色阴影
