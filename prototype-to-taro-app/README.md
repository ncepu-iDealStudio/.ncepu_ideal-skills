# prototype-to-taro-app

## 1. 这个技能是干嘛的

`prototype-to-taro-app` 把**原型**（设计图截图、HTML/CSS 代码、PRD 页面清单）转换成**可运行的 Taro 多端工程**，一套代码编译到微信小程序、支付宝小程序、H5、React Native。

Taro是一款开源的跨平台开发框架；

**核心特点：支持两种技术栈，由用户选择。**

| 分支 | 技术栈 | 适合 |
| --- | --- | --- |
| **Vue3** | Taro 4 + Vue 3 + TS + Vant + Pinia | 团队熟悉 Vue；UI 还原优先 |
| **React** | Taro 4 + React 18 + TS + Dva + Immer | 复杂业务、企业业务 App |

> 两者能力对等，**不设默认值**。技能在开工前必须让用户确认，`parse_prototype.py` 也会强制要求 `--framework` 参数。

## 2. 与参考资料的关系（重要说明）

用户曾提供两个参考脚手架，实际情况如下：

| 参考 | 现状 | 本技能的处理 |
| --- | --- | --- |
| `RealCoolSnow/taro-vue3-ts` | **仓库返回 404（已不存在）** | Vue3 分支按 **Taro 官方规范自建**，不依赖该仓库 |
| `didilinkin/elf-taro` | 存在，但锁定 **Taro 3.0.0-rc + React 16 + Dva**（2020 年） | React 分支沿用其**架构思路**（Dva + Immer + 拦截器 + 异常捕获），版本适配到 **Taro 4 + React 18** |

因此本技能的 Vue3 分支**不是**对某个仓库的复制，而是按官方规范整理；React 分支是 elf-taro 架构的现代化版本。

## 3. 技术基线

| 项 | Vue3 分支 | React 分支 |
| --- | --- | --- |
| Taro | 4.x | 4.x |
| 框架 | Vue 3.4+ | React 18 |
| 语言 | TypeScript | TypeScript |
| 状态 | Pinia | Dva + Immer |
| UI | Vant（H5）/ Vant Weapp（小程序） | taro-ui |
| 构建 | Webpack5（Taro 内置） | Webpack5（Taro 内置） |

## 4. 技能项目结构

```text
prototype-to-taro-app/
├── SKILL.md
├── README.md
└── resources/
    ├── config/
    │   ├── naming_rules.json           # 命名规则（含双框架差异）
    │   ├── dependency_baseline.json    # 双框架依赖版本基线
    │   └── design_tokens.json          # 设计 token
    ├── specifications/
    │   ├── prototype_parser_contract.md  # 原型 → context 契约
    │   └── framework_patterns.md         # 双框架代码范式对照
    ├── templates/
    │   ├── shared/        # 共用：config、请求封装、类型、mock、工程根文件
    │   ├── vue3/          # Vue3 分支：app.ts、页面、Pinia store
    │   └── react/         # React 分支：app.tsx、页面、Dva models
    ├── tools/
    │   ├── parse_prototype.py    # 原型 → proto_context.json（强制 --framework）
    │   ├── preview_plan.py       # 预览生成计划
    │   └── validate_project.py   # 工程校验（12 项）
    └── demo_output/
        ├── skill-swap-vue3/      # 示例：Vue3 分支完整工程
        └── skill-swap-react/     # 示例：React 分支完整工程
```

## 5. 工具用法

### 5.1 解析原型（必须指定框架）

```bash
# Vue3 分支
python resources/tools/parse_prototype.py 原型.html \
  --out proto_context.json \
  --project campus-skill-swap \
  --title "技能互换" \
  --framework vue3 \
  --targets weapp,h5

# React 分支
python resources/tools/parse_prototype.py 原型.html \
  --out proto_context.json \
  --project campus-skill-swap \
  --title "技能互换" \
  --framework react
```

不带 `--framework` 会直接报错：

```text
error: the following arguments are required: --framework
```

### 5.2 预览生成计划

```bash
python resources/tools/preview_plan.py proto_context.json
```

### 5.3 校验生成结果

```bash
python resources/tools/validate_project.py ./your-project
```

12 项检查：

| 检查项 | 说明 |
| --- | --- |
| config/index.ts 声明 framework | 必须是 `vue3` 或 `react` |
| app.config.ts 存在 | 页面注册入口 |
| 入口文件与框架匹配 | `app.ts` vs `app.tsx` |
| 页面已注册 | 每条 pages 都有对应文件 |
| 页面有 index.config.ts | 设置标题等 |
| 未混用框架写法 | Vue3 无 `.tsx` 页面，React 无 `.vue` 页面 |
| 统一请求封装 | `services/request.ts` 存在且配置 BASE_URL |
| 未直接 Taro.request | 页面应走 services |
| 状态管理目录 | Vue3 用 `store/`（Pinia），React 用 `models/`（Dva） |
| tabBar 合法 | 2-5 项、在 pages 中、有图标 |
| 类型定义 | `types/index.ts` |
| 三态渲染 | 取数列表页有 loading/empty |

## 6. 内置能力

| 能力 | Vue3 | React |
| --- | --- | --- |
| 登录 + token 持久化 | ✓ `store/modules/user.ts` | ✓ `models/user.ts` |
| 权限/401 跳登录 | ✓ 请求层统一处理 | ✓ 同左 |
| 请求封装（多环境） | ✓ `services/request.ts` | ✓ 同左 |
| 分页列表 + 下拉刷新 | ✓ Pinia | ✓ Dva effects |
| 空态 / 加载态 | ✓ `components/Empty` | ✓ 同左 |
| 暗黑模式 | 可用 CSS 变量实现 | 同左 |
| 全局异常捕获 | `app.onError` | `App.onError` |
| 多环境配置 | `config/dev.ts` / `prod.ts` | 同左 |

## 7. 示例产物

两个分支各有一套完整示例（`demo_output/skill-swap-*`），均已通过 `validate_project.py` 校验：

```
错误 0 项，警告 0 项
全部通过。
```

## 8. 验证情况

考虑到本机无 Node 依赖环境，做了以下验证：

| 验证项 | 结果 |
| --- | --- |
| Vue3 示例校验（12 项） | ✓ 0 错误 0 警告 |
| React 示例校验（12 项） | ✓ 0 错误 0 警告 |
| Vue 模板标签配对（5 文件） | ✓ 全部正确 |
| JSX 标签配对（6 文件，手写扫描器） | ✓ 全部正确 |
| 括号配平（44 文件） | ✓ 全部通过 |
| 解析器强制 framework | ✓ 缺失时报错 |

**未做**：`pnpm install` 与真实编译（本机无 Taro 环境与依赖）。

## 9. 与其它技能的关系

| 技能 | 目标平台 | 技术栈 |
| --- | --- | --- |
| `prototype-to-app-uniappx` | App / 小程序 / H5 | uni-app x（Vue 语法） |
| `prototype-to-flutter-app` | Android / iOS / Web | Flutter（Dart） |
| **`prototype-to-taro-app`（本技能）** | **小程序 / H5 / RN** | **Taro（Vue3 或 React）** |

小程序优先选 Taro；多端包含原生 App 且接受 Vue 语法选 uni-app x；只做 App 选 Flutter。

## 10. 相关文档

| 内容 | 路径 |
| --- | --- |
| 双框架代码范式对照 | `resources/specifications/framework_patterns.md` |
| 原型解析契约 | `resources/specifications/prototype_parser_contract.md` |
| 依赖版本基线 | `resources/config/dependency_baseline.json` |
| Taro 官方文档 | <https://docs.taro.zone/> |
