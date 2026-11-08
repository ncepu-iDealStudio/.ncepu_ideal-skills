/// 应用级配置
///
/// 对接后端时**只需改这里的两个值**：
/// - [useMock] 改为 false
/// - [apiBaseUrl] 改为你的域名
class AppConfig {
  AppConfig._();

  /// 是否使用 mock 数据。
  ///
  /// true  → 数据来自 data/sources/local/mock
  /// false → 数据来自 data/sources/remote
  static const bool useMock = true;

  /// 后端接口基地址（对接时修改）
  static const String apiBaseUrl = 'https://api.example.com';

  /// 网络超时（秒）
  static const int timeoutSeconds = 15;
}
