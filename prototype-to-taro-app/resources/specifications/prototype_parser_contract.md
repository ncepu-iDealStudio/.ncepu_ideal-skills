# 原型解析契约（Taro 双框架）

定义**原型输入 → proto_context.json** 的转换契约。

---

## 1. context 结构

```json
{
  "project": {
    "project_name": "campus-skill-swap",
    "app_title": "技能互换",
    "appid": "touristappid",
    "framework": "vue3",
    "targets": ["weapp", "h5"],
    "source_type": "html"
  },
  "design": {
    "primary_color": "#2B6DE5",
    "dark_mode": false,
    "token_overrides": {}
  },
  "tab_bar": {
    "enabled": true,
    "items": [
      { "page_path": "pages/home/index", "text": "首页", "icon": "assets/tab-home.png" },
      { "page_path": "pages/mine/index", "text": "我的", "icon": "assets/tab-mine.png" }
    ]
  },
  "pages": [
    {
      "page_name": "home",
      "path": "pages/home/index",
      "title": "首页",
      "is_tab": true,
      "layout": "list",
      "components": ["Card", "Tag", "Empty"],
      "data_model": "Skill",
      "data_fields": ["id", "title", "userName", "tags"],
      "interactions": [
        { "event": "tap", "target": "Card", "action": "navigate", "to": "pages/detail/index" },
        { "event": "pull-down", "action": "refresh" },
        { "event": "reach-bottom", "action": "load-more" }
      ],
      "states": ["loading", "empty", "error", "loaded"]
    }
  ],
  "diagnostics": {
    "parse_errors": [],
    "assumptions": [],
    "need_confirm": []
  }
}
```

---

## 2. 字段约束

| 字段 | 约束 |
|---|---|
| `project_name` | kebab-case，用于目录名 |
| `framework` | **必填**，只能是 `vue3` 或 `react`（无默认值） |
| `targets` | `weapp` / `h5` / `alipay` / `rn` |
| `path` | `pages/<kebab>/index`，**不带扩展名** |
| `is_tab` | 是否 tabBar 页面 |
| `layout` | `list` / `detail` / `form` / `grid` / `profile` |
| `data_model` | PascalCase |
| `states` | 必须含 `loading` 与 `empty` |

---

## 3. 框架分支差异

同一份 context，两个框架生成不同文件：

| context 字段 | Vue3 产出 | React 产出 |
|---|---|---|
| `pages[].path` | `pages/home/index.vue` | `pages/home/index.tsx` |
| 通用配置 | `pages/home/index.config.ts` | 同左 |
| `data_model` 状态 | `store/modules/skill.ts`（Pinia） | `models/skill.ts`（Dva） |
| `config/index.ts` | `framework: 'vue3'` | `framework: 'react'` |

---

## 4. 校验规则

| 编号 | 规则 | 级别 |
|---|---|---|
| T01 | `framework` 只能是 `vue3` / `react` | error |
| T02 | `framework=vue3` 时不应存在 `.tsx` 页面 | error |
| T03 | `framework=react` 时不应存在 `.vue` 页面 | error |
| T04 | 每个页面 `path` 必须在 `app.config.ts` 的 `pages` 中 | error |
| T05 | 每个页面必须有 `index.config.ts` | error |
| T06 | tabBar 项必须在 pages 中且标记 `is_tab` | error |
| T07 | `path` 不能带扩展名 | error |
| T08 | `states` 含 loading 与 empty | warn |

---

## 5. 输入类型要点

### 5.1 设计图 / 截图

按视觉层级识别：tabBar → 顶部导航 → 内容区 → 重复单元 → 原子元素。

小程序与 Web 的差异要提前告知用户：
- 不支持 hover，用 `hover-class`
- 没有 DOM，不能用 `document`
- 滚动用 `scroll-view` 或页面级 `onReachBottom`

### 5.2 HTML / CSS

| HTML | Taro |
|---|---|
| `<div>` | `<View>` |
| `<span>` / 文本 | `<Text>` |
| `<img>` | `<Image>` |
| `<input>` | `<Input>` |
| `<ul><li>` | `v-for` / `map` + `View` |
| 固定底部 | `fixed` + `env(safe-area-inset-bottom)` |

### 5.3 PRD / 页面清单

提取页面名、跳转关系、字段清单。PRD 无视觉信息时用 `design_tokens.json` 默认值并告知用户。

---

## 6. 歧义处理

| 情况 | 处理 |
|---|---|
| 用户没说框架 | **必须问**，不假设 |
| 页面字段缺失 | 按通用模板推断并标注待确认 |
| 是否需要 tabBar 不明 | 默认按"有 tabBar"生成，标注可去掉 |
| 目标平台不明 | 默认 `weapp` + `h5`，标注可增删 |

---

## 7. 最小可用 context

```json
{
  "project": {
    "project_name": "demo-app",
    "app_title": "演示",
    "appid": "touristappid",
    "framework": "vue3",
    "targets": ["weapp"],
    "source_type": "html"
  },
  "pages": [
    {
      "page_name": "home",
      "path": "pages/home/index",
      "title": "首页",
      "is_tab": false,
      "layout": "list",
      "components": ["Empty"],
      "data_model": "Item",
      "data_fields": ["id", "title"],
      "interactions": [],
      "states": ["loading", "empty", "loaded"]
    }
  ],
  "tab_bar": { "enabled": false, "items": [] }
}
```
