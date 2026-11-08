#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""校验生成的 Flutter 工程是否符合本技能的强制约定。

用法：
    python validate_project.py <项目目录>
    python validate_project.py <项目目录> --json

只做静态检查（不依赖 Flutter SDK），退出码 0 表示无阻断性错误。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CHECK_PUBSPEC = "pubspec.yaml 存在且可解析"
CHECK_REQUIRED_FILES = "必备文件齐全"
CHECK_MAIN_RUN_APP = "main.dart 调用 runApp"
CHECK_NO_HTTP_IN_FEATURES = "features 层不直接依赖 http"
CHECK_ROUTES_REGISTERED = "页面已注册到路由表"
CHECK_ANALYSIS_OPTIONS = "存在 analysis_options.yaml"
CHECK_TEST_EXISTS = "存在测试文件"
CHECK_NO_MAGIC_COLOR = "页面无硬编码颜色"
CHECK_LAYER_DIRS = "分层目录齐全"
CHECK_IMPORT_RESOLVABLE = "相对 import 可解析"
CHECK_CONST_CONSTRUCTOR = "Widget 优先使用 const 构造"


def load_yaml_like(path: Path) -> dict:
    """极简 YAML 顶层键解析（不引入 PyYAML 依赖）。

    只解析顶层 `key:` 与二级缩进的 `key:`，足够校验 pubspec 结构。
    """
    result: dict = {}
    if not path.exists():
        return result
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] not in " \t":
            m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
            if m:
                key, val = m.group(1), m.group(2).strip()
                result[key] = val if val else {}
    return result


def check_pubspec(root: Path, results: list) -> None:
    pubspec = root / "pubspec.yaml"
    if not pubspec.exists():
        results.append((CHECK_PUBSPEC, "error", "未找到 pubspec.yaml"))
        return

    text = pubspec.read_text(encoding="utf-8", errors="ignore")
    data = load_yaml_like(pubspec)

    problems = []
    if "name" not in data:
        problems.append("缺少 name 字段")
    else:
        name = str(data.get("name", "")).strip().strip('\'"')
        if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
            problems.append(f"name '{name}' 不是合法 Dart 包名（应 snake_case 且不以数字开头）")
    if "environment" not in data:
        problems.append("缺少 environment（需声明 sdk 版本约束）")
    if "dependencies" not in data:
        problems.append("缺少 dependencies")
    if "\t" in text:
        problems.append("包含 Tab 字符（YAML 不允许用 Tab 缩进）")

    if problems:
        results.append((CHECK_PUBSPEC, "error", "; ".join(problems)))
    else:
        results.append((CHECK_PUBSPEC, "ok", ""))


def check_required_files(root: Path, results: list) -> None:
    required = [
        "pubspec.yaml",
        "analysis_options.yaml",
        "lib/main.dart",
        "lib/app.dart",
        ".gitignore",
        "README.md",
    ]
    missing = [f for f in required if not (root / f).exists()]
    if missing:
        results.append((CHECK_REQUIRED_FILES, "error", "缺少: " + ", ".join(missing)))
    else:
        results.append((CHECK_REQUIRED_FILES, "ok", ""))


def check_main_run_app(root: Path, results: list) -> None:
    main = root / "lib/main.dart"
    if not main.exists():
        results.append((CHECK_MAIN_RUN_APP, "error", "未找到 lib/main.dart"))
        return
    if re.search(r"runApp\s*\(", main.read_text(encoding="utf-8", errors="ignore")):
        results.append((CHECK_MAIN_RUN_APP, "ok", ""))
    else:
        results.append((CHECK_MAIN_RUN_APP, "error", "main.dart 未调用 runApp"))


def check_no_http_in_features(root: Path, results: list) -> None:
    features = root / "lib/features"
    if not features.exists():
        results.append((CHECK_NO_HTTP_IN_FEATURES, "warn", "未找到 lib/features 目录"))
        return

    offenders = []
    for f in features.rglob("*.dart"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"import\s+'package:http/", text):
            offenders.append(str(f.relative_to(root)))
        if re.search(r"dart:io", text):
            offenders.append(str(f.relative_to(root)))

    if offenders:
        results.append(
            (CHECK_NO_HTTP_IN_FEATURES, "error",
             "页面层直接依赖网络/IO（应通过 Repository）: " + ", ".join(sorted(set(offenders))[:5]))
        )
    else:
        results.append((CHECK_NO_HTTP_IN_FEATURES, "ok", ""))


def check_routes_registered(root: Path, results: list) -> None:
    router = root / "lib/core/router/app_router.dart"
    app = root / "lib/app.dart"
    features = root / "lib/features"

    if not router.exists():
        results.append((CHECK_ROUTES_REGISTERED, "error", "未找到 lib/core/router/app_router.dart"))
        return

    routes_text = router.read_text(encoding="utf-8", errors="ignore")
    route_names = set(re.findall(r"static\s+const\s+String\s+(\w+)\s*=", routes_text))

    app_text = app.read_text(encoding="utf-8", errors="ignore") if app.exists() else ""
    unregistered = [r for r in route_names if f"AppRoutes.{r}" not in app_text]

    # 每个 page 文件应被 app.dart 引用
    pages = []
    if features.exists():
        pages = [p for p in features.rglob("*_page.dart")]

    unimported = []
    for p in pages:
        stem = p.stem
        camel = "".join(part.capitalize() for part in stem.split("_"))
        if camel not in app_text:
            unimported.append(camel)

    if unregistered:
        results.append(
            (CHECK_ROUTES_REGISTERED, "error", "路由常量未在 app.dart 的 routes 中注册: " + ", ".join(unregistered))
        )
    elif unimported:
        results.append(
            (CHECK_ROUTES_REGISTERED, "warn", "页面类未在 app.dart 引用: " + ", ".join(unimported))
        )
    else:
        results.append((CHECK_ROUTES_REGISTERED, "ok", ""))


def check_analysis_options(root: Path, results: list) -> None:
    path = root / "analysis_options.yaml"
    if path.exists():
        results.append((CHECK_ANALYSIS_OPTIONS, "ok", ""))
    else:
        results.append((CHECK_ANALYSIS_OPTIONS, "error", "缺少 analysis_options.yaml（无法保证代码规范）"))


def check_test_exists(root: Path, results: list) -> None:
    test_dir = root / "test"
    tests = list(test_dir.rglob("*_test.dart")) if test_dir.exists() else []
    if tests:
        results.append((CHECK_TEST_EXISTS, "ok", ""))
    else:
        results.append((CHECK_TEST_EXISTS, "error", "test/ 下没有 *_test.dart"))


def check_no_magic_color(root: Path, results: list) -> None:
    features = root / "lib/features"
    if not features.exists():
        results.append((CHECK_NO_MAGIC_COLOR, "ok", ""))
        return

    offenders = []
    for f in features.rglob("*.dart"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        # 页面里出现 Color(0xFF...) 即视为硬编码
        if re.search(r"Color\(0x[0-9A-Fa-f]{8}\)", text):
            offenders.append(str(f.relative_to(root)))

    if offenders:
        results.append(
            (CHECK_NO_MAGIC_COLOR, "warn",
             "页面含硬编码颜色，应走 AppColors: " + ", ".join(sorted(offenders)[:5]))
        )
    else:
        results.append((CHECK_NO_MAGIC_COLOR, "ok", ""))


def check_layer_dirs(root: Path, results: list) -> None:
    expected = [
        "lib/core/config",
        "lib/core/network",
        "lib/core/theme",
        "lib/core/router",
        "lib/data/models",
        "lib/data/repositories",
        "lib/data/sources",
        "lib/features",
    ]
    missing = [d for d in expected if not (root / d).is_dir()]
    if missing:
        results.append((CHECK_LAYER_DIRS, "error", "缺少分层目录: " + ", ".join(missing)))
    else:
        results.append((CHECK_LAYER_DIRS, "ok", ""))


def check_import_resolvable(root: Path, results: list) -> None:
    lib = root / "lib"
    if not lib.exists():
        results.append((CHECK_IMPORT_RESOLVABLE, "error", "未找到 lib 目录"))
        return

    broken = []
    for f in lib.rglob("*.dart"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"import\s+'([^']+)'", text):
            p = m.group(1)
            if p.startswith("package:") or p.startswith("dart:"):
                continue
            if not (f.parent / p).resolve().exists():
                broken.append(f"{f.relative_to(root)} -> {p}")

    if broken:
        results.append((CHECK_IMPORT_RESOLVABLE, "error", "相对 import 无法解析: " + "; ".join(broken[:5])))
    else:
        results.append((CHECK_IMPORT_RESOLVABLE, "ok", ""))


def check_const_constructor(root: Path, results: list) -> None:
    features = root / "lib/features"
    if not features.exists():
        results.append((CHECK_CONST_CONSTRUCTOR, "ok", ""))
        return

    offenders = []
    for f in features.rglob("*.dart"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        # StatelessWidget 的构造若可行却未加 const
        for m in re.finditer(r"class\s+(\w+)\s+extends\s+StatelessWidget", text):
            cls = m.group(1)
            ctor = re.search(rf"const\s+{cls}\s*\(", text) or re.search(rf"^\s*{cls}\s*\(", text, re.M)
            if ctor and "const" not in ctor.group(0):
                offenders.append(f"{f.relative_to(root)}:{cls}")

    if offenders:
        results.append(
            (CHECK_CONST_CONSTRUCTOR, "warn", "StatelessWidget 建议加 const 构造: " + ", ".join(offenders[:5]))
        )
    else:
        results.append((CHECK_CONST_CONSTRUCTOR, "ok", ""))


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
    check_pubspec(root, results)
    check_required_files(root, results)
    check_main_run_app(root, results)
    check_no_http_in_features(root, results)
    check_routes_registered(root, results)
    check_analysis_options(root, results)
    check_test_exists(root, results)
    check_no_magic_color(root, results)
    check_layer_dirs(root, results)
    check_import_resolvable(root, results)
    check_const_constructor(root, results)

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
