# 原型解析契约（Flutter）

定义**原型输入 → proto_context.json**的转换契约。

---

## 1. context 结构

```json
{
  "project": {
    "project_name": "skill_swap_app",
    "app_title": "技能互换",
    "package_name": "skill_swap_app",
    "target_platforms": ["android", "ios"],
    "flutter_channel": "stable",
    "use_mock": true,
    "source_type": "html"
  },
  "design": {
    "primary_color": "#2B6DE5",
    "dark_mode": false,
    "radius_style": "md",
    "token_overrides": {}
  },
  "navigation": {
    "type": "bottom_nav",
    "items": [
      { "label": "首页", "route": "/", "icon": "home", "page": "home" },
      { "label": "我的", "route": "/profile", "icon": "person", "page": "profile" }
    ]
  },
  "pages": [
    {
      "page_name": "home",
      "route": "/",
      "widget_class": "HomePage",
      "feature_dir": "features/home",
      "layout_type": "list",
      "data_model": "Skill",
      "components": ["SkillCard", "EmptyView"],
      "data_fields": ["id", "title", "userName", "avatar", "tags"],
      "interactions": [
        { "event": "tap", "target": "SkillCard", "action": "navigate", "to": "/detail" },
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
| --- | --- |
| `project_name` | snake_case，符合 Dart 包名规范 |
| `package_name` | 同上，二者通常一致 |
| `route` | 以 `/` 开头；首页为 `/` |
| `widget_class` | PascalCase + `Page` 后缀 |
| `feature_dir` | `features/<snake_case>` |
| `layout_type` | `list`/`detail`/`form`/`grid`/`profile`/`custom` |
| `data_model` | PascalCase，对应 `data/models/` 下的类 |
| `states` | 必须含 `loading` 与 `empty` |

---

## 3. 校验规则

`validate_project.py` 检查：

| 编号 | 规则 | 级别 |
| --- | --- | --- |
| F01 | `project_name` 为 snake_case 且不以数字开头 | error |
| F02 | 每个 `widget_class` 在 `lib/features/**` 中有对应文件 | error |
| F03 | 每个 `route` 在 `core/router/app_router.dart` 中注册 | error |
| F04 | `states` 含 loading 与 empty | error |
| F05 | 页面文件不 `import 'package:http/http.dart'` | error |
| F06 | 存在 `analysis_options.yaml` | error |
| F07 | `test/` 下至少一个 `*_test.dart` | error |
| F08 | 底部导航项数在 2-5 之间 | warn |
| F09 | 布局原型是已知枚举值 | warn |

---

## 4. 解析优先级

```text
视觉表现（图片/截图） > 结构层级（HTML） > 业务规则（PRD）
```

冲突写入 `diagnostics.need_confirm`，按高优先级临时生成并标注。

---

## 5. 各输入类型要点

### 5.1 HTML / CSS

| HTML 特征 | Flutter 映射 |
| --- | --- |
| 纵向区块堆叠 | `Column` |
| `display:flex; flex-direction:row` | `Row` |
| `display:grid` | `GridView` 或 `Wrap` |
| `<img>` | `Image.network` / `Image.asset` |
| `<button>` | `ElevatedButton` / `InkWell` |
| `<input>` | `TextField` / `TextFormField` |
| `<ul><li>` 重复 | `ListView.builder` |
| 固定顶部 | `AppBar` 或将容器放在 `Column` 顶部 |
| 固定底部 | `bottomNavigationBar` 或 `Column` + `Spacer` |

### 5.2 设计图 / 截图

1. 划分大区块（AppBar / 内容区 / 底部导航）
2. 识别重复单元（卡片、列表项）
3. 识别原子元素（文本、图标、按钮、标签）

不确定的写入 `need_confirm`。

### 5.3 PRD / 页面清单

- 页面名与用途 → `pages[]`
- 跳转描述 → `interactions[]`
- 字段清单 → `data_fields[]` + `data_model`

PRD 无视觉信息时用 `design_tokens.json` 默认值，并告知用户。

---

## 6. 最小可用 context

```json
{
  "project": {
    "project_name": "demo_app", "app_title": "演示", "package_name": "demo_app",
    "target_platforms": ["android"], "flutter_channel": "stable",
    "use_mock": true, "source_type": "html"
  },
  "pages": [{
    "page_name": "home", "route": "/", "widget_class": "HomePage",
    "feature_dir": "features/home", "layout_type": "list",
    "data_model": "Item", "components": ["EmptyView"],
    "data_fields": ["id", "title"], "interactions": [],
    "states": ["loading", "empty", "loaded"]
  }],
  "navigation": { "type": "none", "items": [] }
}
```
