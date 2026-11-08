#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""根据 proto_context.json 预览将要生成的 Flutter 工程文件计划。

用法：
    python preview_plan.py <proto_context.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def build_plan(ctx: dict) -> list[str]:
    files: list[str] = [
        "pubspec.yaml",
        "analysis_options.yaml",
        ".gitignore",
        "README.md",
        "lib/main.dart",
        "lib/app.dart",
        "lib/core/config/app_config.dart",
        "lib/core/network/api_client.dart",
        "lib/core/theme/app_colors.dart",
        "lib/core/theme/app_spacing.dart",
        "lib/core/theme/app_theme.dart",
        "lib/core/router/app_router.dart",
        "lib/core/utils/formatters.dart",
        "lib/core/utils/validators.dart",
        "test/widget_test.dart",
    ]

    # 数据层：按出现过的 data_model 去重
    models: list[str] = []
    for page in ctx.get("pages", []):
        model = page.get("data_model")
        if model and model not in models:
            models.append(model)

    for model in models:
        snake = to_snake(model)
        files.extend([
            f"lib/data/models/{snake}.dart",
            f"lib/data/repositories/{snake}_repository.dart",
            f"lib/data/sources/remote/{snake}_api.dart",
            f"lib/data/sources/local/mock/{snake}_mock.dart",
        ])

    # 功能模块
    for page in ctx.get("pages", []):
        feature_dir = page.get("feature_dir")
        page_name = page.get("page_name")
        if not feature_dir or not page_name:
            continue
        files.extend([
            f"lib/{feature_dir}/{page_name}_page.dart",
            f"lib/{feature_dir}/{page_name}_controller.dart",
        ])
        for comp in page.get("components", []):
            files.append(f"lib/{feature_dir}/widgets/{to_snake(comp)}.dart")

    return files


def to_snake(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python preview_plan.py <proto_context.json>")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"错误：文件不存在 {path}")
        return 2

    ctx = json.loads(path.read_text(encoding="utf-8"))
    pages = ctx.get("pages", [])
    plan = build_plan(ctx)

    project = ctx.get("project", {})
    print(f"工程名（Dart 包名）：{project.get('project_name', '')}")
    print(f"应用标题：{project.get('app_title', '')}")
    print(f"目标平台：{', '.join(project.get('target_platforms', []))}")
    print(f"数据模式：{'mock' if project.get('use_mock') else 'remote'}")
    print(f"页面数：{len(pages)}")
    print(f"计划文件数：{len(plan)}")
    print()

    print("页面清单：")
    for page in pages:
        print(f"  - {page.get('page_name')} → {page.get('widget_class')} ({page.get('layout_type')})")
        print(f"      路由 {page.get('route')}")
        print(f"      目录 lib/{page.get('feature_dir')}/")
        if page.get("components"):
            print(f"      组件 {', '.join(page['components'])}")
    print()

    print("计划生成文件：")
    for f in plan:
        print(f"  - {f}")

    diagnostics = ctx.get("diagnostics", {})
    need_confirm = diagnostics.get("need_confirm", [])
    if need_confirm:
        print()
        print("⚠️  待确认项：")
        for item in need_confirm:
            print(f"  - {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
