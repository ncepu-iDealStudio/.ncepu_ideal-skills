import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    meta: { icon: 'lucide:chart-column', order: 30, title: '数据统计' },
    name: 'Statistics',
    path: '/statistics',
    children: [
      {
        name: 'StatisticsSalesAnalysis',
        path: 'sales-analysis',
        component: () => import('#/views/statistics/sales-analysis/list.vue'),
        meta: { icon: 'lucide:trending-up', title: '销售数据分析' },
      },
      {
        name: 'StatisticsUserBehaviorAnalysis',
        path: 'user-behavior-analysis',
        component: () => import('#/views/statistics/user-behavior-analysis/list.vue'),
        meta: { icon: 'lucide:activity', title: '用户行为分析' },
      },
    ],
  },
];

export default routes;
