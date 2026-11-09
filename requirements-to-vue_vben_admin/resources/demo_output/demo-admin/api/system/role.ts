import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace SystemRoleApi {
  export interface SystemRole {
    [key: string]: any;
    id: string;
    code: string;
    description: string;
    name: string;
    status: 0 | 1;
    remark: string;
    createTime: string;
  }
}

export async function getSystemRoleList(params: Recordable<any>) {
  return requestClient.get<Array<SystemRoleApi.SystemRole>>('/system/role/list', { params });
}

export async function createSystemRole(data: Omit<SystemRoleApi.SystemRole, 'id'>) {
  return requestClient.post('/system/role', data);
}

export async function updateSystemRole(id: string, data: Omit<SystemRoleApi.SystemRole, 'id'>) {
  return requestClient.put(`/system/role/${id}`, data);
}

export async function deleteSystemRole(id: string) {
  return requestClient.delete(`/system/role/${id}`);
}
