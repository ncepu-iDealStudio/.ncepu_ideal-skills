/**
 * 统一请求封装
 *
 * 职责：
 * - 拼接 baseURL（来自多环境配置 defineConstants）
 * - 自动带 token
 * - 统一解包 { code, message, data }
 * - 401 自动跳登录
 */
import Taro from '@tarojs/taro'

declare const TARO_APP_API: string

export const BASE_URL = TARO_APP_API || 'https://api.example.com'

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, any>
  header?: Record<string, string>
  /** 是否显示全局 loading，默认 false */
  showLoading?: boolean
}

export function request<T>(options: RequestOptions): Promise<T> {
  const { url, method = 'GET', data, header = {}, showLoading = false } = options

  if (showLoading) {
    Taro.showLoading({ title: '加载中', mask: true })
  }

  return new Promise<T>((resolve, reject) => {
    Taro.request({
      url: BASE_URL + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        Authorization: Taro.getStorageSync('token') || '',
        ...header,
      },
      success(res) {
        const body = res.data as ApiResponse<T>

        // 401：登录态失效
        if (res.statusCode === 401) {
          Taro.removeStorageSync('token')
          Taro.showToast({ title: '登录已过期', icon: 'none' })
          setTimeout(() => Taro.reLaunch({ url: '/pages/login/index' }), 800)
          reject(new Error('登录已过期'))
          return
        }

        if (res.statusCode >= 200 && res.statusCode < 300 && body?.code === 0) {
          resolve(body.data)
        } else {
          const msg = body?.message || `请求失败(${res.statusCode})`
          Taro.showToast({ title: msg, icon: 'none' })
          reject(new Error(msg))
        }
      },
      fail(err) {
        Taro.showToast({ title: '网络异常，请重试', icon: 'none' })
        reject(new Error(err.errMsg || '网络异常'))
      },
      complete() {
        if (showLoading) Taro.hideLoading()
      },
    })
  })
}
