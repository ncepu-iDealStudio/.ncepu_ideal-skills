# 需求解析契约（Requirements Parser Contract）

定义**中文需求描述 → req_context.json** 的转换契约。所有页面生成必须基于该 context。

---

## 1. 设计目标

1. 把自由文本的需求，转成**结构化的模块树**
2. 让生成器只依赖 context，不重复解析文本
3. context 可校验、可审查、可作为快照基线

---

## 2. context 结构

```json
{
  "app": {
    "title": "后台管理系统",
    "ui": "antd",
    "vben_version": "5.x"
  },
  "modules": [
    {
      "name": "系统管理",
      "name_en": "System",
      "path": "/system",
      "icon": "lucide:settings",
      "order": 10,
      "children": [
        {
          "name": "用户管理",
          "name_en": "SystemUser",
          "path": "user",
          "full_path": "/system/user",
          "icon": "lucide:users",
          "type": "crud",
          "model": "SystemUser",
          "route_file": "system.ts",
          "view_dir": "views/system/user",
          "api_file": "api/system/user.ts",
          "fields": [
            { "field": "id", "label": "ID", "type": "string", "column": true, "form": false },
            { "field": "name", "label": "名称", "type": "string", "column": true, "form": true, "required": true }
          ],
          "actions": ["create", "edit", "detail", "delete"],
          "has_mock": true
        }
      ]
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

## 3. 字段定义

### 3.1 `app`

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `title` | string | 是 | 系统标题 |
| `ui` | string | 是 | `antd` / `ele` / `naive` / `tdesign`，默认 `antd` |
| `vben_version` | string | 是 | 固定 `5.x` |

### 3.2 `modules[]`（一级菜单）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | string | 是 | 中文模块名，用作菜单标题 |
| `name_en` | string | 是 | PascalCase，路由 `name` 前缀 |
| `path` | string | 是 | 以 `/` 开头的 kebab-case |
| `icon` | string | 否 | lucide 图标名 |
| `order` | number | 是 | 菜单排序，从 10 起，每个 +10 |
| `children` | array | 是 | 二级页面列表 |

### 3.3 `children[]`（二级页面）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | string | 是 | 中文页面名 |
| `name_en` | string | 是 | PascalCase，路由 `name` |
| `path` | string | 是 | 相对路径，kebab-case |
| `full_path` | string | 是 | `模块path + '/' + path` |
| `type` | enum | 是 | `crud` / `dashboard` / `tree` / `form` |
| `model` | string | 是 | 数据模型名，PascalCase |
| `fields` | array | 是 | 字段定义（见 3.4） |
| `actions` | string[] | 否 | CRUD 操作，默认全部 |

### 3.4 `fields[]`

| 字段 | 类型 | 说明 |
|---|---|---|
| `field` | string | 字段名，camelCase |
| `label` | string | 中文标签 |
| `type` | string | `string` / `number` / `boolean` / `datetime` / `switch` / `select` / `tag` / `textarea` |
| `column` | boolean | 是否显示在表格列 |
| `form` | boolean | 是否出现在表单 |
| `required` | boolean | 是否必填 |
| `width` | number | 列宽（表格列） |
| `options` | array | 枚举选项（switch/select/tag 用） |

---

## 4. 解析规则

### 4.1 模块识别

匹配 `module_mapping.json` 的 `module_keywords`：

```text
"系统管理模块包括：" → 一级模块「系统管理」
"业务管理模块包括：" → 一级模块「业务管理」
"数据统计模块包含：" → 一级模块「数据统计」
```

识别不出时，用 `"模块N"` 兜底并写入 `need_confirm`。

### 4.2 页面识别

模块下的条目即二级页面：

```text
"包括：- 用户管理，- 角色管理，- 权限管理"
      → 用户管理 / 角色管理 / 权限管理
```

支持分隔符：`、` `，` `,` `-` 换行、序号 `1.` 等。

### 4.3 页面类型判定

按 `page_type_keywords` 顺序匹配（**先匹配更具体的类型**）：

```text
先查 dashboard 关键词（分析/统计/报表/看板）
再查 tree 关键词（权限/菜单/组织/分类）
再查 form 关键词（设置/配置）
最后默认 crud
```

> 注意：`权限管理` 含"权限"→ `tree`；`用户行为分析` 含"分析"→ `dashboard`。

### 4.4 字段推断

1. 先取 `field_templates.domain_specific[页面名]`（如"订单管理"有专属字段）
2. 再合并 `field_templates.crud_common`（id/name/status/remark/createTime）
3. 去重（同名字段以 domain_specific 优先）

`dashboard` / `tree` 类型用各自的模板，不合并 crud_common。

---

## 5. 校验规则

| 编号 | 规则 | 级别 |
|---|---|---|
| R01 | 至少 1 个模块 | error |
| R02 | 每个模块至少 1 个页面 | error |
| R03 | `path` 为 kebab-case 且不以 `/` 结尾（模块级以 `/` 开头） | error |
| R04 | `name_en` 为 PascalCase | error |
| R05 | `type` 在枚举内 | error |
| R06 | `crud` 类型的 `fields` 非空，且至少一个 `column=true` | error |
| R07 | `full_path` 唯一（不能两个页面同路由） | error |
| R08 | `order` 唯一且递增 | warn |
| R09 | `ui` 在允许枚举内 | error |

---

## 6. 歧义处理

需求含糊时**不要猜**，写入 `diagnostics.need_confirm`：

| 情况 | 处理 |
|---|---|
| 只写"用户管理"没说字段 | 用 `domain_specific` 模板，标注"字段为推断值，请确认" |
| 模块名不在词典 | 用原名建模块，图标用默认，标注待确认 |
| 页面类型模糊（如"数据管理"） | 默认 `crud`，标注待确认 |
| 出现"权限控制"但没说粒度和码值 | 生成基础版，标注"权限码需对接后端" |

---

## 7. 最小可用 context

```json
{
  "app": { "title": "后台管理系统", "ui": "antd", "vben_version": "5.x" },
  "modules": [
    {
      "name": "系统管理", "name_en": "System", "path": "/system",
      "icon": "lucide:settings", "order": 10,
      "children": [
        {
          "name": "用户管理", "name_en": "SystemUser", "path": "user",
          "full_path": "/system/user", "type": "crud", "model": "SystemUser",
          "route_file": "system.ts", "view_dir": "views/system/user",
          "api_file": "api/system/user.ts",
          "fields": [
            { "field": "id", "label": "ID", "type": "string", "column": true, "form": false },
            { "field": "name", "label": "名称", "type": "string", "column": true, "form": true, "required": true }
          ],
          "actions": ["create", "edit", "delete"],
          "has_mock": true
        }
      ]
    }
  ]
}
```

---

## 8. 完整示例（对应 SKILL.md 的输入）

输入：

```text
我需要实现一个后台管理系统，包含以下功能模块：
系统管理模块包括：-用户管理，-角色管理，-权限管理；
业务管理模块包括：-订单管理；-商品管理；-库存管理；
数据统计模块包括：-销售数据分析；-用户行为分析；
```

期望解析结果：

| 模块 | 页面 | 类型 | 模型 |
|---|---|---|---|
| 系统管理 `/system` | 用户管理 `/system/user` | crud | SystemUser |
| | 角色管理 `/system/role` | crud | SystemRole |
| | 权限管理 `/system/permission` | **tree** | SystemPermission |
| 业务管理 `/business` | 订单管理 `/business/order` | crud | BusinessOrder |
| | 商品管理 `/business/product` | crud | BusinessProduct |
| | 库存管理 `/business/inventory` | crud | BusinessInventory |
| 数据统计 `/statistics` | 销售数据分析 `/statistics/sales-analysis` | **dashboard** | StatisticsSales |
| | 用户行为分析 `/statistics/user-behavior` | **dashboard** | StatisticsUserBehavior |

共 **3 个模块、8 个页面**。
