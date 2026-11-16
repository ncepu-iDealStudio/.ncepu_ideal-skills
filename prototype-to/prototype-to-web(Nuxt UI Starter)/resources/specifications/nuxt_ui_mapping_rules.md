# HTML 原型 → Nuxt UI 组件映射规则

定义如何将 HTML/CSS 原型元素映射为 Nuxt UI 组件与 Tailwind 样式。

---

## 1. 布局容器

| HTML / CSS | Nuxt UI + Tailwind |
| --- | --- |
| `<div class="container">` | `<div class="mx-auto max-w-7xl px-4">` |
| `display: flex; flex-direction: row` | `<div class="flex flex-row gap-4">` |
| `display: flex; flex-direction: column` | `<div class="flex flex-col gap-4">` |
| `display: grid; grid-template-columns: repeat(3, 1fr)` | `<div class="grid grid-cols-1 md:grid-cols-3 gap-4">` |
| `justify-content: space-between` | `justify-between` |
| `align-items: center` | `items-center` |
| `flex-wrap: wrap` | `flex-wrap` |
| 固定宽度居中 | `mx-auto max-w-7xl` |

---

## 2. 基础组件映射

### 2.1 文本

| HTML | 推荐写法 |
| --- | --- |
| `<h1>` | `<h1 class="text-3xl font-bold">` |
| `<h2>` | `<h2 class="text-2xl font-semibold">` |
| `<h3>` | `<h3 class="text-xl font-semibold">` |
| `<p>` | `<p class="text-base text-muted">` |
| `<span>` | `<span>` + 工具类 |
| 强调文本 | `UText` 组件或 `font-medium text-primary` |

### 2.2 按钮

| HTML | Nuxt UI |
| --- | --- |
| `<button>` 主按钮 | `<UButton color="primary">` |
| `<button>` 次要 | `<UButton color="neutral" variant="subtle">` |
| `<a class="btn">` | `<UButton to="/path">` 或 `<NuxtLink>` |
| 图标按钮 | `<UButton icon="i-lucide-plus" aria-label="添加" />` |
| 危险操作 | `<UButton color="red">` |

### 2.3 表单

| HTML | Nuxt UI |
| --- | --- |
| `<input type="text">` | `<UInput v-model="..." />` |
| `<textarea>` | `<UTextarea v-model="..." />` |
| `<select>` | `<USelect :items="..." v-model="..." />` |
| `<input type="checkbox">` | `<UCheckbox v-model="..." />` |
| `<input type="radio">` | `<URadioGroup>` |
| `<input type="range">` | `<USlider>` |
| `<input type="file">` | `<UInput type="file" />` |
| `<form>` + 校验 | `<UForm> + <UFormField>` + `UFormGroup` |

### 2.4 数据展示

| HTML 结构 | Nuxt UI |
| --- | --- |
| 卡片 `<div class="card">` | `<UCard>` |
| 列表 `<ul><li>` | `v-for` + `UListItem` 或自定义卡片 |
| 表格 `<table>` | `<UTable :rows="..." :columns="..." />` |
| 标签 `<span class="tag">` | `<UBadge>` |
| 头像 `<img class="avatar">` | `<UAvatar src="..." />` |
| 图片 `<img>` | `<img class="rounded-lg w-full">` 或 `UAvatar` |
| 图标 | `i-lucide-*` / `i-simple-icons-*`（Iconify 语法） |
| 空状态 | 自定义 `EmptyState` 组件 + `UIcon` |

### 2.5 导航与反馈

| HTML | Nuxt UI |
| --- | --- |
| 顶部导航栏 | `<UHeader>` + `<UNavigationMenu :items="navItems">`，数据来自 `app/navigation.ts` |
| 侧边栏 | `<USidebar>` |
| 面包屑 | `<UBreadcrumb>` |
| 页脚 | `<UFooter>` |
| 下拉菜单 | `<UDropdownMenu>` |
| 分页 | `<UPagination>` |
| 模态框 | `<UModal>` |
| 抽屉 | `<UDrawer>` |
| 全局提示 | `toast.add(...)`（`useToast()`） |
| 内联提示 | `<UAlert>` |
| 确认对话框 | `<UConfirmDialog>` 或 `UModal` |

---

## 3. 状态展示

### 3.1 Loading

```vue
<UCard v-if="loading" class="animate-pulse">
  <div class="h-32 bg-muted rounded" />
</UCard>
<!-- 或 -->
<UIcon name="i-lucide-loader-2" class="animate-spin" />
```

### 3.2 Empty

```vue
<UCard class="text-center py-12">
  <UIcon name="i-lucide-inbox" class="w-12 h-12 mx-auto text-muted" />
  <p class="mt-4 text-muted">暂无数据</p>
</UCard>
```

### 3.3 Error

```vue
<UAlert color="red" :title="error" />
<UButton color="red" variant="subtle" @click="load">重试</UButton>
```

---

## 4. 交互模式映射

| 原型交互 | Nuxt 实现 |
| --- | --- |
| 点击跳转 | `<NuxtLink to="...">` 或 `useRouter().push()` |
| 点击事件 | `@click="handler"` |
| 表单提交 | `@submit.prevent="onSubmit"` |
| 下拉刷新（移动端） | `@touchstart`/`@touchend` + 自定义（Web 端通常用"重新加载"按钮） |
| 上拉加载更多 | `v-on:scroll.passive` + 滚动到底部检测，或 `useIntersectionObserver` |
| 输入防抖 | `useDebounceFn`（需 @vueuse，或手写 setTimeout） |
| 弹窗确认 | `UModal` + `v-model:open` |

---

## 5. 响应式断点

Tailwind 默认断点（与 Nuxt UI 一致）：

| 断点 | 宽度 | 用途 |
| --- | --- | --- |
| `sm` | ≥ 640px | 手机横屏 |
| `md` | ≥ 768px | 平板 |
| `lg` | ≥ 1024px | 笔记本 |
| `xl` | ≥ 1280px | 桌面 |
| `2xl` | ≥ 1536px | 大屏 |

**移动优先**：先写移动端样式，再用 `md:`/`lg:` 叠加桌面端。

---

## 6. 图片处理

原型图片链接**不可直接引用**（可能失效）。做法：

- 占位用 `UIcon` 或纯色背景块
- 网络图用 `<img>` + `loading="lazy"`，并提供 `@error` 回退
- 本地图片放 `public/` 目录，通过 `/images/xxx.png` 引用

---

## 7. 复杂样式降级

| 原型特性 | 降级方案 |
| --- | --- |
| CSS 动画 | `transition-*` / `animate-*` Tailwind 类 |
| 渐变色 | `bg-gradient-to-r from-* to-*` |
| 复杂阴影 | `shadow-md` / `shadow-lg` |
| 固定定位 | `sticky` / `fixed` |
| CSS Grid 复杂布局 | `grid` + `grid-cols-*` + `col-span-*` |

---

## 8. 命名建议

| 原型元素 | 组件命名 |
| --- | --- |
| 列表卡片 | `XxxCard` |
| 空状态 | `EmptyState` |
| 加载骨架 | `XxxSkeleton` |
| 表单项 | `XxxForm` |
| 筛选栏 | `FilterBar` |
| 确认弹窗 | `ConfirmDialog` |
