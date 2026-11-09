import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridColumns } from '#/adapter/vxe-table';

export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'orderNo', label: '订单号' },
    { component: 'Input', fieldName: 'customerName', label: '客户' },
    { component: 'Input', fieldName: 'amount', label: '金额' },
  ];
}

export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'customerName', label: '客户' },
    { component: 'InputNumber', fieldName: 'amount', label: '金额' },
    { component: 'Input', fieldName: 'name', label: '名称', rules: 'required' },
    { component: 'RadioGroup', fieldName: 'status', label: '状态' },
    { component: 'Textarea', fieldName: 'remark', label: '备注' },
  ];
}

export function useColumns(): VxeTableGridColumns {
  return [
    { field: 'orderNo', title: '订单号', width: 200 },
    { field: 'customerName', title: '客户', width: 160 },
    { field: 'amount', title: '金额', width: 140 },
    { field: 'orderTime', title: '下单时间', width: 200 },
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
