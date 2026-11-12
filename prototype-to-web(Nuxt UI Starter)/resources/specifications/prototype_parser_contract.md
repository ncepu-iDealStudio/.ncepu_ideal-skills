# 原型解析契约（Nuxt UI Starter）

定义**原型输入 → proto_context.json**的转换契约。

---

## 1. context 结构

```json
{
  "project": {
    "project_name": "skill-swap-web",
    "app_title": "技能互换",
    "package_name": "skill-swap-web",
    "target_platforms": ["web"],
    "nuxt_version": "4",
    "ui_library": "@nuxt/ui",
    "use_mock": true,
    "source_type": "html"
  },
  "design": {
    "primary_color": "green",
    "primary_hex": "#00DC82",
    "neutral_color": "slate",
    "dark_mode": true,
    "radius_style": "md",
    "token_overrides": {}
  },
  "navigation": {
    "type": "header",
    "items": [
      { "label": "首页", "route": "/", "icon": "i-lucide-home", "page": "index" },
      { "label": "我的", "route": "/profile", "icon": "i-lucide-user", "page": "profile" }
    ]
  },
  "pages": [
    {
      "page_name": "index",
      "route": "/",
      "file_path": "app/pages/index.vue",
      "layout_type": "list",
      "data_model": "Skill",
      "components": ["SkillCard", "EmptyState"],
      "data_fields": ["id", "title", "userName", "avatar", "tags"],
      "interactions": [
        { "event": "click", "target": "SkillCard", "action": "navigate", "to": "/detail" },
        { "event": "scroll-bottom", "action": "load-more" }
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
| --- | --- |
| `project_name` | kebab-case，符合 npm 包名规范 |
| `package_name` | 同上，二者通常一致 |
| `route` | 以 `/` 开头；首页为 `/`；与 `app/pages/` 文件路径对应 |
| `file_path` | `app/pages/` 下的相对路径，`.vue` 后缀 |
| `layout_type` | `list`/`detail`/`form`/`grid`/`profile`/`landing`/`custom` |
| `data_model` | PascalCase，对应 `app/types/` 下的类型 |
| `components` | PascalCase，对应 `app/components/` 下的组件 |
| `states` | 必须含 `loading` 与 `empty` |

---

## 3. 校验规则

`validate_project.py` 检查：

| 编号 | 规则 | 级别 |
| --- | --- | --- |
| F01 | `project_name` 为 kebab-case 且不以数字/连字符开头 | error |
| F02 | 每个 `file_path` 在 `app/pages/` 中有对应 `.vue` 文件 | error |
| F03 | 每个 `route` 有对应页面文件（文件路由推断） | error |
| F04 | `states` 含 loading 与 empty | error |
| F05 | 页面文件不直接使用原生 `fetch`（应用 `$fetch` 或 service 层） | warn |
| F06 | 存在 `nuxt.config.ts` 且 modules 含 `@nuxt/ui` | error |
| F07 | 存在 `app/app.vue` 且包含 `<NuxtPage />` | error |
| F08 | 导航项数在 1-6 之间 | warn |
| F09 | 布局原型是已知枚举值 | warn |
| F10 | `app.config.ts` 中声明了 `ui.colors.primary` | error |

---

## 4. 解析优先级

```text
视觉表现（图片/截图） > 结构层级（HTML） > 业务规则（PRD）
```

冲突写入 `diagnostics.need_confirm`，按高优先级临时生成并标注。

---

## 5. 各输入类型要点

### 5.1 HTML / CSS

| HTML 特征 | Nuxt UI 映射 |
| --- | --- |
| 纵向区块堆叠 | `div` + `flex flex-col` 或直接文本流 |
| `display:flex; flex-direction:row` | `flex` / `flex-row` |
| `display:grid` | `grid` + `grid-cols-*` |
| `<img>` | `UAvatar` / `<img>` + Tailwind 类 |
| `<button>` | `UButton` |
| `<input>` / `<textarea>` | `UInput` / `UTextarea` |
| `<select>` | `USelect` |
| `<form>` | `UForm` + `UFormField` |
| `<ul><li>` 重复 | `v-for` 循环 + `UCard` 等组件 |
| 导航栏 | `UHeader` + `UNavigation` |
| 卡片 | `UCard` |
| 表格 | `UTable` |
| 模态框 | `UModal` |
| 下拉菜单 | `UDropdownMenu` |
| 提示 | `UToast` / `UAlert` |

### 5.2 设计图 / 截图

1. 划分大区块（Header / 内容区 / Footer）
2. 识别重复单元（卡片、列表项）
3. 识别原子元素（文本、图标、按钮、标签、表单控件）
4. 优先用 Nuxt UI 组件（`U*`），自定义部分用 Tailwind 工具类

不确定的写入 `need_confirm`。

### 5.3 PRD / 页面清单

- 页面名与用途 → `pages[]`
- 跳转描述 → `interactions[]`
- 字段清单 → `data_fields[]` + `data_model`

PRD 无视觉信息时用 `design_tokens.json` 默认值（primary=green, neutral=slate），并告知用户。

---

## 6. 最小可用 context

```json
{
  "project": {
    "project_name": "demo-web",
    "app_title": "演示",
    "package_name": "demo-web",
    "target_platforms": ["web"],
    "nuxt_version": "4",
    "ui_library": "@nuxt/ui",
    "use_mock": true,
    "source_type": "html"
  },
  "pages": [{
    "page_name": "index",
    "route": "/",
    "file_path": "app/pages/index.vue",
    "layout_type": "list",
    "data_model": "Item",
    "components": ["EmptyState"],
    "data_fields": ["id", "title"],
    "interactions": [],
    "states": ["loading", "empty", "loaded"]
  }],
  "navigation": { "type": "none", "items": [] }
}
```
