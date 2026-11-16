import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './app.scss'

const App = createApp({
  onShow() {
    // 应用显示
  },
  onHide() {
    // 应用隐藏
  },
  onError(msg: string) {
    // 全局异常捕获
    console.error('[App Error]', msg)
  },
})

App.use(createPinia())

export default App
