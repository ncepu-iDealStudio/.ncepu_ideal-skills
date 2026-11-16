<script setup lang="ts">
defineProps<{
  item: Skill
}>()
</script>

<template>
  <UCard class="transition-shadow hover:shadow-lg">
    <div class="flex items-start gap-4">
      <UAvatar
        :src="item.avatar || undefined"
        :alt="item.userName"
        size="md"
        icon="i-lucide-user"
      />
      <div class="flex-1 min-w-0">
        <h3 class="font-semibold truncate">{{ item.title }}</h3>
        <p class="text-sm text-muted mt-1">发布者：{{ item.userName }}</p>
        <div class="flex flex-wrap gap-2 mt-3">
          <UBadge
            v-for="tag in item.tags"
            :key="tag"
            :label="tag"
            color="primary"
            variant="subtle"
          />
        </div>
        <p class="text-xs text-muted mt-3">{{ formatDate(item.createdAt) }}</p>
      </div>
    </div>
  </UCard>
</template>
