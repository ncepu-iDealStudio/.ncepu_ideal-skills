import Taro from '@tarojs/taro'
import { login, getUserInfo } from '@/services/modules/auth'
import type { UserInfo } from '@/types'

interface UserState {
  token: string
  userInfo: UserInfo | null
}

export default {
  namespace: 'user',

  state: {
    token: Taro.getStorageSync('token') || '',
    userInfo: null,
  } as UserState,

  effects: {
    /** 登录：成功后持久化 token */
    *login({ payload }: any, { call, put }: any) {
      const res: { token: string; user: UserInfo } = yield call(login, payload)
      Taro.setStorageSync('token', res.token)
      yield put({ type: 'setToken', payload: res.token })
      yield put({ type: 'setUserInfo', payload: res.user })
      return res
    },

    /** 拉取用户信息 */
    *fetchUserInfo(_: unknown, { call, put }: any) {
      const info: UserInfo = yield call(getUserInfo)
      yield put({ type: 'setUserInfo', payload: info })
      return info
    },

    /** 登出 */
    *logout(_: unknown, { put }: any) {
      Taro.removeStorageSync('token')
      yield put({ type: 'setToken', payload: '' })
      yield put({ type: 'setUserInfo', payload: null })
      Taro.reLaunch({ url: '/pages/login/index' })
    },
  },

  reducers: {
    setToken(state: UserState, { payload }: any) {
      state.token = payload
    },
    setUserInfo(state: UserState, { payload }: any) {
      state.userInfo = payload
    },
  },
}
