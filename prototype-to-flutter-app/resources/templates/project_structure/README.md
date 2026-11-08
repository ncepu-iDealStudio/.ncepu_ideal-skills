# {{app_title}}

由技能 `prototype-to-flutter-app` 根据原型生成的 Flutter 应用骨架。

## 技术栈

- Flutter（stable 渠道）
- Dart 3.x
- 状态管理：`ChangeNotifier` + `ListenableBuilder`（官方推荐，零第三方依赖）
- 网络：`http`
- 架构：UI 层 / 数据层分离，Repository 模式

## 快速开始（开箱即用）

```bash
flutter pub get
flutter run
```

默认使用 **mock 数据**，无需后端即可看到完整界面与交互。

## 项目结构

```
lib/
├── main.dart                 # 入口
├── app.dart                  # MaterialApp / 主题 / 路由
├── core/
│   ├── config/               # 环境配置（mock 开关、baseUrl）
│   ├── network/              # HTTP 封装
│   ├── theme/                # 颜色、间距、主题
│   ├── router/               # 路由常量
│   └── utils/                # 纯函数工具
├── data/
│   ├── models/               # 数据模型
│   ├── repositories/         # 仓库接口 + 实现（数据接缝）
│   └── sources/
│       ├── remote/           # 真实 API
│       └── local/mock/       # mock 数据
└── features/
    ├── home/                 # 首页（页面 + 状态 + 私有组件）
    └── detail/               # 详情页
```

## 对接后端 API

只需三步，**页面与 Controller 无需改动**：

1. 打开 `lib/core/config/app_config.dart`，把 `useMock` 改为 `false`
2. 设置 `apiBaseUrl` 为你的后端地址
3. 按 `lib/data/sources/remote/skill_api.dart` 中的骨架核对接口路径与返回结构

数据流转：

```
Page → Controller → SkillRepository(接口)
                         ├── useMock=true  → SkillMockSource
                         └── useMock=false → SkillApiSource → ApiClient → HTTP
```

## 已实现的功能

- 首页列表：mock 12 条数据，含超长标题、缺图等边界
- 三态渲染：Loading / Empty / Error（含重试）
- 下拉刷新、上拉加载更多
- 点击卡片进入详情，详情页含底部操作栏
- 主题集中管理，无魔法数字

## 测试

```bash
flutter test
```

## 代码规范

```bash
flutter analyze
```

已配置 `analysis_options.yaml`（基于 `flutter_lints`），强制 `const` 构造、单引号、避免 `print` 等最佳实践。
