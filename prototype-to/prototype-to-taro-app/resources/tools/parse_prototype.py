#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""把 HTML 原型解析为 proto_context.json（初稿，Taro 双框架版）。

用法：
    python parse_prototype.py <原型.html> --out proto_context.json \
        --project campus-skill-swap --title "技能互换" \
        --framework vue3 [--targets weapp,h5]

注意：--framework 必填，只能是 vue3 或 react。本技能不设默认框架。

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
}

INTERACTION_HINTS = {
    '@click': "tap",
    'onclick': "tap",
    "href": "navigate",
}


def camelize(name: str) -> str:
    """kebab-case -> PascalCase（组件名）"""
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[-_]", name) if part)


def camel_to_kebab(name: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1-\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    return s.replace("_", "-").lower()


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
        "content", "box", "inner", "outer", "wrap", "layout",
    }
    components: list[str] = []
    for name in class_names:
        base = name.split("__")[0].split("--")[0]
        if base in ignore or len(base) < 3:
            continue
        if any(h in base for h in ["card", "item", "tag", "avatar", "empty", "nav", "bar", "header"]):
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


def extract_interactions(html: str, class_names: list[str]) -> list[dict]:
    interactions: list[dict] = []
    for attr, event in INTERACTION_HINTS.items():
        if attr in html.lower():
            interactions.append({"event": event, "target": "element", "action": "navigate", "to": ""})
    if "pull" in html.lower() or "refresh" in html.lower():
        interactions.append({"event": "pull-down", "action": "refresh"})
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
    return {"primary_color": primary}


def main() -> int:
    parser = argparse.ArgumentParser(description="HTML 原型 -> proto_context.json（启发式初稿）")
    parser.add_argument("html", help="原型 HTML 文件路径")
    parser.add_argument("--out", default="proto_context.json", help="输出 JSON 路径")
    parser.add_argument("--project", default="prototype-app", help="工程名（kebab-case）")
    parser.add_argument("--title", default="", help="应用标题")
    parser.add_argument("--framework", required=True, choices=["vue3", "react"],
                        help="框架（必填，无默认值）")
    parser.add_argument("--targets", default="weapp,h5", help="目标平台，逗号分隔：weapp,h5,alipay,rn")
    parser.add_argument("--page-name", default="index", help="页面名（kebab-case）")
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"错误：文件不存在 {html_path}")
        return 2

    html = html_path.read_text(encoding="utf-8", errors="ignore")

    page_name = camel_to_kebab(args.page_name)
    title = args.title or extract_title(html) or "首页"
    layout = guess_layout(html)
    class_names = extract_class_names(html)
    components = extract_components(class_names)
    data_fields = extract_data_fields(class_names)
    interactions = extract_interactions(html, class_names)
    colors = extract_colors(html)

    context = {
        "project": {
            "project_name": args.project,
            "app_title": title,
            "appid": "touristappid",
            "framework": args.framework,
            "targets": [t.strip() for t in args.targets.split(",") if t.strip()],
            "source_type": "html",
        },
        "design": {
            "primary_color": colors.get("primary_color", "#2B6DE5"),
            "radius_style": "md",
            "theme": "light",
            "token_overrides": {},
        },
        "pages": [
            {
                "page_name": page_name,
                "path": f"pages/{page_name}/index",
                "title": title,
                "is_tab": False,
                "is_home": True,
                "layout": layout,
                "components": [camelize(c) for c in components],
                "data_model": "Item",
                "data_fields": data_fields,
                "interactions": interactions,
                "states": ["loading", "empty", "error", "loaded"],
            }
        ],
        "tab_bar": {"enabled": False, "items": []},
        "diagnostics": {
            "parse_errors": [],
            "assumptions": [
                f"布局原型按关键词推断为 {layout}",
                "组件与字段由 class 名启发式推断，需人工核对",
                "颜色取 HTML 中出现频次最高的 hex 值",
            ],
            "need_confirm": [
                "页面间跳转关系（HTML 通常无法体现）",
                "是否需要 tabBar",
                "加载态与空态的具体样式",
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
            "layout": layout,
            "framework": args.framework,
            "components": [camelize(c) for c in components],
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
