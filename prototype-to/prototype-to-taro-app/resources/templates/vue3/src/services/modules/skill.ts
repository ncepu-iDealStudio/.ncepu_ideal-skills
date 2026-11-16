import { request } from '../request'
import type { SkillItem } from '@/types'

/** 获取技能列表 */
export function getSkillList(params: { page?: number; pageSize?: number }) {
  return request<SkillItem[]>({ url: '/skills', data: params })
}

/** 获取技能详情 */
export function getSkillDetail(id: number | string) {
  return request<SkillItem>({ url: `/skills/${id}` })
}
