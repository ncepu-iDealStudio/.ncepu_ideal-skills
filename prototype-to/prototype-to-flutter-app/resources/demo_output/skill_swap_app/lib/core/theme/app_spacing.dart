/// 间距、圆角、尺寸、字号 token
///
/// 页面中**不要**写魔法数字，统一引用这里。
class AppSpacing {
  AppSpacing._();

  static const double xs = 4;
  static const double sm = 8;
  static const double md = 12;
  static const double lg = 16;
  static const double xl = 24;

  /// 页面左右内边距
  static const double pagePadding = 16;

  /// 区块间距
  static const double sectionGap = 12;
}

class AppRadius {
  AppRadius._();

  static const double sm = 6;
  static const double md = 10;
  static const double lg = 16;
  static const double pill = 999;
}

class AppSizing {
  AppSizing._();

  static const double appBarHeight = 56;
  static const double avatarSm = 32;
  static const double avatarMd = 44;
  static const double avatarLg = 64;
  static const double iconSm = 16;
  static const double iconMd = 24;
  static const double buttonHeight = 44;
}

class AppFontSize {
  AppFontSize._();

  static const double xs = 11;
  static const double sm = 12;
  static const double base = 14;
  static const double md = 15;
  static const double lg = 17;
  static const double xl = 20;
  static const double xxl = 24;
}

class AppDuration {
  AppDuration._();

  static const Duration fast = Duration(milliseconds: 150);
  static const Duration base = Duration(milliseconds: 250);
}
