<template>
  <View class="page">
    <!-- 加载态 -->
    <View v-if="loading" class="page__loading">
      <Text class="page__loading-text">加载中…</Text>
    </View>

    <!-- 空态 -->
    <Empty v-else-if="list.length === 0" text="还没有内容，去发布一个吧" />

    <!-- 有数据 -->
    <ScrollView
      v-else
      class="page__body"
      scroll-y
      :refresher-enabled="true"
      :refresher-triggered="refreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="onLoadMore"
    >
      <View class="page__list">
        <View
          v-for="item in list"
          :key="item.id"
          class="card"
          hover-class="card--active"
          :hover-stay-time="100"
          @tap="goDetail(item.id)"
        >
          <View class="card__body">
            <Text class="card__title">{{ item.title }}</Text>
            <Text class="card__subtitle">{{ item.userName }}</Text>
            <View class="card__tags">
              <Text v-for="tag in item.tags" :key="tag" class="tag">{{ tag }}</Text>
            </View>
          </View>
        </View>
      </View>

      <View v-if="noMore" class="page__footer">
        <Text class="page__footer-text">没有更多了</Text>
      </View>
    </ScrollView>
  </View>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Taro, { useDidShow, useReachBottom } from '@tarojs/taro'
import { View, Text, ScrollView } from '@tarojs/components'
import Empty from '@/components/Empty.vue'
import { useSkillStore } from '@/store/modules/skill'
import type { SkillItem } from '@/types'

const list = ref<SkillItem[]>([])
const loading = ref(true)
const refreshing = ref(false)
const noMore = ref(false)
const store = useSkillStore()

async function load(reset = false) {
  if (reset) loading.value = true
  try {
    const rows = await store.fetchList(reset)
    list.value = rows
    noMore.value = rows.length < 10
  } catch {
    // 请求层已提示
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

async function onRefresh() {
  refreshing.value = true
  await load(true)
}

async function onLoadMore() {
  if (noMore.value) return
  const rows = await store.loadMore()
  list.value = [...list.value, ...rows]
  if (rows.length === 0) noMore.value = true
}

function goDetail(id: number) {
  Taro.navigateTo({ url: `/pages/detail/index?id=${id}` })
}

useDidShow(() => {
  if (list.value.length === 0) load(true)
})

useReachBottom(() => onLoadMore())
</script>

<style lang="scss">
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: $color-background;
}

.page__loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $space-xl;
}

.page__loading-text {
  font-size: $font-base;
  color: $text-tertiary;
}

.page__body {
  flex: 1;
}

.page__list {
  padding: $page-padding;
}

.card {
  display: flex;
  flex-direction: row;
  padding: $space-md;
  margin-bottom: $space-md;
  background-color: $color-surface;
  border-radius: $radius-md;
}

.card--active {
  background-color: #F7F8FA;
}

.card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card__title {
  font-size: $font-md;
  font-weight: 500;
  color: $text-primary;
  line-height: 1.5;
}

.card__subtitle {
  margin-top: $space-xs;
  font-size: $font-sm;
  color: $text-tertiary;
}

.card__tags {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin-top: $space-sm;
}

.tag {
  padding: 4rpx $space-sm;
  margin-right: $space-xs;
  margin-bottom: $space-xs;
  font-size: $font-xs;
  color: $color-primary;
  background-color: $color-primary-light;
  border-radius: $radius-sm;
}

.page__footer {
  padding: $space-md;
  text-align: center;
}

.page__footer-text {
  font-size: $font-xs;
  color: $text-tertiary;
}
</style>
