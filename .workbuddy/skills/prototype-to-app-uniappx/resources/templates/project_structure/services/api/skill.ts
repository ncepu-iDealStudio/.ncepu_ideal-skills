/**
 * 示例业务接口：技能列表
 *
 * 页面只调用这里导出的函数，不直接接触 mock 或 HTTP 细节。
 * 对接接口文档时，保持函数签名不变，在函数内把文档字段映射成 Skill，再走 request()。
 * 文档的 data 还不是 Skill 时，不要写成 request<Skill[]>()。未对接的函数继续走 USE_MOCK。
 */

import { USE_MOCK, request } from './request'
import { mockDelay } from '../mock/delay'
import { mockSkillList, mockSkillEmpty } from '../mock/skill.mock'
import type { Skill } from '@/types/skill'

/**
 * 获取技能列表（分页）
 * @param page 页码，从 1 开始
 * @param pageSize 每页条数
 */
export async function getSkillList(page: number = 1, pageSize: number = 10): Promise<Skill[]> {
  if (USE_MOCK) {
    await mockDelay()
    // 模拟分页：第 1 页返回全部，第 2 页返回空（便于验证"加载更多到底"）
    if (page === 1) {
      return mockSkillList.slice(0, pageSize)
    }
    return []
  }
  return request<Skill[]>({
    url: '/skills',
    method: 'GET',
    data: { page, pageSize }
  })
}

/**
 * 获取技能详情
 */
export async function getSkillDetail(id: number): Promise<Skill | null> {
  if (USE_MOCK) {
    await mockDelay()
    const found = mockSkillList.find((item) => item.id === id)
    return found ?? null
  }
  return request<Skill>({
    url: `/skills/${id}`,
    method: 'GET'
  })
}

/**
 * 获取空列表示例（用于验证空态）
 * 真实后端一般通过返回空数组实现，此处单独导出便于演示
 */
export function getEmptySkillList(): Skill[] {
  return mockSkillEmpty
}
