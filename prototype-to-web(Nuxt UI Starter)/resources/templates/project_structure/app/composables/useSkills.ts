/**
 * 技能列表组合式函数
 * 持有列表状态，调用 skillService 获取数据
 */
export const useSkills = () => {
  const items = ref<Skill[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function load() {
    loading.value = true
    error.value = null
    try {
      items.value = await skillService.getSkills()
    }
    catch (e) {
      error.value = e instanceof Error ? e.message : '加载失败，请重试'
    }
    finally {
      loading.value = false
    }
  }

  return { items, loading, error, load }
}
