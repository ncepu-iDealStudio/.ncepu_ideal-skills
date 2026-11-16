/// 校验工具（纯函数）
class Validators {
  Validators._();

  /// 是否为空或纯空白
  static bool isBlank(String? value) => value == null || value.trim().isEmpty;

  /// 手机号
  static bool isPhone(String value) =>
      RegExp(r'^1[3-9]\d{9}$').hasMatch(value);

  /// 邮箱
  static bool isEmail(String value) =>
      RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').hasMatch(value);

  /// 返回错误信息，通过返回 null（用于 TextFormField.validator）
  static String? required(String? value, String label) {
    if (isBlank(value)) return '请填写$label';
    return null;
  }

  /// 长度区间校验
  static String? length(String? value, String label, int min, int max) {
    final len = (value ?? '').trim().length;
    if (len < min) return '$label不能少于 $min 个字';
    if (len > max) return '$label不能超过 $max 个字';
    return null;
  }
}
