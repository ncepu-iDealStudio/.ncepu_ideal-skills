# Widget 映射规则

原型结构 → Flutter Widget 的映射，以及布局原型的选型规则。

---

## 1. 布局原型选型

| 布局原型 | 判断依据 | 模板 | 典型页面 |
|---|---|---|---|
| `list` | 可滚动的重复单元 | `list_page_template.dart` | 信息流、商品列表 |
| `detail` | 单体内容 + 图文 + 底部操作 | `detail_page_template.dart` | 文章、商品详情 |
| `form` | 多个输入项 + 提交 | `form_page_template.dart` | 编辑、新建、反馈 |
| `grid` | 宫格入口 | `grid_page_template.dart` | 首页金刚区 |
| `profile` | 用户信息头 + 设置项 | `profile_page_template.dart` | 我的 |
| `custom` | 以上不符 | 自由组合 | 地图、聊天 |

**判断顺序**：大量重复单元 → list/grid；有输入项 → form；单体内容 → detail。

---

## 2. HTML → Flutter 对照

| HTML / CSS | Flutter |
|---|---|
| `<div>` | `Container` / `Padding` / `Column` |
| `display:flex; flex-direction:row` | `Row` |
| `display:flex; flex-direction:column` | `Column` |
| `justify-content: space-between` | `MainAxisAlignment.spaceBetween` |
| `align-items: center` | `CrossAxisAlignment.center` |
| `flex: 1` | `Expanded` |
| `padding` | `Padding` / `EdgeInsets` |
| `margin` | `Padding` 包裹或 `Container(margin:)` |
| `width/height` | `SizedBox` |
| `border-radius` | `BorderRadius.circular()` |
| `box-shadow` | `BoxShadow` in `BoxDecoration` |
| `background-color` | `color:` / `BoxDecoration(color:)` |
| `background: linear-gradient` | `LinearGradient` |
| `display: grid` | `GridView` / `Wrap` |
| `position: absolute` | `Stack` + `Positioned` |
| `overflow: hidden` | `ClipRRect` / `ClipRect` |
| `<img>` | `Image.network` / `Image.asset` |
| `<button>` | `ElevatedButton` / `TextButton` / `InkWell` |
| `<input>` | `TextField` / `TextFormField` |
| `<ul><li>` | `ListView.builder` |
| 固定顶部栏 | `AppBar` |
| 固定底部栏 | `bottomNavigationBar` / `Column` + `Expanded` + 底栏 |
| `:hover` / `:active` | `InkWell` 水波纹 / `GestureDetector` |
| `@keyframes` | `AnimatedContainer` / `TweenAnimationBuilder` |

---

## 3. 常见布局配方

### 3.1 页面骨架（有 AppBar）

```dart
Scaffold(
  appBar: AppBar(title: const Text('首页')),
  body: _buildBody(),
)
```

### 3.2 页面骨架（底部导航）

```dart
Scaffold(
  body: IndexedStack(index: _currentIndex, children: _pages),
  bottomNavigationBar: NavigationBar(
    selectedIndex: _currentIndex,
    onDestinationSelected: (i) => setState(() => _currentIndex = i),
    destinations: const [
      NavigationDestination(icon: Icon(Icons.home), label: '首页'),
      NavigationDestination(icon: Icon(Icons.person), label: '我的'),
    ],
  ),
)
```

### 3.3 横向卡片（图片 + 文字）

```dart
Card(
  child: Padding(
    padding: const EdgeInsets.all(AppSpacing.md),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(AppRadius.md),
          child: SizedBox(
            width: AppSizing.avatarMd,
            height: AppSizing.avatarMd,
            child: Image.network(item.avatar, fit: BoxFit.cover),
          ),
        ),
        const SizedBox(width: AppSpacing.md),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(item.title, maxLines: 2, overflow: TextOverflow.ellipsis),
              const SizedBox(height: AppSpacing.xs),
              Text(item.userName, style: ...),
            ],
          ),
        ),
      ],
    ),
  ),
)
```

### 3.4 三态渲染

```dart
Widget _buildBody() {
  if (controller.loading) {
    return const Center(child: CircularProgressIndicator());
  }
  if (controller.error != null) {
    return ErrorView(message: controller.error!, onRetry: controller.load);
  }
  if (controller.items.isEmpty) {
    return const EmptyView(message: '暂无内容');
  }
  return ListView.builder(
    itemCount: controller.items.length,
    itemBuilder: (context, index) => SkillCard(item: controller.items[index]),
  );
}
```

### 3.5 下拉刷新 + 加载更多

```dart
RefreshIndicator(
  onRefresh: controller.refresh,
  child: ListView.builder(
    controller: _scrollController,
    itemCount: controller.items.length + (controller.hasMore ? 1 : 0),
    itemBuilder: (context, index) {
      if (index == controller.items.length) {
        return const Padding(
          padding: EdgeInsets.all(16),
          child: Center(child: CircularProgressIndicator()),
        );
      }
      return SkillCard(item: controller.items[index]);
    },
  ),
)
```

`ScrollController` 监听接近底部时触发 `loadMore()`。

---

## 4. 字段 → Dart 类型

| 字段特征 | 类型 | 示例 |
|---|---|---|
| `id` / `*Id` | `int` | `final int id;` |
| `count` / `total` / `num` | `int` | `final int count;` |
| `price` / `amount` / `rating` | `double` | `final double rating;` |
| `is*` / `has*` | `bool` | `final bool isActive;` |
| `*At` / `time` / `date` | `DateTime` | `final DateTime createdAt;` |
| `tags` / `list` / `items` | `List<String>` / `List<T>` | `final List<String> tags;` |
| 其余 | `String` | `final String title;` |

**可空性**：后端可能不返回的字段用 `String?`，并在 UI 侧做兜底。

---

## 5. 图片处理

| 场景 | 做法 |
|---|---|
| 网络图 | `Image.network(url, errorBuilder: ...)` |
| 本地占位 | `Image.asset('assets/images/placeholder.png')` |
| 圆形头像 | `ClipOval` + `SizedBox` |
| 圆角图片 | `ClipRRect(borderRadius: ...)` |
| 骨架占位 | `Image.network(..., loadingBuilder: ...)` |

**必须给 `width` / `height` 或 `fit`**，否则可能布局异常。

---

## 6. 交互映射

| 原型行为 | Flutter 实现 |
|---|---|
| 点击跳转 | `Navigator.pushNamed(context, AppRoutes.detail)` |
| 返回 | `Navigator.pop(context)` |
| 切换 Tab | `setState` + `IndexedStack` |
| 下拉刷新 | `RefreshIndicator` |
| 上拉加载 | `ScrollController` + 判断 `position.pixels` |
| 轻提示 | `ScaffoldMessenger.of(context).showSnackBar(...)` |
| 确认弹窗 | `showDialog` + `AlertDialog` |
| 底部操作表 | `showModalBottomSheet` |
| 长按 | `GestureDetector(onLongPress:)` |
| 输入 | `TextField` + `TextEditingController`（记得 `dispose`） |

---

## 7. 组件拆分原则

满足任一即拆：

1. 同一结构在 **2 个以上页面**出现
2. 单个 `build()` 超过 **80 行**
3. 有独立交互逻辑

组件放哪：

- 只被**一个 feature** 用 → `features/<feature>/widgets/`
- 被**多个 feature** 用 → `core/widgets/`
