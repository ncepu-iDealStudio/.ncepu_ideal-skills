/**
 * 校验工具（纯函数）
 */

/** 是否为空字符串或纯空白 */
export function isBlank(value: string): boolean {
  return !value || value.trim().length === 0
}

/** 中国大陆手机号 */
export function isPhone(value: string): boolean {
  return /^1[3-9]\d{9}$/.test(value)
}

/** 邮箱 */
export function isEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

/** 长度区间校验，返回错误信息或空字符串 */
export function checkLength(value: string, min: number, max: number, label: string): string {
  const len = (value ?? '').trim().length
  if (len < min) return `${label}不能少于 ${min} 个字`
  if (len > max) return `${label}不能超过 ${max} 个字`
  return ''
}
