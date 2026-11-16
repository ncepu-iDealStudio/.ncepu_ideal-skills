# prototype-to-flutter-app

## 1. 这个技能是干嘛的

`prototype-to-flutter-app` 是一个面向 AI 开发场景的 Skill，用于把**原型**（HTML/CSS 代码、设计图截图、PRD 页面清单）转换成**开箱即用的 Flutter 工程**。

与"给几个 Widget 示例"不同，它产出的是**完整可运行的脚手架**：

- 按 Flutter 官方 App Architecture 指南分层（UI 层 / 数据层）
- 按功能切分目录，而非按技术层平铺
- 内置 mock 数据，无需后端即可看到完整界面与交互
- Repository 模式预留数据接缝，对接后端只改一处

核心价值：

1. **开箱即用** —— `flutter pub get && flutter run` 即可看到效果
2. **还原度高** —— 布局、视觉层级、交互效果按原型还原
3. **可持续演进** —— 分层清晰，后续对接真实 API 无需重构

## 2. 适用场景

- 拿到设计稿/原型，要快速搭出 Flutter 工程骨架
- 需要给客户演示"能点"的 App，但后端还没好
- 新项目起手，需要一套符合规范的目录与分层

**不适用**：既有 Flutter 项目重构；纯 Widget 片段问答；后端接口实现。

## 3. 技术栈与关键决策

| 项 | 选择 | 理由 |
| --- | --- | --- |
| 状态管理 | `ChangeNotifier` + `ListenableBuilder` | Flutter 官方教程方案，零第三方依赖 |
| 网络 | `http` | 官方推荐，API 稳定，依赖轻 |
| 路由 | `Navigator` + 命名路由表 | 原型阶段够用，无需 go_router |
| 序列化 | 手写 `fromJson` / `toJson` | 避免引入 build_runner 与代码生成 |
| 主题 | `core/theme/` 集中管理 | 禁止魔法数字，保证一致性 |
| Lint | `flutter_lints` + 自定义规则 | 强制 const 构造、单引号等最佳实践 |

**默认零重型依赖**，最大化 `flutter pub get` 成功率 —— 这是"开箱即用"的前提。

## 4. 技能项目结构

```text
prototype-to-flutter-app/
├── SKILL.md                                # 技能定义与工作流（AI 读取）
├── README.md                               # 本文件
└── resources/
    ├── config/
    │   ├── naming_rules.json               # 命名规则（Dart/pubspec 硬约束）
    │   ├── design_tokens.json              # 设计 token（颜色/间距/字号）
    │   └── dependency_policy.json          # 依赖策略（默认/拒绝/何时引入）
    ├── specifications/
    │   ├── prototype_parser_contract.md    # 原型 → context 契约
    │   ├── architecture_conventions.md     # 分层架构与依赖方向
    │   └── widget_mapping_rules.md         # HTML → Widget 映射
    ├── templates/
    │   └── project_structure/              # 完整工程骨架（可直接复制）
    │       ├── pubspec.yaml
    │       ├── analysis_options.yaml
    │       ├── lib/
    │       │   ├── main.dart
    │       │   ├── app.dart
    │       │   ├── core/{config,network,theme,router,utils}
    │       │   ├── data/{models,repositories,sources}
    │       │   └── features/{home,detail}
    │       └── test/widget_test.dart
    ├── tools/
    │   ├── parse_prototype.py              # HTML 原型 → proto_context.json
    │   ├── validate_project.py             # 生成工程静态自检
    │   └── preview_plan.py                 # 预览生成计划
    └── demo_output/
        └── skill_swap_app/                 # 示例：校园技能互换 App
```

## 5. 工具用法

### 5.1 从 HTML 原型生成 context 初稿

```bash
python resources/tools/parse_prototype.py 原型.html \
  --out proto_context.json \
  --project skill_swap_app \
  --title "技能互换" \
  --platform android,ios
```

输出 `proto_context.json`，包含识别的布局类型、组件、字段、交互。**这是初稿**，需核对 `diagnostics.need_confirm`。

### 5.2 预览生成计划

```bash
python resources/tools/preview_plan.py proto_context.json
```

输出页面清单与将要生成的文件列表，确认无误再生成。

### 5.3 校验生成结果

```bash
python resources/tools/validate_project.py ./skill_swap_app
```

检查 11 项：pubspec 合法性、必备文件、`runApp` 调用、features 层无 http 依赖、路由注册、lint 配置、测试存在、无硬编码颜色、分层目录、import 可解析、const 构造。

加 `--json` 输出机器可读结果。

## 6. 生成的目标工程

```text
skill_swap_app/
├── pubspec.yaml                  # 依赖：仅 flutter + http
├── analysis_options.yaml         # lint 规则
├── .gitignore
├── README.md
├── lib/
│   ├── main.dart                 # runApp
│   ├── app.dart                  # MaterialApp + 路由 + 主题
│   ├── core/
│   │   ├── config/app_config.dart      # useMock 开关、baseUrl
│   │   ├── network/api_client.dart     # HTTP 封装 + ApiException
│   │   ├── theme/{app_colors,app_spacing,app_theme}.dart
│   │   ├── router/app_router.dart      # 路由常量
│   │   └── utils/{formatters,validators}.dart
│   ├── data/
│   │   ├── models/skill.dart
│   │   ├── repositories/skill_repository.dart   # 接口 + 实现
│   │   └── sources/
│   │       ├── remote/skill_api.dart
│   │       └── local/mock/skill_mock.dart
│   └── features/
│       ├── home/
│       │   ├── home_page.dart
│       │   ├── home_controller.dart
│       │   └── widgets/{skill_card,empty_view}.dart
│       └── detail/detail_page.dart
└── test/widget_test.dart
```

## 7. 对接后端 API

三步，**页面代码零改动**：

```dart
// 1. lib/core/config/app_config.dart
static const bool useMock = false;
static const String apiBaseUrl = 'https://api.your-domain.com';

// 2. 核对 lib/data/sources/remote/skill_api.dart 中的接口路径与返回结构

// 3. Repository 自动切换数据源（已实现，无需改）
```

数据流转：

```text
Page → Controller → SkillRepository（接口）
                        ├── useMock=true  → SkillMockSource
                        └── useMock=false → SkillApiSource → ApiClient → HTTP
```

## 8. 示例产物

`resources/demo_output/skill_swap_app/` 是完整示例（校园技能互换 App），已通过 `validate_project.py` 全部 11 项检查。

## 9. 与 uni-app x 版技能的关系

本技能与 `prototype-to-app-uniappx` 是姊妹技能：

| 项 | uni-app x 版 | Flutter 版（本技能） |
| --- | --- | --- |
| 目标 | 多端（App/小程序/H5） | Android/iOS/Web/桌面 |
| 语言 | Vue + TS/UTS | Dart |
| 状态 | `reactive` / `ref` | `ChangeNotifier` |
| 输入 | 同样支持三类原型 | 同样支持三类原型 |

两者共享同一套原型解析契约设计思路，可按团队技术栈二选一。
