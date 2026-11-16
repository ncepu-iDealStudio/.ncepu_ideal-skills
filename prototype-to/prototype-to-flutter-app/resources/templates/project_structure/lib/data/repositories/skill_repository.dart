import '../../core/config/app_config.dart';
import '../../core/network/api_client.dart';
import '../models/skill.dart';
import '../sources/local/mock/skill_mock.dart';
import '../sources/remote/skill_api.dart';

/// 技能仓库接口
///
/// UI 与 Controller 只依赖本接口，不关心数据来自 mock 还是真实接口。
abstract class SkillRepository {
  Future<List<Skill>> fetchSkills({int page, int pageSize});
  Future<Skill?> fetchSkillDetail(int id);
}

/// 仓库实现：根据 [AppConfig.useMock] 自动切换数据源
class SkillRepositoryImpl implements SkillRepository {
  SkillRepositoryImpl({SkillApiSource? api, SkillMockSource? mock})
      : _api = api ?? SkillApiSource(ApiClient()),
        _mock = mock ?? const SkillMockSource();

  final SkillApiSource _api;
  final SkillMockSource _mock;

  @override
  Future<List<Skill>> fetchSkills({int page = 1, int pageSize = 10}) {
    return AppConfig.useMock
        ? _mock.fetchSkills(page: page, pageSize: pageSize)
        : _api.fetchSkills(page: page, pageSize: pageSize);
  }

  @override
  Future<Skill?> fetchSkillDetail(int id) {
    return AppConfig.useMock ? _mock.fetchSkillDetail(id) : _api.fetchSkillDetail(id);
  }
}
