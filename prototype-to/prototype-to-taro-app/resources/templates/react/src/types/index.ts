export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

export interface PageQuery {
  page?: number
  pageSize?: number
}

export interface UserInfo {
  id: string
  name: string
  avatar?: string
}

export interface LoginResult {
  token: string
  user: UserInfo
}

export interface SkillItem {
  id: number
  title: string
  userName: string
  avatar?: string
  tags: string[]
  wantTags?: string[]
  rating?: number
  swapCount?: number
  description?: string
}
