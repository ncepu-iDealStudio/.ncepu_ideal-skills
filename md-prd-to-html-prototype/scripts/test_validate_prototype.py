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
                "<button id='addBtn' onclick='openModal()'>新增</button>"
                "<div id='modal' class='modal hidden'></div>"
                "<input id='kw'><button onclick='filterRows()'>筛选</button>"
                "<button onclick='resetFilter()'>重置</button>"
                "<form><input name='x' required></form>"
                "<script>const MOCK_users=[{name:'张三'}]; "
                "function openModal(){} function filterRows(){} "
                "function resetFilter(){} function toast(){}</script></body></html>",
                encoding="utf-8",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 0, proc.stdout)


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


if __name__ == "__main__":
    unittest.main()
