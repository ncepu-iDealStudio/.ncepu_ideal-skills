#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Validate md-prd-to-html-prototype output for offline + layout contracts."""

from __future__ import annotations

import argparse
import html.parser
import sys
from pathlib import Path

SIDES = {"www", "admin", "app"}


class PrototypeInspector(html.parser.HTMLParser):
    """Collect the structural facts we validate from one HTML file."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype = False
        self.lang: str | None = None
        self.viewport = False
        self.title = ""
        self.style = False
        self.script = False
        self.external_refs: list[str] = []
        self.mock_data = False
        self.local_hrefs: list[str] = []
        self.has_modal = False
        self.has_filter = False
        self.has_toast = False
        self.has_required = False
        self._in_title = False
        self._in_script = False

    def handle_decl(self, decl: str) -> None:
        if decl.lower().startswith("doctype"):
            self.doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag == "title":
            self._in_title = True
        if tag == "style":
            self.style = True
        if tag == "script":
            self.script = True
            src = a.get("src", "")
            if src:
                self.external_refs.append(f"script src={src}")
            self._in_script = True
        if tag == "link" and a.get("rel") == "stylesheet":
            self.external_refs.append(f"link stylesheet={a.get('href', '')}")
        for key in ("href", "src"):
            val = a.get(key, "")
            if val.startswith(("http://", "https://", "//")):
                self.external_refs.append(f"{tag} {key}={val}")
        href = a.get("href", "")
        if href and not href.startswith(("http://", "https://", "//", "#", "mailto:", "javascript:")):
            self.local_hrefs.append(href.split("#", 1)[0])
        attrs_blob = " ".join(f"{k}={v}" for k, v in a.items()).lower()
        if "modal" in attrs_blob:
            self.has_modal = True
        if "filter" in attrs_blob or "reset" in attrs_blob:
            self.has_filter = True
        if "required" in attrs_blob:
            self.has_required = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_script = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()
        if "MOCK_" in data:
            self.mock_data = True
        low = data.lower()
        if "modal" in low:
            self.has_modal = True
        if "filter" in low or "resetfilter" in low:
            self.has_filter = True
        if "toast" in low:
            self.has_toast = True
        if "required" in low:
            self.has_required = True


def inspect_html(path: Path) -> tuple[list[str], PrototypeInspector]:
    text = path.read_text(encoding="utf-8", errors="replace")
    inspector = PrototypeInspector()
    inspector.feed(text)
    errors: list[str] = []
    if not inspector.doctype:
        errors.append("missing DOCTYPE")
    if inspector.lang != "zh-CN":
        errors.append('missing or wrong lang="zh-CN"')
    if not inspector.viewport:
        errors.append("missing viewport meta")
    if not inspector.title:
        errors.append("empty or missing <title>")
    if not inspector.style:
        errors.append("missing <style> (CSS must be inline)")
    if not inspector.script:
        errors.append("missing <script> (JS must be inline)")
    if inspector.external_refs:
        errors.append("external resource not allowed: " + ", ".join(inspector.external_refs))
    if not inspector.mock_data:
        errors.append("missing Mock data marker (e.g. const MOCK_...)")
    return errors, inspector


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a prototype root produced by md-prd-to-html-prototype."
    )
    parser.add_argument("root", help="prototype root directory")
    parser.add_argument("--expect-side", choices=sorted(SIDES), help="side generated this run")
    parser.add_argument("--mode", choices=["single", "multi"], help="prototype mode")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        print(f"usage error: root not found: {root}", file=sys.stderr)
        return 2

    errors: list[str] = []
    state = root / "_原型说明.md"
    if not state.is_file():
        errors.append(f"_原型说明.md: missing state file")

    for child in sorted(root.iterdir()):
        if child.is_dir() and child.name.startswith("."):
            continue
        if child.is_dir() and child.name not in SIDES:
            errors.append(f"{child.name}: unexpected directory (allowed: www/admin/app)")

    html_files = sorted(p for p in root.rglob("*.html") if p.is_file())
    for page in html_files:
        rel = page.relative_to(root).as_posix()
        page_errors, info = inspect_html(page)
        errors.extend(f"{rel}: {e}" for e in page_errors)
        for marker, present in [
            ("modal", info.has_modal),
            ("filter", info.has_filter),
            ("toast", info.has_toast),
            ("required", info.has_required),
        ]:
            if not present:
                errors.append(f"{rel}: missing interaction marker '{marker}'")

    if args.mode == "multi":
        for side in SIDES:
            side_dir = root / side
            if not side_dir.is_dir():
                continue
            if not (side_dir / "index.html").is_file():
                errors.append(f"{side}/index.html: missing index for multi-page mode")
        for page in html_files:
            rel = page.relative_to(root).as_posix()
            _, info = inspect_html(page)
            for href in info.local_hrefs:
                if not href:
                    continue
                target = (page.parent / href).resolve()
                if not target.is_file() or target.suffix.lower() != ".html":
                    errors.append(f"{rel}: broken link -> {href}")

    if errors:
        for err in errors:
            print(f"[ERROR] {err}")
        return 1

    print(f"OK: layout checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
