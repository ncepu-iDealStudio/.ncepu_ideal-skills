import { View, Text, ScrollView } from '@tarojs/components'
import Taro, { useLoad } from '@tarojs/taro'
import { useState } from 'react'
import Empty from '@/components/Empty'
import { getSkillDetail } from '@/services/modules/skill'
import type { SkillItem } from '@/types'
import './index.scss'

export default function Detail() {
  const [detail, setDetail] = useState<SkillItem | null>(null)
  const [loading, setLoading] = useState(true)
  const [skillId, setSkillId] = useState('')

  async function load(id: string) {
    try {
      setLoading(true)
      setDetail(await getSkillDetail(id))
    } catch {
      setDetail(null)
    } finally {
      setLoading(false)
    }
  }

  function onSwap() {
    Taro.showModal({
      title: '发起互换',
      content: '将向对方发送互换请求，确认吗？',
      success(res) {
        if (res.confirm) {
          Taro.showToast({ title: '已发送请求', icon: 'none' })
        }
      },
    })
  }

  useLoad((options) => {
    const id = options?.id || ''
    setSkillId(id)
    load(id)
  })

  if (loading) {
    return (
      <View className="page__loading">
        <Text className="page__loading-text">加载中…</Text>
      </View>
    )
  }

  if (!detail) {
    return <Empty text="内容不存在或已下架" />
  }

  return (
    <View className="page">
      <ScrollView className="page__body" scrollY>
        <View className="content">
          <Text className="content__title">{detail.title}</Text>
          <View className="content__meta">
            <Text className="content__meta-text">{detail.userName}</Text>
          </View>

          {detail.tags?.length > 0 && (
            <View className="content__tags">
              {detail.tags.map((tag) => (
                <Text key={tag} className="tag">{tag}</Text>
              ))}
            </View>
          )}

          {detail.description && (
            <View className="content__section">
              <Text className="content__section-title">详细介绍</Text>
              <Text className="content__text">{detail.description}</Text>
            </View>
          )}
        </View>
      </ScrollView>

      <View className="bottom-bar">
        <View className="bottom-bar__btn" hoverClass="bottom-bar__btn--active" onClick={onSwap}>
          <Text className="bottom-bar__btn-text">发起互换</Text>
        </View>
      </View>
    </View>
  )
}
