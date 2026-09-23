#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""common-website-design 输出验证器（Python 标准库，无第三方依赖）

用法:
    python validate.py <template目录或site目录>

检查项:
  结构:   index.html / site-manifest.json 存在; manifest 可解析且必填字段齐全
  文档:   DOCTYPE / html lang / title / viewport / meta description / body 标签存在
  语义:   每页恰一个 h1; heading 不跳级; 无重复 id; img 必有 alt
  资源:   内部链接与本地资源(css/js/img)路径有效; 远程引用已登记 external.cdn
  契约:   data-slot 命名合法; manifest 的 pages/components/collections 与页面一致
退出码: 0 = 通过(可有警告); 1 = 存在错误; 2 = 用法/路径错误
"""

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

EXTERNAL_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.has_doctype = False
        self.has_body = False
        self.lang = None
        self.title_text = ""
        self._in_title = False
        self.meta_names = set()
        self.ids = []
        self.headings = []          # [(level, lineno)]
        self.links = []             # [(href, lineno)]
        self.assets = []            # [(kind, url, lineno)]
        self.imgs_missing_alt = 0
        self.data_components = set()
        self.data_collections = set()
        self.data_slots = set()
        self.bad_slots = []         # [(value, lineno)]
        self.remote_refs = set()
        # 结构性容器: 只跟踪这些标签的平衡性(p/li 等允许隐式闭合, 不纳入)
        self.CONTAINERS = ("div", "section", "article", "aside", "header", "footer",
                           "main", "nav", "ul", "ol", "dl", "form", "details",
                           "figure", "blockquote", "table", "dialog")
        self.stack = []             # [(tag, lineno)]
        self.unclosed = []          # [(tag, lineno)]

    # ---- helpers -------------------------------------------------------
    @staticmethod
    def _attr(attrs, name):
        for k, v in attrs:
            if k == name:
                return v
        return None

    # ---- parser hooks --------------------------------------------------
    def handle_decl(self, decl):
        if decl.strip().lower().startswith("doctype"):
            self.has_doctype = True

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        if tag == "html" and self.lang is None:
            self.lang = self._attr(attrs, "lang")
        if tag == "body":
            # 模板拼接最容易漏掉这一个标签：浏览器会容错补回来，肉眼几乎看不出，
            # 但删掉 data-* 交给下游拆解时就是一份不合法的 HTML。
            self.has_body = True
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            name = (self._attr(attrs, "name") or "").lower()
            if name:
                self.meta_names.add(name)
        if tag == "link":
            rel = (self._attr(attrs, "rel") or "").lower()
            href = self._attr(attrs, "href")
            if href and "stylesheet" in rel:
                self.assets.append(("css", href, line))
        if tag == "script":
            src = self._attr(attrs, "src")
            if src:
                self.assets.append(("js", src, line))
        if tag == "img":
            if self._attr(attrs, "alt") is None:
                self.imgs_missing_alt += 1
            src = self._attr(attrs, "src")
            if src:
                self.assets.append(("img", src, line))
        if tag == "a":
            href = self._attr(attrs, "href")
            if href:
                self.links.append((href, line))

        if tag in self.CONTAINERS:
            self.stack.append((tag, line))

        _id = self._attr(attrs, "id")
        if _id:
            self.ids.append(_id)

        m = re.fullmatch(r"h([1-6])", tag)
        if m:
            self.headings.append((int(m.group(1)), line))

        dc = self._attr(attrs, "data-component")
        if dc:
            self.data_components.add(dc)
        dcol = self._attr(attrs, "data-collection")
        if dcol:
            self.data_collections.add(dcol)
        ds = self._attr(attrs, "data-slot")
        if ds:
            if re.fullmatch(r"[a-z][A-Za-z0-9]*\.[a-z][A-Za-z0-9]*", ds):
                self.data_slots.add(ds)
            else:
                self.bad_slots.append((ds, line))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in self.CONTAINERS:
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break
            # 未找到对应开标签则忽略(浏览器同样容错)

    def finish(self):
        self.unclosed = list(self.stack)

    def handle_data(self, data):
        if self._in_title:
            self.title_text += data

    def classify(self, url):
        """返回 (kind, value): external / anchor / local"""
        if url.startswith(EXTERNAL_PREFIXES):
            return "external", url
        if url.startswith("#") or url.strip() == "":
            return "anchor", url
        return "local", url


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def done(self):
        for w in self.warnings:
            print(f"  [警告] {w}")
        for e in self.errors:
            print(f"  [错误] {e}")
        print(f"结果: {len(self.errors)} 错误, {len(self.warnings)} 警告")
        if self.errors:
            print("验证未通过")
            return 1
        print("验证通过")
        return 0


def resolve_local(base: Path, page_dir: Path, url: str) -> Path:
    if url.startswith("/"):
        return base / url.lstrip("/")
    return page_dir / url


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"路径不存在或不是目录: {root}")
        return 2

    # 允许传入 site 根目录或 template 目录
    tpl = root if (root / "site-manifest.json").exists() else root / "template"
    if not (tpl / "site-manifest.json").exists():
        print(f"未找到 site-manifest.json (检查 {tpl})")
        return 2

    rep = Report()
    print(f"验证目标: {tpl}")

    # ---- manifest ------------------------------------------------------
    try:
        manifest = json.loads((tpl / "site-manifest.json").read_text(encoding="utf-8"))
    except Exception as exc:
        rep.error(f"site-manifest.json 解析失败: {exc}")
        return rep.done()

    for field in ("site", "pages", "components", "collections"):
        if field not in manifest:
            rep.error(f"manifest 缺少必填字段: {field}")
    if "designPack" not in manifest.get("site", {}):
        rep.error("manifest.site 缺少 designPack")

    manifest_pages = {p.get("file"): p.get("type") for p in manifest.get("pages", [])}
    for f, t in manifest_pages.items():
        if not t:
            rep.error(f"manifest 页面 {f} 缺少 type")
    valid_types = {"home", "list", "detail", "landing", "about", "contact", "search", "error"}
    for f, t in manifest_pages.items():
        if t and t not in valid_types:
            rep.error(f"manifest 页面 {f} 的 type 非法: {t} (合法值: {sorted(valid_types)})")

    registered_cdn = set(manifest.get("external", {}).get("cdn", []))

    # ---- pages on disk ---------------------------------------------------
    html_files = sorted(p.name for p in tpl.glob("*.html"))
    if "index.html" not in html_files:
        rep.error("缺少 index.html")

    disk_only = set(html_files) - set(manifest_pages)
    mfest_only = set(manifest_pages) - set(html_files)
    for f in sorted(disk_only):
        rep.error(f"页面 {f} 存在但未登记进 manifest.pages")
    for f in sorted(mfest_only):
        rep.error(f"manifest.pages 登记了 {f} 但文件不存在")

    all_components, all_collections, all_slots = set(), set(), set()

    for fname in html_files:
        path = tpl / fname
        try:
            parser = PageParser()
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
            parser.finish()
        except Exception as exc:
            rep.error(f"{fname}: HTML 解析失败: {exc}")
            continue

        # 文档骨架
        if not parser.has_doctype:
            rep.error(f"{fname}: 缺少 DOCTYPE")
        if not parser.lang:
            rep.error(f"{fname}: html 标签缺少 lang 属性")
        if not parser.title_text.strip():
            rep.error(f"{fname}: title 为空")
        if "viewport" not in parser.meta_names:
            rep.error(f"{fname}: 缺少 meta viewport")
        if "description" not in parser.meta_names:
            rep.error(f"{fname}: 缺少 meta description")
        if not parser.has_body:
            rep.error(f"{fname}: 缺少 <body> 标签")
        if parser.unclosed:
            t, line = parser.unclosed[0]
            extra = f" (另有 {len(parser.unclosed) - 1} 处)" if len(parser.unclosed) > 1 else ""
            rep.error(f"{fname}:{line}: 容器标签 <{t}> 未闭合{extra}")

        # heading
        h1_count = sum(1 for lvl, _ in parser.headings if lvl == 1)
        if h1_count != 1:
            rep.error(f"{fname}: h1 数量为 {h1_count} (必须恰为 1)")
        prev = 1
        for lvl, line in parser.headings:
            if lvl > prev + 1:
                rep.error(f"{fname}:{line}: heading 跳级 h{prev} -> h{lvl}")
            prev = lvl

        # id / alt
        dup = [i for i, c in Counter(parser.ids).items() if c > 1]
        if dup:
            rep.error(f"{fname}: 重复 id: {', '.join(sorted(dup))}")
        if parser.imgs_missing_alt:
            rep.error(f"{fname}: {parser.imgs_missing_alt} 个 img 缺少 alt")

        # data-*
        for val, line in parser.bad_slots:
            rep.error(f"{fname}:{line}: data-slot 命名非法: {val} (应为 model.field)")

        # 链接与资源
        page_dir = path.parent
        for href, line in parser.links:
            kind, val = parser.classify(href)
            if kind == "local":
                target = resolve_local(tpl, page_dir, val.split("#")[0].split("?")[0])
                if not target.exists():
                    rep.error(f"{fname}:{line}: 内部链接失效: {val}")
        for kind_name, url, line in parser.assets:
            kind, val = parser.classify(url)
            if kind == "external":
                parser.remote_refs.add(url)
            elif kind == "local":
                target = resolve_local(tpl, page_dir, val.split("#")[0].split("?")[0])
                if not target.exists():
                    rep.error(f"{fname}:{line}: 本地资源缺失: {kind_name} {val}")

        all_components |= parser.data_components
        all_collections |= parser.data_collections
        all_slots |= parser.data_slots

    # ---- CDN 登记 --------------------------------------------------------
    unregistered = {r for r in collect_remote(tpl) if r not in registered_cdn}
    for url in sorted(unregistered):
        rep.error(f"远程资源未登记进 manifest.external.cdn: {url}")

    # ---- manifest 与页面互相吻合 -----------------------------------------
    mfest_components = set(manifest.get("components", []))
    for c in sorted(all_components - mfest_components):
        rep.error(f"页面中 data-component '{c}' 未登记进 manifest.components")
    for c in sorted(mfest_components - all_components):
        rep.error(f"manifest.components 中的 '{c}' 未出现在任何页面")

    mfest_collections = set(manifest.get("collections", {}).keys())
    for c in sorted(all_collections - mfest_collections):
        rep.error(f"页面中 data-collection '{c}' 未登记进 manifest.collections")
    for c in sorted(mfest_collections - all_collections):
        rep.warn(f"manifest.collections 中的 '{c}' 未出现在任何页面 (集合页未生成?)")

    for name, spec in manifest.get("collections", {}).items():
        fields = set(spec.get("fields", []))
        # data-slot 前缀是模型名(单数, 如 post), 集合键是集合名(复数, 如 posts), 故按字段后缀比对
        all_field_names = {s.split(".", 1)[1] for s in all_slots}
        missing_in_html = fields - all_field_names
        if missing_in_html:
            rep.warn(f"集合 '{name}' 的字段 {sorted(missing_in_html)} 未在页面 data-slot 中出现")
        if not spec.get("sample"):
            rep.warn(f"集合 '{name}' 未标记 sample: true (样例数据必须声明)")

    if "contentSample" not in manifest:
        rep.warn("manifest 缺少 contentSample 声明 (样例数据必须全局声明)")

    return rep.done()


def collect_remote(tpl: Path) -> set:
    """复扫所有页面收集远程引用(含 a 链接之外的所有资源)"""
    remote = set()
    for p in tpl.glob("*.html"):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)["\']', text):
            remote.add(m.group(1))
    return remote


if __name__ == "__main__":
    sys.exit(main(sys.argv))
