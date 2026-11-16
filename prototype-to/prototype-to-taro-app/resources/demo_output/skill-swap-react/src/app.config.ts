export default {
  pages: [
    'pages/home/index',
    'pages/detail/index',
    'pages/mine/index',
    'pages/login/index',
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#FFFFFF',
    navigationBarTitleText: '技能互换',
    navigationBarTextStyle: 'black',
    backgroundColor: '#F5F6F8',
  },
  tabBar: {
    color: '#9099A3',
    selectedColor: '#2B6DE5',
    backgroundColor: '#FFFFFF',
    borderStyle: 'black',
    list: [
      {
        pagePath: 'pages/home/index',
        text: '首页',
        iconPath: 'assets/tab-home.png',
        selectedIconPath: 'assets/tab-home-active.png',
      },
      {
        pagePath: 'pages/mine/index',
        text: '我的',
        iconPath: 'assets/tab-mine.png',
        selectedIconPath: 'assets/tab-mine-active.png',
      },
    ],
  },
}
