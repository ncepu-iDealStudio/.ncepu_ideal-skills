/**
 * 技能列表。
 * 用 useAsyncData 包住 service，预渲染和客户端共用同一次结果。
 * 页面只调用本函数，不要再写 onMounted 去 load。
 */
export const useSkills = () => {
  const requestFetch = useRequestFetch()
  const apiBase = useRuntimeConfig().public.apiBase

  const { data, pending, error, refresh } = useAsyncData(
    'skills',
    () => skillService.getSkills(requestFetch, apiBase),
    { default: () => [] as Skill[] }
  )

  const message = computed(() => error.value?.message ?? null)

  return {
    items: data,
    loading: pending,
    error: message,
    load: refresh
  }
}
