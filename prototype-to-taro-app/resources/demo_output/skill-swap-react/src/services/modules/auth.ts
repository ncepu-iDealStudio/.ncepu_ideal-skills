import { request } from '../request'
import type { LoginResult, UserInfo } from '@/types'

export function login(data: { account: string; password: string }) {
  return request<LoginResult>({ url: '/auth/login', method: 'POST', data })
}

export function getUserInfo() {
  return request<UserInfo>({ url: '/auth/userinfo' })
}
