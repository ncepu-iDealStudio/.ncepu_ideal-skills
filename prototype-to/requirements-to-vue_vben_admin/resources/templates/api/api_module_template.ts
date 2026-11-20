import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace SystemUserApi {
  export interface SystemUser {
    [key: string]: any;
    id: string;
    account: string;
    nickname: string;
    email: string;
    phone: string;
    name: string;
    status: 0 | 1;
    remark: string;
    createTime: string;
  }
}

export async function getSystemUserList(params: Recordable<any>) {
  return requestClient.get<Array<SystemUserApi.SystemUser>>('/system/user/list', { params });
}

export async function createSystemUser(data: Omit<SystemUserApi.SystemUser, 'id'>) {
  return requestClient.post('/system/user', data);
}

export async function updateSystemUser(id: string, data: Omit<SystemUserApi.SystemUser, 'id'>) {
  return requestClient.put(`/system/user/${id}`, data);
}

export async function deleteSystemUser(id: string) {
  return requestClient.delete(`/system/user/${id}`);
}
