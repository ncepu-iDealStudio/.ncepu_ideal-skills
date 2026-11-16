#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""把 HTML 原型解析为 proto_context.json（初稿，Nuxt UI Starter 版）。

用法：
    python parse_prototype.py <原型.html> --out proto_context.json \
        --project skill-swap-web --title "技能互换"

设计说明：
    这是一个**启发式**解析器，只做结构化初稿，不追求完美。
    解析结果需要人工或模型补全（尤其是交互、状态、视觉细节）。
    解析器只依赖标准库，不引入 BeautifulSoup。
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# ---- 启发式规则 ----------------------------------------------------------

LAYOUT_HINTS = {
    "list": ["list", "feed", "item", "card", "list-item"],
    "grid": ["grid", "row", "col", "cell", "entry"],
    "form": ["form", "input", "textarea", "label", "submit"],
    "detail": ["detail", "article", "content", "description"],
    "profile": ["profile", "avatar", "user-info", "mine"],
    "landing": ["hero", "banner", "cta", "feature"],
}

INTERACTION_HINTS = {
    '@click': "click",
    'onclick': "click",
    "href": "navigate",
    "@submit": "submit",
}


def camel_to_kebab(name: str) -> str:
    """camelCase / snake_case -> kebab-case（npm 包名要求）"""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1-\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    return s.replace("_", "-").lower()


def pascalize(name: str) -> str:
    """kebab-case / snake_case -> PascalCase（组件名）"""
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[-_]", name) if part)


def guess_layout(html: str) -> str:
    """按关键词出现频次判定布局原型。"""
    lowered = html.lower()
    scores = {}
    for layout, hints in LAYOUT_HINTS.items():
        scores[layout] = sum(lowered.count(h) for h in hints)
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "custom"


def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return ""


def extract_class_names(html: str) -> list[str]:
    names: list[str] = []
    for m in re.finditer(r'class="([^"]+)"', html):
        for part in m.group(1).split():
            if part and part not in names:
                names.append(part)
    return names


def extract_texts(html: str, limit: int = 20) -> list[str]:
    """提取模板里的中文文本，作为 data_fields 命名的线索。"""
    texts = re.findall(r">\s*([\u4e00-\u9fa5][^<>]{0,30})\s*<", html)
    seen: list[str] = []
    for t in texts:
        t = t.strip()
        if t and t not in seen:
            seen.append(t)
        if len(seen) >= limit:
            break
    return seen


def extract_components(class_names: list[str]) -> list[str]:
    """从 class 名推断组件（去重、过滤过短或纯布局名）。"""
    ignore = {
        "page", "container", "wrapper", "row", "col", "flex", "main",
        "content", "box", "inner", "outer", "wrap", "layout", "div",
    }
    components: list[str] = []
    for name in class_names:
        base = name.split("__")[0].split("--")[0]
        if base in ignore or len(base) < 3:
            continue
        if any(h in base for h in ["card", "item", "tag", "avatar", "empty", "nav", "bar", "header", "form"]):
            if base not in components:
                components.append(base)
    return components[:10]


def extract_data_fields(class_names: list[str]) -> list[str]:
    """按常见语义推断字段。"""
    mapping = {
        "avatar": "avatar",
        "img": "image",
        "image": "image",
        "title": "title",
        "name": "userName",
        "desc": "description",
        "price": "price",
        "tag": "tags",
        "time": "createdAt",
        "date": "createdAt",
        "count": "count",
        "rating": "rating",
        "status": "status",
    }
    fields: list[str] = ["id"]
    for name in class_names:
        for key, field in mapping.items():
            if key in name.lower() and field not in fields:
                fields.append(field)
    return fields


def extract_interactions(html: str) -> list[dict]:
    interactions: list[dict] = []
    for attr, event in INTERACTION_HINTS.items():
        if attr in html.lower():
            interactions.append({"event": event, "target": "element", "action": "navigate", "to": ""})
    if "scroll" in html.lower() or "infinite" in html.lower():
        interactions.append({"event": "scroll-bottom", "action": "load-more"})
    return interactions


def extract_colors(html: str) -> dict:
    """从 style 中提取主色（取出现频次最高的 hex 色值）。"""
    colors = re.findall(r"#([0-9a-fA-F]{6})\b", html)
    if not colors:
        return {}
    freq: dict[str, int] = {}
    for c in colors:
        key = "#" + c.upper()
        freq[key] = freq.get(key, 0) + 1
    primary = max(freq, key=lambda k: freq[k])
    return {"primary_hex": primary}


def hex_to_tailwind_color(hex_color: str) -> str:
    """将 hex 颜色粗略映射到 Tailwind 颜色名。无法精确匹配时返回 green。"""
    mapping = {
        "#00DC82": "green", "#22C55E": "green", "#10B981": "emerald",
        "#3B82F6": "blue", "#2563EB": "blue",
        "#8B5CF6": "violet", "#A855F7": "purple",
        "#F59E0B": "amber", "#F97316": "orange",
        "#EF4444": "red", "#EC4899": "pink",
        "#06B6D4": "cyan", "#14B8A6": "teal",
    }
    return mapping.get(hex_color.upper(), "green")


def main() -> int:
    parser = argparse.ArgumentParser(description="HTML 原型 -> proto_context.json（启发式初稿）")
    parser.add_argument("html", help="原型 HTML 文件路径")
    parser.add_argument("--out", default="proto_context.json", help="输出 JSON 路径")
    parser.add_argument("--project", default="prototype-web", help="工程名（kebab-case）")
    parser.add_argument("--title", default="", help="应用标题")
    parser.add_argument("--page-name", default="index", help="页面名（kebab-case，对应 app/pages/<name>.vue）")
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"错误：文件不存在 {html_path}")
        return 2

    html = html_path.read_text(encoding="utf-8", errors="ignore")

    page_name = camel_to_kebab(args.page_name)
    # index 页对应根路由 /
    route = "/" if page_name == "index" else f"/{page_name}"
    file_path = f"app/pages/{page_name}.vue"

    title = args.title or extract_title(html) or "首页"
    layout = guess_layout(html)
    class_names = extract_class_names(html)
    components = extract_components(class_names)
    data_fields = extract_data_fields(class_names)
    interactions = extract_interactions(html)
    colors = extract_colors(html)

    project_name = camel_to_kebab(args.project)
    primary_hex = colors.get("primary_hex", "#00DC82")
    primary_color = hex_to_tailwind_color(primary_hex)

    context = {
        "project": {
            "project_name": project_name,
            "app_title": title,
            "package_name": project_name,
            "target_platforms": ["web"],
            "nuxt_version": "4",
            "ui_library": "@nuxt/ui",
            "use_mock": True,
            "source_type": "html",
        },
        "design": {
            "primary_color": primary_color,
            "primary_hex": primary_hex,
            "neutral_color": "slate",
            "dark_mode": True,
            "radius_style": "md",
            "token_overrides": {},
        },
        "pages": [
            {
                "page_name": page_name,
                "route": route,
                "file_path": file_path,
                "layout_type": layout,
                "data_model": "Item",
                "components": [pascalize(c) for c in components],
                "data_fields": data_fields,
                "interactions": interactions,
                "states": ["loading", "empty", "error", "loaded"],
            }
        ],
        "navigation": {"type": "header", "items": []},
        "diagnostics": {
            "parse_errors": [],
            "assumptions": [
                f"布局原型按关键词推断为 {layout}",
                "组件与字段由 class 名启发式推断，需人工核对",
                f"主色取 HTML 中出现频次最高的 hex 值 {primary_hex}，映射为 Tailwind 色 {primary_color}",
                "Nuxt 文件路由：app/pages/index.vue → /",
            ],
            "need_confirm": [
                "页面间跳转关系（HTML 通常无法体现）",
                "是否需要底部导航或侧边栏",
                "加载态与空态的具体样式",
                "表单校验规则",
            ],
            "extracted_texts": extract_texts(html),
        },
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(
        {
            "output": str(out_path),
            "layout_type": layout,
            "route": route,
            "file_path": file_path,
            "components": [pascalize(c) for c in components],
            "data_fields": data_fields,
            "interactions": len(interactions),
            "texts_found": len(context["diagnostics"]["extracted_texts"]),
            "note": "这是初稿，请核对 diagnostics.need_confirm 中的待确认项",
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
