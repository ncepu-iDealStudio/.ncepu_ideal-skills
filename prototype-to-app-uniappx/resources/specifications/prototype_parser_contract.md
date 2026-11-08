# 原型解析契约（Prototype Parser Contract）

本文定义**原型输入 → 中间语义（proto_context.json）**的转换契约。所有页面生成必须基于该 context，不允许跳过。

---

## 1. 设计目标

1. 把 HTML 结构、设计图理解结果、PRD 文字统一为**同一份语义中间产物**
2. 让页面生成只依赖 context，不直接耦合原始输入
3. context 可被工具校验、可被人工审查、可 diff、可作为快照基线

---

## 2. context 结构

```json
{
  "project": {
    "project_name": "skill-swap",
    "app_title": "技能互换",
    "appid": "__UNI__XXXXXXX",
    "target_platforms": ["app", "h5"],
    "compile_mode": "vapor",
    "source_type": "html"
  },
  "design": {
    "primary_color": "#2B6DE5",
    "radius_style": "md",
    "theme": "light",
    "token_overrides": {}
  },
  "pages": [
    {
      "page_name": "index",
      "page_path": "pages/index/index.uvue",
      "route": "/pages/index/index",
      "title": "技能互换",
      "is_tab": true,
      "is_home": true,
      "layout_type": "list",
      "components": ["nav-bar", "skill-card", "empty-state"],
      "data_fields": ["id", "title", "tags", "avatar", "userName"],
      "interactions": [
        { "event": "tap", "target": "skill-card", "action": "navigate", "to": "/pages/detail/detail" },
        { "event": "pull-down", "action": "refresh" },
        { "event": "reach-bottom", "action": "load-more" }
      ],
      "states": ["loading", "empty", "error", "loaded"]
    }
  ],
  "tab_bar": {
    "enabled": true,
    "items": [
      { "page_path": "pages/index/index", "text": "首页", "icon": "static/tab-home.png" },
      { "page_path": "pages/mine/mine", "text": "我的", "icon": "static/tab-mine.png" }
    ]
  },
  "diagnostics": {
    "parse_errors": [],
    "assumptions": [],
    "need_confirm": []
  }
}
```

---

## 3. 字段定义

### 3.1 `project`

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `project_name` | string | 是 | kebab-case，用于工程目录名 |
| `app_title` | string | 是 | 应用显示名 |
| `appid` | string | 是 | `__UNI__` 开头；未知时用 `__UNI__PROTOTYPE` |
| `target_platforms` | string[] | 是 | `app` / `h5` / `mp-weixin` 等 |
| `compile_mode` | string | 是 | `vapor`（蒸汽模式，默认）或 `vdom` |
| `source_type` | string | 是 | `html` / `image` / `prd` / `mixed` |

### 3.2 `pages[]`

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `page_name` | string | 是 | kebab-case 页面标识 |
| `page_path` | string | 是 | 必须 `pages/<name>/<name>.uvue` |
| `route` | string | 是 | 必须与 `page_path` 去掉 `.uvue` 后一致 |
| `title` | string | 是 | 导航栏标题 |
| `is_tab` | boolean | 是 | 是否为 tabBar 页面 |
| `is_home` | boolean | 是 | 是否为首页（`pages.json` 数组第一项） |
| `layout_type` | enum | 是 | `list` / `detail` / `form` / `grid` / `profile` / `custom` |
| `components` | string[] | 是 | 该页需要的组件文件名词干 |
| `data_fields` | string[] | 是 | 页面渲染所需的数据字段 |
| `interactions` | object[] | 否 | 交互行为清单 |
| `states` | string[] | 是 | 必须覆盖 `loading` 与 `empty` |

### 3.3 `interactions[]`

| 字段 | 类型 | 说明 |
|---|---|---|
| `event` | string | `tap` / `pull-down` / `reach-bottom` / `submit` / `long-press` |
| `target` | string | 触发元素（组件名或 class） |
| `action` | string | `navigate` / `switch-tab` / `back` / `refresh` / `load-more` / `toast` / `modal` |
| `to` | string | `action` 为跳转时的目标路由 |

---

## 4. 校验规则（强制）

`validate_project.py` 会对 context 与生成产物检查以下项：

| 编号 | 规则 | 级别 |
|---|---|---|
| P01 | `page_path` 后缀必须是 `.uvue` | error |
| P02 | `route` 必须与 `page_path` 去掉后缀一致 | error |
| P03 | 每个 `page_path` 必须在 `pages.json` 的 `pages` 中注册 | error |
| P04 | `is_home` 的页面必须是 `pages` 数组第一项 | error |
| P05 | `states` 必须含 `loading` 与 `empty` | error |
| P06 | `is_tab=true` 的页面必须出现在 `tabBar.list` | error |
| P07 | `compile_mode` 只能是 `vapor` 或 `vdom` | error |
| P08 | `data_fields` 非空 | warn |

---

## 5. 解析优先级

同一信息在多种输入中冲突时：

```text
视觉表现（图片/截图）  >  结构层级（HTML 代码）  >  业务规则（PRD 文字）
```

冲突处理原则：

- **不自行裁决**，写入 `diagnostics.need_confirm`
- 暂时按优先级取高者生成，并在输出中明确标注
- 用户确认后再修正

---

## 6. 各输入类型的解析要点

### 6.1 HTML / CSS 原型

| HTML 特征 | 映射为 |
|---|---|
| 顶层多个同级区块 | 按纵向堆叠，对应页面 `view` 子块 |
| `display: flex; flex-direction: row` | 保持横向，**显式**写出 |
| `display: grid` | 拆为嵌套 flex（App 端不支持 grid） |
| `<img>` | `<image mode="aspectFill">` |
| `<button>` / 可点 `div` | `<view>` + `@tap`，或用 `<button>` |
| `<input>` / `<textarea>` | `<input>` / `<textarea>` |
| `<ul><li>` 重复结构 | `v-for` 列表 + 单项组件 |
| 固定在顶/底的导航 | `<view class="fixed">` 或页面 `navigationStyle` |

### 6.2 设计图 / 截图

按视觉层级识别：

1. 先划分**大区块**（顶部导航 / 内容区 / 底部 tab）
2. 再识别区块内**重复单元**（卡片、列表项）
3. 最后识别**原子元素**（文字、图标、按钮、标签）

识别不确定时，写入 `need_confirm`，不要猜。

### 6.3 PRD / 页面清单

从文字中提取：

- 页面名与用途 → `pages[]`
- 页面间跳转描述 → `interactions[]`
- 字段清单 → `data_fields[]`（需补类型，见 `page_mapping_rules.md`）

PRD 通常**不含视觉信息**，必须用 `design_tokens.json` 默认值，并明确告知用户"视觉为默认风格，请确认或提供设计稿"。

---

## 7. 最小可用 context

时间紧张时，至少提供：

```json
{
  "project": { "project_name": "...", "app_title": "...", "appid": "__UNI__PROTOTYPE",
               "target_platforms": ["h5"], "compile_mode": "vapor", "source_type": "html" },
  "pages": [
    { "page_name": "index", "page_path": "pages/index/index.uvue",
      "route": "/pages/index/index", "title": "首页",
      "is_tab": false, "is_home": true, "layout_type": "list",
      "components": ["empty-state"], "data_fields": ["id", "title"],
      "interactions": [], "states": ["loading", "empty", "loaded"] }
  ],
  "tab_bar": { "enabled": false, "items": [] }
}
```
