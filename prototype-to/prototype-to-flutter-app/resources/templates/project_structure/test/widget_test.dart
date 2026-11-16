import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:{{project_name}}/app.dart';

void main() {
  testWidgets('应用能正常启动并渲染首页标题', (WidgetTester tester) async {
    await tester.pumpWidget(const SkillSwapApp());

    // 首帧：应进入 loading 态
    expect(find.byType(CircularProgressIndicator), findsWidgets);

    // 等待 mock 数据返回（mock 延迟 400ms）
    await tester.pump(const Duration(milliseconds: 600));
    await tester.pumpAndSettle();

    // 应渲染出首页标题
    expect(find.text('技能互换'), findsWidgets);
  });

  testWidgets('首页列表渲染出 mock 数据', (WidgetTester tester) async {
    await tester.pumpWidget(const SkillSwapApp());
    await tester.pump(const Duration(milliseconds: 600));
    await tester.pumpAndSettle();

    // mock 的第一条数据
    expect(find.text('摄影入门：从构图到后期'), findsWidgets);
  });
}
