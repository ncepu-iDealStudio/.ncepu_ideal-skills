import type { UserConfigExport } from '@tarojs/cli'

export default {
  env: {
    NODE_ENV: '"production"',
  },
  defineConstants: {
    TARO_APP_API: '"https://api.example.com"',
  },
  mini: {},
  h5: {},
} satisfies UserConfigExport
