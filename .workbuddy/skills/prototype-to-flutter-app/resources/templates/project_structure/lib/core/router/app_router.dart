/// 路由常量
///
/// 新增页面时必须：
/// 1. 在这里加常量
/// 2. 在 app.dart 的 routes 表中注册
class AppRoutes {
  AppRoutes._();

  /// 首页
  static const String home = '/';

  /// 详情页（通过 arguments 传 id）
  static const String detail = '/detail';
}
