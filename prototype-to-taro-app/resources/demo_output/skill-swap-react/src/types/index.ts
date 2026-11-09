/** 通用分页响应 */
export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

/** 分页请求参数 */
export interface PageQuery {
  page?: number
  pageSize?: number
}

/** 登录用户信息 */
export interface UserInfo {
  id: string
  name: string
  avatar?: string
}

/** 登录响应 */
export interface LoginResult {
  token: string
  user: UserInfo
}
