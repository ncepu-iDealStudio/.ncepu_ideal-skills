import { PropsWithChildren } from 'react'
import { Provider } from 'react-redux'
import Taro from '@tarojs/taro'
import store from './store'
import './app.scss'

/**
 * 应用入口
 *
 * 参考 elf-taro 的 Provider 包裹思路，适配 Taro4 + React18：
 * - 用 Dva 管理状态（effects 处理副作用）
 * - 全局异常在 onError 中捕获
 */
function App({ children }: PropsWithChildren) {
  return <Provider store={store}>{children}</Provider>
}

App.onError = (error: string) => {
  console.error('[App Error]', error)
}

export default App
