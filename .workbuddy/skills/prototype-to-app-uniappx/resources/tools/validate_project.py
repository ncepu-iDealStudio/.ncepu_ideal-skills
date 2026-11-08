#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""校验生成的 uni-app x 工程是否符合本技能的强制约定。

用法：
    python validate_project.py <项目目录>
    python validate_project.py <项目目录> --json

只做静态检查，不编译不运行。退出码 0 表示全部通过。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---- 检查项定义 ----------------------------------------------------------

CHECK_PAGES_JSON_EXISTS = "pages.json 存在"
CHECK_PAGES_REGISTERED = "pages.json 注册的页面文件都存在"
CHECK_NO_VUE_PAGES = "没有 .vue 页面（应为 .uvue）"
CHECK_MANIFEST_X_FLAG = "manifest.json 含 uni-app-x 标记"
CHECK_PAGE_NO_HARDCODED_DATA = "页面未直接写死业务数据"
CHECK_TEXT_WRAPPED = "模板文字位于 <text> 内"
CHECK_FLEX_ROW_EXPLICIT = "横向容器显式声明 flex-direction: row"
CHECK_HAS_STATES = "页面含 loading/empty 状态分支"
CHECK_IMAGE_HAS_SIZE = "image 有明确宽高"
CHECK_VFOR_HAS_KEY = "v-for 带 :key"


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"__error__": str(exc)}


def check_pages(root: Path, results: list) -> None:
    pages_json = root / "pages.json"
    if not pages_json.exists():
        results.append((CHECK_PAGES_JSON_EXISTS, "error", "未找到 pages.json"))
        return
    results.append((CHECK_PAGES_JSON_EXISTS, "ok", ""))

    data = load_json(pages_json)
    if "__error__" in data:
        results.append((CHECK_PAGES_REGISTERED, "error", f"pages.json 解析失败: {data['__error__']}"))
        return

    missing = []
    for page in data.get("pages", []):
        rel = page.get("path", "")
        if not rel:
            continue
        target = root / f"{rel}.uvue"
        if not target.exists():
            missing.append(rel)

    if missing:
        results.append(
            (CHECK_PAGES_REGISTERED, "error", "以下页面在 pages.json 注册但文件不存在: " + ", ".join(missing))
        )
    else:
        results.append((CHECK_PAGES_REGISTERED, "ok", ""))

    # 首页必须是 pages 数组第一项
    pages = data.get("pages", [])
    if pages:
        first = pages[0].get("path", "")
        if first and not (root / f"{first}.uvue").exists():
            results.append((CHECK_PAGES_REGISTERED, "warn", f"首页 {first} 文件不存在"))


def check_no_vue_pages(root: Path, results: list) -> None:
    offenders = [
        str(p.relative_to(root))
        for p in root.rglob("*.vue")
        if "node_modules" not in str(p)
    ]
    if offenders:
        results.append(
            (CHECK_NO_VUE_PAGES, "error", "发现 .vue 文件（uni-app x 页面必须用 .uvue）: " + ", ".join(offenders[:10]))
        )
    else:
        results.append((CHECK_NO_VUE_PAGES, "ok", ""))


def check_manifest(root: Path, results: list) -> None:
    manifest = root / "manifest.json"
    if not manifest.exists():
        results.append((CHECK_MANIFEST_X_FLAG, "error", "未找到 manifest.json"))
        return
    data = load_json(manifest)
    if "__error__" in data:
        results.append((CHECK_MANIFEST_X_FLAG, "error", f"manifest.json 解析失败: {data['__error__']}"))
        return
    if "uni-app-x" in data:
        results.append((CHECK_MANIFEST_X_FLAG, "ok", ""))
    else:
        results.append(
            (CHECK_MANIFEST_X_FLAG, "error", "manifest.json 缺少 \"uni-app-x\": {}，会被识别为普通 uni-app 项目")
        )


def iter_uvue(root: Path):
    for p in root.rglob("*.uvue"):
        if "node_modules" in str(p):
            continue
        yield p


def check_hardcoded_data(root: Path, results: list) -> None:
    """页面内不应出现大段硬编码数组/对象字面量（应走 services/mock）。"""
    offenders = []
    array_literal = re.compile(r"(?:const|let|var)\s+\w+\s*(?::\s*[^=]+)?=\s*\[\s*\{", re.M)
    for path in iter_uvue(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        script = extract_script(text)
        if array_literal.search(script):
            offenders.append(str(path.relative_to(root)))
    if offenders:
        results.append(
            (CHECK_PAGE_NO_HARDCODED_DATA, "warn", "页面内疑似硬编码数据数组，应移至 services/mock: " + ", ".join(offenders[:5]))
        )
    else:
        results.append((CHECK_PAGE_NO_HARDCODED_DATA, "ok", ""))


def check_text_wrapped(root: Path, results: list) -> None:
    """检测模板中**位于 <text> 之外**的裸文字（App 端不渲染）。

    正确做法：逐个定位 text 节点区间并剔除，再看剩余部分是否含中文。
    不能简单"删掉所有标签"——那样会把 <text> 内部的内容也误判为裸文字。
    """
    offenders = []
    text_block = re.compile(r"<text\b[^>]*>.*?</text>", re.S | re.I)

    for path in iter_uvue(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        template = extract_template(text)
        if not template:
            continue

        # 1) 先剔除所有 <text>...</text> 区块（这些是合法的）
        remainder = text_block.sub("", template)
        # 2) 再剔除注释
        remainder = re.sub(r"<!--.*?-->", "", remainder, flags=re.S)
        # 3) 剔除所有标签，只留文本节点
        remainder = re.sub(r"<[^>]+>", "", remainder)
        # 4) 剔除插值表达式
        remainder = re.sub(r"\{\{[^}]*\}\}", "", remainder)
        remainder = remainder.strip()

        if re.search(r"[\u4e00-\u9fa5]", remainder):
            offenders.append(str(path.relative_to(root)))

    if offenders:
        results.append(
            (CHECK_TEXT_WRAPPED, "warn", "模板存在位于 <text> 之外的裸文字（App 端不渲染）: " + ", ".join(offenders[:5]))
        )
    else:
        results.append((CHECK_TEXT_WRAPPED, "ok", ""))


def check_flex_row(root: Path, results: list) -> None:
    """横向排列意图的容器是否显式写了 flex-direction: row。

    启发式：class 名含 row / between / tags / stats / menu 等横向语义，
    且该 class 使用了 display:flex 但未声明 flex-direction: row。
    """
    row_hint = re.compile(r"\.(?:[\w-]*(?:row|between|tags|stats|menu|bar|header|meta|grid)[\w-]*)\s*\{([^}]*)\}", re.S)
    offenders = []
    for path in iter_uvue(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        style = extract_style(text)
        if not style:
            continue
        for match in row_hint.finditer(style):
            body = match.group(1)
            if "flex-direction" not in body and "flex: 1" in body or (
                "flex-direction" not in body and "justify-content" in body
            ):
                offenders.append(f"{path.relative_to(root)}:{match.group(0)[:40]}")
    if offenders:
        results.append(
            (CHECK_FLEX_ROW_EXPLICIT, "warn", "横向容器可能缺少 flex-direction: row: " + "; ".join(offenders[:5]))
        )
    else:
        results.append((CHECK_FLEX_ROW_EXPLICIT, "ok", ""))


def check_states(root: Path, results: list) -> None:
    """需要 loading/empty 分支的是**会发起数据请求**的页面。

    判定依据：页面是否从 services/api 导入并调用。
    纯静态页（如个人中心、设置页）虽可能有 v-for 渲染静态配置，但不强制三态。
    """
    offenders = []
    fetches_data = re.compile(r"from\s+['\"]@?/?services/api/", re.M)

    for path in iter_uvue(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        template = extract_template(text)
        script = extract_script(text)
        if not template:
            continue
        # 不取数的页面不要求三态
        if not fetches_data.search(script):
            continue
        has_loading = "loading" in text
        has_empty = ("EmptyState" in template) or ("empty" in template.lower())
        if not (has_loading and has_empty):
            offenders.append(str(path.relative_to(root)))

    if offenders:
        results.append(
            (CHECK_HAS_STATES, "warn", "取数页面缺少 loading 或 empty 状态: " + ", ".join(offenders[:5]))
        )
    else:
        results.append((CHECK_HAS_STATES, "ok", ""))


def check_image_size(root: Path, results: list) -> None:
    """<image> 应带 class 或 style 指定尺寸。"""
    offenders = []
    for path in iter_uvue(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"<image\b[^>]*>", text):
            tag = match.group(0)
            if "class=" in tag or "style=" in tag or "width=" in tag:
                continue
            offenders.append(str(path.relative_to(root)))
            break
    if offenders:
        results.append((CHECK_IMAGE_HAS_SIZE, "warn", "image 未指定尺寸: " + ", ".join(offenders[:5])))
    else:
        results.append((CHECK_IMAGE_HAS_SIZE, "ok", ""))


def check_vfor_key(root: Path, results: list) -> None:
    offenders = []
    for path in iter_uvue(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"v-for=\"[^\"]*\"([^>]*)", text):
            tail = match.group(1)
            if ":key" not in tail and "key=" not in tail:
                offenders.append(str(path.relative_to(root)))
                break
    if offenders:
        results.append((CHECK_VFOR_HAS_KEY, "warn", "v-for 缺少 :key: " + ", ".join(offenders[:5])))
    else:
        results.append((CHECK_VFOR_HAS_KEY, "ok", ""))


# ---- 辅助 ----------------------------------------------------------------


def extract_template(text: str) -> str:
    m = re.search(r"<template>(.*?)</template>", text, re.S)
    return m.group(1) if m else ""


def extract_script(text: str) -> str:
    m = re.search(r"<script[^>]*>(.*?)</script>", text, re.S)
    return m.group(1) if m else ""


def extract_style(text: str) -> str:
    m = re.search(r"<style[^>]*>(.*?)</style>", text, re.S)
    return m.group(1) if m else ""


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
    check_pages(root, results)
    check_no_vue_pages(root, results)
    check_manifest(root, results)
    check_hardcoded_data(root, results)
    check_text_wrapped(root, results)
    check_flex_row(root, results)
    check_states(root, results)
    check_image_size(root, results)
    check_vfor_key(root, results)

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
        print("存在错误，需修复后才能运行。")
        return 1
    if warns:
        print("无阻断性错误，但有警告建议处理。")
    else:
        print("全部通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
