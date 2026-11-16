<script setup lang="ts">
const { items, loading, error, load } = useSkills()
</script>

<template>
  <div class="mx-auto max-w-5xl px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold">技能互换</h1>
      <p class="mt-2 text-muted">发现并交换你感兴趣的技能</p>
    </div>

    <!-- 加载态 -->
    <div v-if="loading" class="space-y-4">
      <UCard v-for="i in 3" :key="i" class="animate-pulse">
        <div class="h-4 bg-muted rounded w-3/4 mb-2" />
        <div class="h-3 bg-muted rounded w-1/2" />
      </UCard>
    </div>

    <!-- 错误态 -->
    <UAlert
      v-else-if="error"
      color="red"
      :title="error"
      icon="i-lucide-alert-circle"
    >
      <template #actions>
        <UButton color="red" variant="subtle" size="xs" @click="load">重试</UButton>
      </template>
    </UAlert>

    <!-- 空态 -->
    <EmptyState v-else-if="!items.length" />

    <!-- 列表 -->
    <div v-else class="grid gap-4 md:grid-cols-2">
      <SkillCard
        v-for="item in items"
        :key="item.id"
        :item="item"
      />
    </div>
  </div>
</template>
