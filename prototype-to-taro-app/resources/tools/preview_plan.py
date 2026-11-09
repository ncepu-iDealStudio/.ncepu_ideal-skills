#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""根据 proto_context.json 预览将要生成的 Taro 工程文件计划。

用法：
    python preview_plan.py <proto_context.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def build_plan(ctx: dict) -> list[str]:
    project = ctx.get("project", {})
    fw = project.get("framework", "vue3")
    page_ext = ".vue" if fw == "vue3" else ".tsx"

    files: list[str] = [
        "package.json",
        "project.config.json",
        "tsconfig.json",
        "babel.config.js",
        "config/index.ts",
        "config/dev.ts",
        "config/prod.ts",
        "src/app.config.ts",
        "src/app.scss",
        "src/app.ts" if fw == "vue3" else "src/app.tsx",
        "src/services/request.ts",
        "src/types/index.ts",
        "src/styles/variables.scss",
        "src/mock/skill.mock.ts",
    ]

    # 页面
    for page in ctx.get("pages", []):
        path = page.get("path", "")
        if not path:
            continue
        files.append(f"src/{path}{page_ext}")
        files.append(f"src/{Path(path).parent}/index.config.ts")

    # 状态管理
    if fw == "vue3":
        files.append("src/store/index.ts")
        files.append("src/store/modules/user.ts")
        files.append("src/store/modules/skill.ts")
    else:
        files.append("src/store/index.ts")
        files.append("src/models/user.ts")
        files.append("src/models/skill.ts")

    # 公共组件
    files.append(f"src/components/Empty{page_ext}")

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
    project = ctx.get("project", {})
    pages = ctx.get("pages", [])
    plan = build_plan(ctx)
    fw = project.get("framework", "")

    fw_label = {"vue3": "Vue3 + TS + Vant + Pinia", "react": "React + TS + Dva + Immer"}.get(fw, fw)

    print(f"工程名：{project.get('project_name', '')}")
    print(f"应用标题：{project.get('app_title', '')}")
    print(f"框架：{fw_label}")
    print(f"目标平台：{', '.join(project.get('targets', []))}")
    print(f"页面数：{len(pages)}")
    print(f"计划文件数：{len(plan)}")
    print()

    print("页面清单：")
    for p in pages:
        tab = " [tab]" if p.get("is_tab") else ""
        print(f"  - {p.get('page_name'):14s} {p.get('layout', ''):10s} {p.get('path')}{tab}")
        if p.get("components"):
            print(f"      组件 {', '.join(p['components'])}")
    print()

    print("计划生成文件：")
    for f in plan:
        print(f"  - {f}")

    diag = ctx.get("diagnostics", {})
    if diag.get("need_confirm"):
        print()
        print("⚠️  待确认项：")
        for n in diag["need_confirm"]:
            print(f"  - {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
