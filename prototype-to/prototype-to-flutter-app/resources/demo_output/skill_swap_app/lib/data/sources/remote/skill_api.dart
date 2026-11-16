import '../../../core/network/api_client.dart';
import '../../models/skill.dart';

/// 真实 API 数据源
///
/// 对接后端时：确认接口路径与返回结构，必要时调整解析。
class SkillApiSource {
  SkillApiSource(this._client);

  final ApiClient _client;

  Future<List<Skill>> fetchSkills({int page = 1, int pageSize = 10}) async {
    final data = await _client.get(
      '/skills',
      query: {'page': '$page', 'pageSize': '$pageSize'},
    );

    if (data is List) {
      return data
          .whereType<Map<String, dynamic>>()
          .map(Skill.fromJson)
          .toList(growable: false);
    }
    return const [];
  }

  Future<Skill?> fetchSkillDetail(int id) async {
    final data = await _client.get('/skills/$id');
    if (data is Map<String, dynamic>) {
      return Skill.fromJson(data);
    }
    return null;
  }
}
