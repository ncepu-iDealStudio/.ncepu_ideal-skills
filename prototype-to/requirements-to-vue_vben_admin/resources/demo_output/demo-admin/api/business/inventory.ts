import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace BusinessInventoryApi {
  export interface BusinessInventory {
    [key: string]: any;
    id: string;
    productName: string;
    warehouse: string;
    quantity: number;
    warningLine: number;
    name: string;
    status: 0 | 1;
    remark: string;
    createTime: string;
  }
}

export async function getBusinessInventoryList(params: Recordable<any>) {
  return requestClient.get<Array<BusinessInventoryApi.BusinessInventory>>('/business/inventory/list', { params });
}

export async function createBusinessInventory(data: Omit<BusinessInventoryApi.BusinessInventory, 'id'>) {
  return requestClient.post('/business/inventory', data);
}

export async function updateBusinessInventory(id: string, data: Omit<BusinessInventoryApi.BusinessInventory, 'id'>) {
  return requestClient.put(`/business/inventory/${id}`, data);
}

export async function deleteBusinessInventory(id: string) {
  return requestClient.delete(`/business/inventory/${id}`);
}
