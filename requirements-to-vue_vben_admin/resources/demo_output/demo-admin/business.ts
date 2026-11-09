import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    meta: { icon: 'lucide:briefcase', order: 20, title: '业务管理' },
    name: 'Business',
    path: '/business',
    children: [
      {
        name: 'BusinessOrder',
        path: 'order',
        component: () => import('#/views/business/order/list.vue'),
        meta: { icon: 'lucide:shopping-cart', title: '订单管理' },
      },
      {
        name: 'BusinessProduct',
        path: 'product',
        component: () => import('#/views/business/product/list.vue'),
        meta: { icon: 'lucide:package', title: '商品管理' },
      },
      {
        name: 'BusinessInventory',
        path: 'inventory',
        component: () => import('#/views/business/inventory/list.vue'),
        meta: { icon: 'lucide:warehouse', title: '库存管理' },
      },
    ],
  },
];

export default routes;
