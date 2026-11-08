import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../data/models/skill.dart';

/// 技能卡片：列表项
///
/// 只接收数据、抛事件，不感知数据来源。
class SkillCard extends StatelessWidget {
  const SkillCard({
    super.key,
    required this.item,
    this.onTap,
  });

  final Skill item;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.md),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.md),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildAvatar(),
              const SizedBox(width: AppSpacing.md),
              Expanded(child: _buildBody()),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAvatar() {
    if (item.avatar.isEmpty) {
      return Container(
        width: AppSizing.avatarMd,
        height: AppSizing.avatarMd,
        decoration: BoxDecoration(
          color: AppColors.divider,
          borderRadius: BorderRadius.circular(AppRadius.md),
        ),
        child: const Icon(Icons.person, color: AppColors.textTertiary),
      );
    }
    return ClipRRect(
      borderRadius: BorderRadius.circular(AppRadius.md),
      child: SizedBox(
        width: AppSizing.avatarMd,
        height: AppSizing.avatarMd,
        child: Image.network(
          item.avatar,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stack) => Container(
            color: AppColors.divider,
            child: const Icon(Icons.person, color: AppColors.textTertiary),
          ),
        ),
      ),
    );
  }

  Widget _buildBody() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          item.title,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(
            fontSize: AppFontSize.md,
            fontWeight: FontWeight.w500,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: AppSpacing.xs),
        Text(
          item.userName,
          style: const TextStyle(fontSize: AppFontSize.sm, color: AppColors.textTertiary),
        ),
        if (item.tags.isNotEmpty) ...[
          const SizedBox(height: AppSpacing.sm),
          Wrap(
            spacing: AppSpacing.xs,
            runSpacing: AppSpacing.xs,
            children: item.tags.map(_buildTag).toList(growable: false),
          ),
        ],
      ],
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
}
