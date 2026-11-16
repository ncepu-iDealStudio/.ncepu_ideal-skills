/**
 * 技能数据服务层（唯一数据接缝）
 *
 * useMock 为 true 时返回本文件里的示例数据。
 * 改为 false 后，用调用方传入的 fetcher 请求真实接口。
 * 基地址来自 nuxt.config 的 runtimeConfig.public.apiBase（可用 NUXT_PUBLIC_API_BASE 覆盖）。
 */

const useMock = true

type Fetcher = typeof $fetch

/** 模拟网络延迟，让加载态可见 */
function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/** 与 server/api/skills.get.ts 的返回字段一致 */
const mockSkills: Skill[] = [
  { id: '1', title: 'Vue 3 组合式 API 入门', userName: '张三', avatar: '', tags: ['前端', 'Vue'], createdAt: '2024-01-15' },
  { id: '2', title: 'TypeScript 类型体操实战', userName: '李四', avatar: '', tags: ['TypeScript'], createdAt: '2024-01-14' },
  { id: '3', title: 'Tailwind CSS 实用技巧', userName: '王五', avatar: '', tags: ['CSS', 'Tailwind'], createdAt: '2024-01-13' },
  { id: '4', title: 'Nuxt 4 全栈开发指南，这是一条故意写得很长的标题用来检查卡片是否截断', userName: '赵六', avatar: '', tags: ['Nuxt', '全栈'], createdAt: '2024-01-12' },
  { id: '5', title: '没有头像的技能', userName: '钱七', avatar: '', tags: ['示例'], createdAt: '2024-01-11' },
  { id: '6', title: 'ESLint 与类型检查', userName: '孙八', avatar: '', tags: ['工程化'], createdAt: '2024-01-10' }
]

function skillsUrl(apiBase: string, id?: string) {
  const path = id ? `/api/skills/${id}` : '/api/skills'
  return `${apiBase}${path}`
}

export const skillService = {
  /** 获取技能列表 */
  async getSkills(fetcher: Fetcher = $fetch, apiBase = ''): Promise<Skill[]> {
    if (useMock) {
      await delay(300)
      return mockSkills
    }
    return await fetcher<Skill[]>(skillsUrl(apiBase))
  },

  /** 根据 ID 获取技能详情 */
  async getSkillById(id: string, fetcher: Fetcher = $fetch, apiBase = ''): Promise<Skill | null> {
    if (useMock) {
      await delay(200)
      return mockSkills.find(s => s.id === id) ?? null
    }
    return await fetcher<Skill>(skillsUrl(apiBase, id))
  }
}
