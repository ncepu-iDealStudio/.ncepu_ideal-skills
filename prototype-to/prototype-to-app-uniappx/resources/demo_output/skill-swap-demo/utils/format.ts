/**
 * 格式化工具（纯函数，无副作用）
 */

/** 数字千分位，如 12345 -> "12,345" */
export function formatNumber(value: number): string {
  if (value === null || value === undefined) return '0'
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/** 评分保留一位小数，如 4.85 -> "4.9" */
export function formatRating(value: number): string {
  if (value === null || value === undefined) return '0.0'
  return value.toFixed(1)
}

/** 按最大长度截断并追加省略号 */
export function truncate(text: string, maxLength: number): string {
  if (!text) return ''
  return text.length > maxLength ? text.slice(0, maxLength) + '…' : text
}

/** 时间戳（毫秒）转 "YYYY-MM-DD" */
export function formatDate(timestamp: number): string {
  const d = new Date(timestamp)
  const pad = (n: number) => (n < 10 ? '0' + n : '' + n)
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}
