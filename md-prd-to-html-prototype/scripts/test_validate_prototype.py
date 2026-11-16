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
