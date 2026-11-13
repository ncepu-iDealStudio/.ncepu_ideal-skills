/**
 * 示例接口：GET /api/skills/:id
 * 找不到时返回 404，前端 service 收到后进入错误态。
 */
const skills = [
  { id: '1', title: 'Vue 3 组合式 API 入门', userName: '张三', avatar: '', tags: ['前端', 'Vue'], createdAt: '2024-01-15' },
  { id: '2', title: 'TypeScript 类型体操实战', userName: '李四', avatar: '', tags: ['TypeScript'], createdAt: '2024-01-14' },
  { id: '3', title: 'Tailwind CSS 实用技巧', userName: '王五', avatar: '', tags: ['CSS', 'Tailwind'], createdAt: '2024-01-13' },
  { id: '4', title: 'Nuxt 4 全栈开发指南，这是一条故意写得很长的标题用来检查卡片是否截断', userName: '赵六', avatar: '', tags: ['Nuxt', '全栈'], createdAt: '2024-01-12' },
  { id: '5', title: '没有头像的技能', userName: '钱七', avatar: '', tags: ['示例'], createdAt: '2024-01-11' },
  { id: '6', title: 'ESLint 与类型检查', userName: '孙八', avatar: '', tags: ['工程化'], createdAt: '2024-01-10' }
]

export default defineEventHandler((event) => {
  const id = getRouterParam(event, 'id')
  const found = skills.find(item => item.id === id)
  if (!found) {
    throw createError({ statusCode: 404, statusMessage: '技能不存在' })
  }
  return found
})
