# {{app_title}}

{{description}}

> 本工程由 prototype-to-app-uniappx 技能基于原型生成，采用 uni-app x（蒸汽模式 / TS）。

## 技术栈

- 框架：uni-app x（蒸汽模式，Vue3 `<script setup lang="ts">`）
- 运行端：App（Android / iOS）/ 小程序 / H5
- 数据：当前为 mock 驱动（`services/mock`），统一经 `services/api` 接入，可平滑切换真实后端

## 如何运行

1. 使用 **HBuilder 5.25+** 打开本目录
2. 运行 → 运行到浏览器（最快验证）或 运行到手机 / 模拟器
3. 若被识别为普通 uni-app 项目，检查 `manifest.json` 是否含 `"uni-app-x": {}`

## 在 VS Code 中开发（运行仍用 HBuilderX）

> 结论先说：**代码可以全程在 VS Code 里写，但编译、预览、真机调试目前仍需 HBuilderX**。uni-app x 官方只提供 HBuilderX 作为 IDE 与运行基座，没有 VS Code 扩展或 npm 脚本能直接把它跑起来。

推荐工作方式：**VS Code 负责编辑，HBuilderX 负责运行**，两个 IDE 打开同一个目录，改完文件在 HBuilderX 里重新运行即可。

### 1. 打开工程

用 VS Code 打开本目录（含 `manifest.json` 的那一层，即工程根目录），不要只打开 `pages/` 之类的子目录，否则别名与配置不生效。

### 2. 安装扩展

| 扩展 | 作用 |
| --- | --- |
| Vue - Official（Volar） | `.uvue` 的模板高亮、补全与错误提示 |
| SCSS IntelliSense | `uni.scss` 中 `$color-primary` 等变量的补全 |

### 3. 已有配置（无需手动创建）

工程已内置以下文件，保证 VS Code 里不飘红：

| 文件 | 作用 |
| --- | --- |
| `.vscode/settings.json` | 把 `*.uvue` 关联为 Vue 语法，Volar 才会生效 |
| `jsconfig.json` | 声明 `@/*` 别名指向工程根目录，`@/services/api/*` 这类导入可正常跳转 |

### 4. 如何运行

1. 用 HBuilderX 5.25+ 打开同一目录
2. 运行 → 运行到浏览器（最快）/ 运行到手机或模拟器
3. 需要看完整日志、断点调试、真机基座，都在 HBuilderX 内完成

### 5. 注意事项

- 本工程**不是 CLI 工程**，没有 `package.json`，**不要**执行 `npm install` / `npm run dev`
- VS Code 中 `uni.*` API 与 uni-app x 内置组件的类型提示较弱（完整类型由 HBuilderX 提供），属正常现象，不是配置错误
- 新增页面后要先在 `pages.json` 注册，并在 HBuilderX 重新运行才能访问

## 目录结构

{{structure}}

## 页面清单

{{pages}}

## 对接后端 API

工程已预留数据接缝，对接真实后端只需三步（**页面代码零改动**）：

1. 打开 `services/api/request.ts`，将 `USE_MOCK` 改为 `false`
2. 设置 `BASE_URL` 为你的后端域名
3. 按 `services/api/*.ts` 中的函数签名与后端接口对齐返回结构

数据流转：

```text
页面 → services/api/*.ts → USE_MOCK ?
                             ├── true  → services/mock/*（当前）
                             └── false → uni.request → 后端
```

## 注意事项

- 页面文件后缀为 `.uvue`，非 `.vue`
- App 端 flex 默认竖向，横向布局必须显式 `flex-direction: row`
- 文字必须包裹在 `<text>` 内，样式不继承
- 新增页面需在 `pages.json` 注册，否则不会被打包

<!--
模板填写说明（生成时请删除本注释块）：
- {{app_title}}   应用显示名
- {{description}} 一句话项目简介（来源 / 原型 / 主要功能）
- {{structure}}   目录结构，用 ```text 代码块呈现
- {{pages}}       页面清单，推荐表格：页面 / 路由 / 说明
-->
