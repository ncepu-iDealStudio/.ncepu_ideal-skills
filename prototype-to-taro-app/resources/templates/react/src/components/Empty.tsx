import { View, Text } from '@tarojs/components'
import './Empty.scss'

interface Props {
  text?: string
}

/** 空态组件：只接收 props，不感知数据来源 */
export default function Empty({ text = '暂无数据' }: Props) {
  return (
    <View className="empty">
      <Text className="empty__text">{text}</Text>
    </View>
  )
}
