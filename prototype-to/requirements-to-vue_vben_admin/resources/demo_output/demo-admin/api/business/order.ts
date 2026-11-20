import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace BusinessOrderApi {
  export interface BusinessOrder {
    [key: string]: any;
    id: string;
    orderNo: string;
    customerName: string;
    amount: number;
    orderTime: string;
    name: string;
    status: 0 | 1;
    remark: string;
    createTime: string;
  }
}

export async function getBusinessOrderList(params: Recordable<any>) {
  return requestClient.get<Array<BusinessOrderApi.BusinessOrder>>('/business/order/list', { params });
}

export async function createBusinessOrder(data: Omit<BusinessOrderApi.BusinessOrder, 'id'>) {
  return requestClient.post('/business/order', data);
}

export async function updateBusinessOrder(id: string, data: Omit<BusinessOrderApi.BusinessOrder, 'id'>) {
  return requestClient.put(`/business/order/${id}`, data);
}

export async function deleteBusinessOrder(id: string) {
  return requestClient.delete(`/business/order/${id}`);
}
