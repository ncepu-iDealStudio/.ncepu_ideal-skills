<template>
  <View class="page">
    <View v-if="loading" class="page__loading">
      <Text class="page__loading-text">加载中…</Text>
    </View>

    <Empty v-else-if="!detail" text="内容不存在或已下架" />

    <ScrollView v-else class="page__body" scroll-y>
      <View class="content">
        <Text class="content__title">{{ detail.title }}</Text>
        <View class="content__meta">
          <Text class="content__meta-text">{{ detail.userName }}</Text>
          <Text v-if="detail.rating" class="content__meta-text">评分 {{ detail.rating.toFixed(1) }}</Text>
        </View>

        <View v-if="detail.tags?.length" class="content__tags">
          <Text v-for="tag in detail.tags" :key="tag" class="tag">{{ tag }}</Text>
        </View>

        <View v-if="detail.description" class="content__section">
          <Text class="content__section-title">详细介绍</Text>
          <Text class="content__text">{{ detail.description }}</Text>
        </View>
      </View>
    </ScrollView>

    <View v-if="detail" class="bottom-bar">
      <View class="bottom-bar__btn" hover-class="bottom-bar__btn--active" @tap="onSwap">
        <Text class="bottom-bar__btn-text">发起互换</Text>
      </View>
    </View>
  </View>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Taro, { useLoad } from '@tarojs/taro'
import { View, Text, ScrollView } from '@tarojs/components'
import Empty from '@/components/Empty.vue'
import { getSkillDetail } from '@/services/modules/skill'
import type { SkillItem } from '@/types'

const detail = ref<SkillItem | null>(null)
const loading = ref(true)
let skillId = ''

async function load() {
  try {
    loading.value = true
    detail.value = await getSkillDetail(skillId)
  } catch {
    detail.value = null
  } finally {
    loading.value = false
  }
}

function onSwap() {
  Taro.showModal({
    title: '发起互换',
    content: '将向对方发送互换请求，确认吗？',
    success(res) {
      if (res.confirm) Taro.showToast({ title: '已发送请求', icon: 'none' })
    },
  })
}

useLoad((options) => {
  skillId = options?.id || ''
  load()
})
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

.content {
  padding: $page-padding;
  background-color: $color-surface;
}

.content__title {
  font-size: $font-xl;
  font-weight: 600;
  color: $text-primary;
  line-height: 1.4;
}

.content__meta {
  display: flex;
  flex-direction: row;
  margin-top: $space-sm;
}

.content__meta-text {
  margin-right: $space-md;
  font-size: $font-sm;
  color: $text-tertiary;
}

.content__tags {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin-top: $space-md;
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

.content__section {
  margin-top: $space-lg;
}

.content__section-title {
  font-size: $font-md;
  font-weight: 500;
  color: $text-primary;
}

.content__text {
  display: block;
  margin-top: $space-sm;
  font-size: $font-base;
  color: $text-secondary;
  line-height: 1.8;
}

.bottom-bar {
  padding: $space-sm $page-padding;
  padding-bottom: calc(#{$space-sm} + env(safe-area-inset-bottom));
  background-color: $color-surface;
  border-top: 1rpx solid $color-border;
}

.bottom-bar__btn {
  display: flex;
  align-items: center;
  justify-content: center;
  height: $button-height;
  background-color: $color-primary;
  border-radius: $radius-md;
}

.bottom-bar__btn--active {
  opacity: 0.85;
}

.bottom-bar__btn-text {
  font-size: $font-md;
  font-weight: 500;
  color: #FFFFFF;
}
</style>
