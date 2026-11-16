#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""校验生成的 Nuxt UI Starter 工程是否符合本技能的强制约定。

用法：
    python validate_project.py <项目目录>
    python validate_project.py <项目目录> --json

只做静态检查（不依赖 Node/npm），退出码 0 表示无阻断性错误。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CHECK_PACKAGE_JSON = "package.json 存在且可解析"
CHECK_REQUIRED_FILES = "必备文件齐全"
CHECK_NUXT_CONFIG = "nuxt.config.ts 含 @nuxt/ui 模块"
CHECK_APP_VUE = "app.vue 包含 NuxtPage"
CHECK_APP_CONFIG = "app.config.ts 声明 ui.colors.primary"
CHECK_NO_FETCH_IN_PAGES = "页面不直接使用原生 fetch"
CHECK_MAIN_CSS = "main.css 导入 tailwindcss 与 @nuxt/ui"
CHECK_POSTINSTALL = "package.json 的 postinstall 为 nuxt prepare"
CHECK_NO_PINIA = "未默认引入 Pinia（原型阶段用 composables）"
CHECK_TYPESCRIPT = "存在 tsconfig.json"
CHECK_SERVICE_LAYER = "存在 services 数据服务层"
CHECK_COMPOSABLES = "存在 composables 逻辑层"
CHECK_NAVIGATION = "navigation.ts 的栏目能落到页面文件"

VALID_PRIMARY_COLORS = {
    "green", "emerald", "blue", "indigo", "violet", "purple",
    "pink", "rose", "red", "orange", "amber", "yellow", "lime",
    "teal", "cyan", "sky", "slate", "gray", "zinc", "neutral", "stone"
}


def load_package_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"__error__": "invalid json"}


def check_package_json(root: Path, results: list) -> None:
    pkg_path = root / "package.json"
    if not pkg_path.exists():
        results.append((CHECK_PACKAGE_JSON, "error", "未找到 package.json"))
        return

    data = load_package_json(pkg_path)
    if "__error__" in data:
        results.append((CHECK_PACKAGE_JSON, "error", "package.json 不是合法 JSON"))
        return

    problems = []
    name = data.get("name", "")
    if not name:
        problems.append("缺少 name 字段")
    elif not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        problems.append(f"name '{name}' 不是合法 npm 包名（应 kebab-case）")

    if data.get("type") != "module":
        problems.append("type 应为 'module'（Nuxt 4 要求）")

    if problems:
        results.append((CHECK_PACKAGE_JSON, "error", "; ".join(problems)))
    else:
        results.append((CHECK_PACKAGE_JSON, "ok", ""))


def check_required_files(root: Path, results: list) -> None:
    required = [
        "package.json",
        "nuxt.config.ts",
        "tsconfig.json",
        "eslint.config.mjs",
        "app/app.vue",
        "app/app.config.ts",
        "app/assets/css/main.css",
        ".gitignore",
        "README.md",
    ]
    missing = [f for f in required if not (root / f).exists()]
    if missing:
        results.append((CHECK_REQUIRED_FILES, "error", "缺少: " + ", ".join(missing)))
    else:
        results.append((CHECK_REQUIRED_FILES, "ok", ""))


def check_nuxt_config(root: Path, results: list) -> None:
    path = root / "nuxt.config.ts"
    if not path.exists():
        results.append((CHECK_NUXT_CONFIG, "error", "未找到 nuxt.config.ts"))
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    if "@nuxt/ui" not in text:
        results.append((CHECK_NUXT_CONFIG, "error", "nuxt.config.ts 的 modules 中未包含 '@nuxt/ui'"))
    else:
        results.append((CHECK_NUXT_CONFIG, "ok", ""))


def check_app_vue(root: Path, results: list) -> None:
    path = root / "app" / "app.vue"
    if not path.exists():
        results.append((CHECK_APP_VUE, "error", "未找到 app/app.vue"))
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    if "NuxtPage" not in text:
        results.append((CHECK_APP_VUE, "error", "app.vue 未包含 <NuxtPage />，页面无法渲染"))
    elif "UApp" not in text:
        results.append((CHECK_APP_VUE, "warn", "建议使用 <UApp> 包裹以启用 Nuxt UI 应用外壳"))
    else:
        results.append((CHECK_APP_VUE, "ok", ""))


def check_app_config(root: Path, results: list) -> None:
    path = root / "app" / "app.config.ts"
    if not path.exists():
        results.append((CHECK_APP_CONFIG, "error", "未找到 app/app.config.ts"))
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"primary:\s*['\"](\w+)['\"]", text)
    if not m:
        results.append((CHECK_APP_CONFIG, "error", "app.config.ts 未声明 ui.colors.primary"))
        return

    color = m.group(1)
    if color not in VALID_PRIMARY_COLORS:
        results.append((CHECK_APP_CONFIG, "warn", f"primary 颜色 '{color}' 可能不是 Tailwind 合法色名"))
    else:
        results.append((CHECK_APP_CONFIG, "ok", ""))


def check_no_fetch_in_pages(root: Path, results: list) -> None:
    pages = root / "app" / "pages"
    if not pages.exists():
        results.append((CHECK_NO_FETCH_IN_PAGES, "warn", "未找到 app/pages 目录"))
        return

    offenders = []
    for f in pages.rglob("*.vue"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        # 原生 fetch（非 $fetch）
        if re.search(r"(?<!\$)fetch\s*\(", text):
            offenders.append(str(f.relative_to(root)))

    if offenders:
        results.append(
            (CHECK_NO_FETCH_IN_PAGES, "warn",
             "页面直接使用原生 fetch，建议通过 service 层 + $fetch: " + ", ".join(sorted(set(offenders))[:5]))
        )
    else:
        results.append((CHECK_NO_FETCH_IN_PAGES, "ok", ""))


def check_main_css(root: Path, results: list) -> None:
    path = root / "app" / "assets" / "css" / "main.css"
    if not path.exists():
        results.append((CHECK_MAIN_CSS, "error", "未找到 app/assets/css/main.css"))
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    problems = []
    if 'tailwindcss' not in text:
        problems.append("未 @import 'tailwindcss'")
    if '@nuxt/ui' not in text:
        problems.append("未 @import '@nuxt/ui'")

    if problems:
        results.append((CHECK_MAIN_CSS, "error", "; ".join(problems)))
    else:
        results.append((CHECK_MAIN_CSS, "ok", ""))


def check_postinstall(root: Path, results: list) -> None:
    data = load_package_json(root / "package.json")
    if "__error__" in data or not data:
        results.append((CHECK_POSTINSTALL, "error", "无法读取 package.json"))
        return

    scripts = data.get("scripts", {})
    postinstall = scripts.get("postinstall", "")
    if postinstall != "nuxt prepare":
        results.append((CHECK_POSTINSTALL, "error", f"postinstall 应为 'nuxt prepare'，当前为 '{postinstall}'"))
    else:
        results.append((CHECK_POSTINSTALL, "ok", ""))


def check_no_pinia(root: Path, results: list) -> None:
    data = load_package_json(root / "package.json")
    if "__error__" in data or not data:
        results.append((CHECK_NO_PINIA, "warn", "无法读取 package.json"))
        return

    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    if "pinia" in deps or "@pinia/nuxt" in deps:
        results.append((CHECK_NO_PINIA, "warn", "原型阶段不建议引入 Pinia，用 composables 即可"))
    else:
        results.append((CHECK_NO_PINIA, "ok", ""))


def check_typescript(root: Path, results: list) -> None:
    path = root / "tsconfig.json"
    if path.exists():
        results.append((CHECK_TYPESCRIPT, "ok", ""))
    else:
        results.append((CHECK_TYPESCRIPT, "error", "缺少 tsconfig.json"))


def check_service_layer(root: Path, results: list) -> None:
    services = root / "app" / "services"
    if services.exists() and any(services.rglob("*.ts")):
        results.append((CHECK_SERVICE_LAYER, "ok", ""))
    else:
        results.append((CHECK_SERVICE_LAYER, "warn", "建议建立 app/services/ 作为数据服务层（唯一数据接缝）"))


def check_composables(root: Path, results: list) -> None:
    composables = root / "app" / "composables"
    if composables.exists() and any(composables.rglob("*.ts")):
        results.append((CHECK_COMPOSABLES, "ok", ""))
    else:
        results.append((CHECK_COMPOSABLES, "warn", "建议建立 app/composables/ 存放状态与逻辑"))


def route_has_page(root: Path, route: str) -> bool:
    path = route.split("?", 1)[0].split("#", 1)[0]
    if path.startswith(("http://", "https://")):
        return True
    if not path.startswith("/"):
        return False
    parts = [part for part in path.strip("/").split("/") if part]
    pages = root / "app" / "pages"
    if not parts:
        return (pages / "index.vue").exists()
    relative = Path(*parts)
    return (pages / f"{relative}.vue").exists() or (pages / relative / "index.vue").exists()


def check_navigation(root: Path, results: list) -> None:
    nav_path = root / "app" / "navigation.ts"
    app_vue = root / "app" / "app.vue"
    if not nav_path.exists():
        results.append((CHECK_NAVIGATION, "warn", "未找到 app/navigation.ts，新增栏目时无法只追加一项"))
        return

    nav_text = nav_path.read_text(encoding="utf-8", errors="ignore")
    app_text = app_vue.read_text(encoding="utf-8", errors="ignore") if app_vue.exists() else ""
    problems = []
    if "navItems" not in app_text or "UNavigationMenu" not in app_text:
        problems.append("app.vue 未用 UNavigationMenu 渲染 navItems")

    missing = []
    for route in re.findall(r"""to:\s*['"]([^'"]+)['"]""", nav_text):
        if ":" in route:
            continue
        if not route_has_page(root, route):
            missing.append(route)
    if missing:
        problems.append("栏目路由没有对应页面: " + ", ".join(missing))

    if problems:
        results.append((CHECK_NAVIGATION, "error", "; ".join(problems)))
    else:
        results.append((CHECK_NAVIGATION, "ok", ""))


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python validate_project.py <项目目录> [--json]")
        return 1

    root = Path(sys.argv[1])
    as_json = "--json" in sys.argv

    if not root.is_dir():
        print(f"错误：目录不存在 {root}")
        return 2

    results: list[tuple[str, str, str]] = []
    check_package_json(root, results)
    check_required_files(root, results)
    check_nuxt_config(root, results)
    check_app_vue(root, results)
    check_app_config(root, results)
    check_no_fetch_in_pages(root, results)
    check_main_css(root, results)
    check_postinstall(root, results)
    check_no_pinia(root, results)
    check_typescript(root, results)
    check_service_layer(root, results)
    check_composables(root, results)
    check_navigation(root, results)

    errors = [r for r in results if r[1] == "error"]
    warns = [r for r in results if r[1] == "warn"]

    if as_json:
        print(json.dumps(
            {
                "ok": len(errors) == 0,
                "errors": len(errors),
                "warnings": len(warns),
                "checks": [{"name": n, "level": l, "detail": d} for n, l, d in results],
            },
            ensure_ascii=False,
            indent=2,
        ))
        return 0 if not errors else 1

    print(f"校验目录：{root}")
    print("=" * 60)
    for name, level, detail in results:
        icon = {"ok": "✅", "warn": "⚠️ ", "error": "❌"}[level]
        print(f"{icon} {name}")
        if detail:
            print(f"    {detail}")

    print("=" * 60)
    print(f"错误 {len(errors)} 项，警告 {len(warns)} 项")
    if errors:
        print("存在错误，工程可能无法运行。")
        return 1
    if warns:
        print("无阻断性错误，但有警告建议处理。")
    else:
        print("全部通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
