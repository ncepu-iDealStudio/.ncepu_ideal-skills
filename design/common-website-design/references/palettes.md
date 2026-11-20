# Color Palettes（色彩选项库）

学生说"我要绿色系/科技感配色/暖一点"时，从本库取**三色配色**（主色 primary + 辅助 secondary + 点缀 accent）作为 Palette Override 的选项呈现给学生，而不是现场编造色值。中性色（背景/表面/文字）由设计包自身提供，本库只管三个彩色位。

**用法**：选定设计包后，从本库挑 1–3 个与该包气质相容的配色方案展示给学生；确认后按 design-pack-schema 的 Palette Override 流程落盘。每套配色标注了适配的包，**不得把深色底配色套到浅色底包上**。

## 配色落地规则

- 三色分工：primary 主导航/CTA/标题强调（约 60% 色彩面积），secondary 次元素/辅助区块（30%），accent 仅作点缀（10%，如角标/徽标/装饰线）
- 对比度：彩色位用于文字或按钮文字底时，必须满足 4.5:1
- 每套方案注明"适配包"与"深色底/浅色底"属性，跨底型混用即视为违规

---

## 稳重商务系（浅色底）

### 深海蓝金（默认企业首选）
- primary `#0F4C8C` 深海蓝 · secondary `#2E6DA4` 雾蓝 · accent `#C8A24B` 哑光金
- 气质：可信、稳健、金融/制造/机构
- 适配包：corporate-clean ★ / editorial

### 墨绿铜
- primary `#0E5F4C` 墨绿 · secondary `#2F8F76` 青绿 · accent `#B87A3D` 铜
- 气质：能源/环保/农业/医药企业的沉稳感
- 适配包：corporate-clean ★ / editorial

### 砖红木
- primary `#8C2F1B` 砖红 · secondary `#B3541E` 赭石 · accent `#D9CBA3` 米金
- 气质：老字号/食品/文化机构的温度感
- 适配包：editorial ★ / corporate-clean

## 现代科技系（浅色底）

### 电光蓝紫（默认科技首选）
- primary `#1A73E8` 电光蓝 · secondary `#00C2FF` 天青 · accent `#7C4DFF` 量子紫
- 气质：SaaS/App/AI 产品的现代感
- 适配包：flat-material ★ / swiss-minimal（取 primary 单用）

### 青柠科技
- primary `#00A896` 青碧 · secondary `#02C39A` 薄荷 · accent `#FFB703` 亮黄
- 气质：开发者工具/教育科技的清爽感
- 适配包：flat-material / corporate-clean（科技型子公司）

## 活力促销系（浅色底）

### 促销红橙（默认电商首选）
- primary `#E1251B` 促销红 · secondary `#FF7A00` 活力橙 · accent `#FFC300` 明黄
- 气质：大促/商城/直播电商
- 适配包：commerce-rich ★

### 珊瑚青
- primary `#FF5A5F` 珊瑚红 · secondary `#3EC1D3` 湖青 · accent `#FFB400` 蜜黄
- 气质：生活方式/文创/年轻品牌
- 适配包：commerce-rich / flat-material

## 深色底专用系

### 信号绿琥珀（默认控制台）
- primary `#00E676` 信号绿 · secondary `#1B9E57` 暗绿 · accent `#FFB800` 警示琥珀
- 气质：工程控制台/仪表盘
- 适配包：industrial-dark ★

### 极光霓虹
- primary `#7C4DFF` 霓虹紫 · secondary `#00E5FF` 霓虹青 · accent `#FF4D8D` 霓虹粉
- 气质：AI 发布页/电竞/潮流科技
- 适配包：tech-aurora ★ / retro-futuristic（取双色对）

## 东方国风系（浅色底，特色选项）

### 故宫红金
- primary `#9E2B25` 宫墙红 · secondary `#C8A24B` 琉璃金 · accent `#2E3A48` 黛蓝
- 气质：文博/茶/中式品牌/政务文化站
- 适配包：corporate-clean / editorial ★

### 青瓷
- primary `#4A7C7E` 青瓷绿 · secondary `#9FC5C3` 釉色 · accent `#D9A441` 赭金
- 气质：手工艺/新中式/生活方式品牌
- 适配包：editorial / swiss-minimal（取 primary 单用）

---

## 自定配色区（压迫感三套 · 用户本人设计）

> 用户自己设计的配色方案，标注 `custom: true`，**候选展示时优先于上方通用方案**。
>
> 三套的共同手法，落盘时必须守住：**大面积低饱和压场 + 极少量高饱和刺点**。压迫感来自"克制"——
> 60% 的色是沉的、不抢戏的；10% 的色是刺的、只出现一次的。把刺点色用满 = 压迫感消失，变成廉价促销页。

```yaml
- name: "热异常"
  custom: true
  primary: "#1F1E23"     # 暖黑，60%：底色、骨架、正文块
  secondary: "#A9A9A9"   # 中灰，30%：次级文字、分隔线、弱化区块
  accent: "#FF5D13"      # 信号橙，10%：告警标记、CTA、唯一高亮
  base: dark
  mood: "设备告警 / 热成像 / 工业现场的紧张感。橙只用于'出事了'的地方，用第二处就失效"
  best_for: [industrial-dark]
  caution: "禁用于对外企业官网首页（会读出'控制台'而非'企业形象'）。accent 全站出现≤3 处"
  preview: "page-design-showcase/gallery/pressure-heat.html"

- name: "暮色森林"
  custom: true
  primary: "#443959"     # 暮紫，60%：标题、正文、栏目骨架
  secondary: "#DCD6E2"   # 浅紫，30%：页面底与大块铺底
  accent: "#1D7B80"      # 深青，10%：链接、引注、点睛线
  base: light
  mood: "日落后林间的安静压迫。紫立骨、浅紫铺底，青色是唯一'活口'"
  best_for: [editorial]
  caution: "浅紫 secondary 与白底对比极弱，正文必须落在 primary 上，别用 secondary 写长段落"
  preview: "page-design-showcase/gallery/pressure-twilight.html"

- name: "界园"
  custom: true
  primary: "#E5026B"     # 品红，主色调：报头/大标题/印章/粗规则
  secondary: "#D3CCB9"   # 骨白，底与渐变：纸面、版面背景
  accent: "#017A80"      # 青，结构点缀：栏线、表格、界桩、建筑装饰
  base: light
  mood: "粉绿主调——品红造梦境感、青绿续山水园林意象，明媚里带一丝阴森。骨白只做纸，不做主角"
  best_for: [editorial]
  caution: "品红 #E5026B 在骨白上对比度约 2.9:1，只用于大号标题与印章；小字改用深品红 #A8004A。青 #017A80 同理，小字用 #015F63"
  preview: "page-design-showcase/gallery/pressure-garden.html"
```

**选型提示**：自定配色自带强气质（均为"压迫感"取向），学生没有明确提出风格诉求时**不要默认给自定配色**；只有当需求里出现"压迫感/克制/高级/冷峻/张力"等词，或学生主动选色时，才把它作为候选呈现。企业官网类默认仍走上方"稳重商务系"。

**命名提示**：自定配色区的名字（热异常 / 暮色森林 / 界园）都是有出处的梗，不是描述性命名。用这类配色出页时，**必须先把名字背后的母题查清楚并落成视觉**（波形与削波、巨树与萤火虫、园林测绘图与印章），只做"换色的通用骨架"等于没做。
