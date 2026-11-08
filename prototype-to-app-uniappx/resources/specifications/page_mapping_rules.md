# 页面与组件映射规则

本文定义**原型结构 → uni-app x 组件**的映射关系，以及页面布局原型的选型规则。

---

## 1. 布局原型选型

先判断页面属于哪种布局原型，再选对应模板。选错会导致结构别扭、后续难改。

| 布局原型 | 判断依据 | 模板 | 典型页面 |
|---|---|---|---|
| `list` | 主体是可滚动的重复单元 | `list_page_template.uvue` | 信息流、商品列表、消息 |
| `detail` | 单体内容 + 图文混排 + 底部操作 | `detail_page_template.uvue` | 文章详情、商品详情 |
| `form` | 多个输入项 + 提交按钮 | `form_page_template.uvue` | 编辑资料、新建、反馈 |
| `grid` | 宫格式功能入口 | `grid_page_template.uvue` | 首页金刚区、分类 |
| `profile` | 用户信息头 + 设置项列表 | `profile_page_template.uvue` | 我的、个人中心 |
| `custom` | 以上都不符合 | 自行组合 | 地图页、聊天、播放器 |

**判断顺序**：先看是否有大量重复单元（→ list/grid）→ 再看是否有输入项（→ form）→ 再看是否单体内容（→ detail）。

---

## 2. HTML 元素 → uni-app x 组件

| HTML | uni-app x | 注意事项 |
|---|---|---|
| `<div>` | `<view>` | 默认 block，flex 容器 |
| `<span>` / 文本节点 | `<text>` | **文字必须包在 text 内** |
| `<p>` / `<h1>`-`<h6>` | `<text>` + class 控制字号 | 无默认层级样式 |
| `<img>` / `<image>` | `<image>` | 必须给宽高；用 `mode` 控制填充 |
| `<button>` | `<button>` 或 `<view>` + `@tap` | 需要原生按钮样式时用前者 |
| `<input>` | `<input>` | 不能设置宽高为百分比之外的奇怪值 |
| `<textarea>` | `<textarea>` | |
| `<ul>` / `<ol>` / `<li>` | `<view>` + `v-for` | 无列表语义 |
| `<a href>` | `<navigator>` 或 `@tap` + `uni.navigateTo` | 推荐后者，便于参数处理 |
| `<video>` | `<video>` | |
| `<canvas>` | `<canvas>` | 图表建议用插件 |
| `<scroll-view>` 场景 | `<scroll-view>` | 长列表必须用，页面本身不滚动时配合 `scroll-y` |
| `<hr>` | `<view class="divider">` | |
| `<svg>` | `<image src="xxx.svg">` | 内联 svg 支持有限 |

---

## 3. 常见页面区域的标准写法

### 3.1 页面根容器

```vue
<template>
  <view class="page">
    <!-- 内容 -->
  </view>
</template>

<style>
.page {
  flex: 1;
  flex-direction: column;   /* App 端默认即 column，显式写出避免歧义 */
  background-color: #F5F6F8;
}
</style>
```

### 3.2 顶部导航

方案 A：用原生导航栏（`pages.json` 配置 `navigationBarTitleText`），页面内不写。

方案 B：自定义导航栏（需要高度定制时），在 `pages.json` 设 `"navigationStyle": "custom"`，页面内留出状态栏高度。

**推荐方案 A**，除非原型明显是沉浸式设计。

### 3.3 底部 tabBar

优先用 `pages.json` 的 `tabBar` 原生配置。需要特殊样式（如中间凸起按钮）时，用 `uni-tab-bar` 组件。

### 3.4 列表项

```vue
<view class="skill-card" @tap="goDetail(item.id)">
  <image class="skill-card__avatar" :src="item.avatar" mode="aspectFill" />
  <view class="skill-card__body">
    <text class="skill-card__title">{{ item.title }}</text>
    <text class="skill-card__subtitle">{{ item.userName }}</text>
  </view>
</view>
```

要点：

- 卡片本身是 `flex-direction: row`（**必须显式写**）
- 文字用 `<text>`，不裸写
- 图片必须给固定宽高，避免布局跳动

---

## 4. 数据字段 → 类型推断

| 字段名特征 | 推断类型 | 示例 |
|---|---|---|
| `id` / `*_id` / `*Id` | `number` 或 `string` | `id: number` |
| `count` / `num` / `total` | `number` | `count: number` |
| `is_*` / `has_*` / `*ed` | `boolean` | `isDeleted: boolean` |
| `price` / `amount` | `number` | `price: number` |
| `time` / `date` / `*At` | `string`（ISO 或格式化字符串） | `createdAt: string` |
| `avatar` / `image` / `icon` / `url` | `string` | `avatar: string` |
| `tags` / `list` / `items` | `string[]` 或 `T[]` | `tags: string[]` |
| 其余 | `string` | `title: string` |

**不确定时用 `string`**，并在输出中标注待确认。

---

## 5. 交互 → 事件绑定

| 原型行为 | uni-app x 实现 |
|---|---|
| 点击进入详情 | `@tap="uni.navigateTo({ url: '/pages/detail/detail?id=' + item.id })"` |
| 切换 tab | `uni.switchTab({ url })` |
| 返回 | `uni.navigateBack()` |
| 下拉刷新 | `pages.json` 中 `enablePullDownRefresh: true` + `onPullDownRefresh()` + `uni.stopPullDownRefresh()` |
| 上拉加载 | `onReachBottom()` |
| 轻提示 | `uni.showToast({ title, icon: 'none' })` |
| 确认弹窗 | `uni.showModal({ content, success })` |
| 底部操作面板 | `uni.showActionSheet` |
| 长按 | `@longpress` |
| 表单提交 | `@tap` 或 `<form @submit>` |

---

## 6. 状态管理

每个数据页面**必须**实现四种状态：

```vue
<template>
  <view class="page">
    <!-- 加载中 -->
    <view v-if="loading" class="page__loading">
      <text>加载中…</text>
    </view>

    <!-- 空态 -->
    <EmptyState v-else-if="list.length === 0" text="还没有内容" />

    <!-- 有数据 -->
    <view v-else>
      <view v-for="item in list" :key="item.id"> ... </view>
    </view>
  </view>
</template>
```

| 状态 | 触发 | 表现 |
|---|---|---|
| `loading` | 首次进入 / 刷新 | 骨架屏或文字提示 |
| `empty` | 请求成功但数组为空 | 空态组件 + 引导文案 |
| `error` | 请求失败 | 错误提示 + 重试按钮 |
| `loaded` | 有数据 | 正常渲染 |

**只实现 loaded 态是最常见的问题**，必须在自检中拦截。

---

## 7. 组件拆分原则

满足以下任一条件就拆成组件：

1. 同一结构在 **2 个以上页面**出现
2. 单文件超过 **300 行**
3. 有明显的**独立交互**（如一个完整的评论输入区）

组件命名与职责：

| 组件 | 职责 |
|---|---|
| `nav-bar.uvue` | 自定义顶部导航（需要时） |
| `empty-state.uvue` | 空态展示，接收文案与图标 props |
| `loading-skeleton.uvue` | 骨架屏 |
| `*-card.uvue` | 列表项卡片，接收 item props |
| `tag.uvue` | 标签 |

**组件不感知数据来源** —— 只接收 props、抛事件，不 import services。
