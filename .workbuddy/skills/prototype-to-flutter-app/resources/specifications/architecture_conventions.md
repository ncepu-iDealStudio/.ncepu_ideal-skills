# 架构约定（对齐 Flutter 官方 App Architecture）

本文定义生成工程的分层规则，确保符合官方推荐且便于后续演进。

参考：https://docs.flutter.dev/app-architecture/guide

---

## 1. 三层职责

```text
UI 层（features/）        ← 只负责展示与交互
   ↓ 调用
数据层（data/）           ← Repository 抽象 + 数据源
   ↓ 依赖
基础设施（core/）         ← 网络、主题、路由、配置
```

### UI 层

| 组成 | 职责 | 禁止 |
|---|---|---|
| `*_page.dart` | 组装 Widget、绑定事件、监听状态 | 直接发 HTTP、写业务规则 |
| `*_controller.dart` | 持有状态、调用 Repository、`notifyListeners` | 引用 `BuildContext`、操作 UI |
| `widgets/` | 该功能私有组件 | 感知数据来源 |

**关键**：Controller **不持有 BuildContext**，UI 单向依赖 Controller。

### 数据层

| 组成 | 职责 |
|---|---|
| `models/` | 不可变数据模型 + `fromJson` / `toJson` |
| `repositories/` | **接口** + **实现**，实现里决定走 mock 还是 remote |
| `sources/remote/` | 真实 API 调用 |
| `sources/local/mock/` | mock 数据 |

**Repository 是唯一接缝**：页面与 Controller 只依赖 `Repository` 接口，不依赖具体数据源。

### 基础设施

| 组成 | 职责 |
|---|---|
| `core/config` | 环境开关（useMock）、baseUrl |
| `core/network` | `http` 封装、统一错误处理 |
| `core/theme` | 颜色、间距、字体、ThemeData |
| `core/router` | 路由常量与路由表 |
| `core/utils` | 纯函数（格式化、校验） |

---

## 2. 依赖方向（严格单向）

```text
features  →  data  →  core
    │          │        ↑
    └──────────┴────────┘
```

禁止：

- `core` 反向依赖 `features` 或 `data`
- `data` 依赖 `features`
- 同一 feature 的组件被另一个 feature 直接 import（应上提到 `core` 或共享 feature）

---

## 3. 按功能切分，不按技术层切分

### ✅ 正确

```text
features/
├── home/
│   ├── home_page.dart
│   ├── home_controller.dart
│   └── widgets/skill_card.dart
└── detail/
    ├── detail_page.dart
    └── detail_controller.dart
```

一个功能的页面、状态、私有组件**放在一起**。

### ❌ 错误

```text
pages/
├── home_page.dart
└── detail_page.dart
controllers/
├── home_controller.dart
└── detail_controller.dart
widgets/
├── skill_card.dart
└── empty_view.dart
```

按技术层平铺会导致：改一个功能要跨 3 个目录、删除功能易留死代码、多人协作冲突高。

### 什么时候上提到共享位置

组件被 **2 个以上 feature** 使用时，移到 `core/widgets/`（本技能默认不建该目录，按需新增）。

---

## 4. 状态管理约定

### 标准写法

```dart
class HomeController extends ChangeNotifier {
  HomeController(this._repository);

  final SkillRepository _repository;

  List<Skill> items = const [];
  bool loading = true;
  String? error;

  Future<void> load() async {
    loading = true;
    error = null;
    notifyListeners();

    try {
      items = await _repository.fetchSkills();
    } catch (e) {
      error = e.toString();
    } finally {
      loading = false;
      notifyListeners();
    }
  }
}
```

页面侧：

```dart
class _HomePageState extends State<HomePage> {
  late final HomeController _controller;

  @override
  void initState() {
    super.initState();
    _controller = HomeController(widget.repository);
    _controller.load();
  }

  @override
  void dispose() {
    _controller.dispose();   // 必须释放
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: _controller,
      builder: (context, _) => _buildBody(),
    );
  }
}
```

### 强制规则

1. **必须 `dispose()`** Controller，否则内存泄漏
2. 状态变更后**必须** `notifyListeners()`
3. 不要在 `build()` 里调用 `load()`
4. 不允许 Controller 持有 `BuildContext`

---

## 5. 路由约定

```dart
// core/router/app_router.dart
class AppRoutes {
  static const home = '/';
  static const detail = '/detail';
  static const profile = '/profile';
}
```

注册：

```dart
// app.dart
routes: {
  AppRoutes.home: (context) => const HomePage(),
  AppRoutes.detail: (context) => const DetailPage(),
},
```

传参：

```dart
Navigator.pushNamed(context, AppRoutes.detail, arguments: skillId);

// 接收
final skillId = ModalRoute.of(context)!.settings.arguments as int?;
```

**新增页面必须同步注册**，否则 `pushNamed` 运行时报错。

---

## 6. 错误处理约定

### 网络层

`core/network/api_client.dart` 统一抛出 `ApiException`：

```dart
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  ApiException(this.message, {this.statusCode});
}
```

### Controller 层

捕获后写入 `error` 字段，UI 据此展示错误态：

```dart
try {
  items = await _repository.fetchSkills();
} catch (e) {
  error = e is ApiException ? e.message : '加载失败，请重试';
} finally {
  loading = false;
  notifyListeners();
}
```

### UI 层

三态 + 错误重试：

```dart
if (controller.loading) return const Center(child: CircularProgressIndicator());
if (controller.error != null) return ErrorView(message: controller.error!, onRetry: controller.load);
if (controller.items.isEmpty) return const EmptyView();
return ListView.builder(...);
```

---

## 7. 测试约定

至少提供一个可跑的 widget test：

```dart
testWidgets('首页渲染标题', (tester) async {
  await tester.pumpWidget(const MyApp());
  expect(find.text('技能互换'), findsWidgets);
});
```

要求：

- `flutter test` 必须能通过
- 不依赖真实网络（mock 数据源）
- 关键交互（如点击跳转）建议补测试

---

## 8. 性能约定

| 规则 | 原因 |
|---|---|
| 长列表用 `ListView.builder` | 懒加载，避免一次构建全部 |
| 能 `const` 的 Widget 一律 `const` | 减少重建 |
| 图片指定 `width` / `height` | 避免布局跳动 |
| 避免在 `build()` 中做重计算 | 每次重建都会执行 |
| `AnimatedBuilder` 只包需要动画的部分 | 缩小重建范围 |
