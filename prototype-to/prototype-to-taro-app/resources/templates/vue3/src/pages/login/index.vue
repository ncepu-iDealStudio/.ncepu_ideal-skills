<template>
  <View class="page">
    <View class="brand">
      <Text class="brand__title">{{ appTitle }}</Text>
      <Text class="brand__desc">登录后即可使用全部功能</Text>
    </View>

    <View class="form">
      <View class="form__item">
        <Text class="form__label">账号</Text>
        <Input
          v-model="account"
          class="form__input"
          placeholder="请输入账号"
          :maxlength="50"
        />
      </View>

      <View class="form__item">
        <Text class="form__label">密码</Text>
        <Input
          v-model="password"
          class="form__input"
          password
          placeholder="请输入密码"
          :maxlength="50"
        />
      </View>

      <View
        class="btn"
        :class="{ 'btn--disabled': submitting }"
        hover-class="btn--active"
        @tap="onSubmit"
      >
        <Text class="btn__text">{{ submitting ? '登录中…' : '登录' }}</Text>
      </View>
    </View>
  </View>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Taro from '@tarojs/taro'
import { View, Text, Input } from '@tarojs/components'
import { useUserStore } from '@/store/modules/user'

const appTitle = '{{app_title}}'
const account = ref('')
const password = ref('')
const submitting = ref(false)
const userStore = useUserStore()

async function onSubmit() {
  if (submitting.value) return

  if (!account.value.trim()) {
    Taro.showToast({ title: '请输入账号', icon: 'none' })
    return
  }
  if (!password.value.trim()) {
    Taro.showToast({ title: '请输入密码', icon: 'none' })
    return
  }

  submitting.value = true
  try {
    await userStore.doLogin(account.value.trim(), password.value)
    Taro.showToast({ title: '登录成功', icon: 'success' })
    setTimeout(() => Taro.switchTab({ url: '/pages/home/index' }), 600)
  } catch {
    // 请求层已提示
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss">
.page {
  min-height: 100vh;
  padding: 120rpx $page-padding;
  background-color: $color-surface;
}

.brand__title {
  font-size: 48rpx;
  font-weight: 600;
  color: $text-primary;
}

.brand__desc {
  display: block;
  margin-top: $space-sm;
  font-size: $font-sm;
  color: $text-tertiary;
}

.form {
  margin-top: 80rpx;
}

.form__item {
  margin-bottom: $space-lg;
}

.form__label {
  font-size: $font-sm;
  color: $text-secondary;
}

.form__input {
  margin-top: $space-xs;
  padding: $space-sm $space-md;
  font-size: $font-base;
  background-color: $color-background;
  border-radius: $radius-sm;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  height: $button-height;
  margin-top: $space-xl;
  background-color: $color-primary;
  border-radius: $radius-md;
}

.btn--active {
  opacity: 0.85;
}

.btn--disabled {
  opacity: 0.6;
}

.btn__text {
  font-size: $font-md;
  font-weight: 500;
  color: #FFFFFF;
}
</style>
