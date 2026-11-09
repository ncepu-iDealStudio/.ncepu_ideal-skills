---
name: "requirements-to-vue_vben_admin"
description: "把后台管理的需求描述转换成基于 vue-vben-admin（vben5）的可运行后台管理脚手架：自动划分功能模块、生成路由菜单、CRUD 页面（列表/搜索/新增编辑抽屉/详情）、API 层与图表页，并内置 mock 数据可直接运行。用户说「做一个后台管理系统」「生成管理端页面」「需要用户管理/订单管理/数据统计」或给出模块清单时使用。"
---

# Requirements to Vue Vben Admin Skill

## 概述

把**一段后台管理需求描述**转换成**基于 vue-vben-admin 的可运行后台管理工程**。

典型输入：

```text
我需要实现一个后台管理系统，包含以下功能模块：
系统管理模块包括：用户管理、角色管理、权限管理；
业务管理模块包括：订单管理、商品管理、库存管理；
数据统计模块包括：销售数据分析、用户行为分析。
```

产出：

1. **模块化的路由与菜单**（按需求里的"XX模块"自动分组）
2. **每个功能一个 CRUD 页面**（列表 + 搜索 + 新增/编辑 + 详情 + 删除）
3. **数据统计页**（图表看板）
4. **API 层**（`requestClient` + 类型定义）
5. **mock 数据**（无需后端即可运行看到效果）
6. 可直接 `pnpm dev` 跑起来的工程

---

## 什么时候使用此技能

触发场景：

- 用户给出后台管理系统的**功能模块清单**
- 用户说"做一个管理后台""生成管理端页面""XX 管理模块"
- 用户要求基于 vue-vben-admin 生成/扩展页面

**不适用**：前端展示型官网（用 `common-website-design`）；移动端（用 `prototype-to-*`）；纯接口开发。

---

## 目标框架基线（重要）

本技能面向 **vue-vben-admin v5.x（monorepo）**，不是 v2/v3 的单体版本。关键事实：

| 项 | 值 |
|---|---|
| 版本 | 5.x（当前 5.7.0） |
| 包管理 | **pnpm 11+**，Node **22.18+ / 24.12+** |
| 结构 | monorepo：`apps/`（web-antd、web-ele、web-naive、web-tdesign、backend-mock）+ `packages/`（@core、effects、icons、locales、stores、styles、types、utils） |
| 应用 | 每个 `apps/web-*` 是一个独立 UI 框架的可运行应用 |
| **默认目标** | `apps/web-antd`（Ant Design 版，生态最全） |
| 路由 | `src/router/routes/modules/*.ts`，**自动 glob 加载** |
| 别名 | `#/` → `apps/web-antd/src/` |
| 数据请求 | `requestClient`（`#/api/request`） |
| 表格 | `useVbenVxeGrid`（`#/adapter/vxe-table`） |
| 行操作 | `VbenTableAction`（**`@vben/common-ui`**，非 adapter） |
| UI 组件 | `ant-design-vue`（**注意不是 `antdv-next`**） |
| 表单 | `useVbenForm`（`#/adapter/form`） |
| 抽屉 | `useVbenDrawer`（`@vben/common-ui`） |
| 图表 | `EchartsUI` + `useEcharts`（`@vben/plugins/echarts`） |
| mock 后端 | `apps/backend-mock`（nitro + faker） |

> ⚠️ **不要按 v2/v3 的写法生成**（`src/views/system/user/index.vue` 单体 + `src/router/routes/index.ts` 手写数组）。vben5 的目录、API、组件用法都不同。

---

## 核心设计：需求 → 模块树 → 页面

### 需求解析规则

从需求描述中提取**两级结构**：

```text
「XX模块」  →  一级菜单（routeGroup）
「- YY」   →  二级菜单（页面，通常是一个 CRUD）
```

示例映射：

| 需求原文 | 一级菜单 | 二级页面 | 页面类型 |
|---|---|---|---|
| 系统管理模块包括：用户管理、角色管理、权限管理 | 系统管理 | 用户管理 | CRUD |
| | | 角色管理 | CRUD |
| | | 权限管理 | CRUD（树形） |
| 业务管理模块包括：订单管理、商品管理、库存管理 | 业务管理 | 订单管理 | CRUD |
| | | 商品管理 | CRUD |
| | | 库存管理 | CRUD（含数量列） |
| 数据统计模块包括：销售数据分析、用户行为分析 | 数据统计 | 销售数据分析 | 图表看板 |
| | | 用户行为分析 | 图表看板 |

### 页面类型判定

| 关键词 | 页面类型 | 生成内容 |
|---|---|---|
| 管理 / 列表 / 记录 | `crud` | 表格 + 搜索 + 增删改查 + 详情 |
| 分析 / 统计 / 报表 / 看板 | `dashboard` | 图表卡片 + 概览数字 |
| 权限 / 菜单 / 组织 / 分类 | `tree` | 树形表格或树 + 详情 |
| 设置 / 配置 | `form` | 表单页 |

---

## 使用流程

### 步骤 1：解析需求

读取用户描述，输出**模块树**：

```json
{
  "app": { "title": "后台管理系统", "ui": "antd" },
  "modules": [
    {
      "name": "系统管理",
      "path": "/system",
      "icon": "lucide:settings",
      "order": 10,
      "children": [
        { "name": "用户管理", "path": "user", "type": "crud", "model": "SystemUser" }
      ]
    }
  ]
}
```

机器可读中间产物按 `resources/specifications/requirements_parser_contract.md` 输出 `req_context.json`。可用 `resources/tools/parse_requirements.py` 从中文描述自动生成初稿。

### 步骤 2：确认关键决策

必须确认（用选择题）：

- **UI 框架**：默认 antd；若团队用 Element Plus / Naive / TDesign 需说明
- **每个 CRUD 的字段**：需求通常不写字段，需按模块名推断并确认
- **是否需要权限控制**（`auth` 码）
- **是否要 mock 数据**（默认要，保证能跑）
- **是否只要页面骨架**（只要界面）还是**含完整交互**（增删改查闭环）

### 步骤 3：生成路由模块

在 `apps/web-antd/src/router/routes/modules/` 下**每个一级模块一个文件**：

```ts
// modules/system.ts
const routes: RouteRecordRaw[] = [
  {
    meta: { icon: 'lucide:settings', order: 10, title: '系统管理' },
    name: 'System',
    path: '/system',
    children: [
      {
        name: 'SystemUser',
        path: 'user',
        component: () => import('#/views/system/user/list.vue'),
        meta: { icon: 'lucide:users', title: '用户管理' },
      },
    ],
  },
];
export default routes;
```

> 不要改 `routes/index.ts`——它用 `import.meta.glob('./modules/**/*.ts')` 自动收集。

### 步骤 4：生成页面（四件套）

每个 CRUD 模块生成：

```text
views/<module>/<page>/
├── list.vue          # 列表页（表格 + 搜索 + 工具栏）
├── data.ts           # 列定义 + 表单 schema + 详情项
└── modules/
    ├── form.vue      # 新增/编辑抽屉
    └── detail.vue    # 详情抽屉
```

### 步骤 5：生成 API 层

```text
api/<module>/<page>.ts     # requestClient 调用 + namespace 类型
api/<module>/index.ts      # 汇总导出
```

### 步骤 6：生成 mock 数据

两种方式（按需选）：

- **A. 复用 `apps/backend-mock`**：新增路由返回假数据（推荐，最接近真实）
- **B. 前端内置 mock**：在 `api/` 里判断开关返回本地数据（改动小，适合纯演示）

### 步骤 7：自检

运行 `resources/tools/validate_project.py`：

- 路由文件是否被 glob 到（在 `routes/modules/` 下）
- 每个路由的 `component` 指向的文件是否存在
- 页面是否用了 `useVbenVxeGrid`（而非自己写 `<table>`）
- 是否直接用了 `axios`（应该用 `requestClient`）
- `.vue` 是否含 `<script lang="ts" setup>`

---

## 关键代码范式（必须遵循）

### 列表页骨架

```vue
<script lang="ts" setup>
import type { VxeTableGridOptions } from '#/adapter/vxe-table';
import type { SystemUserApi } from '#/api';

import { Page, useVbenDrawer, VbenTableAction } from '@vben/common-ui';
import { Plus } from '@vben/icons';
import { Button } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { deleteUser, getUserList } from '#/api';

import { useColumns, useGridFormSchema } from './data';
import Form from './modules/form.vue';

const [FormDrawer, formDrawerApi] = useVbenDrawer({
  connectedComponent: Form,
  destroyOnClose: true,
});

const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: {
    schema: useGridFormSchema(),
    submitOnChange: true,
  },
  gridOptions: {
    columns: useColumns(),
    height: 'auto',
    keepSource: true,
    proxyConfig: {
      ajax: {
        query: async ({ page }, formValues) => {
          return await getUserList({
            page: page.currentPage,
            pageSize: page.pageSize,
            ...formValues,
          });
        },
      },
    },
    rowConfig: { keyField: 'id' },
    toolbarConfig: { custom: true, refresh: true, search: true, zoom: true },
  } as VxeTableGridOptions<SystemUserApi.SystemUser>,
});
</script>

<template>
  <Page auto-content-height>
    <FormDrawer @success="gridApi.query()" />
    <Grid :table-title="$t('system.user.list')">
      <template #toolbar-tools>
        <Button type="primary" @click="formDrawerApi.setData(null).open()">
          <Plus class="size-5" />
          新增
        </Button>
      </template>
      <template #action="{ row }">
        <VbenTableAction
          :actions="[
            { text: '编辑', icon: 'lucide:edit', onClick: () => formDrawerApi.setData(row).open() },
          ]"
          :dropdown-actions="[
            {
              text: '删除',
              icon: 'lucide:trash-2',
              danger: true,
              popConfirm: { title: `确认删除 ${row.name}？`, confirm: () => onDelete(row) },
            },
          ]"
          align="center"
        />
      </template>
    </Grid>
  </Page>
</template>
```

### 列定义（data.ts）

```ts
export function useColumns(): VxeTableGridColumns {
  return [
    { field: 'name', title: '名称', width: 200 },
    {
      cellRender: { attrs: { beforeChange: onStatusChange }, name: 'CellSwitch' },
      field: 'status',
      title: '状态',
      width: 100,
    },
    { field: 'createTime', title: '创建时间', width: 200 },
    {
      align: 'center',
      field: 'operation',
      fixed: 'right',
      slots: { default: 'action' },
      title: '操作',
      width: 180,
    },
  ];
}
```

### 表单 schema（data.ts）

```ts
export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    {
      component: 'RadioGroup',
      componentProps: {
        buttonStyle: 'solid',
        options: [{ label: '启用', value: 1 }, { label: '禁用', value: 0 }],
        optionType: 'button',
      },
      defaultValue: 1,
      fieldName: 'status',
      label: '状态',
    },
    { component: 'Textarea', fieldName: 'remark', label: '备注' },
  ];
}
```

### API 层

```ts
import type { Recordable } from '@vben/types';
import { requestClient } from '#/api/request';

export namespace SystemUserApi {
  export interface SystemUser {
    [key: string]: any;
    id: string;
    name: string;
    status: 0 | 1;
    remark?: string;
  }
}

export async function getUserList(params: Recordable<any>) {
  return requestClient.get<Array<SystemUserApi.SystemUser>>('/system/user/list', { params });
}

export async function createUser(data: Omit<SystemUserApi.SystemUser, 'id'>) {
  return requestClient.post('/system/user', data);
}

export async function updateUser(id: string, data: Omit<SystemUserApi.SystemUser, 'id'>) {
  return requestClient.put(`/system/user/${id}`, data);
}

export async function deleteUser(id: string) {
  return requestClient.delete(`/system/user/${id}`);
}
```

---

## 文件结构（生成物）

```text
apps/web-antd/src/
├── router/routes/modules/
│   ├── system.ts              # 系统管理（用户/角色/权限）
│   ├── business.ts            # 业务管理（订单/商品/库存）
│   └── statistics.ts          # 数据统计（销售/用户行为）
├── views/
│   ├── system/
│   │   ├── user/
│   │   │   ├── list.vue
│   │   │   ├── data.ts
│   │   │   └── modules/{form.vue,detail.vue}
│   │   ├── role/
│   │   └── permission/
│   ├── business/
│   │   ├── order/
│   │   ├── product/
│   │   └── inventory/
│   └── statistics/
│       ├── sales/            # dashboard 类型
│       └── user-behavior/
└── api/
    ├── system/{user.ts,role.ts,permission.ts,index.ts}
    ├── business/{order.ts,...}
    └── statistics/{sales.ts,...}
```

---

## 命名规范

| 对象 | 规则 | 示例 |
|---|---|---|
| 路由模块文件 | kebab-case | `system.ts`、`statistics.ts` |
| 路由 `name` | PascalCase | `SystemUser` |
| 路由 `path` | kebab-case | `/system/user`、`/system/user-role` |
| 视图目录 | kebab-case | `views/system/user/` |
| API 文件 | kebab-case | `api/system/user.ts` |
| API namespace | PascalCase + `Api` | `SystemUserApi` |
| 类型 | PascalCase | `SystemUser` |
| i18n key | 点分小写 | `system.user.list` |
| 菜单标题 | 中文 | `用户管理` |

---

## 输出格式

```text
✅ 已生成后台管理脚手架：后台管理系统（基于 vue-vben-admin v5 / antd）

📁 模块结构
系统管理    ├─ 用户管理（CRUD）
           ├─ 角色管理（CRUD）
           └─ 权限管理（树形）
业务管理    ├─ 订单管理（CRUD）
           ├─ 商品管理（CRUD）
           └─ 库存管理（CRUD）
数据统计    ├─ 销售数据分析（看板）
           └─ 用户行为分析（看板）

📄 新增文件
- 路由模块 3 个
- 页面 {{N}} 个（含 list/data/form/detail）
- API 模块 {{M}} 个
- mock 路由 {{K}} 个

▶️ 如何运行
1. pnpm install
2. pnpm dev:antd
3. 打开 http://localhost:5555
（内置 mock，无需后端）

⚠️ 待确认
- 各模块的字段定义（当前按模块名推断）
- 是否需要权限码控制
```

---

## 重要提示

1. **面向 vben5 monorepo**，不要用 v2/v3 写法（目录与 API 完全不同）
2. **路由放 `modules/` 下**，不要改 `routes/index.ts`（它自动 glob）
3. **表格用 `useVbenVxeGrid`**，不要手写 `<table>` 或用 el-table
4. **请求用 `requestClient`**，不要直接 `axios`
5. **别名 `#/` 指向 `apps/web-antd/src/`**，不要用相对路径跨层引用
6. **表单/抽屉用 `useVbenForm` + `useVbenDrawer`**，不要手写 el-dialog
7. **菜单标题用中文**，代码标识用英文
8. **必须给 mock**，否则用户跑起来是空表格，以为生成失败
9. **字段要问清楚**：需求通常只写模块名，字段靠推断容易返工
10. **不要生成用不到的依赖**，vben5 已内置绝大多数能力
11. **UI 库导入来源**：`web-antd` 用 `ant-design-vue`；`playground` 用 `antdv-next`，两者不同，别照搬
12. **`VbenTableAction` 从 `@vben/common-ui` 导入**：`playground` 在 adapter 里再导出了它，`web-antd` 没有
