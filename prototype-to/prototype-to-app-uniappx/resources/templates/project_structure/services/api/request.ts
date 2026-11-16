/**
 * 请求封装
 *
 * 这是整个工程对接后端的唯一接缝：
 * - USE_MOCK = true  时所有请求走 services/mock
 * - USE_MOCK = false 时走真实 HTTP
 *
 * 对接接口文档时：在对应业务函数内映射字段，再让该函数走 request()。
 * 仍有函数未对接时，不要把 USE_MOCK 改成 false。
 */

/** 是否使用 mock 数据。未对接的函数读取它；不要提前改成 false。 */
export const USE_MOCK = true

/** 后端接口基地址。对接时改成你的域名。 */
export const BASE_URL = 'https://api.example.com'

/** 统一响应结构，按你的后端规范调整 */
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
}

/**
 * 发起请求，自动解包 data 字段。
 * 失败时抛出错误，由调用方 try/catch 或上层统一处理。
 */
export function request<T>(options: RequestOptions): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    uni.request({
      url: BASE_URL + options.url,
      method: options.method ?? 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        ...(options.header ?? {})
      },
      success: (res) => {
        const body = res.data as ApiResponse<T>
        if (res.statusCode >= 200 && res.statusCode < 300 && body.code === 0) {
          resolve(body.data)
        } else {
          reject(new Error(body?.message || `请求失败：${res.statusCode}`))
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || '网络异常'))
      }
    })
  })
}
