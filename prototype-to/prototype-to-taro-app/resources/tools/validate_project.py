#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""校验生成的 Taro 工程是否符合本技能约定（Vue3 / React 双框架）。

用法：
    python validate_project.py <工程目录>
    python validate_project.py <工程目录> --json

只做静态检查，不依赖 Node。退出码 0 表示无阻断性错误。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---- 检查项 ----------------------------------------------------------------

CHECK_CONFIG = "config/index.ts 存在且声明 framework"
CHECK_APP_CONFIG = "src/app.config.ts 存在"
CHECK_ENTRY = "应用入口文件与框架匹配"
CHECK_PAGES_REGISTERED = "所有页面已在 app.config.ts 注册"
CHECK_PAGE_CONFIG = "每个页面有 index.config.ts"
CHECK_FRAMEWORK_PURITY = "未混用两套框架写法"
CHECK_REQUEST_WRAPPER = "存在统一请求封装"
CHECK_NO_DIRECT_TARO_REQUEST = "页面未直接调用 Taro.request"
CHECK_STATE_MGMT = "状态管理目录符合框架"
CHECK_TABBAR = "tabBar 配置合法"
CHECK_TYPES = "存在类型定义"
CHECK_STATES = "列表页有三态渲染"


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return ""


def detect_framework(root: Path) -> str | None:
    """从 config/index.ts 读取 framework 值。"""
    cfg = root / "config" / "index.ts"
    if not cfg.exists():
        return None
    text = read(cfg)
    m = re.search(r"framework:\s*['\"](\w+)['\"]", text)
    if m:
        return m.group(1)
    # 模板占位符未替换的情况
    if "{{framework}}" in text:
        return "unreplaced"
    return None


def check_config(root: Path, results: list, fw: str | None) -> None:
    cfg = root / "config" / "index.ts"
    if not cfg.exists():
        results.append((CHECK_CONFIG, "error", "未找到 config/index.ts"))
        return
    if fw is None:
        results.append((CHECK_CONFIG, "error", "config/index.ts 未声明 framework"))
    elif fw == "unreplaced":
        results.append((CHECK_CONFIG, "error", "framework 占位符 {{framework}} 未替换"))
    elif fw not in ("vue3", "react"):
        results.append((CHECK_CONFIG, "error", f"framework 值非法: {fw}（应为 vue3 或 react）"))
    else:
        results.append((CHECK_CONFIG, "ok", f"framework = {fw}"))


def check_app_config(root: Path, results: list) -> None:
    p = root / "src" / "app.config.ts"
    results.append((CHECK_APP_CONFIG, "ok", "") if p.exists() else (CHECK_APP_CONFIG, "error", "未找到 src/app.config.ts"))


def check_entry(root: Path, results: list, fw: str | None) -> None:
    src = root / "src"
    if fw == "vue3":
        if (src / "app.ts").exists():
            results.append((CHECK_ENTRY, "ok", "app.ts"))
        else:
            results.append((CHECK_ENTRY, "error", "Vue3 工程应有 src/app.ts"))
    elif fw == "react":
        if (src / "app.tsx").exists():
            results.append((CHECK_ENTRY, "ok", "app.tsx"))
        else:
            results.append((CHECK_ENTRY, "error", "React 工程应有 src/app.tsx"))
    else:
        results.append((CHECK_ENTRY, "warn", "无法判定框架，跳过"))


def get_registered_pages(root: Path) -> list[str]:
    text = read(root / "src" / "app.config.ts")
    m = re.search(r"pages:\s*\[(.*?)\]", text, re.S)
    if not m:
        return []
    return re.findall(r"['\"]([^'\"]+)['\"]", m.group(1))


def check_pages_registered(root: Path, results: list, fw: str | None) -> None:
    pages = get_registered_pages(root)
    if not pages:
        results.append((CHECK_PAGES_REGISTERED, "error", "app.config.ts 未注册任何页面"))
        return

    src_pages = root / "src" / "pages"
    missing: list[str] = []
    for p in pages:
        if "." in p.split("/")[-1]:
            skeleton = [{""}]  # 占位，后面单独检查扩展名
        # 页面目录 + 入口文件
        page_dir = src_pages / Path(p).parent.name if "/" in p else None
        # p 形如 pages/home/index → 目录 src/pages/home
        parts = p.split("/")
        if len(parts) < 3:
            missing.append(f"{p}（格式应为 pages/<name>/index）")
            continue
        d = src_pages / parts[1]
        ext = ".vue" if fw == "vue3" else ".tsx" if fw == "react" else None
        candidates = [d / f"index{ext}"] if ext else [d / "index.vue", d / "index.tsx"]
        if not any(c.exists() for c in candidates):
            missing.append(p)

    if missing:
        results.append((CHECK_PAGES_REGISTERED, "error", "注册了但文件不存在: " + ", ".join(missing[:6])))
    else:
        results.append((CHECK_PAGES_REGISTERED, "ok", f"{len(pages)} 个页面"))


def check_page_config(root: Path, results: list, fw: str | None) -> None:
    src_pages = root / "src" / "pages"
    if not src_pages.is_dir():
        results.append((CHECK_PAGE_CONFIG, "error", "未找到 src/pages"))
        return

    ext = ".vue" if fw == "vue3" else ".tsx"
    pages = [p for p in src_pages.glob(f"*/index{ext}")]
    if not pages:
        results.append((CHECK_PAGE_CONFIG, "warn", f"未找到 index{ext} 页面"))
        return

    missing = [p.parent.name for p in pages if not (p.parent / "index.config.ts").exists()]
    if missing:
        results.append((CHECK_PAGE_CONFIG, "error", "缺少 index.config.ts: " + ", ".join(missing)))
    else:
        results.append((CHECK_PAGE_CONFIG, "ok", f"{len(pages)} 个页面"))


def check_framework_purity(root: Path, results: list, fw: str | None) -> None:
    src = root / "src"
    if not src.is_dir() or fw not in ("vue3", "react"):
        results.append((CHECK_FRAMEWORK_PURITY, "warn", "无法判定，跳过"))
        return

    vue_pages = list((src / "pages").glob("*/index.vue")) if (src / "pages").is_dir() else []
    tsx_pages = list((src / "pages").glob("*/index.tsx")) if (src / "pages").is_dir() else []

    problems = []
    if fw == "vue3" and tsx_pages:
        problems.append(f"Vue3 工程出现 {len(tsx_pages)} 个 .tsx 页面")
    if fw == "react" and vue_pages:
        problems.append(f"React 工程出现 {len(vue_pages)} 个 .vue 页面")

    if problems:
        results.append((CHECK_FRAMEWORK_PURITY, "error", "; ".join(problems)))
    else:
        results.append((CHECK_FRAMEWORK_PURITY, "ok", ""))


def check_request_wrapper(root: Path, results: list) -> None:
    p = root / "src" / "services" / "request.ts"
    if p.exists():
        text = read(p)
        has_url = "BASE_URL" in text or "TARO_APP_API" in text
        results.append((CHECK_REQUEST_WRAPPER, "ok", "存在 request.ts") if has_url
                       else (CHECK_REQUEST_WRAPPER, "warn", "request.ts 未配置 BASE_URL"))
    else:
        results.append((CHECK_REQUEST_WRAPPER, "error", "未找到 src/services/request.ts"))


def check_direct_request(root: Path, results: list) -> None:
    src = root / "src"
    if not src.is_dir():
        results.append((CHECK_NO_DIRECT_TARO_REQUEST, "warn", "无 src"))
        return

    offenders = []
    for p in list(src.rglob("*.vue")) + list(src.rglob("*.tsx")):
        text = read(p)
        if "Taro.request(" in text:
            offenders.append(str(p.relative_to(root)))

    if offenders:
        results.append((CHECK_NO_DIRECT_TARO_REQUEST, "warn",
                        "页面直接调用 Taro.request（应走 services）: " + ", ".join(offenders[:4])))
    else:
        results.append((CHECK_NO_DIRECT_TARO_REQUEST, "ok", ""))


def check_state_mgmt(root: Path, results: list, fw: str | None) -> None:
    src = root / "src"
    if fw == "vue3":
        store = src / "store"
        if store.is_dir() and list(store.rglob("*.ts")):
            has_pinia = any("defineStore" in read(f) for f in store.rglob("*.ts"))
            results.append((CHECK_STATE_MGMT, "ok", "Pinia") if has_pinia
                           else (CHECK_STATE_MGMT, "warn", "store 目录存在但未见 defineStore"))
        else:
            results.append((CHECK_STATE_MGMT, "warn", "Vue3 工程建议有 src/store（Pinia）"))
    elif fw == "react":
        models = src / "models"
        if models.is_dir() and list(models.glob("*.ts")):
            has_ns = any("namespace:" in read(f) for f in models.glob("*.ts"))
            results.append((CHECK_STATE_MGMT, "ok", "Dva models") if has_ns
                           else (CHECK_STATE_MGMT, "warn", "models 缺少 namespace 定义"))
        else:
            results.append((CHECK_STATE_MGMT, "warn", "React 工程建议有 src/models（Dva）"))
    else:
        results.append((CHECK_STATE_MGMT, "warn", "无法判定框架"))


def check_tabbar(root: Path, results: list) -> None:
    text = read(root / "src" / "app.config.ts")
    if "tabBar" not in text:
        results.append((CHECK_TABBAR, "ok", "未使用 tabBar"))
        return

    m = re.search(r"tabBar:\s*\{(.*?)\n\s*\},\n\}", text, re.S)
    block = m.group(1) if m else text
    items = re.findall(r"pagePath:\s*['\"]([^'\"]+)['\"]", block)

    pages = get_registered_pages(root)
    not_in_pages = [i for i in items if i not in pages]

    problems = []
    if not (2 <= len(items) <= 5):
        problems.append(f"tabBar 项数 {len(items)}（应为 2-5）")
    if not_in_pages:
        problems.append("tabBar 页面未在 pages 注册: " + ", ".join(not_in_pages))
    if "iconPath" not in block:
        problems.append("tabBar 缺少 iconPath")

    if problems:
        results.append((CHECK_TABBAR, "error", "; ".join(problems)))
    else:
        results.append((CHECK_TABBAR, "ok", f"{len(items)} 个 tab"))


def check_types(root: Path, results: list) -> None:
    p = root / "src" / "types" / "index.ts"
    if p.exists() and ("interface" in read(p) or "type " in read(p)):
        results.append((CHECK_TYPES, "ok", ""))
    else:
        results.append((CHECK_TYPES, "warn", "建议提供 src/types/index.ts"))


def check_states(root: Path, results: list, fw: str | None) -> None:
    src = root / "src" / "pages"
    if not src.is_dir() or fw not in ("vue3", "react"):
        results.append((CHECK_STATES, "warn", "跳过"))
        return

    ext = ".vue" if fw == "vue3" else ".tsx"
    offenders = []
    for p in src.glob(f"*/index{ext}"):
        text = read(p)
        # 只检查有列表渲染的页面
        has_list = ("v-for" in text) or (".map(" in text)
        if not has_list:
            continue
        # 只有「列表数据直接来自 services 层」的页面才要求三态。
        # 注意不能用 dispatch/fetch 字样判断：个人中心会 dispatch 拉用户信息，
        # 但它的列表仍是固定菜单，不需要 loading/empty。
        imports_services = ("services/modules" in text) or ("@/services" in text)
        if not imports_services:
            continue
        has_loading = "loading" in text or "Loading" in text
        has_empty = "Empty" in text or "empty" in text.lower()
        if not (has_loading and has_empty):
            offenders.append(p.parent.name)

    if offenders:
        results.append((CHECK_STATES, "warn", "列表页缺少 loading/empty 态: " + ", ".join(offenders)))
    else:
        results.append((CHECK_STATES, "ok", ""))


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python validate_project.py <工程目录> [--json]")
        return 1

    root = Path(sys.argv[1])
    as_json = "--json" in sys.argv

    if not root.is_dir():
        print(f"错误：目录不存在 {root}")
        return 2

    fw = detect_framework(root)

    results: list[tuple[str, str, str]] = []
    check_config(root, results, fw)
    check_app_config(root, results)
    check_entry(root, results, fw)
    check_pages_registered(root, results, fw)
    check_page_config(root, results, fw)
    check_framework_purity(root, results, fw)
    check_request_wrapper(root, results)
    check_direct_request(root, results)
    check_state_mgmt(root, results, fw)
    check_tabbar(root, results)
    check_types(root, results)
    check_states(root, results, fw)

    errors = [r for r in results if r[1] == "error"]
    warns = [r for r in results if r[1] == "warn"]

    if as_json:
        print(json.dumps({
            "framework": fw,
            "ok": len(errors) == 0,
            "errors": len(errors),
            "warnings": len(warns),
            "checks": [{"name": n, "level": l, "detail": d} for n, l, d in results],
        }, ensure_ascii=False, indent=2))
        return 0 if not errors else 1

    print(f"校验目录：{root}")
    print(f"框架：{fw or '未识别'}")
    print("=" * 64)
    for name, level, detail in results:
        icon = {"ok": "✅", "warn": "⚠️ ", "error": "❌"}[level]
        print(f"{icon} {name}")
        if detail:
            print(f"    {detail}")
    print("=" * 64)
    print(f"错误 {len(errors)} 项，警告 {len(warns)} 项")
    if errors:
        print("存在错误，工程可能无法编译。")
        return 1
    if warns:
        print("无阻断性错误，但有警告建议处理。")
    else:
        print("全部通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
