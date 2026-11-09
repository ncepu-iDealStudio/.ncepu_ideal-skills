<script lang="ts" setup>
import type { EchartsUIType } from '@vben/plugins/echarts';

import { onMounted, ref } from 'vue';

import { Page } from '@vben/common-ui';
import { EchartsUI, useEcharts } from '@vben/plugins/echarts';
import { Card } from 'ant-design-vue';

const chartRef = ref<EchartsUIType>();
const { renderEcharts } = useEcharts(chartRef);

const stats = [
  { label: '总量', value: '1,280' },
  { label: '今日', value: '342' },
  { label: '环比', value: '+12.5%' },
  { label: '同比', value: '+8.2%' },
];

onMounted(() => {
  renderEcharts({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [{ name: '趋势', type: 'line', smooth: true, data: [820, 932, 1010, 1180, 1290, 1410] }],
  });
});
</script>

<template>
  <Page auto-content-height>
    <div class="flex flex-col gap-4 p-4">
      <div class="grid grid-cols-4 gap-4">
        <Card v-for="item in stats" :key="item.label">
          <div class="text-sm text-gray-500">{{ item.label }}</div>
          <div class="mt-2 text-2xl font-semibold">{{ item.value }}</div>
        </Card>
      </div>
      <Card title="用户行为分析">
        <EchartsUI ref="chartRef" height="360px" />
      </Card>
    </div>
  </Page>
</template>
