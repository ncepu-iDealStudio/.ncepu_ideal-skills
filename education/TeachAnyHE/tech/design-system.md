# 视觉设计系统（学科门类模式）

对应 TeachAny 的 `tech/visual-stage-modes.md` 与 `tech/design-system.md`。高等教育用「学科门类 + 学位层次」替代 K-12 的「学段（小/初/高）」。原则：**专业、学术、克制**，杜绝 K-12 的糖果色与游戏化动效。

## 1. 三套学科门类模式

| 门类 | body class | 风格关键词 | 背景 | 主色/辅色/强调 |
| --- | --- | --- | --- | --- |
| **理科（数学/物理/化学）** | `teachanyhe-science` | 专业、学术、深色、克制 | 深蓝 `#0f172a` | `#60a5fa` / `#2dd4bf` / `#fbbf24` |
| **工科（计算机/通信/电气/自动化/机械）** | `teachanyhe-engineering` | 严谨、工程、清晰、浅色 | 浅灰白 `#f8fafc` | `#2563eb` / `#0891b2` / `#f59e0b` |
| **经管/文科** | `teachanyhe-econ` | 典雅、清晰、留白 | 米白 `#fdfdfa` | `#1f6f5f` / `#b8860b` / `#b5533c` |

**9 类课程 → 3 门类归属（强制，唯一口径）**：理科（`science`）＝数学、物理、化学；工科（`engineering`）＝计算机、通信、电气、自动化、机械；经管/文科（`econ`）＝经济管理、其他文科。化学类归属理科（`science`），不单独设门类；自动化、机械归属工科（`engineering`）。

**强制**：`teachanyhe-stage` meta、`body` class、`:root` 配色三者一致，不得混用。

## 2. 学位层次修饰（叠加在门类上）

| 层次 | 修饰 | 说明 |
| --- | --- | --- |
| 本科低年级 | 标准卡片、更直观图表 | 概念建立阶段，图形辅助多 |
| 本科高年级 | 更多公式区、推导步骤、仿真区 | 体系化、工程应用 |
| 研究生 | 论文引用区、开放问题区、参考文献 | 前沿、批判性 |

## 3. 设计令牌（design tokens）

### 3.1 理科（science）示例

```css
:root {
  --bg: #0f172a;               /* 深蓝背景 */
  --surface: rgba(30,41,59,.7);/* 卡片（玻璃拟态） */
  --primary: #60a5fa;          /* 浅蓝 */
  --secondary: #2dd4bf;        /* 青 */
  --accent: #fbbf24;           /* 金（公式框、重点） */
  --text: #e2e8f0;             /* 正文 */
  --muted: #94a3b8;            /* 次要 */
  --radius: 12px;
  --shadow: 0 4px 24px rgba(0,0,0,.35);
}
```

### 3.2 工科（engineering）示例

```css
:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --primary: #2563eb;
  --secondary: #0891b2;
  --accent: #f59e0b;
  --text: #0f172a;
  --muted: #64748b;
  --radius: 10px;
  --shadow: 0 2px 12px rgba(15,23,42,.08);
}
```

## 4. 高等教育特有组件

| 组件 | CSS 类 | 说明 |
| --- | --- | --- |
| **公式框** | `.formula-box` | 金/蓝强调边框、衬线字体、可居中、可编号 `(1)` |
| **推导步骤** | `.derivation` | 编号步骤、可逐步展开/折叠、当前步高亮 |
| **定理/定义** | `.theorem` / `.definition` | 学术卡片（定理带「定理」「证明」标签） |
| **证明** | `.proof` | 折叠式，默认收起，点击展开 |
| **代码块** | `.code-block` | 等宽字体、行号、语言高亮、可运行按钮 |
| **算法可视化区** | `.algo-viz` | 步骤高亮、复杂度对比 |
| **毕业要求标签** | `.graduate-attr` | 展示支撑的毕业要求指标点 |
| **参考文献区** | `.references` | 论文/教材引用（研究生课） |

## 5. 共享排版

- 正文：16px，行高 1.8，字重 400
- 公式：KaTeX 默认（行内 `\(...\)`，行间 `\[...\]`）
- 代码：`Consolas` / `SF Mono` / 等宽，14px
- 标题层级：H2 章节、H3 模块、H4 卡片
- 响应式网格：`grid-template-columns: repeat(auto-fit, minmax(280-340px, 1fr))`
- 模块间距 `margin: 40-48px 0`，卡片间距 `margin-bottom: 16-20px`
- 移动端：`@media (max-width: 600px)` 全面适配

## 6. 与 TeachAny 的对应

| TeachAny | TeachAnyHE |
| --- | --- |
| elementary（糖果色） | 经管/文科（典雅留白） |
| middle-school（蓝绿渐变） | 工科（严谨清晰浅色） |
| high-school（深蓝学术） | 理科（深色学术） |
| 学段决定视觉 | 学科门类决定视觉 + 学位层次做修饰 |
