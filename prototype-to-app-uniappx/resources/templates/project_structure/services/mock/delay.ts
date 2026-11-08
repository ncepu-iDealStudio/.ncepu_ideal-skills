/**
 * mock 延迟
 *
 * 目的：让加载态真实可见，避免页面"瞬间出现"掩盖了 loading 逻辑的问题。
 */

/** 返回一个在 [min, max] 毫秒后 resolve 的 Promise */
export function mockDelay(min: number = 200, max: number = 800): Promise<void> {
  const ms = Math.floor(Math.random() * (max - min + 1)) + min
  return new Promise((resolve) => {
    setTimeout(() => resolve(), ms)
  })
}
