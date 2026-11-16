import { request } from '../request'
import type { SkillItem } from '@/types'

export function getSkillList(params: { page?: number; pageSize?: number }) {
  return request<SkillItem[]>({ url: '/skills', data: params })
}

export function getSkillDetail(id: number | string) {
  return request<SkillItem>({ url: `/skills/${id}` })
}
