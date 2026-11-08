/**
 * 数据模型：技能
 * 字段与未来后端接口保持一致，避免对接时改动页面。
 */

export interface Skill {
  /** 主键 */
  id: number
  /** 技能标题 */
  title: string
  /** 发布者昵称 */
  userName: string
  /** 头像地址，空字符串表示无头像 */
  avatar: string
  /** 我会的技能标签 */
  tags: string[]
  /** 我想学的技能标签 */
  wantTags: string[]
  /** 评分 0-5 */
  rating: number
  /** 已成功互换次数 */
  swapCount: number
  /** 补充说明 */
  description: string
}
