import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace SystemPermissionApi {
  export interface SystemPermission {
    [key: string]: any;
    id: string;
    name: string;
    code: string;
    type: string;
  }
}

export async function getSystemPermissionList(params: Recordable<any>) {
  return requestClient.get<Array<SystemPermissionApi.SystemPermission>>('/system/permission/list', { params });
}

export async function createSystemPermission(data: Omit<SystemPermissionApi.SystemPermission, 'id'>) {
  return requestClient.post('/system/permission', data);
}

export async function updateSystemPermission(id: string, data: Omit<SystemPermissionApi.SystemPermission, 'id'>) {
  return requestClient.put(`/system/permission/${id}`, data);
}

export async function deleteSystemPermission(id: string) {
  return requestClient.delete(`/system/permission/${id}`);
}
