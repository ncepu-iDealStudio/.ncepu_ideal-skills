# Commerce Rich（电商丰富）

购物网站的超大量图片风格：促销色 + 大图商品网格 + 角标 + 价格突出 + 高密度信息。品牌旗舰店、商城首页、促销专题的选择。

```yaml
id: commerce-rich
version: 1
name: 电商丰富

source:
  derived_from: "self（自研；参考主流电商平台通行版式，未复制任何第三方仓库代码）"
  repo: ""
  license: "本项目 MIT"
  attribution: "自研设计包"
  local_changes: ""

identity:
  mood: [lively, promotional, image-first, dense]
  best_for: [商城/电商, 品牌旗舰店页面, 促销专题, 内容电商, 展销目录]
  not_for: [极简作品集, 严肃机构官网, 控制台, 长文阅读]

colors:
  background: "#FFFFFF"
  surface: "#F6F6F6"
  text: "#222222"
  muted: "#888888"
  primary: "#E1251B"           # 促销红（价格/CTA/促销标签）
  secondary: "#FF7A00"         # 橙（辅助促销色，克制使用）
  border: "#EAEAEA"

typography:
  heading: "'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif（粗体大字号）"
  body: "同 heading"
  price: "tabular-nums，货币符号小一号上标，整数大 1.5–2 倍，红色"
  scale: "1.2（信息密度优先）"

geometry:
  radius: "4–8px（小圆角，卡片利落）"
  border: "1px solid var(--border)"
  shadow: "hover 0 2px 10px rgba(0,0,0,.08)（仅 hover 出现）"

layout:
  density: dense
  max_width: "1200px"
  grid_tendency: |
    频道导航条（多分类入口）+ 大图轮播位 + 4–5 列商品网格；
    图片占卡面 60% 以上；价格与标题同级显眼

effects:
  texture: "促销角标（左上斜角色块）、限时倒计时条"
  image_treatment: "白底或场景商品大图；hover 图片放大 1.03–1.05"

motion:
  duration: "150–250ms"
  easing: "ease"

rules:
  prefer:
    - "价格永远是卡面第一视觉焦点（红色 + 大字号 + tabular-nums）"
    - "角标每卡最多 1 个（新品/热卖/直降 选一），禁止多角标打架"
    - "促销区用整条色带 + 倒计时，与普通商品区拉开"
    - "商品网格图片主体占比 ≥60%"
  avoid:
    - "低质量/模糊图片（本包图片即生命线，模糊大图毁一切）"
    - "每个卡都堆促销标签的'炸街'感"
    - "大面积留白极简（与本包气质相反）"

breaks_if:
  - "商品图被弱化、价格不显眼、信息密度降到 medium-low，即视为锚点被破坏"
```

## 色彩覆盖（Palette Override）

- **可变**：`primary` 促销红 → 品牌橙/玫红等（保持高唤醒度促销色，不可换成低饱和沉稳色）
- **锁定**：白底网格、价格红色规则（价格永远是第一视觉焦点）、角标配色体系
- **冲突**：学生要克制低饱和的商务感 → 不是改包，换 corporate-clean

## 使用提示

- 样例图片用本地纯色/SVG 占位图 + 产品名标注；后续接入真实商品图时图片容器比例（1:1 或 4:3）必须保持
- 价格格式：`¥` 小字上标 + 整数大字号（如 ¥¹²⁹⁹），配合 tabular-nums
- 与 corporate-clean 的区别：corporate 是"展示企业"，commerce-rich 是"卖货"；学生提到"商城/旗舰/促销/双十一"就选本包
