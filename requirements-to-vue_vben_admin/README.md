# requirements-to-vue_vben_admin

## 1. 这个技能是干嘛的

`requirements-to-vue_vben_admin` 是一个面向 AI 开发场景的 Skill，用于把**后台管理的需求描述**转换成**基于 [vue-vben-admin](https://github.com/vbenjs/vue-vben-admin) 的可运行后台管理工程**。

你只需要描述业务，例如：

```text
我需要实现一个后台管理系统，包含以下功能模块：
系统管理模块包括：-用户管理，-角色管理，-权限管理；
业务管理模块包括：-订单管理；-商品管理；-库存管理；
数据统计模块包括：-销售数据分析；-用户行为分析；
```

技能会产出：

| 产出 | 说明 |
| --- | --- |
| **路由与菜单** | 按"XX模块"自动生成一级菜单，模块下的条目生成二级页面 |
| **CRUD 页面** | 列表 + 搜索 + 新增/编辑抽屉 + 详情 + 删除 |
| **数据统计页** | Echarts 图表看板 + 概览数字卡片 |
| **API 层** | `requestClient` 封装 + `namespace` 类型定义 |
| **Mock 数据** | 支持 `apps/backend-mock`，无需后端即可运行 |

## 2. 关键技术基线

本技能面向 **vue-vben-admin v5.x（monorepo）**，不是 v2/v3 的单体版本。

| 项 | 值 |
| --- | --- |
| 版本 | 5.x（参考 5.7.0） |
| 包管理 | **pnpm 11+** |
| Node | **22.18+ / 24.12+** |
| 结构 | `apps/`（web-antd、web-ele、web-naive、web-tdesign、backend-mock）+ `packages/` |
| 默认目标 | `apps/web-antd` |
| 路由 | `src/router/routes/modules/*.ts`（**自动 glob 收集**） |
| 别名 | `#/` → `apps/web-antd/src/` |

### 2.1 容易踩的三个坑

这三个是本技能在真实仓库中验证出来的，写代码时务必注意：

**坑 1：UI 组件导入来源**

```ts
// ✅ 正确（web-antd）
import { Button, message, Modal } from 'ant-design-vue';

// ❌ 错误（antdv-next 是 playground 应用用的）
import { Button } from 'antdv-next';
```

**坑 2：`VbenTableAction` 导入来源**

```ts
// ✅ 正确
import { VbenTableAction } from '@vben/common-ui';

// ❌ 错误（#/adapter 里 vben5 只有 useVbenVxeGrid）
import { VbenTableAction } from '#/adapter/vxe-table';
```

**坑 3：不要在 `routes/index.ts` 手动注册路由**

它用 `import.meta.glob('./modules/**/*.ts', { eager: true })` 自动收集，新增模块只需在 `modules/` 下加文件。

## 3. 技能项目结构

```text
requirements-to-vue_vben_admin/
├── SKILL.md                                    # 技能定义与工作流
├── README.md                                   # 本文件
└── resources/
    ├── config/
    │   ├── module_mapping.json                 # 需求关键词 → 模块/页面/字段 的映射词典
    │   └── framework_baseline.json             # vben5 版本、路径、API、禁用写法
    ├── specifications/
    │   ├── requirements_parser_contract.md     # 需求 → req_context.json 契约
    │   ├── page_generation_patterns.md         # 各页面类型的标准代码写法
    │   └── api_binding.md                      # 已有页面上按接口文档对接真实数据
    ├── templates/                              # 可复用模板
    ├── tools/
    │   ├── parse_requirements.py               # 中文需求 → req_context.json
    │   ├── preview_plan.py                     # 预览生成计划
    │   └── validate_project.py                 # 生成工程静态校验（14 项）
    └── demo_output/
        └── demo-admin/                         # 示例：3 模块 8 页面的完整产物
```

## 4. 工具用法

### 4.1 解析需求

```bash
python resources/tools/parse_requirements.py 需求.txt --out req_context.json --title "运营管理后台"
```

或直接用文本：

```bash
python resources/tools/parse_requirements.py --text "系统管理模块包括：用户管理、角色管理" --out ctx.json
```

输出示例：

```
模块数: 3 | 页面数: 8
  系统管理: ['用户管理', '角色管理', '权限管理']
  业务管理: ['订单管理', '商品管理', '库存管理']
  数据统计: ['销售数据分析', '用户行为分析']
```

### 4.2 预览生成计划

```bash
python resources/tools/preview_plan.py req_context.json
```

会列出模块树、页面类型、路由、模型名和将要生成的文件清单。

### 4.3 校验生成结果

```bash
python resources/tools/validate_project.py <vben工程根目录>
```

14 项检查：

| 检查项 | 说明 |
| --- | --- |
| monorepo 结构 | 必须是 `apps/` + `packages/`（v5） |
| 路由模块位置 | 必须在 `routes/modules/` 下 |
| 路由 component | 指向的 `.vue` 文件必须存在 |
| routes/index.ts | 未被篡改为手动注册 |
| useVbenVxeGrid | 列表页使用（看板页豁免） |
| 无原生 table | 未手写 `<table>` 或 `el-table` |
| requestClient | API 层未直接用 axios |
| UI 导入来源 | web-antd 未误用 `antdv-next` |
| VbenTableAction | 从 `@vben/common-ui` 导入 |
| script setup | SFC 使用 `<script lang="ts" setup>` |
| #/ 别名 | 无三层以上相对引用 |
| API 类型 | 有 `namespace`/`interface` 定义 |
| 字段一致 | 表单字段能在 API 类型中找到 |
| mock 存在 | 有 backend-mock 或前端 mock |

## 5. 需求 → 模块映射规则

| 需求关键词 | 页面类型 | 生成内容 |
| --- | --- | --- |
| 管理 / 列表 / 记录 | `crud` | 表格 + 搜索 + 增删改查 + 详情 |
| 分析 / 统计 / 报表 / 看板 | `dashboard` | Echarts 图表 + 概览卡片 |
| 权限 / 菜单 / 组织 / 分类 | `tree` | 树形表格 |
| 设置 / 配置 | `form` | 表单页 |

**判定顺序**：先 dashboard → 再 tree → 再 form → 最后默认 crud。

> 例：`权限管理` 含"权限" → `tree`；`用户行为分析` 含"分析" → `dashboard`。

## 6. 生成结果示例

`resources/demo_output/demo-admin/` 是用上面的示例需求生成的完整产物：

```text
demo-admin/
├── system.ts / business.ts / statistics.ts    # 3 个路由模块
├── system/
│   ├── user/{list.vue, data.ts, modules/form.vue}
│   ├── role/{...}
│   └── permission/{...}
├── business/
│   ├── order/{...}
│   ├── product/{...}
│   └── inventory/{...}
├── statistics/
│   ├── sales-analysis/list.vue                # 图表看板
│   └── user-behavior-analysis/list.vue
└── api/                                        # 8 个 API 模块
```

共 **8 个页面、3 个路由模块、8 个 API 文件、31 个文件**。

## 7. 实测验证结果

本技能的所有规范均在**真实 vue-vben-admin 仓库**中验证过：

| 验证项 | 结果 |
| --- | --- |
| 解析示例需求 | ✓ 3 模块 / 8 页面，页面名无截断 |
| 在真实 repo 生成完整模块 | ✓ 31 个文件 |
| `validate_project.py` 校验 | ✓ **0 错误 0 警告** |
| Vue `<template>` 标签配对（Node 解析） | ✓ 14 个文件全部正确 |
| TS 文件括号配平与导出检查 | ✓ 11 个文件全部通过 |

验证过程中修正的问题：

1. 页面名截断：`销售数据分析` 被模块词"数据"误伤 → 改为只剥离片段开头的模块名
2. 路径全退化：`to_kebab`/`to_pascal` 逐字遍历匹配不上双字词 → 改为按词匹配
3. 校验误报：dashboard 页被要求用 VxeGrid、vben 自带 `api/core` 被误判 → 修正判定逻辑

## 8. 使用建议

1. **先解析再生成**：`parse_requirements.py` 出初稿，人工核对 `need_confirm` 后再生成
2. **字段要确认**：需求通常只写模块名，字段靠推断容易返工
3. **先生成一个模块验证**：确认风格对了再批量生成其余模块
4. **必须给 mock**：否则跑起来是空表格，容易误判为生成失败
5. **接口文档后补**：页面已经生成时，按 `resources/specifications/api_binding.md` 只改 api 函数，不改表格列和路由

## 9. 相关文档

| 内容 | 路径 |
| --- | --- |
| 需求解析契约 | `resources/specifications/requirements_parser_contract.md` |
| 页面生成范式（含完整代码） | `resources/specifications/page_generation_patterns.md` |
| 接口文档对接 | `resources/specifications/api_binding.md` |
| 框架基线（版本/API/禁用写法） | `resources/config/framework_baseline.json` |
| vue-vben-admin 官方文档 | <https://doc.vben.pro/> |
