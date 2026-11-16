import { View, Text, ScrollView } from '@tarojs/components'
import Taro, { useDidShow, useReachBottom } from '@tarojs/taro'
import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import Empty from '@/components/Empty'
import './index.scss'

export default function Home() {
  const dispatch = useDispatch()
  const { list, loading, hasMore } = useSelector((s: any) => s.skill)
  const [refreshing, setRefreshing] = useState(false)

  async function load(reset = false) {
    setRefreshing(false)
    if (reset) {
      await dispatch({ type: 'skill/fetchList' })
    }
  }

  function onRefresh() {
    setRefreshing(true)
    load(true)
  }

  async function onLoadMore() {
    if (!hasMore) return
    await dispatch({ type: 'skill/loadMore' })
  }

  function goDetail(id: number) {
    Taro.navigateTo({ url: `/pages/detail/index?id=${id}` })
  }

  useDidShow(() => {
    if (list.length === 0) load(true)
  })

  useReachBottom(() => onLoadMore())

  if (loading && list.length === 0) {
    return (
      <View className="page__loading">
        <Text className="page__loading-text">加载中…</Text>
      </View>
    )
  }

  if (list.length === 0) {
    return <Empty text="还没有内容，去发布一个吧" />
  }

  return (
    <ScrollView
      className="page__body"
      scrollY
      refresherEnabled
      refresherTriggered={refreshing}
      onRefresherRefresh={onRefresh}
      onScrollToLower={onLoadMore}
    >
      <View className="page__list">
        {list.map((item: any) => (
          <View
            key={item.id}
            className="card"
            hoverClass="card--active"
            hoverStayTime={100}
            onClick={() => goDetail(item.id)}
          >
            <View className="card__body">
              <Text className="card__title">{item.title}</Text>
              <Text className="card__subtitle">{item.userName}</Text>
              <View className="card__tags">
                {(item.tags || []).map((tag: string) => (
                  <Text key={tag} className="tag">{tag}</Text>
                ))}
              </View>
            </View>
          </View>
        ))}
      </View>

      {!hasMore && (
        <View className="page__footer">
          <Text className="page__footer-text">没有更多了</Text>
        </View>
      )}
    </ScrollView>
  )
}
