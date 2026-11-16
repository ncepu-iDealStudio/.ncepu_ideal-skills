"""CLI tests for scan_sinks. Fixtures live under this directory and are removed."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class ScanSinksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=HERE)
        self.root = Path(self.tmp.name)
        self.addCleanup(self.cleanup_fixture)

    def cleanup_fixture(self):
        if self.root.resolve().parent != HERE.resolve():
            raise RuntimeError("Refusing to remove a fixture outside the scripts directory")
        self.tmp.cleanup()

    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "scan_sinks.py"), *(str(arg) for arg in args)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_flags_candidates_and_redacts_literals(self):
        body = "\n".join(
            [
                "import subprocess, pickle, requests",
                "subprocess.run(cmd, shell=" + "True)",
                "pickle." + "loads(blob)",
                "requests.get(url, verify=" + "False)",
                "password = \"" + ("x" * 12) + "\"",
            ]
        )
        (self.root / "app.py").write_text(body, encoding="utf-8")
        (self.root / ".env").write_text("TOKEN=" + ("y" * 12), encoding="utf-8")
        skipped = self.root / "node_modules"
        skipped.mkdir()
        (skipped / "lib.py").write_text("subprocess.run(cmd, shell=" + "True)\n", encoding="utf-8")

        result = self.run_tool(self.root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        findings = json.loads(result.stdout)
        rules = {item["rule"] for item in findings}
        self.assertEqual(
            rules,
            {"python-shell-true", "python-pickle", "tls-verify-disabled", "hardcoded-secret", "secret-file"},
        )
        self.assertNotIn("node_modules", result.stdout)
        self.assertNotIn("x" * 12, result.stdout)
        self.assertNotIn("y" * 12, result.stdout)
        secret = next(item for item in findings if item["rule"] == "hardcoded-secret")
        self.assertIn("***", secret["snippet"])
        env = next(item for item in findings if item["rule"] == "secret-file")
        self.assertEqual(env["snippet"], "(file not read)")

    def test_clean_tree_has_no_findings(self):
        (self.root / "ok.py").write_text("subprocess.run(['ls'], shell=False)\n", encoding="utf-8")
        result = self.run_tool(self.root, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])

    def test_missing_target_exits_2(self):
        result = self.run_tool(self.root / "missing")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
