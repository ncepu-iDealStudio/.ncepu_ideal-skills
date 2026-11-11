---
name: "prototype-to-flutter-app"
description: "从原型（HTML/CSS 代码、设计图截图或 PRD 页面清单）生成符合 Flutter 官方架构指南与最佳实践的应用骨架：分层目录、路由、主题、mock 数据驱动的页面还原、可直接 flutter run 的工程。用户提到「原型转 Flutter」「设计稿做 App」「照这个页面做 Flutter」「生成 Flutter 项目」时使用。生成后可直接对接后端 API。"
---

# Prototype-to-Flutter-App Skill

## 概述

把**原型**转换成**开箱即用的 Flutter 工程**。

核心目标：

1. 按 Flutter 官方推荐的**分层架构**（UI 层 / Data 层）组织代码
2. 用 **mock 数据**驱动页面，还原布局、视觉与交互
3. 产出**能直接 `flutter run`** 的工程，无需再补脚手架
4. 数据层预留 Repository 接缝，对接后端时**只改一处**

**分层约定**（对齐 Flutter 官方 App Architecture 指南）：

```text
lib/
├── main.dart                 # 入口：runApp
├── app.dart                  # MaterialApp / 主题 / 路由装配
├── core/                     # 跨功能基础设施
│   ├── config/               # 环境配置（API baseURL、是否 mock）
│   ├── network/              # HTTP 客户端封装
│   ├── theme/                # 主题、颜色、字体、间距 token
│   ├── router/               # 路由表
│   └── utils/                # 纯函数工具
├── data/                     # 数据层
│   ├── models/               # 数据模型（fromJson / toJson）
│   ├── repositories/         # 仓库接口 + 实现（唯一对接后端的接缝）
│   └── sources/
│       ├── remote/           # 真实 API 数据源
│       └── local/mock/       # mock 数据源
└── features/                 # 功能模块（按业务切分，不是按技术层）
    └── <feature>/
        ├── <feature>_page.dart        # 页面（UI）
        ├── <feature>_controller.dart  # 状态（ChangeNotifier）
        └── widgets/                   # 该功能私有组件
```

**强制约定**：

- **按功能切分**，不按技术层平铺（不要把所有页面塞进 `pages/`、所有组件塞进 `widgets/`）
- 页面**不直接调用 HTTP**，只调 Repository
- Repository 是**唯一**数据接缝，切换 mock/真实只改 `data/sources` 与配置
- 状态用 `ChangeNotifier` + `ListenableBuilder`（官方推荐，零第三方依赖）

---

## 什么时候使用此技能

触发场景：

- 用户提供**原型 HTML/CSS**，要求转 Flutter
- 用户提供**设计图/截图**，要求照做 Flutter App
- 用户提供**PRD/页面清单**，要求生成 Flutter 工程骨架
- 用户说"这个页面用 Flutter 怎么写"、"生成一个 Flutter 项目"

**不适用**：Flutter 项目迁移改造；纯 Widget 片段问答；后端实现。

---

## 输入形态

支持三类，可混合：

| 输入 | 提取方式 | 可靠性 |
| --- | --- | --- |
| **HTML/CSS 原型代码** | 解析 DOM 结构，映射 Widget 树 | 最高 |
| **设计图 / 截图** | 视觉理解区域、层级、控件 | 中 |
| **PRD / 页面清单** | 抽取页面、字段、跳转 | 低，需补视觉决策 |

**优先级**：视觉以图片为准，结构以代码为准，业务规则以 PRD 为准。冲突时**停下来问**。

### 最小澄清清单

- 目标平台：Android / iOS / Web / 桌面？
- 页面清单与主流程：首页、关键跳转
- 视觉基调：主色、圆角、是否深色模式
- 是否需要底部导航（BottomNavigationBar）
- 状态管理偏好：默认 `ChangeNotifier`，若团队有 Riverpod/Bloc 要求需说明

---

## 关键技术决策（直接影响开箱即用）

### 1. 零重型依赖

默认只引入 **`http`**（官方推荐的最简网络库）。不默认引入：

- 状态管理框架（Provider / Riverpod / Bloc）→ 用内置 `ChangeNotifier`
- 路由框架（go_router）→ 用 `Navigator` + 命名路由
- 代码生成（json_serializable / freezed）→ 手写 `fromJson`

**理由**：依赖越少，`flutter pub get` 越不容易失败，开箱即用率越高。团队要用重型方案时再按需替换。

### 2. 状态管理用官方推荐组合

```dart
// controller
class SkillListController extends ChangeNotifier {
  final SkillRepository _repo;
  List<Skill> items = [];
  bool loading = true;

  SkillListController(this._repo);

  Future<void> load() async {
    loading = true;
    notifyListeners();
    items = await _repo.fetchSkills();
    loading = false;
    notifyListeners();
  }
}

// page
ListenableBuilder(
  listenable: controller,
  builder: (context, _) => _buildBody(controller),
)
```

### 3. 路由使用命名路由表

```dart
// core/router/app_router.dart
class AppRoutes {
  static const home = '/';
  static const detail = '/detail';
}

// app.dart
routes: {
  AppRoutes.home: (_) => const HomePage(),
  AppRoutes.detail: (_) => const DetailPage(),
},
```

跨页面传参用 `Navigator.pushNamed(context, AppRoutes.detail, arguments: id)`。

### 4. 主题集中管理

所有颜色、字号、间距集中在 `core/theme/`，页面**不写魔法数字**：

```dart
class AppColors {
  static const primary = Color(0xFF2B6DE5);
  static const background = Color(0xFFF5F6F8);
}

class AppSpacing {
  static const sm = 8.0;
  static const md = 16.0;
  static const lg = 24.0;
}
```

---

## 使用流程

### 步骤 1：解析原型 → page inventory

产出页面清单：

| 字段 | 示例 |
| --- | --- |
| `page_name` | `home` |
| `route` | `/` |
| `widget_class` | `HomePage` |
| `layout_type` | `list` / `detail` / `form` / `grid` / `profile` |
| `feature_dir` | `features/home/` |
| `data_model` | `Skill` |
| `components` | `SkillCard`, `EmptyView` |
| `interactions` | 跳转、下拉刷新、加载更多 |

机器可读中间产物按 `resources/specifications/prototype_parser_contract.md` 输出 `proto_context.json`。HTML 输入可用 `resources/tools/parse_prototype.py` 生成初稿。

### 步骤 2：确认视觉与交互

问清楚：主色、是否深色模式、底部导航项、列表是否分页、空态样式。

### 步骤 3：生成工程骨架

从 `resources/templates/project_structure/` 复制，替换占位符：

```text
{{project_name}}        工程名（snake_case，pubspec 要求）
{{app_title}}           应用显示名
{{package_name}}        Dart 包名（snake_case）
{{primary_color}}       主色
```

必生成文件：

- `pubspec.yaml`（含 `http` 依赖与 assets 声明）
- `analysis_options.yaml`（lint 规则）
- `lib/main.dart`、`lib/app.dart`
- `lib/core/{config,network,theme,router,utils}/`
- `lib/data/{models,repositories,sources}/`
- `lib/features/<feature>/`
- `test/`（至少一个可跑的 widget test）
- `README.md`
- `.gitignore`

### 步骤 4：生成页面与组件

按布局原型选模板：

| 布局 | 模板 | 说明 |
| --- | --- | --- |
| 列表 | `list_page_template.dart` | `ListView.builder` + 下拉刷新 + 加载更多 |
| 详情 | `detail_page_template.dart` | 滚动内容 + 底部操作栏 |
| 表单 | `form_page_template.dart` | `Form` + `TextFormField` + 校验 |
| 宫格 | `grid_page_template.dart` | `GridView` |
| 个人中心 | `profile_page_template.dart` | 头部 + 设置列表 |

### 步骤 5：填充 mock 数据

`data/sources/local/mock/` 下提供与真实接口**同形状**的数据：

- 列表至少 10 条，撑满一屏
- 含边界数据：超长标题、缺图、空列表
- 用 `Future.delayed` 模拟网络延迟，让 Loading 态可见

### 步骤 6：实现交互

必须覆盖：

- 页面跳转与返回
- 下拉刷新（`RefreshIndicator`）
- 上拉加载更多（`ScrollController` 监听）
- 点击反馈（`InkWell` / `Material` 水波纹）
- 轻提示（`SnackBar`）、确认弹窗（`showDialog`）
- 表单校验与提交反馈

### 步骤 7：自检

运行 `resources/tools/validate_project.py`：

- `pubspec.yaml` 可解析、依赖声明完整
- `lib/main.dart` 存在且调用 `runApp`
- 所有页面在路由表注册
- 页面未直接 `import http`
- 存在 `analysis_options.yaml`
- `test/` 至少有一个测试
- 无硬编码的主色（应走 theme）

---

## 文件结构（生成的目标工程）

```text
{{project_name}}/
├── pubspec.yaml
├── analysis_options.yaml
├── .gitignore
├── README.md
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── config/app_config.dart
│   │   ├── network/api_client.dart
│   │   ├── theme/app_colors.dart
│   │   ├── theme/app_spacing.dart
│   │   ├── theme/app_theme.dart
│   │   ├── router/app_router.dart
│   │   └── utils/formatters.dart
│   ├── data/
│   │   ├── models/skill.dart
│   │   ├── repositories/skill_repository.dart
│   │   └── sources/
│   │       ├── remote/skill_api.dart
│   │       └── local/mock/skill_mock.dart
│   └── features/
│       ├── home/
│       │   ├── home_page.dart
│       │   ├── home_controller.dart
│       │   └── widgets/skill_card.dart
│       └── detail/
│           ├── detail_page.dart
│           └── detail_controller.dart
└── test/
    └── widget_test.dart
```

---

## 对接后端 API（收尾目标）

三步切换：

### 1. 改开关

`lib/core/config/app_config.dart`：

```dart
class AppConfig {
  static const bool useMock = true;   // 改 false 走真实接口
  static const String apiBaseUrl = 'https://api.your-domain.com';
}
```

### 2. 实现远程数据源

`data/sources/remote/skill_api.dart` 已给出骨架，补上接口路径即可。

### 3. Repository 自动切换

```dart
class SkillRepositoryImpl implements SkillRepository {
  final SkillApi _api;
  final SkillMock _mock;

  @override
  Future<List<Skill>> fetchSkills() {
    return AppConfig.useMock ? _mock.fetch() : _api.fetch();
  }
}
```

**页面与 Controller 一行不用改**。

---

## 代码规范

### 命名

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 文件 | snake_case | `skill_card.dart` |
| 类 | PascalCase | `SkillCard` |
| 方法/变量 | camelCase | `fetchSkills` |
| 常量 | lowerCamelCase | `useMock` |
| 私有成员 | 下划线前缀 | `_controller` |
| 路由常量 | lowerCamelCase | `AppRoutes.home` |

### Widget 规范

- **拆分原则**：单个 `build()` 超过 80 行就抽子 Widget
- **const 优先**：能 const 的构造函数一律加 `const`（性能 + lint）
- **不用 `late` 滥用**：仅在明确需要延迟初始化时使用
- **`ListView.builder`**：长列表禁止用 `Column` + `map`
- **`Key`**：列表项建议给 `ValueKey(item.id)`

### 注释

- 中文注释
- public 类/方法用 `///` 文档注释
- 页面顶部说明：用途、数据来源、主要交互

---

## 输出格式

```text
✅ 已生成 Flutter 工程：{{project_name}}

📁 结构
├── lib/core/        基础设施（主题、路由、网络、配置）
├── lib/data/        数据层（模型、仓库、mock/remote 数据源）
└── lib/features/    {{N}} 个功能模块

🎨 已还原
- 页面：首页 / 详情（2 个）
- 组件：SkillCard、EmptyView
- 交互：下拉刷新、上拉加载、点击跳转、SnackBar 提示

▶️ 如何运行（开箱即用）
1. flutter pub get
2. flutter run
（无需额外配置；mock 数据已内置）

🔌 如何对接后端
1. lib/core/config/app_config.dart 中 useMock 改为 false
2. 设置 apiBaseUrl
3. 按 data/sources/remote/*.dart 的骨架补接口路径

⚠️ 待确认
- 详情页评论区分页规则
- 空态文案
```

---

## 错误处理与边界

### 原型含 Web 专有特性

| Web | Flutter 处理 |
| --- | --- |
| CSS Grid | `GridView` 或 `Wrap` |
| 绝对定位 | `Stack` + `Positioned` |
| CSS 动画 | `AnimatedContainer` / `Hero` / `TweenAnimationBuilder` |
| 渐变色 | `LinearGradient` |
| 复杂阴影 | `BoxShadow` |
| 图标字体 | `Icons.*` 或 `SvgPicture`（需 flutter_svg） |

### 图片资源

原型图片链接**不可直接引用**。做法：

- 占位用 `Icons.image` 或本地 `assets/images/placeholder.png`
- 网络图用 `Image.network` 并配置 `errorBuilder`
- 在 `pubspec.yaml` 声明 assets

### 无法推断时

不臆造。生成静态可看版本，把不确定项列入"待确认"，不要静默决定。

---

## 资源文件结构

```text
prototype-to-flutter-app/
├── SKILL.md
├── README.md
├── docs/
└── resources/
    ├── config/
    │   ├── naming_rules.json
    │   ├── design_tokens.json
    │   └── dependency_policy.json
    ├── specifications/
    │   ├── prototype_parser_contract.md
    │   ├── architecture_conventions.md
    │   └── widget_mapping_rules.md
    ├── templates/
    │   ├── project_structure/
    │   ├── layers/
    │   └── features/
    ├── tools/
    │   ├── parse_prototype.py
    │   ├── validate_project.py
    │   └── preview_plan.py
    └── demo_output/
```

---

## 重要提示

1. **按功能切分目录** —— 不是 `pages/`、`widgets/` 平铺
2. **页面不碰 HTTP** —— 只调 Repository，否则无法切真实接口
3. **零重型依赖** —— 默认只用 `http`，保证 `pub get` 成功率
4. **`ChangeNotifier` + `ListenableBuilder`** —— 官方推荐，无需第三方
5. **常量集中** —— 颜色/间距走 theme，不写魔法数字
6. **三态齐全** —— Loading / Empty / Error 必须有，不能只有成功态
7. **mock 要像真数据** —— 有长度、有边界、有延迟
8. **`const` 构造函数** —— 能加就加，lint 会检查
9. **`pubspec.yaml` 必须正确** —— 缩进错误直接导致 `pub get` 失败
10. **中文注释** —— 与团队习惯一致
