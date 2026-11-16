import { request } from '../request'
import type { LoginResult, UserInfo } from '@/types'

/** 登录 */
export function login(data: { account: string; password: string }) {
  return request<LoginResult>({ url: '/auth/login', method: 'POST', data })
}

/** 获取当前用户信息 */
export function getUserInfo() {
  return request<UserInfo>({ url: '/auth/userinfo' })
}
