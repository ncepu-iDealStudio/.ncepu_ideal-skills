#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""根据 req_context.json 预览将要生成的后台管理工程文件计划。

用法：
    python preview_plan.py <req_context.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

APP_SRC = "apps/web-antd/src"


def build_plan(ctx: dict) -> list[str]:
    files: list[str] = []
    modules = ctx.get("modules", [])

    # 1) 路由模块
    seen_route_files: list[str] = []
    for m in modules:
        for c in m.get("children", []):
            rf = c.get("route_file")
            if rf and rf not in seen_route_files:
                seen_route_files.append(rf)
    for rf in seen_route_files:
        files.append(f"{APP_SRC}/router/routes/modules/{rf}")

    # 2) 页面
    for m in modules:
        for c in m.get("children", []):
            view_dir = c.get("view_dir", "")
            ptype = c.get("type", "crud")
            files.append(f"{APP_SRC}/{view_dir}/list.vue")
            if ptype == "crud":
                files.append(f"{APP_SRC}/{view_dir}/data.ts")
                files.append(f"{APP_SRC}/{view_dir}/modules/form.vue")
            elif ptype == "tree":
                files.append(f"{APP_SRC}/{view_dir}/data.ts")
                files.append(f"{APP_SRC}/{view_dir}/modules/form.vue")

    # 3) API
    for m in modules:
        for c in m.get("children", []):
            api_file = c.get("api_file")
            if api_file:
                files.append(f"{APP_SRC}/{api_file}")

    return files


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python preview_plan.py <req_context.json>")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"错误：文件不存在 {path}")
        return 2

    ctx = json.loads(path.read_text(encoding="utf-8"))
    app = ctx.get("app", {})
    modules = ctx.get("modules", [])
    plan = build_plan(ctx)

    total_pages = sum(len(m.get("children", [])) for m in modules)

    print(f"系统标题：{app.get('title', '')}")
    print(f"UI 框架：{app.get('ui', 'antd')}")
    print(f"Vben 版本：{app.get('vben_version', '5.x')}")
    print(f"模块数：{len(modules)}")
    print(f"页面数：{total_pages}")
    print(f"计划文件数：{len(plan)}")
    print()

    print("模块与页面：")
    for m in modules:
        print(f"  [{m['name']}] {m['path']}  (order={m.get('order', 0)})")
        for c in m.get("children", []):
            print(f"    - {c['name']:12s} {c['type']:10s} {c['full_path']}")
            print(f"        model={c['model']}  view={c['view_dir']}")
    print()

    print("计划生成文件：")
    for f in plan:
        print(f"  - {f}")

    diag = ctx.get("diagnostics", {})
    if diag.get("assumptions"):
        print()
        print("ℹ️  解析假设：")
        for a in diag["assumptions"]:
            print(f"  - {a}")
    if diag.get("need_confirm"):
        print()
        print("⚠️  待确认项：")
        for n in diag["need_confirm"]:
            print(f"  - {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
