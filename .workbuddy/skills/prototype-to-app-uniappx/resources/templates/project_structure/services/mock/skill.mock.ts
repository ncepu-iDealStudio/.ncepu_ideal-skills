/**
 * 技能相关的 mock 数据
 *
 * 遵循 resources/config/mock_policy.json：
 * - 数量足够撑满一屏（10 条以上）
 * - 含超长文本、缺图、零值等边界情况
 * - 文案为中文，与真实业务一致
 */

import type { Skill } from '@/types/skill'

export const mockSkillList: Skill[] = [
  {
    id: 1,
    title: '摄影入门：从构图到后期',
    userName: '李同学',
    avatar: '/static/placeholder.png',
    tags: ['摄影', '后期'],
    wantTags: ['吉他'],
    rating: 4.9,
    swapCount: 12,
    description: '会拍人像和风景，想找人教我弹吉他，零基础。'
  },
  {
    id: 2,
    title: '吉他弹唱，可以带你从零开始',
    userName: '王同学',
    avatar: '/static/placeholder.png',
    tags: ['吉他', '弹唱'],
    wantTags: ['摄影'],
    rating: 4.7,
    swapCount: 8,
    description: '学琴五年，能教基础和弦与弹唱，想学摄影。'
  },
  {
    id: 3,
    title: 'Python 数据分析入门',
    userName: '张同学',
    avatar: '/static/placeholder.png',
    tags: ['编程', '数据分析'],
    wantTags: ['英语口语'],
    rating: 5.0,
    swapCount: 21,
    description: '做过两个数据分析项目，可以带入门 pandas 与可视化。'
  },
  {
    id: 4,
    title: '英语口语陪练，雅思 7.5',
    userName: '陈同学',
    avatar: '',
    tags: ['英语', '雅思'],
    wantTags: ['编程'],
    rating: 4.8,
    swapCount: 15,
    description: '可以提供口语陪练和雅思备考建议。'
  },
  {
    id: 5,
    title: '这个标题非常长用来验证列表项在遇到超长文本时的换行与截断表现是否正常不会把卡片撑破',
    userName: '测试长文本',
    avatar: '/static/placeholder.png',
    tags: ['测试', '边界'],
    wantTags: [],
    rating: 3.0,
    swapCount: 0,
    description: '这条数据专门用于验证超长标题的渲染效果，不应导致布局错乱或文字溢出容器。'
  },
  {
    id: 6,
    title: '手绘插画与板绘',
    userName: '赵同学',
    avatar: '/static/placeholder.png',
    tags: ['插画', '板绘'],
    wantTags: ['视频剪辑'],
    rating: 4.6,
    swapCount: 6,
    description: '擅长日系插画，会用 Procreate 和 PS。'
  },
  {
    id: 7,
    title: '视频剪辑：剪映与 Pr 都行',
    userName: '孙同学',
    avatar: '/static/placeholder.png',
    tags: ['视频', '剪辑'],
    wantTags: ['手绘'],
    rating: 4.5,
    swapCount: 4,
    description: '做过校园宣传片，能教基础剪辑节奏与调色。'
  },
  {
    id: 8,
    title: '高数辅导，期末突击',
    userName: '周同学',
    avatar: '/static/placeholder.png',
    tags: ['数学', '辅导'],
    wantTags: ['日语'],
    rating: 4.9,
    swapCount: 33,
    description: '高数两学期 95+，讲题耐心。'
  },
  {
    id: 9,
    title: '日语五十音到 N2 备考',
    userName: '吴同学',
    avatar: '/static/placeholder.png',
    tags: ['日语', 'N2'],
    wantTags: ['数学'],
    rating: 4.4,
    swapCount: 2,
    description: '已过 N1，可以带入门和应试技巧。'
  },
  {
    id: 10,
    title: '健身与饮食规划',
    userName: '郑同学',
    avatar: '/static/placeholder.png',
    tags: ['健身', '饮食'],
    wantTags: ['游泳'],
    rating: 4.3,
    swapCount: 1,
    description: '系统训练两年，可制定入门计划。'
  },
  {
    id: 11,
    title: '游泳教学（蛙泳/自由泳）',
    userName: '冯同学',
    avatar: '/static/placeholder.png',
    tags: ['游泳'],
    wantTags: ['健身'],
    rating: 4.7,
    swapCount: 9,
    description: '校游泳队，可在校游泳馆带练。'
  },
  {
    id: 12,
    title: 'PPT 设计与排版',
    userName: '蒋同学',
    avatar: '/static/placeholder.png',
    tags: ['设计', 'PPT'],
    wantTags: ['摄影'],
    rating: 4.8,
    swapCount: 18,
    description: '做过多次答辩 PPT，注重信息层级。'
  }
]

/** 空列表示例，用于验证空态渲染 */
export const mockSkillEmpty: Skill[] = []
