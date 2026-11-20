import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace BusinessProductApi {
  export interface BusinessProduct {
    [key: string]: any;
    id: string;
    sku: string;
    category: string;
    price: number;
    stock: number;
    name: string;
    status: 0 | 1;
    remark: string;
    createTime: string;
  }
}

export async function getBusinessProductList(params: Recordable<any>) {
  return requestClient.get<Array<BusinessProductApi.BusinessProduct>>('/business/product/list', { params });
}

export async function createBusinessProduct(data: Omit<BusinessProductApi.BusinessProduct, 'id'>) {
  return requestClient.post('/business/product', data);
}

export async function updateBusinessProduct(id: string, data: Omit<BusinessProductApi.BusinessProduct, 'id'>) {
  return requestClient.put(`/business/product/${id}`, data);
}

export async function deleteBusinessProduct(id: string) {
  return requestClient.delete(`/business/product/${id}`);
}
