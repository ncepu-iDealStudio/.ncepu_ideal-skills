
/** 技能条目 */
export interface SkillItem {
  id: number
  title: string
  userName: string
  avatar?: string
  tags: string[]
  wantTags?: string[]
  rating?: number
  swapCount?: number
  description?: string
}
