# 在 WorkBuddy 中使用「原型转应用」技能

> 面向第一次使用本仓库技能的同学。照着本文走完，你能从**一张设计稿或一段原型 HTML**开始，生成一套**能跑起来的移动端工程**（uni-app x 或 Flutter），并且知道后续怎么对接真实后端。
>
> 全文以「校园技能互换社交 App」为贯穿案例。

---

## 1. 这两个技能能帮你做什么

假设你手上只有这些材料中的一种：

- 设计师给的一张或几张**界面截图**
- 前端同学做好的**静态 HTML/CSS 原型**
- 一份写着页面清单和字段的 **PRD 文档**

传统做法是：照着图一个个写页面，写组件、写样式、造假数据、调交互……一个中等规模的 App 起步就要好几天。

这两个技能把这段工作自动化：

| 技能 | 产物 | 适用团队 |
| --- | --- | --- |
| `prototype-to-app-uniappx` | uni-app x 工程（App / 小程序 / H5 多端） | 要一套代码同时上小程序和 App |
| `prototype-to-flutter-app` | Flutter 工程（Android / iOS / Web / 桌面） | 只做 App，或团队已用 Flutter |

**共同点**（这是最关键的）：

1. 生成的是**完整可运行工程**，不是零散代码片段
2. 内置 **mock 数据**，后端还没好就能看到完整界面和交互
3. 预留**数据访问层接缝**，对接真实接口只改一个开关，页面代码不动

---

## 2. 安装：把技能放进 WorkBuddy

### 2.1 确认 WorkBuddy 的技能目录

WorkBuddy 从项目的 `.workbuddy/skills/` 目录加载技能。本仓库已经放好了：

```text
ncepu_ideal-skills/
└── .workbuddy/
    └── skills/
        ├── prototype-to-app-uniappx/     ← uni-app x 版
        └── prototype-to-flutter-app/     ← Flutter 版
```

每个技能目录的结构：

```text
prototype-to-app-uniappx/
├── SKILL.md              # 技能定义（AI 读这个）
├── README.md             # 人类阅读的说明
└── resources/
    ├── config/           # 命名规则、设计 token、mock 策略
    ├── specifications/   # 原型解析契约、映射规则、架构约定
    ├── templates/        # 工程骨架 + 页面模板（核心资产）
    └── tools/            # 解析、校验、预览脚本
```

### 2.2 如果 WorkBuddy 没读到技能

有两种常见做法：

**做法 A：直接在本仓库里用**（推荐新手）

用 WorkBuddy 打开 `ncepu_ideal-skills` 这个仓库目录，技能会自动被发现。

**做法 B：复制到你的项目里**

```bash
# 在你要开发的应用项目根目录执行
mkdir -p .workbuddy/skills
cp -r /path/to/ncepu_ideal-skills/.workbuddy/skills/prototype-to-flutter-app .workbuddy/skills/
```

> 💡 复制时可以**不带** `resources/demo_output/` 目录，那是示例产物，开发时用不到，能省一半体积。

### 2.3 验证安装成功

在 WorkBuddy 里问一句：

```text
我现在有哪些可用的技能？请列出和「原型转应用」相关的。
```

能说出 `prototype-to-app-uniappx` 或 `prototype-to-flutter-app`，就说明装好了。

---

## 3. 先搞清楚：你要做的是哪个

在动手前先选一个，别两个都用：

| 你的情况 | 选哪个 |
| --- | --- |
| 要同时发微信小程序 + App | ✅ uni-app x |
| 只做 Android / iOS App | ✅ Flutter |
| 团队已有 Flutter 技术栈 | ✅ Flutter |
| 团队是 Vue 技术栈 | ✅ uni-app x |
| 需要 H5 版本 | 都可，uni-app x 更顺 |

选好之后，下文只读对应那一节即可。

---

## 4. 案例背景：校园技能互换 App

**需求**：华电有 2 万学生，很多人"我会摄影想学吉他"。做一个 App 让学生互相交换技能。

**你手上有的材料**：一张首页设计图（或一段原型 HTML）。

**你期望的结果**：一个能点、能滚、能跳转的 App，先给老师看效果，后端之后再接。

---

## 5. 上手流程（通用）

不管选哪个技能，流程都是这五步：

```text
① 准备材料  →  ② 描述需求  →  ③ 确认细节  →  ④ 生成工程  →  ⑤ 运行验证
```

### 步骤 ①：准备材料

把材料放到项目里，**告诉 AI 准确路径**：

```text
design/
├── home.png          # 首页设计图
└── detail.png        # 详情页设计图
```

如果只有 HTML 原型，就放 `.html` 文件。

### 步骤 ②：描述需求（关键）

**❌ 不推荐的问法**：

```text
帮我做一个 App
```

太模糊，AI 只能瞎猜。

**✅ 推荐的问法**：

```text
请用 prototype-to-flutter-app 技能，根据 design/home.png 和 design/detail.png，
生成一个校园技能互换 App 的工程。

要求：
- 首页是技能列表（卡片：头像、标题、发布人、标签）
- 点击卡片进入详情页（大图 + 标题 + 描述 + 底部「发起互换」按钮）
- 底部两个 tab：首页、我的
- 用 mock 数据，列表至少 12 条
- 主色用设计图里的蓝色
```

**要素齐全**：技能名 + 材料路径 + 页面清单 + 交互 + 数据要求 + 视觉要求。

### 步骤 ③：确认细节

AI 会反问你一些**从图片里看不出来**的东西，比如：

```text
📋 需要你确认几件事：

1. 列表是否需要下拉刷新和上拉加载？
   [A] 都要   [B] 只要下拉刷新   [C] 都不需要

2. 空列表时显示什么？
   [A] 文字提示「还没有技能」
   [B] 文字 + 引导按钮「去发布」
   [C] 用插画

3. 详情页底部按钮点击后？
   [A] 弹确认框   [B] 直接发起请求   [C] 先跳登录
```

**认真回答**，这一步跳过会导致生成结果不符合预期。

### 步骤 ④：生成工程

AI 会按技能流程生成完整工程。以 Flutter 为例，你会得到：

```text
skill_swap_app/
├── pubspec.yaml
├── analysis_options.yaml
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/          # 主题、路由、网络、配置
│   ├── data/          # 模型、仓库、mock/remote 数据源
│   └── features/      # 首页、详情（按功能切分）
└── test/
```

### 步骤 ⑤：运行验证

**这是最容易被跳过的一步，但必须做。**

---

## 6. uni-app x 版：运行与验证

### 6.1 环境准备

1. 下载 [HBuilder](https://www.dcloud.io/hbuilderx.html)，**5.25 或更高版本**（默认新建项目是蒸汽模式）
2. 无需额外配置 Node 环境

### 6.2 运行

1. HBuilder 菜单：`文件 → 打开目录`，选中生成的工程目录
2. 顶部菜单 `运行 → 运行到浏览器`
3. 浏览器自动打开，看到首页

> ⚠️ 如果 HBuilder 提示"这不是 uni-app x 项目"，检查 `manifest.json` 里是否有这段：
>
> ```json
> "uni-app-x": {}
> ```
>
> 缺了它会被当成普通 uni-app 项目。

### 6.3 验证清单

| 检查项 | 怎么验证 |
| --- | --- |
| 页面能显示 | 首页出现 12 条 mock 卡片 |
| 滚动正常 | 列表能滚动，不卡顿 |
| 跳转正常 | 点卡片能进详情页 |
| 加载态 | 首次进入有"加载中…" |
| 空态 | 把 mock 数据改成空数组，应显示空态提示 |
| 底部 tab | 能切换「首页 / 我的」 |

### 6.4 常见问题

**问题：页面白屏，什么都没显示**

按顺序排查：

1. 文字是否直接写在 `<view>` 里？

   ```vue
   <!-- ❌ 白屏 -->
   <view>技能互换</view>

   <!-- ✅ -->
   <view><text>技能互换</text></view>
   ```

   uni-app x 的 App 端**裸文字不渲染**，必须包在 `<text>` 内。

2. 横向排列的元素是否没写方向？

   ```css
   /* App 端 flex 默认是竖向！ */
   .row {
     flex-direction: row;   /* ← 必须写 */
   }
   ```

3. 页面是否在 `pages.json` 注册了？没注册不会被打包。

**问题：文字颜色/字号不生效**

uni-app x 的**样式不继承**。父级设了 `color`，子级 `<text>` 不会继承，需要每个 `<text>` 自己写样式。

---

## 7. Flutter 版：运行与验证

### 7.1 环境准备

```bash
# 检查 Flutter 是否安装
flutter --version

# 没装的话参考官方文档：
# https://docs.flutter.dev/get-started/install
```

要求：Flutter 3.x，Dart 3.x。

### 7.2 运行

```bash
cd skill_swap_app

# 1. 拉依赖
flutter pub get

# 2. 运行（选一个设备）
flutter run                 # 自动选可用设备
flutter run -d chrome       # 跑在浏览器（最快看效果）
flutter devices             # 查看有哪些设备
```

### 7.3 验证清单

```bash
# 静态检查（应无 error）
flutter analyze

# 单元/组件测试（应通过）
flutter test
```

界面上手动验证：

| 检查项 | 预期 |
| --- | --- |
| 首页列表 | 显示 12 条 mock 卡片 |
| 下拉刷新 | 出现转圈并刷新 |
| 上拉加载 | 滚到底部触发加载 |
| 点击卡片 | 进入详情页，标题正确 |
| 详情页底部按钮 | 弹确认框 |
| 空态 | 改 mock 为空后显示空态 |

### 7.4 常见问题

**问题：`flutter pub get` 失败**

```text
Because skill_swap_app depends on http ^1.2.0 which doesn't match any versions...
```

通常是网络问题。国内环境配置镜像：

```bash
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
flutter pub get
```

**问题：`flutter analyze` 报一堆 lint 警告**

技能配置了较严格的规则（`flutter_lints` + 自定义）。**warning 不影响运行**，但建议修。想先跑起来可以忽略，后续再清。

**问题：详情页拿不到参数，显示"内容不存在"**

这是路由传参的时序问题。检查 `detail_page.dart` 里是否用 `addPostFrameCallback` 取参数——如果还不行，改成在 `didChangeDependencies` 里取。

---

## 8. 生成结果长什么样

以 uni-app x 版为例，生成的首页核心结构：

```vue
<template>
  <view class="page">
    <!-- 加载态 -->
    <view v-if="loading" class="page__loading">
      <text>加载中…</text>
    </view>

    <!-- 空态 -->
    <EmptyState v-else-if="list.length === 0" text="还没有技能" />

    <!-- 有数据 -->
    <scroll-view v-else class="page__body" scroll-y>
      <view v-for="item in list" :key="item.id" class="list-card" @tap="goDetail(item.id)">
        <image class="list-card__avatar" :src="item.avatar" mode="aspectFill" />
        <view class="list-card__body">
          <text class="list-card__title">{{ item.title }}</text>
          <text class="list-card__subtitle">{{ item.userName }}</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>
```

注意三个细节（都是技能强制要求的）：

1. **四种状态**：loading / empty / 有数据，不是只有"有数据"
2. **文字都包在 `<text>` 里**
3. **数据来自 `list`**，而 `list` 来自 `services/api`，不是硬编码

Flutter 版对应的是：

```dart
Widget _buildBody() {
  if (controller.loading) return const Center(child: CircularProgressIndicator());
  if (controller.error != null) return _buildError(controller.error!);
  if (controller.items.isEmpty) return const EmptyView(message: '还没有技能');
  return ListView.builder(...);
}
```

---

## 9. 后续：怎么对接真实后端

这是这两个技能设计的重点——**生成时就把接缝留好了**。

### 9.1 uni-app x 版

只改一个文件：`services/api/request.ts`

```ts
// 改前
export const USE_MOCK = true
export const BASE_URL = 'https://api.example.com'

// 改后
export const USE_MOCK = false
export const BASE_URL = 'https://你的后端域名.com'
```

然后核对 `services/api/skill.ts` 里的接口路径是否符合你的后端：

```ts
export async function getSkillList(page: number): Promise<Skill[]> {
  if (USE_MOCK) {
    await mockDelay()
    return mockSkillList
  }
  // 下面这行是真实请求，确认路径对吗
  return request<Skill[]>({ url: '/skills', method: 'GET', data: { page } })
}
```

**页面代码一行都不用改。**

### 9.2 Flutter 版

只改一个文件：`lib/core/config/app_config.dart`

```dart
class AppConfig {
  static const bool useMock = false;                          // ← 改这里
  static const String apiBaseUrl = 'https://你的后端域名.com';  // ← 和这里
}
```

然后核对 `lib/data/sources/remote/skill_api.dart` 的接口路径。

Repository 会自动切换数据源，Controller 和页面都不用动。

### 9.3 为什么能做到"只改一处"

因为生成时强制了分层：

```text
页面 → Controller → Repository（接口）→ 数据源
                                          ├── mock（USE_MOCK=true）
                                          └── remote（USE_MOCK=false）
```

页面只认 Repository 接口，不关心数据从哪来。这就是为什么切换时页面代码能完全不动。

---

## 10. 让 AI 帮你检查生成结果

两个技能都带了校验脚本，生成后可以让 AI 跑：

```text
请运行 validate_project.py 检查刚生成的工程，把警告和错误列出来并修复。
```

或自己跑：

```bash
# uni-app x 版
python .workbuddy/skills/prototype-to-app-uniappx/resources/tools/validate_project.py ./你的工程目录

# Flutter 版
python .workbuddy/skills/prototype-to-flutter-app/resources/tools/validate_project.py ./你的工程目录
```

**uni-app x 版检查 10 项**：页面注册、`.vue` 误用、`uni-app-x` 标记、硬编码数据、文字包裹、flex 方向、三态、图片尺寸、`:key`。

**Flutter 版检查 11 项**：pubspec 合法性、必备文件、`runApp`、features 层无 HTTP、路由注册、lint 配置、测试存在、硬编码颜色、分层目录、import 可解析、const 构造。

---

## 11. 常见疑问

### Q1：生成的界面和设计图不完全一样？

正常。技能优先保证**能跑、布局不乱、信息层级清晰**，再做像素级逼近。差异主要在：

- Web 有而 App 没有的能力（CSS Grid、复杂动画）
- 字体（设计图用的字体可能没授权或未打包）

想调整就直说："把卡片圆角改成 12，标题字号加大两号"。

### Q2：能不能直接用于生产？

生成的是**骨架**，适合：

- ✅ 快速验证需求、给客户演示
- ✅ 作为正式开发的起点
- ⚠️ 不建议直接上线 —— 缺少错误上报、埋点、性能优化、安全加固

### Q3：我只有截图，没有设计稿源文件，可以吗？

可以。技能支持图片输入，会做视觉理解提取布局。但**截图信息有限**，AI 可能问更多澄清问题，需要你配合确认。

### Q4：生成的代码风格不喜欢怎么办？

技能的设计 token 在 `resources/config/design_tokens.json`（颜色、字号、间距、圆角）。改这里，下次生成就按新规范来；已生成的工程可以直接改 `core/theme/` 里的常量。

### Q5：两个技能可以混用吗？

技术上可以（不同项目），但**同一个页面不要混**。它们的目录结构、状态管理方式完全不同，混用只会增加维护成本。

### Q6：和 `prototype-to-app-uniappx` 名字很像的 `common-website-design` 有什么区别？

| 技能 | 产物 | 用途 |
| --- | --- | --- |
| `common-website-design` | 静态 HTML 页面 | **网站**设计原型，给人看的 |
| `prototype-to-*-app` | 可运行的 App 工程 | **移动应用**，能装到手机上 |

前者是"画出来的样子"，后者是"跑起来的应用"。

---

## 12. 速查：最小上手路径

```text
1. 准备好材料（截图 / HTML / PRD），放进项目
        ↓
2. "请用 prototype-to-flutter-app 技能，
    根据 design/home.png 生成校园技能互换 App，
    首页是列表，点击进详情，用 mock 数据。"
        ↓
3. 回答 AI 的澄清问题
        ↓
4. 生成完成 → flutter pub get → flutter run
        ↓
5. 对照验证清单逐项确认
        ↓
6. 需要接后端时：改 useMock 一个开关
```

---

## 附录：相关文件

| 内容 | 路径 |
| --- | --- |
| uni-app x 技能说明 | `.workbuddy/skills/prototype-to-app-uniappx/README.md` |
| Flutter 技能说明 | `.workbuddy/skills/prototype-to-flutter-app/README.md` |
| uni-app x 工程骨架模板 | `prototype-to-app-uniappx/resources/templates/` |
| Flutter 工程骨架模板 | `prototype-to-flutter-app/resources/templates/` |
| 示例产物（uni-app x） | `prototype-to-app-uniappx/resources/demo_output/skill-swap-demo/` |
| 示例产物（Flutter） | `prototype-to-flutter-app/resources/demo_output/skill_swap_app/` |
| DSH 中使用 superpowers | `docs/dsh中使用superpowers技能.md` |
| 官方文档 | [uni-app x](https://doc.dcloud.net.cn/uni-app-x/) ・ [Flutter](https://docs.flutter.dev/) |
