<script lang="ts" setup>
import { ref } from 'vue';

import { useVbenDrawer } from '@vben/common-ui';

import { useVbenForm } from '#/adapter/form';

import { useFormSchema } from '../data';

const emit = defineEmits<{ success: [] }>();

const id = ref<string>();
const [Form, formApi] = useVbenForm({
  schema: useFormSchema(),
  showDefaultActions: false,
});

const [Drawer, drawerApi] = useVbenDrawer({
  async onConfirm() {
    const { valid } = await formApi.validate();
    if (!valid) return;
    const values = await formApi.getValues();
    drawerApi.lock();
    // 生成阶段不接真实接口。用户提供接口文档后，按 api_binding.md 调用已有的 create/update。
    console.log('submit', id.value, values);
    setTimeout(() => {
      emit('success');
      drawerApi.close();
    }, 300);
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
