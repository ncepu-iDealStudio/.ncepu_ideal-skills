import { defineStore } from 'pinia'
import { ref } from 'vue'
import Taro from '@tarojs/taro'
import { login, getUserInfo } from '@/services/modules/auth'
import type { UserInfo } from '@/types'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(Taro.getStorageSync('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  async function doLogin(account: string, password: string) {
    const res = await login({ account, password })
    token.value = res.token
    userInfo.value = res.user
    Taro.setStorageSync('token', res.token)
    return res
  }

  async function fetchUserInfo() {
    if (!token.value) return null
    userInfo.value = await getUserInfo()
    return userInfo.value
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    Taro.removeStorageSync('token')
    Taro.reLaunch({ url: '/pages/login/index' })
  }

  return { token, userInfo, doLogin, fetchUserInfo, logout }
})
