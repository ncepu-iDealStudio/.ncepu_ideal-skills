# prototype-to-app-uniappx

## 1. 这个技能是干嘛的

`prototype-to-app-uniappx` 是一个面向 AI 开发场景的 Skill，用于把**原型**（HTML/CSS 代码、设计图截图、PRD 页面清单）转换成**可运行的 uni-app x 工程**。

产出的是**完整脚手架**，而非零散页面：

- 用 mock 数据还原页面布局、视觉层级与交互
- 分层清晰：页面 / 组件 / 服务层分离
- `services/api` 是唯一数据接缝。按接口文档对接时，字段映射留在这一层，页面调用方式不变
- 可直接在 HBuilder 打开运行（App / 小程序 / H5）

核心价值：

1. **能看到效果** —— mock 数据撑满界面，不是空白骨架
2. **能点得动** —— 还原跳转、下拉刷新、加载更多、弹层
3. **能接后端** —— 提供接口文档后，在 `services/api` 内映射字段并切换对应函数

## 2. 适用场景

- 拿到原型/设计稿，要快速搭出 uni-app x 工程
- 需要多端（App + 小程序 + H5）同时交付
- 后端未就绪，先用 mock 演示
- 起步工程已经生成，并提供接口文档，要把真实数据接到现有页面

**不适用**：既有 uni-app（非 x）项目迁移；纯组件问答；实现后端接口。按接口文档对接前端见第 7 节。

## 3. 关键技术点

### 3.1 双模式兼容（蒸汽模式为默认）

uni-app x 在 2026 年推出**蒸汽模式**，改用 js/ts，渲染性能反超原生，官方称将逐步替代旧的 VDOM/UTS 模式。

本技能**默认输出蒸汽模式（TS）**，同时提供 uts 写法的切换说明：

| 项 | 蒸汽模式（默认） | UTS 模式 |
| --- | --- | --- |
| 入口 | `main.ts` | `main.uts` |
| 脚本块 | `<script setup lang="ts">` | `<script setup>` |
| 类型 | `.ts` | `.uts`，必须显式标注 |
| 接口 | TS `interface` | UTS `type` |

**禁止混用**：一个工程要么全 ts，要么全 uts。

### 3.2 必须遵守的框架差异

uni-app x 与 uni-app 有实质差异，踩坑会导致白屏或跑不起来：

| 差异 | 说明 |
| --- | --- |
| 页面后缀 | 必须是 `.uvue`，不是 `.vue` |
| flex 方向 | App 端**默认竖向**，横向必须显式 `flex-direction: row` |
| 样式继承 | **不继承**，每个 `<text>` 自带样式 |
| 文本渲染 | 文字**必须**在 `<text>` 内，裸文字不显示 |
| 布局 | 不支持 grid / float / inline |
| 页面注册 | 必须在 `pages.json` 注册，否则不打包 |
| 项目标记 | `manifest.json` 必须含 `"uni-app-x": {}` |

## 4. 技能项目结构

```text
prototype-to-app-uniappx/
├── SKILL.md                                # 技能定义与工作流（AI 读取）
├── README.md                               # 本文件
└── resources/
    ├── config/
    │   ├── naming_rules.json               # 命名规则（页面/组件/样式类）
    │   ├── design_tokens.json              # 设计 token（颜色/字体/间距）
    │   └── mock_policy.json                # mock 数据生成策略
    ├── specifications/
    │   ├── prototype_parser_contract.md    # 原型 → context 契约
    │   ├── page_mapping_rules.md           # HTML → 组件映射
    │   ├── visual_restoration_rules.md     # 视觉还原规则与检查清单
    │   └── api_binding.md                  # 已有工程上按接口文档对接真实数据
    ├── templates/
    │   ├── project_structure/              # 工程骨架
    │   │   ├── README.md                   # 说明文档模板（生成工程必备）
    │   │   ├── manifest.json               # 必须含 "uni-app-x": {}
    │   │   ├── pages.json                  # 页面注册 + tabBar
    │   │   ├── App.uvue / main.ts
    │   │   ├── uni.scss                    # 设计 token 变量
    │   │   ├── services/{api,mock}/        # 数据接缝
    │   │   ├── types/ utils/ components/ pages/
    │   └── pages/                          # 5 种布局原型模板
    │       ├── list_page_template.uvue
    │       ├── detail_page_template.uvue
    │       ├── form_page_template.uvue
    │       ├── grid_page_template.uvue
    │       └── profile_page_template.uvue
    ├── tools/
    │   ├── parse_prototype.py              # HTML → proto_context.json
    │   ├── validate_project.py             # 生成工程静态自检（10 项）
    │   └── preview_plan.py                 # 预览生成计划
    └── demo_output/
        └── skill-swap-demo/                # 示例：校园技能互换 App
```

## 5. 工具用法

### 5.1 解析 HTML 原型

```bash
python resources/tools/parse_prototype.py 原型.html \
  --out proto_context.json \
  --project skill-swap \
  --title "技能互换" \
  --platform app,h5
```

输出布局类型、组件、字段、交互的初稿，需核对 `diagnostics.need_confirm`。

### 5.2 预览生成计划

```bash
python resources/tools/preview_plan.py proto_context.json
```

### 5.3 校验生成结果

```bash
python resources/tools/validate_project.py ./skill-swap-demo
```

检查 11 项：

| 检查项 | 说明 |
| --- | --- |
| 含 README.md | 工程根目录必须带说明文档 |
| pages.json 存在 | 页面管理配置必需 |
| 页面文件存在 | 注册的页面必须真实存在 |
| 无 .vue 页面 | 必须是 .uvue |
| manifest 含 uni-app-x | 否则被识别为普通 uni-app |
| 页面未硬编码数据 | 应走 services/api |
| 文字在 `<text>` 内 | App 端裸文字不渲染 |
| 横向容器有 flex-direction: row | App 端默认竖向 |
| 取数页面有 loading/empty | 三态完整性 |
| image 有尺寸 | 避免布局塌陷 |
| v-for 带 :key | 列表正确性 |

> Windows 下脚本已内置 UTF-8 输出兼容（`sys.stdout.reconfigure`），GBK 控制台也不会再因 emoji 崩溃。

## 6. 生成的目标工程

```text
skill-swap/
├── README.md              # 工程说明文档（必备）
├── manifest.json          # 含 "uni-app-x": {}
├── pages.json             # 页面注册 + tabBar
├── App.uvue               # 全局样式与应用生命周期
├── main.ts                # Vue 应用入口（蒸汽模式）
├── uni.scss               # 设计 token
├── pages/
│   ├── index/index.uvue
│   ├── detail/detail.uvue
│   └── mine/mine.uvue
├── components/empty-state.uvue
├── services/
│   ├── api/{request.ts, skill.ts}    # 数据接缝
│   └── mock/{delay.ts, skill.mock.ts}
├── types/skill.ts
├── utils/{format.ts, validate.ts}
└── static/
```

## 7. 对接后端 API

起步工程保持 mock。用户提供接口文档后，按 `resources/specifications/api_binding.md` 只改 `services/api`：设置 `BASE_URL`，在对应函数内把文档字段映射成页面类型，再让该函数走 `request()`。

页面调用方式不变。不要只把全局 `USE_MOCK` 改成 `false` 就结束，也不要在页面里直接 `uni.request`。还没对上的函数继续走 mock。

```text
Page → services/api/getSkillList()
          ├── 该函数尚未对接 → services/mock
          └── 该函数已对接   → request() 解开包络 → 映射为 Skill[]
```

## 8. 运行方式

1. 用 **HBuilder 5.25+** 打开工程目录（默认蒸汽模式）
2. 运行 → 运行到浏览器（最快验证）或运行到手机
3. 若提示非 uni-app x 项目，检查 `manifest.json` 是否含 `"uni-app-x": {}`

## 9. 示例产物

`resources/demo_output/skill-swap-demo/` 是完整示例（校园技能互换 App，3 个页面 + tabBar + 12 条 mock 数据），包含根目录 `README.md` 说明文档，已通过 `validate_project.py` 全部 11 项检查。

## 10. 与 Flutter 版技能的关系

与 `prototype-to-flutter-app` 是姊妹技能，共享同一套原型解析契约设计思路：

| 项 | 本技能（uni-app x） | Flutter 版 |
| --- | --- | --- |
| 目标 | App / 小程序 / H5 多端 | Android / iOS / Web / 桌面 |
| 语言 | Vue + TS/UTS | Dart |
| 状态 | `ref` / `reactive` | `ChangeNotifier` |
| 布局约束 | flex 默认竖向、文字须在 text 内 | Widget 树、无 CSS |

按团队技术栈二选一即可。
