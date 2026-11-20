#!/usr/bin/env python3
"""从 resources/guides/ 重建本地检索索引 resources/guides_index.json。

零依赖（仅 Python 标准库）。用法：
    python3 resources/tools/build_index.py
    python3 resources/tools/build_index.py --guides <目录> --out <索引文件>

索引是「派生文件」，可随时重建。指南原文永不改动。
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
from pathlib import Path

# 检索时忽略的常见虚词；技术缩写（INP/LCP/CLS/CWV 等）不在其中，会被保留。
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is",
    "it", "of", "on", "or", "that", "the", "this", "to", "use", "using", "with",
    "when", "which", "how", "what", "why", "do", "does", "not", "your", "you",
    "into", "can", "if", "its", "their", "they", "these", "than", "then", "also",
    "more", "most", "some", "such", "over", "under", "each", "any", "all",
    "the", "about", "after", "before", "between", "within", "via", "per",
}

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#.\-]*")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
MD_LINK_RE = re.compile(r"^\s*[-*]?\s*\[.+?\]\(#")  # 目录/锚点链接行
LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|>\s+)")


def tokenize(text: str) -> list[str]:
    """抽取小写英文/数字 token，去掉停用词与过短词。"""
    out: list[str] = []
    for m in TOKEN_RE.finditer(text.lower()):
        t = m.group(0).strip(".-+#")
        if len(t) >= 2 and t not in STOPWORDS and not t.isdigit():
            out.append(t)
    return out


def first_paragraph(lines: list[str]) -> str:
    """取第一段「正文」：跳过标题、目录链接、列表、代码块、表格与纯格式行。"""
    in_code = False
    buf: list[str] = []
    for ln in lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
            if buf:
                break
            continue
        if in_code:
            continue
        s = ln.strip()
        if not s:
            if buf:
                break
            continue
        if s.startswith("#"):          # 标题
            if buf:
                break
            continue
        if MD_LINK_RE.match(ln):        # 目录项
            continue
        if LIST_RE.match(ln):           # 列表/引用
            continue
        if s.startswith("|"):           # 表格
            continue
        if s.startswith("<!--") or s.startswith(">"):
            continue
        buf.append(s)
        # 段落碰到下一个块级元素就停
        joined = " ".join(buf)
        if len(joined) > 400:
            break
    text = " ".join(buf)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # 保留链接文字
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:240]


def build(guides_dir: Path, out_file: Path) -> dict:
    guides_dir = guides_dir.resolve()
    entries: list[dict] = []
    files = sorted(guides_dir.rglob("*.md"))
    for f in files:
        rel = f.relative_to(guides_dir)
        category = rel.parts[0] if len(rel.parts) > 1 else "general"
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()

        title = f.stem
        for ln in lines:
            m = HEADING_RE.match(ln)
            if m:
                title = re.sub(r"[`*]", "", m.group(1)).strip()
                break

        summary = first_paragraph(lines)

        # 关键词：标题 + 各级标题 + 摘要 + id + 分类名，去重后保留顺序
        heading_text = " ".join(
            m.group(1) for ln in lines if (m := HEADING_RE.match(ln))
        )
        raw = " ".join([title, summary, heading_text, f.stem, category])
        seen: set[str] = set()
        keywords: list[str] = []
        for t in tokenize(raw):
            if t not in seen:
                seen.add(t)
                keywords.append(t)

        entries.append({
            "id": f.stem,
            "category": category,
            "path": rel.as_posix(),
            "title": title,
            "summary": summary,
            "keywords": keywords[:80],
        })

    categories: dict[str, int] = {}
    for e in entries:
        categories[e["category"]] = categories.get(e["category"], 0) + 1

    index = {
        "meta": {
            "schema_version": 1,
            "generated_at": datetime.date.today().isoformat(),
            "source": "GoogleChrome/modern-web-guidance @ 4dd968349e54ca45a05dd5c818fb035c9054b022",
            "guide_count": len(entries),
            "guides_dir": "resources/guides",
        },
        "categories": dict(sorted(categories.items())),
        "guides": entries,
    }

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return index


def main() -> int:
    here = Path(__file__).resolve().parent
    default_guides = here.parent / "guides"
    default_out = here.parent / "guides_index.json"
    ap = argparse.ArgumentParser(description="重建 modern-web-guidance 本地检索索引")
    ap.add_argument("--guides", type=Path, default=default_guides)
    ap.add_argument("--out", type=Path, default=default_out)
    args = ap.parse_args()

    idx = build(args.guides, args.out)
    print(f"已生成 {args.out}")
    print(f"指南数：{idx['meta']['guide_count']}，分类数：{len(idx['categories'])}")
    for cat, n in idx["categories"].items():
        print(f"  {cat:<18} {n:>3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
