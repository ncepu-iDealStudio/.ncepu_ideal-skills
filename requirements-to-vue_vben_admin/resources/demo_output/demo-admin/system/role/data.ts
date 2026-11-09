import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridColumns } from '#/adapter/vxe-table';

export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'code', label: '角色编码' },
    { component: 'Input', fieldName: 'id', label: 'ID' },
    { component: 'Input', fieldName: 'name', label: '名称' },
  ];
}

export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'code', label: '角色编码', rules: 'required' },
    { component: 'Textarea', fieldName: 'description', label: '描述' },
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    { component: 'RadioGroup', fieldName: 'status', label: '状态' },
    { component: 'Textarea', fieldName: 'remark', label: '备注' },
  ];
}

export function useColumns(): VxeTableGridColumns {
  return [
    { field: 'code', title: '角色编码', width: 160 },
    { field: 'description', title: '描述', width: 160 },
    { field: 'id', title: 'ID', width: 200 },
    { field: 'name', title: '名称', width: 200 },
    {
      cellRender: { name: 'CellSwitch' },
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
