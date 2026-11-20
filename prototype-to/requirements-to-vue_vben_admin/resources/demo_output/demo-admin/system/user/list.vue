<script lang="ts" setup>
import type { VxeTableGridOptions } from '#/adapter/vxe-table';

import { Page, useVbenDrawer, VbenTableAction } from '@vben/common-ui';
import { Plus } from '@vben/icons';
import { Button } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';

import { useColumns, useGridFormSchema } from './data';
import Form from './modules/form.vue';

const [FormDrawer, formDrawerApi] = useVbenDrawer({
  connectedComponent: Form,
  destroyOnClose: true,
});

const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: { schema: useGridFormSchema(), submitOnChange: true },
  gridOptions: {
    columns: useColumns(),
    height: 'auto',
    keepSource: true,
    rowConfig: { keyField: 'id' },
    toolbarConfig: { custom: true, refresh: true, search: true, zoom: true },
  } as VxeTableGridOptions,
});

function onCreate() {
  formDrawerApi.setData(null).open();
}

function onEdit(row: any) {
  formDrawerApi.setData(row).open();
}

function onRefresh() {
  gridApi.query();
}
</script>

<template>
  <Page auto-content-height>
    <FormDrawer @success="onRefresh" />
    <Grid :table-title="'用户管理'">
      <template #toolbar-tools>
        <Button type="primary" @click="onCreate">
          <Plus class="size-5" />
          新增
        </Button>
      </template>
      <template #action="{ row }">
        <VbenTableAction
          :actions="[{ text: '编辑', icon: 'lucide:edit', onClick: () => onEdit(row) }]"
          align="center"
        />
      </template>
    </Grid>
  </Page>
</template>
