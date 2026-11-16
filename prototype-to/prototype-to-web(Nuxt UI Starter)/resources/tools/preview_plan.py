#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""根据 proto_context.json 预览将要生成的 Nuxt UI Starter 工程文件计划。

用法：
    python preview_plan.py <proto_context.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def to_kebab(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            out.append("-")
        out.append(ch.lower())
    return "".join(out)


def build_plan(ctx: dict) -> list[str]:
    files: list[str] = [
        "package.json",
        "nuxt.config.ts",
        "tsconfig.json",
        "eslint.config.mjs",
        ".gitignore",
        ".editorconfig",
        "README.md",
        "app/app.vue",
        "app/app.config.ts",
        "app/assets/css/main.css",
        "app/components/AppLogo.vue",
    ]

    # 数据层：按出现过的 data_model 去重
    models: list[str] = []
    for page in ctx.get("pages", []):
        model = page.get("data_model")
        if model and model not in models:
            models.append(model)

    for model in models:
        kebab = to_kebab(model)
        files.append(f"app/types/{kebab}.ts")
        files.append(f"app/services/{kebab}Service.ts")
        files.append(f"app/composables/use{pascal(model)}.ts")

    # 页面与组件
    for page in ctx.get("pages", []):
        file_path = page.get("file_path")
        if file_path:
            files.append(file_path)
        for comp in page.get("components", []):
            files.append(f"app/components/{comp}.vue")

    return files


def pascal(name: str) -> str:
    return name[:1].upper() + name[1:]


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
    design = ctx.get("design", {})
    print(f"工程名：{project.get('project_name', '')}")
    print(f"应用标题：{project.get('app_title', '')}")
    print(f"目标平台：{', '.join(project.get('target_platforms', []))}")
    print(f"UI 库：{project.get('ui_library', '@nuxt/ui')}")
    print(f"主色：{design.get('primary_color', 'green')} ({design.get('primary_hex', '')})")
    print(f"数据模式：{'mock' if project.get('use_mock') else 'remote'}")
    print(f"页面数：{len(pages)}")
    print(f"计划文件数：{len(plan)}")
    print()

    print("页面清单：")
    for page in pages:
        print(f"  - {page.get('page_name')} → {page.get('route')} ({page.get('layout_type')})")
        print(f"      文件 {page.get('file_path')}")
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
