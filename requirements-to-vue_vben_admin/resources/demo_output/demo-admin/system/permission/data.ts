import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridColumns } from '#/adapter/vxe-table';

export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'id', label: 'ID' },
    { component: 'Input', fieldName: 'name', label: '名称' },
    { component: 'Input', fieldName: 'code', label: '编码' },
  ];
}

export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    { component: 'Input', fieldName: 'code', label: '编码' },
    { component: 'Input', fieldName: 'type', label: '类型' },
  ];
}

export function useColumns(): VxeTableGridColumns {
  return [
    { field: 'id', title: 'ID', width: 200 },
    { field: 'name', title: '名称', width: 160 },
    { field: 'code', title: '编码', width: 200 },
    { field: 'type', title: '类型', width: 120 },
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
