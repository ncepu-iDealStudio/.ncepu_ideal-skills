# Corporate Clean（企业净白）

传统企业/机构/学校官网的稳重专业：白底、深蓝主色、清晰导航、信息分区明确。不求惊艳，求可信、规整、易读。

```yaml
id: corporate-clean
version: 1
name: 企业净白

source:
  derived_from: "self（自研；参考主流企业官网通例，未复制任何第三方仓库代码）"
  repo: ""
  license: "本项目 MIT"
  attribution: "自研设计包"
  local_changes: ""

identity:
  mood: [professional, trustworthy, calm, structured]
  best_for: [传统企业官网, 机构/学校, 制造/能源企业, B2B 服务, 通知公告型门户]
  not_for: [个人作品集, 娱乐/游戏, 前沿科技发布]

colors:
  background: "#FFFFFF"
  surface: "#F5F7FA"
  text: "#1F2733"
  muted: "#5C6B7F"
  primary: "#0F4C8C"           # 深蓝主色（品牌可替换，但保持深色系稳重色）
  primary_dark: "#0A3568"
  accent: "#C8A24B"            # 辅助金（可选，仅装饰线/徽标）
  border: "#E3E8EF"

typography:
  heading: "'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif（字重 600–700 分层）"
  body: "同 heading（400/500）"
  scale: "1.25（稳健，不夸张）"

geometry:
  radius: "6px（克制的小圆角）"
  border: "1px solid var(--border)"
  shadow: "0 1px 3px rgba(15,39,67,0.08)（仅卡片悬浮/下拉）"

layout:
  density: medium
  max_width: "1200px"
  grid_tendency: "通栏 banner + 三/四列服务卡 + 新闻列表；顶部主导航 + 面包屑"

effects:
  texture: "无"
  image_treatment: "真实场景照片；banner 可加深蓝遮罩压字"

motion:
  duration: "200ms"
  easing: "ease"

rules:
  prefer:
    - "导航结构清晰：主导航 + 面包屑 + 页脚完整站点地图"
    - "信息模块化：服务/产品/新闻/资质/联系 各自独立 section"
    - "数字与事实背书（成立年份、案例数）增强可信度"
  avoid:
    - "炫技渐变、霓虹、扫描线等强风格元素"
    - "过低对比度；标题使用三种以上颜色"
    - "满屏英文装饰性标签（保持中文语境一致）"

breaks_if:
  - "出现暗黑霓虹/强渐变/装饰纹理等与稳重定位冲突的表达，即视为定位被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：`primary`——保持深色系稳重色（深蓝/深绿/深红等），与文字对比度 ≥4.5:1；`accent` 辅助金可换或删除
- **锁定**：`background / surface / text`（白底稳重是本包身份）
- **冲突**：学生要深色底 → 不是改包，换 tech-aurora / industrial-dark

## 使用提示

- 主色可按学生品牌色替换（保持深色系、对比度达标）
- 首页结构参考：banner（机构定位+主 CTA）→ 核心业务三/四卡 → 新闻动态列表 → 资质/伙伴 → 联系引导
- 这是"不出错"的默认选择，但不要把它当成唯一候选——学生要"科技感"时应推荐 tech-aurora / industrial-dark
