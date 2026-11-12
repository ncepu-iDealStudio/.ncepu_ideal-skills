/**
 * 技能数据服务层（唯一数据接缝）
 *
 * 对接后端时：
 * 1. 将 useMock 改为 false
 * 2. 确认 $fetch 的 API 路径与返回结构
 * 3. 页面与 composable 零改动
 */

const useMock = true
const API_BASE = '/api'

/** 模拟网络延迟 */
function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/** mock 数据：与真实接口同形状 */
const mockSkills: Skill[] = [
  { id: '1', title: 'Vue 3 组合式 API 入门', userName: '张三', avatar: '', tags: ['前端', 'Vue'], createdAt: '2024-01-15' },
  { id: '2', title: 'TypeScript 类型体操实战', userName: '李四', avatar: '', tags: ['TypeScript'], createdAt: '2024-01-14' },
  { id: '3', title: 'Tailwind CSS 实用技巧', userName: '王五', avatar: '', tags: ['CSS', 'Tailwind'], createdAt: '2024-01-13' },
  { id: '4', title: 'Nuxt 4 全栈开发指南', userName: '赵六', avatar: '', tags: ['Nuxt', '全栈'], createdAt: '2024-01-12' }
]

export const skillService = {
  /** 获取技能列表 */
  async getSkills(): Promise<Skill[]> {
    if (useMock) {
      await delay(300)
      return mockSkills
    }
    return await $fetch<Skill[]>(`${API_BASE}/skills`)
  },

  /** 根据 ID 获取技能详情 */
  async getSkillById(id: string): Promise<Skill | null> {
    if (useMock) {
      await delay(200)
      return mockSkills.find(s => s.id === id) ?? null
    }
    return await $fetch<Skill>(`${API_BASE}/skills/${id}`)
  }
}
