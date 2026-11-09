import { View, Text, Input } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { APP_TITLE } from '@/constants'
import './index.scss'

export default function Login() {
  const dispatch = useDispatch()
  const [account, setAccount] = useState('')
  const [password, setPassword] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function onSubmit() {
    if (submitting) return
    if (!account.trim()) {
      Taro.showToast({ title: '请输入账号', icon: 'none' })
      return
    }
    if (!password.trim()) {
      Taro.showToast({ title: '请输入密码', icon: 'none' })
      return
    }

    setSubmitting(true)
    try {
      await dispatch({
        type: 'user/login',
        payload: { account: account.trim(), password },
      })
      Taro.showToast({ title: '登录成功', icon: 'success' })
      setTimeout(() => Taro.switchTab({ url: '/pages/home/index' }), 600)
    } catch {
      // 请求层已提示
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <View className="page">
      <View className="brand">
        <Text className="brand__title">{APP_TITLE}</Text>
        <Text className="brand__desc">登录后即可使用全部功能</Text>
      </View>

      <View className="form">
        <View className="form__item">
          <Text className="form__label">账号</Text>
          <Input
            className="form__input"
            placeholder="请输入账号"
            maxlength={50}
            value={account}
            onInput={(e) => setAccount(e.detail.value)}
          />
        </View>

        <View className="form__item">
          <Text className="form__label">密码</Text>
          <Input
            className="form__input"
            password
            placeholder="请输入密码"
            maxlength={50}
            value={password}
            onInput={(e) => setPassword(e.detail.value)}
          />
        </View>

        <View
          className={`btn ${submitting ? 'btn--disabled' : ''}`}
          hoverClass="btn--active"
          onClick={onSubmit}
        >
          <Text className="btn__text">{submitting ? '登录中…' : '登录'}</Text>
        </View>
      </View>
    </View>
  )
}
