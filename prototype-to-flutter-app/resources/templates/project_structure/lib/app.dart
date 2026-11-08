import 'package:flutter/material.dart';

import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';
import 'features/detail/detail_page.dart';
import 'features/home/home_page.dart';

/// 应用根 Widget
///
/// 职责：
/// - 装配主题（AppTheme）
/// - 注册路由表（AppRoutes）
/// - 指定首页
class SkillSwapApp extends StatelessWidget {
  const SkillSwapApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '{{app_title}}',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      initialRoute: AppRoutes.home,
      routes: {
        AppRoutes.home: (context) => const HomePage(),
        AppRoutes.detail: (context) => const DetailPage(),
      },
    );
  }
}
