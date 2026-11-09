import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSkillList } from '@/services/modules/skill'
import type { SkillItem } from '@/types'

export const useSkillStore = defineStore('skill', () => {
  const page = ref(1)
  const pageSize = 10
  const hasMore = ref(true)

  /** 加载第一页 */
  async function fetchList(reset = true): Promise<SkillItem[]> {
    if (reset) {
      page.value = 1
      hasMore.value = true
    }
    const rows = await getSkillList({ page: page.value, pageSize })
    if (rows.length < pageSize) hasMore.value = false
    return rows
  }

  /** 加载下一页 */
  async function loadMore(): Promise<SkillItem[]> {
    if (!hasMore.value) return []
    page.value += 1
    const rows = await getSkillList({ page: page.value, pageSize })
    if (rows.length < pageSize) hasMore.value = false
    return rows
  }

  return { page, hasMore, fetchList, loadMore }
})
