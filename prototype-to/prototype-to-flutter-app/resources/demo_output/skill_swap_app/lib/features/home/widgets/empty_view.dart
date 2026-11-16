import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';

/// 空态组件
///
/// 可被多个 feature 复用，放在 core/widgets 更合适；
/// 当前只有一个 feature 使用，先就近放置。
class EmptyView extends StatelessWidget {
  const EmptyView({
    super.key,
    this.message = '暂无内容',
    this.actionText,
    this.onAction,
    this.icon = Icons.inbox_outlined,
  });

  final String message;
  final String? actionText;
  final VoidCallback? onAction;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 64, color: AppColors.textTertiary),
            const SizedBox(height: AppSpacing.lg),
            Text(
              message,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: AppFontSize.base,
                color: AppColors.textTertiary,
              ),
            ),
            if (actionText != null && onAction != null) ...[
              const SizedBox(height: AppSpacing.xl),
              ElevatedButton(
                onPressed: onAction,
                child: Text(actionText!),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
