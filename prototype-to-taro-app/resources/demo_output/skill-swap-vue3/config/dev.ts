import type { UserConfigExport } from '@tarojs/cli'

export default {
  env: {
    NODE_ENV: '"development"',
  },
  defineConstants: {
    TARO_APP_API: '"https://dev-api.example.com"',
  },
  mini: {},
  h5: {},
} satisfies UserConfigExport
