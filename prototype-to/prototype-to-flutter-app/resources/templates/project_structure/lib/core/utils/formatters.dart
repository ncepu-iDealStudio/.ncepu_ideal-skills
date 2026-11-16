/// 格式化工具（纯函数，无副作用）
class Formatters {
  Formatters._();

  /// 数字千分位：12345 -> "12,345"
  static String number(num value) {
    final text = value.toString();
    final reg = RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))');
    return text.replaceAllMapped(reg, (m) => '${m[1]},');
  }

  /// 评分保留一位小数：4.85 -> "4.9"
  static String rating(double value) => value.toStringAsFixed(1);

  /// 文本截断
  static String truncate(String text, int maxLength) {
    if (text.length <= maxLength) return text;
    return '${text.substring(0, maxLength)}…';
  }

  /// 时间戳格式化：2026-11-08
  static String date(DateTime time) {
    final y = time.year.toString().padLeft(4, '0');
    final m = time.month.toString().padLeft(2, '0');
    final d = time.day.toString().padLeft(2, '0');
    return '$y-$m-$d';
  }
}
