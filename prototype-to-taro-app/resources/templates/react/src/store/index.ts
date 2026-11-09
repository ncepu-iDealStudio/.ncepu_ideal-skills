/**
 * Dva store 装配
 *
 * 参考 elf-taro 的 dva-core + Immer 方案，适配现代版本：
 * - dva-core：轻量 Redux 封装（model / effects / reducers）
 * - dva-immer：reducers 直接修改 draft，无需手写展开
 */
import { create } from 'dva-core'
import createImmerPlugin from 'dva-immer'
import createLoading from 'dva-loading'

import user from '@/models/user'
import skill from '@/models/skill'

const app = create({})
app.use(createImmerPlugin())
app.use(createLoading())
app.model(user)
app.model(skill)
app.start()

export default app._store
