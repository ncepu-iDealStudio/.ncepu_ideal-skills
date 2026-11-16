import 'package:flutter/foundation.dart';

import '../../data/models/skill.dart';
import '../../data/repositories/skill_repository.dart';

/// 首页状态
///
/// 约定：
/// - 不持有 BuildContext
/// - 状态变更后必须 notifyListeners()
class HomeController extends ChangeNotifier {
  HomeController(this._repository);

  final SkillRepository _repository;

  /// 当前列表数据
  List<Skill> items = const [];

  /// 首屏加载中
  bool loading = true;

  /// 加载更多中
  bool loadingMore = false;

  /// 是否还有更多
  bool hasMore = true;

  /// 错误信息，null 表示无错误
  String? error;

  int _page = 1;
  static const int _pageSize = 10;

  /// 首次加载 / 重新加载
  Future<void> load() async {
    loading = true;
    error = null;
    notifyListeners();

    try {
      _page = 1;
      final rows = await _repository.fetchSkills(page: _page, pageSize: _pageSize);
      items = rows;
      hasMore = rows.length >= _pageSize;
    } catch (e) {
      error = e.toString();
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  /// 下拉刷新
  Future<void> refresh() => load();

  /// 上拉加载更多
  Future<void> loadMore() async {
    if (loadingMore || !hasMore || loading) return;

    loadingMore = true;
    notifyListeners();

    try {
      final next = _page + 1;
      final rows = await _repository.fetchSkills(page: next, pageSize: _pageSize);
      if (rows.isEmpty) {
        hasMore = false;
      } else {
        items = [...items, ...rows];
        _page = next;
      }
    } catch (e) {
      error = e.toString();
    } finally {
      loadingMore = false;
      notifyListeners();
    }
  }
}
