<template>
  <View class="page">
    <View class="header">
      <View class="header__avatar" />
      <View class="header__info">
        <Text class="header__name">{{ userInfo?.name || '未登录' }}</Text>
        <Text class="header__desc">点击查看个人资料</Text>
      </View>
    </View>

    <View class="stats">
      <View v-for="s in stats" :key="s.label" class="stats__item">
        <Text class="stats__value">{{ s.value }}</Text>
        <Text class="stats__label">{{ s.label }}</Text>
      </View>
    </View>

    <View class="menu">
      <View
        v-for="item in menuItems"
        :key="item.key"
        class="menu__item"
        hover-class="menu__item--active"
        @tap="onTap(item)"
      >
        <Text class="menu__label">{{ item.label }}</Text>
        <Text class="menu__arrow">›</Text>
      </View>
    </View>

    <View class="logout" hover-class="logout--active" @tap="onLogout">
      <Text class="logout__text">退出登录</Text>
    </View>
  </View>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Taro, { useDidShow } from '@tarojs/taro'
import { View, Text } from '@tarojs/components'
import { useUserStore } from '@/store/modules/user'

const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)

const stats = [
  { label: '已互换', value: '6' },
  { label: '收到评价', value: '12' },
  { label: '信用分', value: '98' },
]

const menuItems = [
  { key: 'profile', label: '个人资料' },
  { key: 'my-swap', label: '我的互换' },
  { key: 'review', label: '我的评价' },
  { key: 'setting', label: '设置' },
]

function onTap(item: { key: string; label: string }) {
  Taro.showToast({ title: `${item.label}（开发中）`, icon: 'none' })
}

function onLogout() {
  Taro.showModal({
    title: '提示',
    content: '确认退出登录？',
    success(res) {
      if (res.confirm) userStore.logout()
    },
  })
}

useDidShow(() => {
  userStore.fetchUserInfo()
})
</script>

<style lang="scss">
.page {
  min-height: 100vh;
  background-color: $color-background;
}

.header {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: $page-padding;
  background-color: $color-surface;
}

.header__avatar {
  width: 128rpx;
  height: 128rpx;
  border-radius: 50%;
  background-color: $color-divider;
}

.header__info {
  flex: 1;
  margin-left: $space-md;
}

.header__name {
  font-size: $font-xl;
  font-weight: 600;
  color: $text-primary;
}

.header__desc {
  display: block;
  margin-top: $space-xs;
  font-size: $font-sm;
  color: $text-tertiary;
}

.stats {
  display: flex;
  flex-direction: row;
  margin-top: $space-md;
  padding: $space-md 0;
  background-color: $color-surface;
}

.stats__item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stats__value {
  font-size: $font-lg;
  font-weight: 600;
  color: $text-primary;
}

.stats__label {
  margin-top: $space-xs;
  font-size: $font-xs;
  color: $text-tertiary;
}

.menu {
  margin-top: $space-md;
  background-color: $color-surface;
}

.menu__item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: $space-md $page-padding;
  border-bottom: 1rpx solid $color-divider;
}

.menu__item--active {
  background-color: #F7F8FA;
}

.menu__label {
  font-size: $font-base;
  color: $text-primary;
}

.menu__arrow {
  font-size: $font-lg;
  color: $text-tertiary;
}

.logout {
  margin: $space-xl $page-padding;
  padding: $space-md 0;
  background-color: $color-surface;
  border-radius: $radius-md;
  text-align: center;
}

.logout--active {
  background-color: #F7F8FA;
}

.logout__text {
  font-size: $font-base;
  color: $color-error;
}
</style>
