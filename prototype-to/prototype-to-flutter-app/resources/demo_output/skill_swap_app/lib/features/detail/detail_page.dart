import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';
import '../../core/theme/app_spacing.dart';
import '../../core/utils/formatters.dart';
import '../../data/models/skill.dart';
import '../../data/repositories/skill_repository.dart';

/// 详情页
///
/// 数据来源：SkillRepository
/// 主要交互：滚动查看、底部发起互换
class DetailPage extends StatefulWidget {
  const DetailPage({super.key});

  @override
  State<DetailPage> createState() => _DetailPageState();
}

class _DetailPageState extends State<DetailPage> {
  final SkillRepository _repository = SkillRepositoryImpl();

  Skill? _detail;
  bool _loading = true;
  String? _error;
  int _skillId = 0;

  @override
  void initState() {
    super.initState();
    // 从路由参数取 id
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final args = ModalRoute.of(context)?.settings.arguments;
      _skillId = args is int ? args : 0;
      _load();
    });
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final result = await _repository.fetchSkillDetail(_skillId);
      if (!mounted) return;
      setState(() {
        _detail = result;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  void _onSwap() {
    showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('发起互换'),
        content: const Text('将向对方发送互换请求，确认吗？'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('取消'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('已发送请求')),
              );
            },
            child: const Text('确认'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('详情')),
      body: _buildBody(),
      bottomNavigationBar: _detail == null ? null : _buildBottomBar(),
    );
  }

  Widget _buildBody() {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(_error!, style: const TextStyle(color: AppColors.textSecondary)),
            const SizedBox(height: AppSpacing.lg),
            ElevatedButton(onPressed: _load, child: const Text('重试')),
          ],
        ),
      );
    }

    final detail = _detail;
    if (detail == null) {
      return const Center(
        child: Text('内容不存在或已下架', style: TextStyle(color: AppColors.textTertiary)),
      );
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.pagePadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            detail.title,
            style: const TextStyle(
              fontSize: AppFontSize.xl,
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: AppSpacing.sm),
          Row(
            children: [
              Text(
                detail.userName,
                style: const TextStyle(fontSize: AppFontSize.sm, color: AppColors.textTertiary),
              ),
              const SizedBox(width: AppSpacing.md),
              Text(
                '评分 ${Formatters.rating(detail.rating)}',
                style: const TextStyle(fontSize: AppFontSize.sm, color: AppColors.textTertiary),
              ),
              const SizedBox(width: AppSpacing.md),
              Text(
                '已换 ${Formatters.number(detail.swapCount)} 次',
                style: const TextStyle(fontSize: AppFontSize.sm, color: AppColors.textTertiary),
              ),
            ],
          ),
          if (detail.tags.isNotEmpty) ...[
            const SizedBox(height: AppSpacing.md),
            Wrap(
              spacing: AppSpacing.xs,
              runSpacing: AppSpacing.xs,
              children: detail.tags.map(_buildTag).toList(growable: false),
            ),
          ],
          const SizedBox(height: AppSpacing.xl),
          const Text(
            '详细介绍',
            style: TextStyle(
              fontSize: AppFontSize.md,
              fontWeight: FontWeight.w500,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            detail.description,
            style: const TextStyle(
              fontSize: AppFontSize.base,
              height: 1.8,
              color: AppColors.textSecondary,
            ),
          ),
          if (detail.wantTags.isNotEmpty) ...[
            const SizedBox(height: AppSpacing.xl),
            const Text(
              '我想学',
              style: TextStyle(
                fontSize: AppFontSize.md,
                fontWeight: FontWeight.w500,
                color: AppColors.textPrimary,
              ),
            ),
            const SizedBox(height: AppSpacing.sm),
            Wrap(
              spacing: AppSpacing.xs,
              runSpacing: AppSpacing.xs,
              children: detail.wantTags.map(_buildTagPlain).toList(growable: false),
            ),
          ],
          const SizedBox(height: AppSpacing.xl),
        ],
      ),
    );
  }

  Widget _buildTag(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2),
      decoration: BoxDecoration(
        color: AppColors.primaryLight,
        borderRadius: BorderRadius.circular(AppRadius.sm),
      ),
      child: Text(
        text,
        style: const TextStyle(fontSize: AppFontSize.xs, color: AppColors.primary),
      ),
    );
  }

  Widget _buildTagPlain(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2),
      decoration: BoxDecoration(
        color: AppColors.divider,
        borderRadius: BorderRadius.circular(AppRadius.sm),
      ),
      child: Text(
        text,
        style: const TextStyle(fontSize: AppFontSize.xs, color: AppColors.textSecondary),
      ),
    );
  }

  Widget _buildBottomBar() {
    return SafeArea(
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.md),
        decoration: const BoxDecoration(
          color: AppColors.surface,
          border: Border(top: BorderSide(color: AppColors.border)),
        ),
        child: ElevatedButton(
          onPressed: _onSwap,
          child: const Text('发起互换'),
        ),
      ),
    );
  }
}
