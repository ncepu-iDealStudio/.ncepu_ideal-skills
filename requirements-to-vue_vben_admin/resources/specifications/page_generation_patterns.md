# 页面生成范式（Page Generation Patterns）

本文给出各类型页面的**标准代码写法**，均基于 `apps/web-antd` 的真实结构核实过。

---

## 0. 前置：导入来源对照（最容易出错的地方）

| 内容 | 正确导入 | 错误写法 |
| --- | --- | --- |
| 页面容器 | `import { Page } from '@vben/common-ui'` | ❌ 自己写 `<div class="page">` |
| 抽屉 | `import { useVbenDrawer } from '@vben/common-ui'` | ❌ `<el-dialog>` / `<a-modal>` |
| 行操作 | `import { VbenTableAction } from '@vben/common-ui'` | ❌ 从 `#/adapter/vxe-table` 导入（那是 playground） |
| UI 组件 | `import { Button } from 'ant-design-vue'` | ❌ `from 'antdv-next'`（playground 才用） |
| 表格 | `import { useVbenVxeGrid } from '#/adapter/vxe-table'` | ❌ 手写 `<table>` |
| 表单 | `import { useVbenForm } from '#/adapter/form'` | ❌ 手写 `<form>` |
| 请求 | `import { requestClient } from '#/api/request'` | ❌ `import axios from 'axios'` |
| 图标 | `import { Plus } from '@vben/icons'` | |
| 图表 | `import { EchartsUI, useEcharts } from '@vben/plugins/echarts'` | |

> `#/` 是别名，指向 `apps/web-antd/src/`。不要用 `../../` 跨层引用。

---

## 1. CRUD 页面（最常用）

### 1.1 文件组成

```text
views/<module>/<page>/
├── list.vue          # 列表页
├── data.ts           # 列定义 + 表单 schema + 详情项
└── modules/
    ├── form.vue      # 新增/编辑抽屉
    └── detail.vue    # 详情抽屉（可选）
```

### 1.2 list.vue

```vue
<script lang="ts" setup>
import type { VxeTableGridOptions } from '#/adapter/vxe-table';
import type { SystemUserApi } from '#/api';

import { Page, useVbenDrawer, VbenTableAction } from '@vben/common-ui';
import { Plus } from '@vben/icons';
import { Button, message, Modal } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { deleteUser, getUserList } from '#/api';

import { useColumns, useGridFormSchema } from './data';
import Detail from './modules/detail.vue';
import Form from './modules/form.vue';

/** 表单抽屉 */
const [FormDrawer, formDrawerApi] = useVbenDrawer({
  connectedComponent: Form,
  destroyOnClose: true,
});

/** 详情抽屉 */
const [DetailDrawer, detailDrawerApi] = useVbenDrawer({
  connectedComponent: Detail,
  destroyOnClose: true,
});

/** 表格 */
const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: {
    schema: useGridFormSchema(),
    submitOnChange: true,
  },
  gridOptions: {
    columns: useColumns(onStatusChange),
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

function onCreate() {
  formDrawerApi.setData(null).open();
}

function onEdit(row: SystemUserApi.SystemUser) {
  formDrawerApi.setData(row).open();
}

function onDetail(row: SystemUserApi.SystemUser) {
  detailDrawerApi.setData(row).open();
}

function onRefresh() {
  gridApi.query();
}

function onDelete(row: SystemUserApi.SystemUser) {
  const hideLoading = message.loading({ content: `正在删除 ${row.name}`, duration: 0, key: 'del' });
  deleteUser(row.id)
    .then(() => {
      message.success({ content: '删除成功', key: 'del' });
      onRefresh();
    })
    .catch(() => hideLoading());
}

/** 状态开关变更前确认 */
async function onStatusChange(newStatus: number, row: SystemUserApi.SystemUser) {
  return new Promise<boolean>((resolve) => {
    Modal.confirm({
      content: `确认将 ${row.name} 的状态切换为【${newStatus === 1 ? '启用' : '禁用'}】？`,
      title: '切换状态',
      onCancel: () => resolve(false),
      onOk: () => resolve(true),
    });
  });
}
</script>

<template>
  <Page auto-content-height>
    <FormDrawer @success="onRefresh" />
    <DetailDrawer />
    <Grid :table-title="'用户管理'">
      <template #toolbar-tools>
        <Button type="primary" @click="onCreate">
          <Plus class="size-5" />
          新增
        </Button>
      </template>
      <template #action="{ row }">
        <VbenTableAction
          :actions="[
            { text: '详情', icon: 'lucide:eye', onClick: () => onDetail(row) },
            { text: '编辑', icon: 'lucide:edit', onClick: () => onEdit(row) },
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

### 1.3 data.ts

```ts
import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridColumns } from '#/adapter/vxe-table';
import type { SystemUserApi } from '#/api';

import { h } from 'vue';
import { Tag } from 'ant-design-vue';

/** 搜索表单 schema */
export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'name', label: '名称' },
    {
      component: 'Select',
      componentProps: {
        allowClear: true,
        options: [
          { label: '启用', value: 1 },
          { label: '禁用', value: 0 },
        ],
      },
      fieldName: 'status',
      label: '状态',
    },
  ];
}

/** 新增/编辑表单 schema */
export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    {
      component: 'RadioGroup',
      componentProps: {
        buttonStyle: 'solid',
        options: [
          { label: '启用', value: 1 },
          { label: '禁用', value: 0 },
        ],
        optionType: 'button',
      },
      defaultValue: 1,
      fieldName: 'status',
      label: '状态',
    },
    { component: 'Textarea', fieldName: 'remark', label: '备注' },
  ];
}

/** 表格列定义 */
export function useColumns(
  onStatusChange?: (newStatus: number, row: SystemUserApi.SystemUser) => Promise<boolean>,
): VxeTableGridColumns {
  return [
    { field: 'name', title: '名称', width: 200 },
    { field: 'account', title: '账号', width: 160 },
    {
      cellRender: {
        attrs: { beforeChange: onStatusChange },
        name: onStatusChange ? 'CellSwitch' : 'CellTag',
      },
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

### 1.4 modules/form.vue

```vue
<script lang="ts" setup>
import type { SystemUserApi } from '#/api';

import { ref } from 'vue';

import { useVbenDrawer } from '@vben/common-ui';

import { useVbenForm } from '#/adapter/form';
import { createUser, updateUser } from '#/api';

import { useFormSchema } from '../data';

const emit = defineEmits<{ success: [] }>();

const id = ref<string>();
const [Form, formApi] = useVbenForm({
  schema: useFormSchema(),
  showDefaultActions: false,
});

const [Drawer, drawerApi] = useVbenDrawer<null | SystemUserApi.SystemUser>({
  async onConfirm() {
    const { valid } = await formApi.validate();
    if (!valid) return;
    const values = await formApi.getValues();
    drawerApi.lock();
    (id.value ? updateUser(id.value, values) : createUser(values))
      .then(() => {
        emit('success');
        drawerApi.close();
      })
      .catch(() => drawerApi.unlock());
  },
  async onOpenChange(isOpen) {
    if (!isOpen) return;
    const data = drawerApi.getData();
    formApi.reset();
    if (data) {
      id.value = data.id;
      formApi.setValues(data);
    } else {
      id.value = undefined;
    }
  },
});
</script>

<template>
  <Drawer :title="id ? '编辑' : '新增'">
    <Form />
  </Drawer>
</template>
```

---

## 2. Dashboard 页面（数据统计）

```vue
<script lang="ts" setup>
import type { EchartsUIType } from '@vben/plugins/echarts';

import { onMounted, ref } from 'vue';

import { Page } from '@vben/common-ui';
import { EchartsUI, useEcharts } from '@vben/plugins/echarts';
import { Card } from 'ant-design-vue';

const chartRef = ref<EchartsUIType>();
const { renderEcharts } = useEcharts(chartRef);

const stats = [
  { label: '总销售额', value: '¥ 1,280,000' },
  { label: '订单数', value: '3,420' },
  { label: '客单价', value: '¥ 374' },
  { label: '环比增长', value: '+12.5%' },
];

onMounted(() => {
  renderEcharts({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月'],
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '销售额',
        type: 'line',
        smooth: true,
        data: [82000, 93200, 101000, 118000, 129000, 141000],
      },
    ],
  });
});
</script>

<template>
  <Page auto-content-height>
    <div class="flex flex-col gap-4 p-4">
      <!-- 概览卡片 -->
      <div class="grid grid-cols-4 gap-4">
        <Card v-for="item in stats" :key="item.label">
          <div class="text-sm text-gray-500">{{ item.label }}</div>
          <div class="mt-2 text-2xl font-semibold">{{ item.value }}</div>
        </Card>
      </div>

      <!-- 趋势图 -->
      <Card title="销售趋势">
        <EchartsUI ref="chartRef" height="360px" />
      </Card>
    </div>
  </Page>
</template>
```

---

## 3. Tree 页面（权限/菜单/组织）

用树形表格展示层级数据：

```ts
// data.ts 中的列定义加 treeConfig
{
  field: 'name',
  title: '名称',
  treeNode: true,   // 关键：标记为树节点列
  width: 240,
}
```

```ts
// list.vue 的 gridOptions 里
treeConfig: {
  transform: false,   // 后端已返回嵌套结构
  rowField: 'id',
  parentField: 'parentId',
},
```

---

## 4. 路由模块文件

每个一级模块一个文件，放在 `src/router/routes/modules/`：

```ts
import type { RouteRecordRaw } from 'vue-router';

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

> **不要**修改 `routes/index.ts`，它用 `import.meta.glob('./modules/**/*.ts')` 自动收集。

---

## 5. API 模块文件

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

## 6. 状态列渲染器

| 渲染器 | 用途 | 配置 |
| --- | --- | --- |
| `CellSwitch` | 开关（可切换状态） | `attrs: { beforeChange }` |
| `CellTag` | 只读标签 | `props: { ... }` |
| `CellImage` | 图片 | `props: { width, height }` |
| `CellLink` | 链接按钮 | `props: { text }` |

状态列标准写法：

```ts
{
  cellRender: {
    attrs: { beforeChange: onStatusChange },   // 有交互时
    name: onStatusChange ? 'CellSwitch' : 'CellTag',
  },
  field: 'status',
  title: '状态',
  width: 100,
}
```

---

## 7. 生成检查清单

每个页面生成后核对这些：

| # | 检查项 |
| --- | --- |
| 1 | `list.vue` 用了 `<Page auto-content-height>` |
| 2 | 表格用 `useVbenVxeGrid`，不是手写 table |
| 3 | `proxyConfig.ajax.query` 返回 `{ items, total }` 结构 |
| 4 | `rowConfig.keyField` 与数据主键一致 |
| 5 | 列定义里操作列有 `slots: { default: 'action' }` |
| 6 | 表单 schema 的 `fieldName` 与 API 字段一致 |
| 7 | 抽屉用 `connectedComponent` 挂载，`destroyOnClose: true` |
| 8 | 编辑时 `setData(row)`，新增时 `setData(null)` |
| 9 | 删除操作带 `popConfirm` |
| 10 | 所有 import 来源正确（见第 0 节） |
