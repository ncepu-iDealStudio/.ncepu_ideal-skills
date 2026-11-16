# 技能互换

校园技能互换社交 App 示例（由 prototype-to-app-uniappx 技能基于原型生成）。

> 本工程为技能示例产物，采用 uni-app x（蒸汽模式 / TS），mock 数据驱动，可平滑切换真实后端。

## 技术栈

- 框架：uni-app x（蒸汽模式，Vue3 `<script setup lang="ts">`）
- 运行端：App（Android / iOS）/ 小程序 / H5
- 数据：mock 驱动（`services/mock`），统一经 `services/api` 接入

## 如何运行

1. 使用 **HBuilder 5.25+** 打开本目录
2. 运行 → 运行到浏览器（最快验证）或 运行到手机 / 模拟器
3. 若被识别为普通 uni-app 项目，检查 `manifest.json` 是否含 `"uni-app-x": {}`

## 目录结构

```text
skill-swap-demo/
├── README.md              # 本说明文档
├── App.uvue               # 全局样式与应用生命周期
├── main.ts                # Vue 应用入口（蒸汽模式）
├── pages.json             # 页面注册 + tabBar
├── manifest.json          # 应用配置（含 "uni-app-x": {}）
├── uni.scss               # 设计 token
├── pages/
│   ├── index/index.uvue   # 首页（技能列表）
│   ├── detail/detail.uvue # 技能详情
│   └── mine/mine.uvue     # 我的
├── components/
│   └── empty-state.uvue   # 空态组件
├── services/
│   ├── api/
│   │   ├── request.ts     # 请求封装（含 mock 开关）
│   │   └── skill.ts       # 技能业务接口
│   └── mock/
│       ├── delay.ts       # 模拟网络延迟
│       └── skill.mock.ts  # mock 数据（12 条）
├── types/
│   └── skill.ts           # 数据模型
├── utils/
│   ├── format.ts
│   └── validate.ts
└── static/
    └── placeholder.png
```

## 页面清单

| 页面 | 路由 | 说明 |
| --- | --- | --- |
| 首页 | `/pages/index/index` | 技能列表，下拉刷新 / 上拉加载 |
| 详情 | `/pages/detail/detail` | 技能详情 + 发起互换 |
| 我的 | `/pages/mine/mine` | 个人信息 + 设置项 |

## 对接后端 API

页面只调用 `services/api`。提供接口文档后，在对应函数内把文档字段映射成现有返回类型，再让该函数走 `request()`。设置 `BASE_URL`。尚未对接的函数继续走 mock。

不要在仍有函数未对接时把 `USE_MOCK` 改成 `false`。页面代码不用改。

## 注意事项

- 页面文件后缀为 `.uvue`，非 `.vue`
- App 端 flex 默认竖向，横向布局必须显式 `flex-direction: row`
- 文字必须包裹在 `<text>` 内，样式不继承
- 新增页面需在 `pages.json` 注册，否则不会被打包
