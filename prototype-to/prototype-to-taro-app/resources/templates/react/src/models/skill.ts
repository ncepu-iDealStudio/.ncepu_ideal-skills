import { getSkillList } from '@/services/modules/skill'
import type { SkillItem } from '@/types'

interface SkillState {
  list: SkillItem[]
  page: number
  pageSize: number
  hasMore: boolean
  loading: boolean
}

export default {
  namespace: 'skill',

  state: {
    list: [],
    page: 1,
    pageSize: 10,
    hasMore: true,
    loading: false,
  } as SkillState,

  effects: {
    /** 加载第一页 */
    *fetchList(_: unknown, { call, put }: any) {
      yield put({ type: 'setLoading', payload: true })
      try {
        const rows: SkillItem[] = yield call(getSkillList, { page: 1, pageSize: 10 })
        yield put({ type: 'setList', payload: rows })
        yield put({ type: 'setMeta', payload: { page: 1, hasMore: rows.length >= 10 } })
      } finally {
        yield put({ type: 'setLoading', payload: false })
      }
    },

    /** 加载下一页 */
    *loadMore(_: unknown, { call, put, select }: any) {
      const { page, hasMore, list } = yield select((s: any) => s.skill)
      if (!hasMore) return
      const rows: SkillItem[] = yield call(getSkillList, { page: page + 1, pageSize: 10 })
      yield put({
        type: 'appendList',
        payload: { rows, page: page + 1, hasMore: rows.length >= 10 },
      })
    },
  },

  reducers: {
    /** 用 Immer：可直接修改 draft */
    setList(state: SkillState, { payload }: any) {
      state.list = payload
    },
    appendList(state: SkillState, { payload }: any) {
      state.list = [...state.list, ...payload.rows]
      state.page = payload.page
      state.hasMore = payload.hasMore
    },
    setMeta(state: SkillState, { payload }: any) {
      state.page = payload.page
      state.hasMore = payload.hasMore
    },
    setLoading(state: SkillState, { payload }: any) {
      state.loading = payload
    },
  },
}
