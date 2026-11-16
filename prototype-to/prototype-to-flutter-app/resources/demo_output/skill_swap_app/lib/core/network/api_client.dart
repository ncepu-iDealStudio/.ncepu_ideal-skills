import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/app_config.dart';

/// 接口异常，统一在数据层抛出、在 Controller 层转为用户可读文案
class ApiException implements Exception {
  ApiException(this.message, {this.statusCode});

  final String message;
  final int? statusCode;

  @override
  String toString() => message;
}

/// HTTP 客户端封装
///
/// - 统一拼 baseUrl
/// - 统一解析 JSON
/// - 统一抛 ApiException
class ApiClient {
  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  Future<dynamic> get(String path, {Map<String, String>? query}) async {
    final uri = Uri.parse('${AppConfig.apiBaseUrl}$path').replace(queryParameters: query);
    try {
      final response = await _client
          .get(uri, headers: {'Content-Type': 'application/json'})
          .timeout(const Duration(seconds: AppConfig.timeoutSeconds));

      return _handle(response);
    } on Exception catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('网络异常，请检查网络连接');
    }
  }

  Future<dynamic> post(String path, {Map<String, dynamic>? body}) async {
    final uri = Uri.parse('${AppConfig.apiBaseUrl}$path');
    try {
      final response = await _client
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(body ?? {}),
          )
          .timeout(const Duration(seconds: AppConfig.timeoutSeconds));

      return _handle(response);
    } on Exception catch (e) {
      if (e is ApiException) rethrow;
      throw ApiException('网络异常，请检查网络连接');
    }
  }

  /// 解析响应。约定后端返回 { "code": 0, "message": "", "data": ... }
  dynamic _handle(http.Response response) {
    final body = response.body;
    if (body.isEmpty) {
      if (response.statusCode >= 200 && response.statusCode < 300) return null;
      throw ApiException('请求失败（${response.statusCode}）', statusCode: response.statusCode);
    }

    dynamic decoded;
    try {
      decoded = jsonDecode(body);
    } catch (_) {
      throw ApiException('响应格式错误', statusCode: response.statusCode);
    }

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw ApiException('请求失败（${response.statusCode}）', statusCode: response.statusCode);
    }

    if (decoded is Map<String, dynamic>) {
      final code = decoded['code'];
      if (code is int && code != 0) {
        throw ApiException(
          (decoded['message'] as String?) ?? '请求失败',
          statusCode: response.statusCode,
        );
      }
      if (decoded.containsKey('data')) return decoded['data'];
    }

    return decoded;
  }
}
