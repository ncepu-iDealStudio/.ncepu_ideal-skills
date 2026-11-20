#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""校验基于 vue-vben-admin 生成的后台管理工程是否符合本技能约定。

用法：
    python validate_project.py <vben工程根目录>          # 校验 apps/web-antd
    python validate_project.py <工程根> --app web-antd
    python validate_project.py <工程根> --json

只做静态检查，不依赖 Node/pnpm。退出码 0 表示无阻断性错误。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---- 检查项 ----------------------------------------------------------------

CHECK_STRUCTURE = "vben5 monorepo 结构（apps/ + packages/）"
CHECK_ROUTE_MODULES = "路由模块位于 src/router/routes/modules/"
CHECK_ROUTE_COMPONENT = "路由 component 指向的文件存在"
CHECK_ROUTER_INDEX_UNTOUCHED = "未篡改 routes/index.ts 的 glob 机制"
CHECK_USE_VBEN_GRID = "列表页使用 useVbenVxeGrid"
CHECK_NO_RAW_TABLE = "未手写 <table> 或 el-table"
CHECK_USE_REQUEST_CLIENT = "使用 requestClient 而非 axios"
CHECK_UI_IMPORT_CORRECT = "UI 组件导入来源正确"
CHECK_TABLE_ACTION_SOURCE = "VbenTableAction 从 @vben/common-ui 导入"
CHECK_SCRIPT_SETUP = "SFC 使用 <script lang=\"ts\" setup>"
CHECK_ALIAS_USED = "使用 #/ 别名而非深层相对路径"
CHECK_API_TYPED = "API 层有 namespace 类型定义"
CHECK_FIELDS_CONSISTENT = "表单字段与 API 类型字段一致"
CHECK_MOCK_PRESENT = "存在 mock 数据或 backend-mock 支持"


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return ""


def find_app_root(root: Path, app: str) -> Path | None:
    """定位 app 目录。支持传入仓库根或 app 目录本身。"""
    direct = root / app
    if direct.is_dir():
        return direct
    if (root / "src").is_dir() and (root / "package.json").exists():
        return root
    for candidate in root.glob("apps/*"):
        if candidate.is_dir() and candidate.name == app:
            return candidate
    return None


def check_structure(root: Path, results: list) -> None:
    has_apps = (root / "apps").is_dir()
    has_packages = (root / "packages").is_dir()
    has_web = (root / "apps" / "web-antd").is_dir()
    if has_apps and has_packages and has_web:
        results.append((CHECK_STRUCTURE, "ok", ""))
    elif has_apps and has_packages:
        results.append((CHECK_STRUCTURE, "warn", "缺少 apps/web-antd，可能用了其他 UI 应用"))
    else:
        results.append(
            (CHECK_STRUCTURE, "error",
             "不是 vben5 monorepo 结构（应有 apps/ 与 packages/）；"
             "若为 v2/v3 单体结构，本技能的生成规范不适用")
        )


def check_route_modules(app_root: Path, results: list) -> None:
    modules_dir = app_root / "src" / "router" / "routes" / "modules"
    if not modules_dir.is_dir():
        results.append((CHECK_ROUTE_MODULES, "error", "未找到 src/router/routes/modules/"))
        return
    files = sorted(modules_dir.glob("*.ts"))
    if not files:
        results.append((CHECK_ROUTE_MODULES, "warn", "modules/ 下没有任何路由文件"))
    else:
        results.append((CHECK_ROUTE_MODULES, "ok", f"{len(files)} 个: " + ", ".join(f.name for f in files)))


def check_route_components(app_root: Path, results: list) -> None:
    modules_dir = app_root / "src" / "router" / "routes" / "modules"
    if not modules_dir.is_dir():
        results.append((CHECK_ROUTE_COMPONENT, "warn", "无路由模块，跳过"))
        return

    src = app_root / "src"
    missing: list[str] = []

    for f in modules_dir.glob("*.ts"):
        text = read(f)
        # 匹配 component: () => import('#/views/xxx/yyy.vue')
        for m in re.finditer(r"import\(\s*['\"]#/([^'\"]+\.vue)['\"]\s*\)", text):
            rel = m.group(1)
            if not (src / rel).exists():
                missing.append(f"{f.name} -> #/{rel}")

    if missing:
        results.append((CHECK_ROUTE_COMPONENT, "error", "component 指向不存在: " + "; ".join(missing[:5])))
    else:
        results.append((CHECK_ROUTE_COMPONENT, "ok", ""))


def check_router_index(app_root: Path, results: list) -> None:
    index = app_root / "src" / "router" / "routes" / "index.ts"
    if not index.exists():
        results.append((CHECK_ROUTER_INDEX_UNTOUCHED, "warn", "未找到 routes/index.ts"))
        return
    text = read(index)
    if "import.meta.glob('./modules/**/*.ts'" in text or 'import.meta.glob("./modules/**/*.ts"' in text:
        results.append((CHECK_ROUTER_INDEX_UNTOUCHED, "ok", ""))
    else:
        results.append(
            (CHECK_ROUTER_INDEX_UNTOUCHED, "warn",
             "routes/index.ts 的 glob 机制可能被改动（vben5 应保持 import.meta.glob 自动收集）")
        )


def check_grid_usage(app_root: Path, results: list) -> None:
    views = app_root / "src" / "views"
    if not views.is_dir():
        results.append((CHECK_USE_VBEN_GRID, "warn", "无 views 目录"))
        return

    list_pages = [p for p in views.rglob("list.vue")]
    if not list_pages:
        results.append((CHECK_USE_VBEN_GRID, "warn", "未找到 list.vue 页面"))
        return

    offenders = []
    for p in list_pages:
        text = read(p)
        if "useVbenVxeGrid" in text:
            continue
        # 图表看板类页面本就不用表格，跳过（如数据统计模块）
        is_dashboard = "EchartsUI" in text or "useEcharts" in text
        if is_dashboard:
            continue
        offenders.append(str(p.relative_to(app_root)))

    if offenders:
        results.append((CHECK_USE_VBEN_GRID, "warn", "列表页未用 useVbenVxeGrid: " + ", ".join(offenders[:5])))
    else:
        results.append((CHECK_USE_VBEN_GRID, "ok", f"{len(list_pages)} 个列表页"))


def check_raw_table(app_root: Path, results: list) -> None:
    views = app_root / "src" / "views"
    if not views.is_dir():
        results.append((CHECK_NO_RAW_TABLE, "warn", "无 views 目录"))
        return

    offenders = []
    for p in views.rglob("*.vue"):
        text = read(p)
        tpl = re.search(r"<template>(.*?)</template>", text, re.S)
        tpl_text = tpl.group(1) if tpl else text
        if re.search(r"<table[\s>]", tpl_text, re.I) or re.search(r"<el-table", tpl_text):
            offenders.append(str(p.relative_to(app_root)))

    if offenders:
        results.append((CHECK_NO_RAW_TABLE, "warn", "使用了原生 table/el-table: " + ", ".join(offenders[:5])))
    else:
        results.append((CHECK_NO_RAW_TABLE, "ok", ""))


def check_request_client(app_root: Path, results: list) -> None:
    api_dir = app_root / "src" / "api"
    if not api_dir.is_dir():
        results.append((CHECK_USE_REQUEST_CLIENT, "warn", "无 api 目录"))
        return

    offenders = []
    for p in api_dir.rglob("*.ts"):
        text = read(p)
        if re.search(r"from\s+['\"]axios['\"]", text):
            offenders.append(str(p.relative_to(app_root)))

    if offenders:
        results.append((CHECK_USE_REQUEST_CLIENT, "error", "API 层直接使用 axios: " + ", ".join(offenders[:5])))
    else:
        results.append((CHECK_USE_REQUEST_CLIENT, "ok", ""))


def check_ui_imports(app_root: Path, results: list) -> None:
    """web-antd 应从 ant-design-vue 导入，不应出现 antdv-next。"""
    src = app_root / "src"
    if not src.is_dir():
        results.append((CHECK_UI_IMPORT_CORRECT, "warn", "无 src 目录"))
        return

    app_name = app_root.name
    offenders = []
    for p in src.rglob("*.vue"):
        text = read(p)
        if app_name == "web-antd" and "from 'antdv-next'" in text:
            offenders.append(str(p.relative_to(app_root)))
        if app_name == "web-antd" and 'from "antdv-next"' in text:
            offenders.append(str(p.relative_to(app_root)))

    if offenders:
        results.append(
            (CHECK_UI_IMPORT_CORRECT, "error",
             "web-antd 应从 'ant-design-vue' 导入，发现 antdv-next: " + ", ".join(sorted(set(offenders))[:5]))
        )
    else:
        results.append((CHECK_UI_IMPORT_CORRECT, "ok", ""))


def check_table_action_source(app_root: Path, results: list) -> None:
    src = app_root / "src"
    if not src.is_dir():
        results.append((CHECK_TABLE_ACTION_SOURCE, "warn", "无 src 目录"))
        return

    offenders = []
    for p in list(src.rglob("*.vue")) + list(src.rglob("*.ts")):
        text = read(p)
        if re.search(r"import\s*\{[^}]*VbenTableAction[^}]*\}\s*from\s*['\"]#/adapter/vxe-table['\"]", text):
            offenders.append(str(p.relative_to(app_root)))

    if offenders:
        results.append(
            (CHECK_TABLE_ACTION_SOURCE, "error",
             "VbenTableAction 应从 '@vben/common-ui' 导入（#/adapter 仅在 playground 有）: "
             + ", ".join(offenders[:5]))
        )
    else:
        results.append((CHECK_TABLE_ACTION_SOURCE, "ok", ""))


def check_script_setup(app_root: Path, results: list) -> None:
    views = app_root / "src" / "views"
    if not views.is_dir():
        results.append((CHECK_SCRIPT_SETUP, "warn", "无 views 目录"))
        return

    offenders = []
    for p in views.rglob("*.vue"):
        text = read(p)
        if not re.search(r"<script[^>]*\bsetup\b", text):
            offenders.append(str(p.relative_to(app_root)))
        elif "lang=\"ts\"" not in text and "lang='ts'" not in text:
            offenders.append(str(p.relative_to(app_root)))

    if offenders:
        results.append((CHECK_SCRIPT_SETUP, "warn", "缺少 <script lang=\"ts\" setup>: " + ", ".join(offenders[:5])))
    else:
        results.append((CHECK_SCRIPT_SETUP, "ok", ""))


def check_alias_usage(app_root: Path, results: list) -> None:
    views = app_root / "src" / "views"
    if not views.is_dir():
        results.append((CHECK_ALIAS_USED, "warn", "无 views 目录"))
        return

    offenders = []
    for p in views.rglob("*.vue"):
        for m in re.finditer(r"from\s+['\"](\.\./\.\./\.\./[^'\"]+)['\"]", read(p)):
            offenders.append(f"{p.relative_to(app_root)} -> {m.group(1)}")

    if offenders:
        results.append((CHECK_ALIAS_USED, "warn", "存在三层以上相对引用，建议改用 #/: " + "; ".join(offenders[:3])))
    else:
        results.append((CHECK_ALIAS_USED, "ok", ""))


def check_api_typed(app_root: Path, results: list) -> None:
    api_dir = app_root / "src" / "api"
    if not api_dir.is_dir():
        results.append((CHECK_API_TYPED, "warn", "无 api 目录"))
        return

    # 跳过 vben 自带的 core 目录（框架自身 API，非本次生成）
    module_files = [
        p for p in api_dir.rglob("*.ts")
        if p.name not in {"request.ts", "index.ts"} and "core" not in p.parts
    ]
    if not module_files:
        results.append((CHECK_API_TYPED, "warn", "无 API 模块文件"))
        return

    missing = []
    for p in module_files:
        text = read(p)
        if "export namespace" not in text and "export interface" not in text and "export type" not in text:
            missing.append(str(p.relative_to(app_root)))

    if missing:
        results.append((CHECK_API_TYPED, "warn", "API 文件缺少类型定义: " + ", ".join(missing[:5])))
    else:
        results.append((CHECK_API_TYPED, "ok", f"{len(module_files)} 个模块"))


def check_fields_consistent(app_root: Path, results: list) -> None:
    """表单 schema 的 fieldName 应能在对应 API 类型中找到。"""
    views = app_root / "src" / "views"
    if not views.is_dir():
        results.append((CHECK_FIELDS_CONSISTENT, "warn", "无 views 目录"))
        return

    problems: list[str] = []
    for data_file in views.rglob("data.ts"):
        text = read(data_file)
        fields = set(re.findall(r"fieldName:\s*['\"](\w+)['\"]", text))
        if not fields:
            continue
        # 找到同页面的 api 文件（粗略：按模块名匹配）
        module = data_file.parts[data_file.parts.index("views") + 1]
        api_file = app_root / "src" / "api" / module
        api_text = ""
        if api_file.is_dir():
            api_text = "\n".join(read(f) for f in api_file.glob("*.ts"))
        if not api_text:
            continue
        missing = [f for f in fields if f not in api_text]
        if missing:
            problems.append(f"{data_file.relative_to(app_root)}: {', '.join(sorted(missing))}")

    if problems:
        results.append((CHECK_FIELDS_CONSISTENT, "warn", "表单字段在 API 类型中缺失: " + "; ".join(problems[:3])))
    else:
        results.append((CHECK_FIELDS_CONSISTENT, "ok", ""))


def check_mock(app_root: Path, results: list) -> None:
    root = app_root.parent.parent  # 回到仓库根
    mock_app = root / "apps" / "backend-mock"
    has_backend_mock = mock_app.is_dir()
    backend_routes = list((mock_app / "routes").rglob("*.ts")) if has_backend_mock else []

    frontend_mock = list(app_root.rglob("*mock*.ts")) + list(app_root.rglob("*mock*.json"))

    if backend_routes:
        results.append((CHECK_MOCK_PRESENT, "ok", f"backend-mock 有 {len(backend_routes)} 个路由"))
    elif frontend_mock:
        results.append((CHECK_MOCK_PRESENT, "ok", f"前端 mock 文件 {len(frontend_mock)} 个"))
    else:
        results.append(
            (CHECK_MOCK_PRESENT, "warn", "未发现 mock 数据，运行后表格可能为空")
        )


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python validate_project.py <vben工程根目录> [--app web-antd] [--json]")
        return 1

    root = Path(sys.argv[1]).resolve()
    as_json = "--json" in sys.argv
    app = "web-antd"
    if "--app" in sys.argv:
        idx = sys.argv.index("--app")
        if idx + 1 < len(sys.argv):
            app = sys.argv[idx + 1]

    if not root.is_dir():
        print(f"错误：目录不存在 {root}")
        return 2

    app_root = find_app_root(root, app)
    if app_root is None:
        print(f"错误：找不到应用目录 {app}")
        return 2

    results: list[tuple[str, str, str]] = []
    check_structure(root, results)
    check_route_modules(app_root, results)
    check_route_components(app_root, results)
    check_router_index(app_root, results)
    check_grid_usage(app_root, results)
    check_raw_table(app_root, results)
    check_request_client(app_root, results)
    check_ui_imports(app_root, results)
    check_table_action_source(app_root, results)
    check_script_setup(app_root, results)
    check_alias_usage(app_root, results)
    check_api_typed(app_root, results)
    check_fields_consistent(app_root, results)
    check_mock(app_root, results)

    errors = [r for r in results if r[1] == "error"]
    warns = [r for r in results if r[1] == "warn"]

    if as_json:
        print(json.dumps({
            "app_root": str(app_root),
            "ok": len(errors) == 0,
            "errors": len(errors),
            "warnings": len(warns),
            "checks": [{"name": n, "level": l, "detail": d} for n, l, d in results],
        }, ensure_ascii=False, indent=2))
        return 0 if not errors else 1

    print(f"校验目录：{app_root}")
    print("=" * 68)
    for name, level, detail in results:
        icon = {"ok": "✅", "warn": "⚠️ ", "error": "❌"}[level]
        print(f"{icon} {name}")
        if detail:
            print(f"    {detail}")
    print("=" * 68)
    print(f"错误 {len(errors)} 项，警告 {len(warns)} 项")
    if errors:
        print("存在错误，工程可能无法编译运行。")
        return 1
    if warns:
        print("无阻断性错误，但有警告建议处理。")
    else:
        print("全部通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
