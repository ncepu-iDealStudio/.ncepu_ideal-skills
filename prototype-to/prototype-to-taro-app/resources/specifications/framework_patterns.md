# 双框架生成范式

同一份原型，Vue3 与 React 两套写法对照。生成时**必须整套选用一种**，禁止混用。

---

## 0. 工程配置差异

### `config/index.ts`

```ts
// Vue3
const config = {
  projectName: '{{project_name}}',
  framework: 'vue3',
  compiler: { type: 'webpack5', prebundle: { enable: false } },
  // ...
}
```

```ts
// React
const config = {
  projectName: '{{project_name}}',
  framework: 'react',
  compiler: { type: 'webpack5', prebundle: { enable: false } },
  // ...
}
```

### 入口文件

**Vue3 `src/app.ts`**

```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './app.scss'

const App = createApp({
  onShow() {},
  onHide() {},
})
App.use(createPinia())
export default App
```

**React `src/app.tsx`**

```tsx
import { PropsWithChildren } from 'react'
import { Provider } from 'react-redux'
import store from './store'
import './app.scss'

function App({ children }: PropsWithChildren<any>) {
  return <Provider store={store}>{children}</Provider>
}

export default App
```

---

## 1. 页面文件

### Vue3 `pages/home/index.vue`

```vue
<template>
  <View class="page">
    <View v-if="loading" class="page__loading">
      <Text>加载中…</Text>
    </View>

    <Empty v-else-if="list.length === 0" text="暂无数据" />

    <ScrollView v-else class="page__body" scroll-y @scrolltolower="onLoadMore">
      <View
        v-for="item in list"
        :key="item.id"
        class="card"
        hover-class="card--active"
        @tap="goDetail(item.id)"
      >
        <Text class="card__title">{{ item.title }}</Text>
      </View>
    </ScrollView>
  </View>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Taro, { useDidShow, usePullDownRefresh, useReachBottom } from '@tarojs/taro'
import { ScrollView, View, Text } from '@tarojs/components'
import Empty from '@/components/Empty.vue'
import { useSkillStore } from '@/store/modules/skill'

const list = ref<any[]>([])
const loading = ref(true)
const store = useSkillStore()

async function load(reset = false) {
  loading.value = true
  try {
    list.value = await store.fetchList()
  } finally {
    loading.value = false
  }
}

function goDetail(id: number) {
  Taro.navigateTo({ url: `/pages/detail/index?id=${id}` })
}

function onLoadMore() {
  store.loadMore()
}

useDidShow(() => { load(true) })
usePullDownRefresh(async () => {
  await load(true)
  Taro.stopPullDownRefresh()
})
useReachBottom(() => onLoadMore())
</script>

<style lang="scss">
.page { display: flex; flex-direction: column; min-height: 100vh; }
</style>
```

### React `pages/home/index.tsx`

```tsx
import { View, Text, ScrollView } from '@tarojs/components'
import Taro, { useDidShow, usePullDownRefresh, useReachBottom } from '@tarojs/taro'
import { useEffect, useState } from 'react'
import Empty from '@/components/Empty'
import { getSkillList } from '@/services/modules/skill'

export default function Home() {
  const [list, setList] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  async function load() {
    setLoading(true)
    try {
      setList(await getSkillList())
    } finally {
      setLoading(false)
    }
  }

  function goDetail(id: number) {
    Taro.navigateTo({ url: `/pages/detail/index?id=${id}` })
  }

  useDidShow(() => { load() })
  usePullDownRefresh(async () => {
    await load()
    Taro.stopPullDownRefresh()
  })
  useReachBottom(() => { /* 加载更多 */ })

  if (loading) {
    return <View className="page__loading"><Text>加载中…</Text></View>
  }
  if (list.length === 0) {
    return <Empty text="暂无数据" />
  }

  return (
    <ScrollView className="page__body" scrollY>
      {list.map((item) => (
        <View
          key={item.id}
          className="card"
          hoverClass="card--active"
          onClick={() => goDetail(item.id)}
        >
          <Text className="card__title">{item.title}</Text>
        </View>
      ))}
    </ScrollView>
  )
}
```

### 页面配置文件（两者相同）

```ts
// pages/home/index.config.ts
export default {
  navigationBarTitleText: '首页',
  enablePullDownRefresh: true,
  backgroundTextStyle: 'dark',
}
```

---

## 2. 状态管理

### Vue3：Pinia `store/modules/skill.ts`

```ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSkillList } from '@/services/modules/skill'

export const useSkillStore = defineStore('skill', () => {
  const list = ref<any[]>([])
  const page = ref(1)
  const hasMore = ref(true)

  async function fetchList() {
    const rows = await getSkillList({ page: page.value })
    list.value = rows
    return rows
  }

  async function loadMore() {
    if (!hasMore.value) return
    page.value += 1
    const rows = await getSkillList({ page: page.value })
    if (rows.length === 0) hasMore.value = false
    else list.value = [...list.value, ...rows]
  }

  return { list, page, hasMore, fetchList, loadMore }
})
```

### React：Dva `models/skill.ts`

```ts
import { getSkillList } from '@/services/modules/skill'

export default {
  namespace: 'skill',

  state: {
    list: [] as any[],
    page: 1,
    hasMore: true,
  },

  effects: {
    *fetchList(_: any, { call, put }: any) {
      const rows = yield call(getSkillList, { page: 1 })
      yield put({ type: 'setList', payload: rows })
    },
    *loadMore(_: any, { call, put, select }: any) {
      const { page, hasMore, list } = yield select((s: any) => s.skill)
      if (!hasMore) return
      const rows = yield call(getSkillList, { page: page + 1 })
      yield put({ type: 'appendList', payload: { rows, page: page + 1 } })
    },
  },

  reducers: {
    setList(state: any, { payload }: any) {
      return { ...state, list: payload }
    },
    appendList(state: any, { payload }: any) {
      const { rows, page } = payload
      return {
        ...state,
        list: [...state.list, ...rows],
        page,
        hasMore: rows.length > 0,
      }
    },
  },
}
```

React 侧读取：

```tsx
import { useSelector, useDispatch } from 'react-redux'

const list = useSelector((s: any) => s.skill.list)
const dispatch = useDispatch()
dispatch({ type: 'skill/fetchList' })
```

---

## 3. 请求封装（两框架共用同一份 TS）

`src/services/request.ts`

```ts
import Taro from '@tarojs/taro'

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

const BASE_URL = process.env.TARO_APP_API || 'https://api.example.com'

export function request<T>(options: {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, any>
}): Promise<T> {
  return new Promise((resolve, reject) => {
    Taro.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        Authorization: Taro.getStorageSync('token') || '',
      },
      success(res) {
        const body = res.data as ApiResponse<T>
        if (res.statusCode === 401) {
          Taro.removeStorageSync('token')
          Taro.reLaunch({ url: '/pages/login/index' })
          reject(new Error('登录已过期'))
          return
        }
        if (res.statusCode >= 200 && res.statusCode < 300 && body.code === 0) {
          resolve(body.data)
        } else {
          Taro.showToast({ title: body?.message || '请求失败', icon: 'none' })
          reject(new Error(body?.message || '请求失败'))
        }
      },
      fail(err) {
        Taro.showToast({ title: '网络异常', icon: 'none' })
        reject(new Error(err.errMsg))
      },
    })
  })
}
```

业务模块 `src/services/modules/skill.ts`：

```ts
import { request } from '../request'

export function getSkillList(params: { page?: number }) {
  return request<any[]>({ url: '/skills', data: params })
}

export function getSkillDetail(id: number) {
  return request<any>({ url: `/skills/${id}` })
}
```

**两个框架完全共用**，不需要分别生成。

---

## 4. tabBar 配置

`src/app.config.ts`（两者相同）

```ts
export default {
  pages: [
    'pages/home/index',
    'pages/detail/index',
    'pages/mine/index',
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#fff',
    navigationBarTitleText: '{{app_title}}',
    navigationBarTextStyle: 'black',
  },
  tabBar: {
    color: '#9099A3',
    selectedColor: '#2B6DE5',
    backgroundColor: '#FFFFFF',
    borderStyle: 'black',
    list: [
      { pagePath: 'pages/home/index', text: '首页', iconPath: 'assets/tab-home.png', selectedIconPath: 'assets/tab-home-active.png' },
      { pagePath: 'pages/mine/index', text: '我的', iconPath: 'assets/tab-mine.png', selectedIconPath: 'assets/tab-mine-active.png' },
    ],
  },
}
```

> 注意：`pages` 数组里写**不带扩展名**的路径；tabBar 页面必须在 `pages` 里。

---

## 5. 差异速查表

| 项 | Vue3 | React |
| --- | --- | --- |
| 页面文件 | `index.vue` | `index.tsx` |
| 组件标签 | `<View>`（PascalCase） | `<View>`（PascalCase） |
| 事件 | `@tap` / `@click` | `onClick` |
| 样式类 | `class` | `className` |
| 条件渲染 | `v-if` / `v-else` | 三元 / `&&` |
| 列表 | `v-for` | `map()` |
| 状态声明 | `ref` / `reactive` | `useState` |
| 副作用 | `watch` / `onMounted` | `useEffect` |
| 页面生命周期 | `useDidShow` 等（直接调用） | 同左（Hooks） |
| 状态读取 | `storeToRefs(useStore())` | `useSelector` |
| 状态更新 | 直接赋值 | `dispatch` |

---

## 6. 生成检查清单

| # | 检查项 |
| --- | --- |
| 1 | 所有页面文件后缀与 `framework` 一致 |
| 2 | 每页都有 `index.config.ts` |
| 3 | 全部页面在 `app.config.ts` 的 `pages` 中注册 |
| 4 | tabBar 页面在 `pages` 中 |
| 5 | 请求统一走 `services/request.ts` |
| 6 | 三态渲染（loading/empty/loaded）齐全 |
| 7 | 列表 `key` 唯一 |
| 8 | 图片有固定宽高 |
| 9 | 底部元素避开安全区 |
| 10 | 未混用两套框架写法 |
