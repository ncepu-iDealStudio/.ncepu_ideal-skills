#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""根据 proto_context.json 预览将要生成的工程文件计划。

用法：
    python preview_plan.py <proto_context.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def build_plan(ctx: dict) -> list[str]:
    files: list[str] = [
        "manifest.json",
        "pages.json",
        "App.uvue",
    ]
    mode = ctx.get("project", {}).get("compile_mode", "vapor")
    files.append("main.ts" if mode == "vapor" else "main.uts")
    files.append("uni.scss")

    pages = ctx.get("pages", [])
    for page in pages:
        path = page.get("page_path", "")
        if path:
            files.append(path)

    # 组件
    components: list[str] = []
    for page in pages:
        for comp in page.get("components", []):
            if comp not in components:
                components.append(comp)
    for comp in components:
        files.append(f"components/{comp}.uvue")

    # 分层
    files.extend([
        "services/api/request.ts",
        "services/api/<domain>.ts",
        "services/mock/<domain>.mock.ts",
        "services/mock/delay.ts",
        "types/<domain>.ts",
        "utils/format.ts",
        "utils/validate.ts",
    ])

    if ctx.get("tab_bar", {}).get("enabled"):
        files.append("static/tab-*.png")

    return files


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

    print(f"工程名：{ctx.get('project', {}).get('project_name', '')}")
    print(f"编译模式：{ctx.get('project', {}).get('compile_mode', '')}")
    print(f"页面数：{len(pages)}")
    print(f"计划文件数：{len(plan)}")
    print()

    print("页面清单：")
    for page in pages:
        flag = " [tab]" if page.get("is_tab") else ""
        home = " [首页]" if page.get("is_home") else ""
        print(f"  - {page.get('page_name')} ({page.get('layout_type')}){home}{flag}")
        print(f"      路由 {page.get('route')}")
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
