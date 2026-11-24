# md-prd-to-html-prototype 多端多页原型技能增强 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 subagent-driven-development（推荐）或 executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 把 `md-prd-to-html-prototype` 从"单文件一次性生成器"升级为"多端分流 + 单页/多静态页可选 + 完全离线 + 自动校验"的原型生成技能。

**架构：** `SKILL.md` 作为主干只编排 6 步工作流与 4 个决策门；三份 `references/` 规范分别承载目录契约、离线交互契约、端识别与状态格式；`scripts/validate_prototype.py` 是唯一可执行校验点，配套标准库单测。根目录版 canonical，`.workbuddy` 安装副本保留叠加节后同步。

**技术栈：** Markdown 技能文档；Python 3 标准库（`argparse`、`html.parser`、`pathlib`、`unittest`、`tempfile`），零第三方依赖。

**规格：** `.docs/specs/2026-11-16-md-prd-to-html-prototype-enhancement-design.md`（commit `316e503`）

---

## 全局约束

- 完全离线：内联 CSS/JS，禁止 CDN、`<link rel="stylesheet">`、`<script src>`、外部字体/图片 URL。
- 端目录固定 `www/`、`admin/`、`app/`，位于用户指定原型根目录下；每次调用只生成一个端。
- 单页 = 一个 HTML 含全部视图；多静态页 = 每页一个 HTML + `index.html` + 真实 `href`。
- 状态文件 `_原型说明.md` 位于原型根目录，含 7 个必含小节（见规格 §4）。
- 步骤 2（选端）与步骤 3（选模式）每次必须问用户，状态文件不得跳过确认。
- 禁止编造业务字段；缺失信息写 `[NEEDS CLARIFICATION]` 并停止生成。
- 校验器退出码：0 通过 / 1 校验错误 / 2 用法错误；错误信息格式 `[ERROR] <相对路径>: <问题>`。
- 校验器与单测只用 Python 标准库，不引入 pytest 等第三方依赖。
- 测试文件放技能目录 `scripts/` 下，不放仓库根或源码目录之外。

---

## 文件结构

| 文件 | 职责 | 动作 |
|------|------|------|
| `md-prd-to-html-prototype/SKILL.md` | 主干：触发、6 步工作流、决策门、reference 读取指引、校验命令 | 重写 |
| `md-prd-to-html-prototype/README.md` | 人读说明：能力、流程、目录、校验器用法 | 新建 |
| `md-prd-to-html-prototype/references/output-contract.md` | 目录/命名/index/状态文件契约 | 新建 |
| `md-prd-to-html-prototype/references/interaction-contract.md` | 离线 HTML 骨架 + 交互清单 + Mock 规范 + 移动端 | 新建 |
| `md-prd-to-html-prototype/references/intake-and-state.md` | 端识别问题、澄清标记、状态文件格式与读写规则 | 新建 |
| `md-prd-to-html-prototype/scripts/validate_prototype.py` | 纯标准库校验器 | 新建 |
| `md-prd-to-html-prototype/scripts/test_validate_prototype.py` | 校验器单测（unittest） | 新建 |
| `.workbuddy/skills/md-prd-to-html-prototype/SKILL.md` | 安装副本：保留叠加节，同步主干 | 修改 |
| `.workbuddy/skills/md-prd-to-html-prototype/` 其余文件 | 与 canonical 的 references/scripts/README 同步 | 新建 |
| `README.md` / `README.en.md` | 技能描述、安装位置、结构树条目 | 修改 |

---

## 任务 1：校验器 `validate_prototype.py` 的"用法与目录"层（TDD 起点）

**文件：**
- 创建：`md-prd-to-html-prototype/scripts/validate_prototype.py`
- 测试：`md-prd-to-html-prototype/scripts/test_validate_prototype.py`

- [ ] **步骤 1：编写失败测试（用法错误 + 缺状态文件 + 错误端目录）**

```python
# md-prd-to-html-prototype/scripts/test_validate_prototype.py
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
VALIDATOR = SCRIPTS / "validate_prototype.py"


def run_validator(root, *args):
    cmd = [sys.executable, str(VALIDATOR), str(root), *args]
    return subprocess.run(cmd, capture_output=True, text=True)


class ValidateCLIAndLayoutTest(unittest.TestCase):
    def test_missing_root_arg_exits_2(self):
        proc = subprocess.run([sys.executable, str(VALIDATOR)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("usage", (proc.stdout + proc.stderr).lower())

    def test_nonexistent_root_exits_2(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "nope"
            proc = run_validator(missing)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("not found", (proc.stdout + proc.stderr).lower())

    def test_missing_state_file_exits_1(self):
        with tempfile.TemporaryDirectory() as td:
            proc = run_validator(Path(td))
            self.assertEqual(proc.returncode, 1)
            self.assertIn("[ERROR]", proc.stdout)
            self.assertIn("_原型说明.md", proc.stdout)

    def test_unknown_side_dir_exits_1(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "_原型说明.md").write_text("# 状态\n", encoding="utf-8")
            (root / "mobile").mkdir()
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("mobile", proc.stdout)

    def test_clean_empty_root_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "_原型说明.md").write_text("# 状态\n", encoding="utf-8")
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 0, proc.stdout)
            self.assertIn("OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python md-prd-to-html-prototype/scripts/test_validate_prototype.py -v`
预期：全部 ERROR（模块 `validate_prototype` 不存在，`run_validator` 调用不存在的脚本 → 退出码非预期）。

- [ ] **步骤 3：实现 CLI 与目录层的校验器骨架**

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Validate md-prd-to-html-prototype output for offline + layout contracts."""

from __future__ import annotations

import argparse
import html.parser
import sys
from pathlib import Path

SIDES = {"www", "admin", "app"}


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

    if errors:
        for err in errors:
            print(f"[ERROR] {err}")
        return 1

    print(f"OK: layout checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python md-prd-to-html-prototype/scripts/test_validate_prototype.py -v`
预期：5 个测试全部 PASS。

- [ ] **步骤 5：Commit**

```bash
git add md-prd-to-html-prototype/scripts/
git commit -m "feat(md-prd-to-html-prototype): add validator CLI and layout checks"
```

---

## 任务 2：校验器 HTML 结构与离线约束层

**文件：**
- 修改：`md-prd-to-html-prototype/scripts/validate_prototype.py`
- 测试：`md-prd-to-html-prototype/scripts/test_validate_prototype.py`

- [ ] **步骤 1：编写失败测试（外链、缺 style/script、缺 DOCTYPE/lang/viewport/title）**

在测试类中加入：

```python
class ValidateHtmlOfflineTest(unittest.TestCase):
    def make_root(self, td, html_name="index.html"):
        root = Path(td)
        (root / "_原型说明.md").write_text("# 状态\n", encoding="utf-8")
        side = root / "www"
        side.mkdir(exist_ok=True)
        return root, side / html_name

    def test_cdn_link_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root, page = self.make_root(td)
            page.write_text(
                '<!DOCTYPE html><html lang="zh-CN"><head><meta name="viewport" '
                'content="width=device-width"><title>T</title>'
                '<link rel="stylesheet" href="https://cdn.example.com/a.css"></head>'
                '<body><style>body{}</style><script>const MOCK_x=[];</script></body></html>',
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("external", proc.stdout.lower())

    def test_external_script_src_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root, page = self.make_root(td)
            page.write_text(
                '<!DOCTYPE html><html lang="zh-CN"><head><meta name="viewport" '
                'content="width=device-width"><title>T</title></head><body>'
                '<style>body{}</style><script src="https://cdn.example.com/a.js"></script>'
                '</body></html>',
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("script", proc.stdout.lower())

    def test_missing_style_or_script_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root, page = self.make_root(td)
            page.write_text(
                '<!DOCTYPE html><html lang="zh-CN"><head><meta name="viewport" '
                'content="width=device-width"><title>T</title></head><body>hi</body></html>',
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("<style>", proc.stdout)
            self.assertIn("<script>", proc.stdout)

    def test_missing_doctype_lang_viewport_title_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root, page = self.make_root(td)
            page.write_text(
                "<html><head></head><body><style>body{}</style>"
                "<script>const MOCK_x=[];</script></body></html>",
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1, proc.stdout)
            for token in ["DOCTYPE", "lang", "viewport", "title"]:
                self.assertIn(token, proc.stdout)

    def test_inline_html_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root, page = self.make_root(td)
            page.write_text(
                '<!DOCTYPE html><html lang="zh-CN"><head><meta name="viewport" '
                'content="width=device-width"><title>T</title></head><body>'
                '<style>body{font-family:sans-serif}</style>'
                "<script>const MOCK_users=[{name:'张三'}];</script></body></html>",
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 0, proc.stdout)
```

- [ ] **步骤 2：运行测试验证新增测试失败**

运行：`python md-prd-to-html-prototype/scripts/test_validate_prototype.py -v`
预期：新增 5 个测试 FAIL（校验器尚未检查 HTML 内容）。

- [ ] **步骤 3：实现 HTML 结构与离线检查**

在 `validate_prototype.py` 中加入：

```python
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
```

在 `main()` 的目录检查之后、错误输出之前，加入：

```python
    html_files = sorted(p for p in root.rglob("*.html") if p.is_file())
    for page in html_files:
        rel = page.relative_to(root).as_posix()
        page_errors, _ = inspect_html(page)
        errors.extend(f"{rel}: {e}" for e in page_errors)
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python md-prd-to-html-prototype/scripts/test_validate_prototype.py -v`
预期：全部 10 个测试 PASS。

- [ ] **步骤 5：Commit**

```bash
git add md-prd-to-html-prototype/scripts/
git commit -m "feat(md-prd-to-html-prototype): validate offline HTML structure"
```

---

## 任务 3：校验器多页链接与交互标记层

**文件：**
- 修改：`md-prd-to-html-prototype/scripts/validate_prototype.py`
- 测试：`md-prd-to-html-prototype/scripts/test_validate_prototype.py`

- [ ] **步骤 1：编写失败测试（断链、缺 index、交互标记不足）**

```python
class ValidateMultiAndInteractionTest(unittest.TestCase):
    def build_page(self, side_dir, name, body):
        (side_dir / name).write_text(
            '<!DOCTYPE html><html lang="zh-CN"><head><meta name="viewport" '
            'content="width=device-width"><title>T</title></head><body>'
            '<style>body{}</style>' + body +
            "<script>const MOCK_users=[];</script></body></html>",
            encoding="utf-8",
        )

    def test_multi_mode_requires_index(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "_原型说明.md").write_text("# 状态\n", encoding="utf-8")
            side = root / "www"
            side.mkdir()
            self.build_page(side, "list.html", "<a href='list.html'>列表</a>")
            proc = run_validator(root, "--mode", "multi")
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("index.html", proc.stdout)

    def test_multi_mode_broken_href_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "_原型说明.md").write_text("# 状态\n", encoding="utf-8")
            side = root / "www"
            side.mkdir()
            self.build_page(side, "index.html", "<a href='missing.html'>详情</a>")
            proc = run_validator(root, "--mode", "multi")
            self.assertEqual(proc.returncode, 1, proc.stdout)
            self.assertIn("broken link", proc.stdout.lower())

    def test_missing_interaction_markers_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "_原型说明.md").write_text("# 状态\n", encoding="utf-8")
            side = root / "www"
            side.mkdir()
            self.build_page(side, "index.html", "<div>no interactions</div>")
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1, proc.stdout)
            for marker in ["modal", "filter", "toast", "required"]:
                self.assertIn(marker, proc.stdout.lower())

    def test_full_interaction_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "_原型说明.md").write_text("# 状态\n", encoding="utf-8")
            side = root / "www"
            side.mkdir()
            body = (
                "<button id='addBtn' onclick=\"openModal()\">新增</button>"
                "<div id='modal' class='modal hidden'></div>"
                "<input id='kw'><button onclick='filterRows()'>筛选</button>"
                "<button onclick='resetFilter()'>重置</button>"
                "<form><input name='x' required></form>"
                "<script>function openModal(){} function filterRows(){} "
                "function resetFilter(){} function toast(){}</script>"
            )
            self.build_page(side, "index.html", body)
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 0, proc.stdout)
```

- [ ] **步骤 2：运行测试验证新增测试失败**

运行：`python md-prd-to-html-prototype/scripts/test_validate_prototype.py -v`
预期：新增 4 个测试 FAIL。

- [ ] **步骤 3：实现多页链接与交互标记检查**

在 `PrototypeInspector` 中补充字段与解析：

```python
        self.local_hrefs: list[str] = []
        self.has_modal = False
        self.has_filter = False
        self.has_toast = False
        self.has_required = False
```

在 `handle_starttag` 中补充：

```python
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
```

在 `handle_data` 中补充：

```python
        low = data.lower()
        if "modal" in low:
            self.has_modal = True
        if "filter" in low or "resetfilter" in low:
            self.has_filter = True
        if "toast" in low:
            self.has_toast = True
        if "required" in low:
            self.has_required = True
```

在 `main()` 中补充多页与交互检查（替换原来的 HTML 检查循环）：

```python
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
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python md-prd-to-html-prototype/scripts/test_validate_prototype.py -v`
预期：全部 14 个测试 PASS。

- [ ] **步骤 5：Commit**

```bash
git add md-prd-to-html-prototype/scripts/
git commit -m "feat(md-prd-to-html-prototype): validate links and interaction markers"
```

---

## 任务 4：三份 references 规范文档

**文件：**
- 创建：`md-prd-to-html-prototype/references/output-contract.md`
- 创建：`md-prd-to-html-prototype/references/interaction-contract.md`
- 创建：`md-prd-to-html-prototype/references/intake-and-state.md`

- [ ] **步骤 1：编写 `output-contract.md`**

内容覆盖（每节给出明确规则，不留占位符）：
- 原型根目录由用户指定；三端子目录 `www/`/`admin/`/`app/` 固定命名；每次调用只写一个端。
- 单页模式：该端目录下 `index.html` 为唯一主文件，菜单切视图。
- 多页模式：该端目录下 `index.html` 为导航入口，`pages/<page-id>.html` 为每页文件，文件名用小写 kebab-case，页面间用相对 `href`。
- `_原型说明.md` 七个必含小节：系统名称与定位、目标角色、候选端与已生成端、页面清单（按端分组并标注模式）、数据字典与 Mock 约定、待确认业务点、生成历史。
- 状态文件读写规则：存在则先读；每次生成后追加生成历史条目（时间、端、模式、产出文件）。

- [ ] **步骤 2：编写 `interaction-contract.md`**

内容覆盖：
- 离线骨架：DOCTYPE、`lang="zh-CN"`、viewport、title、内联 `<style>`/`<script>`、Unicode/内联 SVG 图标、禁用 CDN/外链/外部字体图片。
- Mock 数据：`const MOCK_<实体名复数> = [...]` 命名；字段与 `_原型说明.md` 数据字典一致；值贴近业务。
- 七类交互逐条给出最小实现要求：导航（单页切视图 / 多页真实 href）、modal 开关、表格筛选+重置、表单必填校验、状态切换、列表增改删联动内存数据并刷新、提交 toast。
- 移动端额外：375px 居中手机壳、底部 Tab、卡片列表、同样离线。

- [ ] **步骤 3：编写 `intake-and-state.md`**

内容覆盖：
- 步骤 1 必问：本地 MD 路径 + 原型根目录路径；读全文；解析系统名/角色/页面/字段/按钮弹窗表格筛选/交互/非功能约束。
- 缺信息时输出 `[NEEDS CLARIFICATION: <具体问题>]` 清单并停止，不生成。
- 步骤 2 端识别：按角色/页面推断候选端；列出 `www`/`admin`/`app` 中相关项让用户勾选并指定本次先生成哪个；即使状态文件已有记录也要重新确认。
- 步骤 3 模式选择：单页 vs 多静态页，让用户二选一；解释差异。
- 状态文件模板（含七个小节的 Markdown 骨架示例）。

- [ ] **步骤 4：校验三份文档无占位符、规则不与规格冲突**

运行：`python -c "from pathlib import Path; files=list(Path('md-prd-to-html-prototype/references').glob('*.md')); [print(f.name, len(f.read_text(encoding='utf-8').splitlines()), 'lines') for f in files]"`

预期：输出三行，每份 > 30 行；人工确认无 "TODO/待定"。

- [ ] **步骤 5：Commit**

```bash
git add md-prd-to-html-prototype/references/
git commit -m "docs(md-prd-to-html-prototype): add output/interaction/intake contracts"
```

---

## 任务 5：重写 canonical `SKILL.md` 主干

**文件：**
- 重写：`md-prd-to-html-prototype/SKILL.md`

- [ ] **步骤 1：写入新 SKILL.md**

用 `write_to_file` 覆盖，内容为（保留 frontmatter 触发词，version 升到 2.0.0）：

```markdown
---
skill_name: MD‑PRD转HTML交互原型
version: 2.0.0
author: adapted from openpmkit‑prototype
description: 读取本地Markdown格式PRD/需求文档，分析角色与页面，让用户选择端（前台www/后台admin/移动app）与模式（单页/多静态页），生成完全离线的静态HTML交互原型；内联全部CSS/JS，双击浏览器即可打开评审。信息缺失主动提问，不编造业务字段。
triggers:
  - md生成html原型
  - 根据prd文档生成原型
  - 把需求文档转为html原型
tags:
  - prototype
  - prd
  - html
  - 产品原型
  - ui
---

# MD‑PRD转HTML交互原型 Skill

## 目标
读取用户指定的本地 `.md` 需求/PRD 文档，分析系统角色、页面与交互，让用户选择要生成的端与模式，生成**完全离线、可直接双击打开**的静态 HTML 交互原型，分端存放到用户指定原型根目录的 `www/`、`admin/`、`app/` 下。

> 重要约束
> 1. 每次调用只生成一个端；用户指定原型根目录，三端为其子目录。
> 2. 完全离线：CSS/JS 全部内联，禁止 CDN、外部字体/图片、`<script src>`、`<link rel=stylesheet>`。
> 3. 禁止脑补业务字段；信息不足输出 `[NEEDS CLARIFICATION]` 清单并停止生成。
> 4. 原型定位：需求评审低保真可交互原型，不是上线产品；Mock 交互，无真实后端。
> 5. 步骤 2（选端）与步骤 3（选模式）每次都必须问用户，状态文件不得跳过确认。

## 执行流程

### 步骤 1：确认输入
1. 询问并确认两个路径：本地 MD 路径（如 `./prd/报修系统需求.md`）与原型根目录（如 `./prototype/`）。
2. 读取 MD 全文，解析：系统名称、目标角色、页面清单、字段（输入框/下拉/日期/表格列/按钮）、交互（新增/编辑/删除/筛选/弹窗/状态切换）、非功能约束。
3. 若页面或字段缺失 → 输出 `[NEEDS CLARIFICATION]` 清单并停止，不生成。
4. 读取 `references/intake-and-state.md` 获取问题清单模板与状态文件格式。

### 步骤 2：分析候选端（决策门①）
1. 按角色与页面判断 `www`（前台/C 端）、`admin`（后台管理）、`app`（移动端）哪些相关。
2. 列出候选端让用户勾选，并指定本次先生成哪个端。
3. 即使状态文件已记录历史端，本次仍必须确认。

### 步骤 3：选择模式（决策门②）
让用户二选一：
- **单页**：一个 HTML 含全部视图，菜单切换；输出到该端 `index.html`。
- **多静态页**：每页一个 HTML，`index.html` 为导航入口，真实 `href` 跳转。

### 步骤 4：读取/建立状态
1. 若 `<原型根>/_原型说明.md` 存在 → 读取，复用系统名、数据字典、Mock 约定。
2. 否则按 `references/intake-and-state.md` 的模板新建。
3. 读取 `references/output-contract.md` 获取目录与命名规则。

### 步骤 5：生成
1. 只在用户本次选中的端目录下产出 HTML；不碰其他端目录。
2. 读取 `references/interaction-contract.md`，满足离线骨架、Mock 数据与七类交互。
3. 更新 `_原型说明.md`：登记本次生成端、模式、页面清单，追加生成历史。
4. **必须调用写文件指令写入本地 HTML**，不要只在回复里贴代码块。

### 步骤 6：自检与交付
1. 运行校验：
   ```sh
   python <技能目录>/scripts/validate_prototype.py <原型根> --expect-side <www|admin|app> --mode <single|multi>
   ```
2. 若退出码非 0 → 按 `[ERROR]` 逐条修正后重跑，直到通过。
3. 输出摘要：原型文件路径、本次生成端、页面清单、已实现交互、待确认业务点。
4. 告知用户可继续生成其他端：再次执行本技能并选择另一个端即可续写。

## 禁止行为
1. 不要只输出 markdown 代码块而不写文件。
2. 不要使用任何 CDN 或外部资源；不要拆出本地 css/js 文件。
3. 不要编造业务字段或跳过选端/选模式确认。
4. 不要做高保真美工；保持适合需求评审的低保真原型。
5. 不要实现真实后端逻辑，仅做前端 Mock 交互。
```

- [ ] **步骤 2：校验 SKILL.md 结构**

运行：`python -c "from pathlib import Path; t=Path('md-prd-to-html-prototype/SKILL.md').read_text(encoding='utf-8'); print('lines',len(t.splitlines())); print('steps',t.count('### 步骤')); print('refs',t.count('references/'))"`

预期：行数 60-100；steps = 6；refs ≥ 3。

- [ ] **步骤 3：Commit**

```bash
git add md-prd-to-html-prototype/SKILL.md
git commit -m "feat(md-prd-to-html-prototype): rewrite SKILL.md for multi-side multi-page flow"
```

---

## 任务 6：README 与 `.workbuddy` 副本同步

**文件：**
- 创建：`md-prd-to-html-prototype/README.md`
- 修改：`.workbuddy/skills/md-prd-to-html-prototype/SKILL.md`
- 创建：`.workbuddy/skills/md-prd-to-html-prototype/README.md`
- 复制：references/ 与 scripts/ 到 `.workbuddy` 副本
- 修改：`README.md`、`README.en.md`

- [ ] **步骤 1：编写 canonical README.md**

内容覆盖：技能定位、6 步流程、三端目录结构、单页/多页差异、离线约束、校验器命令、状态文件作用、迭代方式、安装位置（根目录 + `.workbuddy` 副本）。

- [ ] **步骤 2：同步 `.workbuddy` 副本**

用 Python 脚本执行：
- 把 canonical `SKILL.md` 前全部内容写入 `.workbuddy/skills/md-prd-to-html-prototype/SKILL.md`
- 追加改造后的叠加节（把原文"单文件"改为"单端单页/多页"表述，保留 mwg.py 命令与"不改离线/内联约束"）：

```markdown
## 与 modern-web-guidance 叠加

每次只生成一个端、CSS/JS 全部内联、低保真评审这些约束保持不变。写弹窗、表单、表格、键盘操作前，先查阅仓库根目录的 `modern-web-guidance`，再把行为内联进同一个 HTML；不要因为指南拆出外部 css/js，也不要编造业务字段。

```sh
python modern-web-guidance/resources/tools/mwg.py search "<2-5 词的单一 UI 能力>"
python modern-web-guidance/resources/tools/mwg.py retrieve "<id>"
```

没有这类界面任务时不要调用它。用法见仓库 `.docs/使用modern-web-guidance技能编写现代Web前端指南.md` 第 14 节。
```

- `shutil.copytree` 同步 `references/`、`scripts/`；`shutil.copy2` 同步 `README.md`。

- [ ] **步骤 3：更新根 README.md / README.en.md**

中文版 §8（约 101-107 行）：
- 描述改为多端多页离线原型生成（保留"完全独立单文件"相关表述仅在说明单页模式时）。
- 安装位置改为两处：`md-prd-to-html-prototype/`（canonical）与 `.workbuddy/skills/md-prd-to-html-prototype/`。
- 结构树条目（约 325 行）：从只看 `.workbuddy` 路径改为同时体现根目录技能目录和 `.workbuddy` 安装副本。

英文版 §8（约 97-102 行）与结构树（约 264 行）做对应英文更新。

- [ ] **步骤 4：验证两副本内容一致性**

```bash
python -c "from pathlib import Path; a=Path('md-prd-to-html-prototype'); b=Path('.workbuddy/skills/md-prd-to-html-prototype'); print(sorted(p.name for p in a.rglob('*') if p.is_file())); print(sorted(p.name for p in b.rglob('*') if p.is_file()))"
```

预期：两份文件名集合一致（`SKILL.md` 内容允许叠加节差异）。

- [ ] **步骤 5：Commit**

```bash
git add md-prd-to-html-prototype/ .workbuddy/skills/md-prd-to-html-prototype/ README.md README.en.md
git commit -m "docs(md-prd-to-html-prototype): add README and sync workbuddy copy"
```

---

## 任务 7：端到端样例验证

**文件：**
- 临时样例在 `tempfile.TemporaryDirectory()` 中生成，不写入仓库。

- [ ] **步骤 1：编写端到端验证脚本（临时，运行后删除）**

在系统 Temp 目录写脚本，逻辑：
1. 用 `tempfile.TemporaryDirectory()` 造一个 `sample.md`（含一个系统、两个角色、3 个页面、字段与交互描述）。
2. 手工按新规范生成 `www/` 单页样例：含 `_原型说明.md`（七小节）、`www/index.html`（DOCTYPE/lang/viewport/title、内联 style/script、MOCK_users、modal/filter/toast/required）。
3. 调用校验器 `run_validator(root, "--expect-side", "www", "--mode", "single")` 断言退出码 0。
4. 再生成 `admin/` 多页样例：`index.html` + `pages/user-list.html`，href 互相可达，断言 `--mode multi` 退出码 0。
5. 把一个 href 改成断链、把一个 `<style>` 换成 `<link rel=stylesheet>`，断言退出码 1 且错误文本包含 broken link / external。

- [ ] **步骤 2：运行端到端验证**

运行：`python <temp>/e2e_validate.py`
预期：单页 PASS、多页 PASS、两类故障均被正确拒绝（exit 1）。

- [ ] **步骤 3：运行完整单测**

运行：`python md-prd-to-html-prototype/scripts/test_validate_prototype.py -v`
预期：全部 14 个测试 PASS。

- [ ] **步骤 4：清理临时文件**

确认系统 Temp 中的脚本与样例已被 `TemporaryDirectory` 自动清理；仓库内无新增临时文件。运行 `git status --short` 确认工作区只有预期改动。

---

## 自检记录（编写计划后执行）

- **规格覆盖度：** 规格 §1-§8 的需求分别落在任务 5（§1/§2）、任务 4（§2/§3/§4/§5）、任务 1-3（§6）、任务 7（§7）、任务 6（副本与 README 同步）。无遗漏。
- **占位符扫描：** 全计划无 "TODO/待定/后续实现/补充细节"。无 "类似任务 N"。每个代码步骤均含具体代码。
- **类型一致性：** `validate_prototype.py` 的函数名 `main`、`inspect_html`、类 `PrototypeInspector` 及各布尔字段在任务 1-3 中命名一致；CLI 参数 `root`、`--expect-side`、`--mode` 在测试与实现中一致。
