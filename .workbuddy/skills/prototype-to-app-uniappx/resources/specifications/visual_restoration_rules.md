# 视觉还原规则

本文定义如何把原型的**视觉表现**高保真地还原到 uni-app x，重点是避开 App 端渲染限制。

---

## 1. 核心差异：App 端 CSS 是 Web 的子集

这是还原失败最主要的原因。生成任何样式前，先记住三条：

### 1.1 flex 默认方向是**竖向**

```css
/* Web 习惯：默认 row */
.card { display: flex; }

/* uni-app x App 端：默认 column，横向必须显式声明 */
.card {
  display: flex;
  flex-direction: row;   /* ← 必须写 */
}
```

**自检**：任何期望"横向排列"的容器，检查是否写了 `flex-direction: row`。

### 1.2 样式**不继承**

```vue
<!-- ❌ 错误：外层 color 传不下去 -->
<view style="color: #333;">
  <text>这段文字不是 #333</text>
</view>

<!-- ✅ 正确：每个 text 自带样式 -->
<view>
  <text class="text-primary">这段文字是 #333</text>
</view>
```

字号、颜色、行高**都不会继承**。

### 1.3 文字**必须**在 `<text>` 内

```vue
<!-- ❌ 裸文字，App 端不显示 -->
<view>你好</view>

<!-- ✅ -->
<view><text>你好</text></view>
```

---

## 2. 布局方式

### 2.1 只用 flex，不用 grid

| Web | uni-app x |
|---|---|
| `display: grid; grid-template-columns: repeat(3, 1fr)` | 外层 `flex-direction: row; flex-wrap: wrap`，子项 `width: 33.33%` |
| `display: inline-block` | 不支持，用 flex |
| 浮动 `float` | 不支持，用 flex |

### 2.2 常见布局配方

**两端对齐（标题 + 操作）**

```css
.row-between {
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
```

**居中**

```css
.center {
  flex-direction: row;      /* 或 column，取决于主轴 */
  justify-content: center;
  align-items: center;
}
```

**三栏宫格**

```css
.grid {
  flex-direction: row;
  flex-wrap: wrap;
}
.grid__item {
  width: 33.33%;
  align-items: center;      /* column 方向居中 */
}
```

**固定头部 + 滚动内容**

```vue
<view class="page">
  <view class="page__header"> ... </view>
  <scroll-view class="page__body" scroll-y> ... </scroll-view>
</view>
```

```css
.page { flex: 1; flex-direction: column; }
.page__header { height: 88rpx; }
.page__body { flex: 1; }
```

---

## 3. 尺寸单位

| 场景 | 单位 | 理由 |
|---|---|---|
| 绝大多数尺寸 | `rpx` | 按 750 设计稿等比缩放 |
| 1px 细线 | `px` | `rpx` 在部分机型会被渲染成 0 |
| 导航栏高度 | `px`（44px） | 与原生一致 |
| tabBar 高度 | `px`（50px） | 与原生一致 |

**禁止**使用 `%` 做高度（父容器无确定高度时会塌陷），用 `flex: 1` 替代。

---

## 4. 文本样式

### 4.1 截断

```css
/* 单行省略 */
.title-1 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 多行省略（App 端支持 -webkit-line-clamp） */
.title-2 {
  overflow: hidden;
  text-overflow: ellipsis;
  lines: 2;                  /* uni-app x 可用 lines 属性 */
}
```

### 4.2 字号与行高

统一取自 `design_tokens.json`，通过 `uni.scss` 变量引用：

```scss
/* uni.scss */
$text-primary: #1F2225;
$font-base: 28rpx;
$font-lg: 34rpx;
$line-height-normal: 1.5;
```

```vue
<style lang="scss">
.title { font-size: $font-lg; color: $text-primary; }
</style>
```

**避免魔法数字**：不要直接写 `font-size: 31rpx`。

---

## 5. 图片

### 5.1 必须指定尺寸

```vue
<!-- ❌ 未给尺寸，可能塌陷或撑爆 -->
<image :src="item.avatar" />

<!-- ✅ -->
<image class="avatar" :src="item.avatar" mode="aspectFill" />
```

```css
.avatar { width: 88rpx; height: 88rpx; border-radius: 50%; }
```

### 5.2 mode 选择

| mode | 效果 | 适用 |
|---|---|---|
| `aspectFill` | 等比填充，裁剪 | 头像、封面（最常用） |
| `aspectFit` | 等比完整显示，留白 | 商品图、需要完整展示 |
| `scaleToFill` | 拉伸变形 | 几乎不用 |
| `widthFix` | 宽度固定，高度自适应 | 长图 |

### 5.3 原型图片不可直接引用

原型里的图片链接通常失效或跨域。处理：

1. 统一用 `static/placeholder.png` 占位
2. 或使用可访问的 CDN（需用户确认）
3. 在 `services/mock` 中集中管理图片 URL

---

## 6. 交互反馈

### 6.1 点击态

uni-app x 中 `view` 可用 `hover-class`：

```vue
<view class="btn" hover-class="btn--active" :hover-stay-time="100"> ... </view>
```

```css
.btn--active { background-color: rgba(0, 0, 0, 0.05); }
```

### 6.2 过渡动画

```css
.card {
  transition-property: transform, opacity;
  transition-duration: 150ms;
  transition-timing-function: ease-in-out;
}
```

**禁止**引入 Web 动画库（如 animate.css 的复杂 keyframes、GSAP）。用 `transition` 与 `@keyframes`（uni-app x 支持）实现。

### 6.3 安全区

底部固定元素要避让安全区：

```vue
<view class="bottom-bar"> ... </view>
```

```css
.bottom-bar {
  padding-bottom: env(safe-area-inset-bottom);
}
```

---

## 7. 还原检查清单

生成页面后逐项核对：

| # | 检查项 | 判定 |
|---|---|---|
| 1 | 每个文字都在 `<text>` 内 | 搜索模板中裸中文 |
| 2 | 每个横向容器都有 `flex-direction: row` | 检查所有 flex 容器 |
| 3 | 每个 `<text>` 自带 font-size 与 color | 检查样式表 |
| 4 | 每个 `<image>` 有明确宽高 | 检查模板 |
| 5 | 没有使用 grid / float / inline | 搜索样式表 |
| 6 | 尺寸用 rpx，未出现 % 高度 | 搜索 `height: %` |
| 7 | 有 loading 与 empty 两种状态 | 检查模板条件分支 |
| 8 | 列表项有 `:key` | 检查 `v-for` |
| 9 | 底部元素避开安全区 | 检查 `safe-area-inset-bottom` |
| 10 | 颜色/字号取自 token，无魔法数字 | 检查样式表 |

---

## 8. 与原型的取舍原则

当**完全还原**与**框架可行性**冲突时：

| 冲突 | 处理 |
|---|---|
| 原型用了 CSS Grid | 用 flex 嵌套近似，接受微小差异 |
| 原型用了 Web 专有动画 | 降级为简单 transition，并在输出中说明 |
| 原型有复杂遮罩与混合模式 | 简化为半透明纯色遮罩 |
| 原型文字溢出边界 | 用截断规则处理，不硬撑 |
| 原型图表 | 静态图或引入 uts 插件，不做纯 CSS 图表 |

**原则**：优先保证**能跑、布局不乱、信息层级清晰**，再做像素级逼近。差异要**主动告知用户**，不要静默处理。
