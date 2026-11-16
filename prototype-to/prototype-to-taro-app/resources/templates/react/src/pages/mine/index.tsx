import { View, Text } from '@tarojs/components'
import Taro, { useDidShow } from '@tarojs/taro'
import { useDispatch, useSelector } from 'react-redux'
import './index.scss'

export default function Mine() {
  const dispatch = useDispatch()
  const userInfo = useSelector((s: any) => s.user.userInfo)

  const stats = [
    { label: '已互换', value: '6' },
    { label: '收到评价', value: '12' },
    { label: '信用分', value: '98' },
  ]

  const menuItems = [
    { key: 'profile', label: '个人资料' },
    { key: 'my-swap', label: '我的互换' },
    { key: 'review', label: '我的评价' },
    { key: 'setting', label: '设置' },
  ]

  function onTap(item: { label: string }) {
    Taro.showToast({ title: `${item.label}（开发中）`, icon: 'none' })
  }

  function onLogout() {
    Taro.showModal({
      title: '提示',
      content: '确认退出登录？',
      success(res) {
        if (res.confirm) dispatch({ type: 'user/logout' })
      },
    })
  }

  useDidShow(() => {
    dispatch({ type: 'user/fetchUserInfo' })
  })

  return (
    <View className="page">
      <View className="header">
        <View className="header__avatar" />
        <View className="header__info">
          <Text className="header__name">{userInfo?.name || '未登录'}</Text>
          <Text className="header__desc">点击查看个人资料</Text>
        </View>
      </View>

      <View className="stats">
        {stats.map((s) => (
          <View key={s.label} className="stats__item">
            <Text className="stats__value">{s.value}</Text>
            <Text className="stats__label">{s.label}</Text>
          </View>
        ))}
      </View>

      <View className="menu">
        {menuItems.map((item) => (
          <View
            key={item.key}
            className="menu__item"
            hoverClass="menu__item--active"
            onClick={() => onTap(item)}
          >
            <Text className="menu__label">{item.label}</Text>
            <Text className="menu__arrow">›</Text>
          </View>
        ))}
      </View>

      <View className="logout" hoverClass="logout--active" onClick={onLogout}>
        <Text className="logout__text">退出登录</Text>
      </View>
    </View>
  )
}
