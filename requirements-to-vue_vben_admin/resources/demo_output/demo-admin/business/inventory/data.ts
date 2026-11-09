import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridColumns } from '#/adapter/vxe-table';

export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'productName', label: '商品' },
    { component: 'Input', fieldName: 'warehouse', label: '仓库' },
    { component: 'Input', fieldName: 'quantity', label: '库存数量' },
  ];
}

export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'productName', label: '商品' },
    { component: 'Input', fieldName: 'warehouse', label: '仓库' },
    { component: 'InputNumber', fieldName: 'quantity', label: '库存数量' },
    { component: 'InputNumber', fieldName: 'warningLine', label: '预警线' },
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    { component: 'RadioGroup', fieldName: 'status', label: '状态' },
    { component: 'Textarea', fieldName: 'remark', label: '备注' },
  ];
}

export function useColumns(): VxeTableGridColumns {
  return [
    { field: 'productName', title: '商品', width: 200 },
    { field: 'warehouse', title: '仓库', width: 160 },
    { field: 'quantity', title: '库存数量', width: 120 },
    { field: 'warningLine', title: '预警线', width: 120 },
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
