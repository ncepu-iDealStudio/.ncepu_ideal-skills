import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridColumns } from '#/adapter/vxe-table';

export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'account', label: '账号' },
    { component: 'Input', fieldName: 'nickname', label: '昵称' },
    { component: 'Input', fieldName: 'email', label: '邮箱' },
  ];
}

export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'account', label: '账号', rules: 'required' },
    { component: 'Input', fieldName: 'nickname', label: '昵称' },
    { component: 'Input', fieldName: 'email', label: '邮箱' },
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    { component: 'RadioGroup', fieldName: 'status', label: '状态' },
    { component: 'Textarea', fieldName: 'remark', label: '备注' },
  ];
}

export function useColumns(): VxeTableGridColumns {
  return [
    { field: 'account', title: '账号', width: 160 },
    { field: 'nickname', title: '昵称', width: 160 },
    { field: 'email', title: '邮箱', width: 200 },
    { field: 'phone', title: '手机号', width: 150 },
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
