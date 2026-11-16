<template>
  <View class="empty">
    <Text class="empty__text">{{ text }}</Text>
  </View>
</template>

<script setup lang="ts">
/**
 * 空态组件
 * 只接收 props，不感知数据来源。
 */
withDefaults(defineProps<{ text?: string }>(), {
  text: '暂无数据',
})
</script>

<style lang="scss">
.empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120rpx $space-xl;
}

.empty__text {
  font-size: $font-base;
  color: $text-tertiary;
  text-align: center;
}
</style>
