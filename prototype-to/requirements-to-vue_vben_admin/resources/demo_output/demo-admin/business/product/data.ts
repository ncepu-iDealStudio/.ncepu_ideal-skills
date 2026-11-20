import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridColumns } from '#/adapter/vxe-table';

export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'sku', label: 'SKU' },
    { component: 'Input', fieldName: 'category', label: '分类' },
    { component: 'Input', fieldName: 'price', label: '价格' },
  ];
}

export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'sku', label: 'SKU' },
    { component: 'Input', fieldName: 'category', label: '分类' },
    { component: 'InputNumber', fieldName: 'price', label: '价格' },
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    { component: 'RadioGroup', fieldName: 'status', label: '状态' },
    { component: 'Textarea', fieldName: 'remark', label: '备注' },
  ];
}

export function useColumns(): VxeTableGridColumns {
  return [
    { field: 'sku', title: 'SKU', width: 160 },
    { field: 'category', title: '分类', width: 140 },
    { field: 'price', title: '价格', width: 120 },
    { field: 'stock', title: '库存', width: 100 },
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
