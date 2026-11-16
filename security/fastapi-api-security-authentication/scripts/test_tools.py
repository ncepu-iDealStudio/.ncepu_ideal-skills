"""Self-contained CLI tests; temporary fixtures only, no application or database."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class ToolTests(unittest.TestCase):
    def setUp(self):
        # Keep test fixtures in this writable skill directory on restricted hosts.
        self.tmp = tempfile.TemporaryDirectory(dir=HERE)
        self.root = Path(self.tmp.name)
        self.addCleanup(self.cleanup_fixture)

    def cleanup_fixture(self):
        # Check the resolved target before TemporaryDirectory recursively removes it.
        if self.root.resolve().parent != HERE.resolve():
            raise RuntimeError("Refusing to remove a fixture outside the scripts directory")
        self.tmp.cleanup()

    def write_json(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def run_tool(self, name, *args):
        return subprocess.run(
            [sys.executable, str(HERE / name), *(str(arg) for arg in args)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_openapi_inventory_and_warning(self):
        spec = self.write_json("openapi.json", {"paths": {
            "/x": {"get": {}, "post": {}, "parameters": []}, "/x/": {"head": {}}
        }})
        out = self.root / "inventory.json"
        result = self.run_tool("route_inventory.py", spec, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(out.read_text(encoding="utf-8")), {"routes": [
            {"method": "GET", "path": "/x"}, {"method": "POST", "path": "/x"},
            {"method": "HEAD", "path": "/x/"},
        ]})
        self.assertIn("遗漏", result.stderr)

    def test_openapi_rejects_invalid_and_unresolved_ref(self):
        for value in ({}, {"paths": {"/x": {"$ref": "#/components/x"}}},
                      {"paths": {"/x": {"get": "invalid"}}}, {"paths": {}}):
            with self.subTest(value=value):
                spec = self.write_json("bad.json", value)
                self.assertNotEqual(self.run_tool("route_inventory.py", spec).returncode, 0)

    def test_policy_coverage_valid_and_missing(self):
        inv = self.write_json("inv.json", {"routes": [
            {"method": "GET", "path": "/x"}, {"method": "POST", "path": "/login"}
        ]})
        rules = [
            {"method": "GET", "path": "/x", "access": "protected", "roles": ["student"],
             "object_scope": "own", "fields": "public fields only"},
            {"method": "POST", "path": "/login", "access": "public"},
        ]
        policy = self.write_json("policy.json", {"rules": rules})
        self.assertEqual(self.run_tool("check_policy_coverage.py", inv, policy).returncode, 0)
        policy = self.write_json("policy.json", {"rules": rules[:1]})
        result = self.run_tool("check_policy_coverage.py", inv, policy)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少策略", result.stderr)

    def test_policy_detects_duplicates_extra_and_missing_properties(self):
        route = {"method": "GET", "path": "/x"}
        inv = self.write_json("inv.json", {"routes": [route, route]})
        rule = {"method": "GET", "path": "/x", "access": "protected", "roles": [],
                "object_scope": "", "fields": ""}
        policy = self.write_json("policy.json", {"rules": [rule, rule,
                                  {"method": "GET", "path": "/x/", "access": "public"}]})
        result = self.run_tool("check_policy_coverage.py", inv, policy)
        self.assertNotEqual(result.returncode, 0)
        for expected in ("重复库存路由", "重复策略规则", "roles", "object_scope", "fields", "库存中不存在"):
            self.assertIn(expected, result.stderr)

    def test_invalid_json_and_duplicate_keys_fail(self):
        bad = self.root / "bad.json"
        bad.write_text('{"paths":{},"paths":{}}', encoding="utf-8")
        self.assertNotEqual(self.run_tool("route_inventory.py", bad).returncode, 0)
        empty = self.write_json("empty.json", {"routes": []})
        policy = self.write_json("policy.json", {"rules": []})
        self.assertNotEqual(self.run_tool("check_policy_coverage.py", empty, policy).returncode, 0)
        invalid = self.write_json("invalid.json", {"routes": [{"method": "get", "path": "/x"}]})
        self.assertNotEqual(self.run_tool("check_policy_coverage.py", invalid, policy).returncode, 0)

    def test_preflight_finds_account_table_without_login(self):
        models = self.root / "models"
        models.mkdir()
        (models / "sso_user.py").write_text(
            "class SsoUser:\n"
            "    __tablename__ = 'sso_user'\n"
            "    account = Column('account', String(255))\n"
            "    password = Column('password', String(255))\n"
            "    user_type = Column('userType', Integer)\n",
            encoding="utf-8",
        )
        (self.root / "service").mkdir()
        (self.root / "service" / "sso_user_service.py").write_text(
            "class SsoUserService:\n    async def get_list(self):\n        return []\n",
            encoding="utf-8",
        )
        (self.root / "api").mkdir()
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["account_tables"][0]["table"], "sso_user")
        self.assertIn("password", report["account_tables"][0]["password_fields"])
        self.assertEqual(report["login_service"], [])
        self.assertEqual(report["login_http"], [])
        self.assertEqual(report["role_signals"][0]["field"].lower().replace("_", ""), "usertype")

    def test_preflight_detects_login_route_and_service(self):
        (self.root / "service").mkdir()
        (self.root / "service" / "sso_user_service.py").write_text(
            "class SsoUserService:\n    async def login(self, account, password):\n        return {}\n",
            encoding="utf-8",
        )
        api = self.root / "api" / "v1" / "sso_user"
        api.mkdir(parents=True)
        (api / "sso_userResource.py").write_text(
            "router = APIRouter(prefix='/sso-user')\n"
            "@router.post('/login')\n"
            "async def login_sso_user():\n    return {}\n",
            encoding="utf-8",
        )
        (self.root / "core").mkdir()
        (self.root / "core" / "security.py").write_text(
            "def create_access_token(data):\n    return 'jwt'\n",
            encoding="utf-8",
        )
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["login_service"][0]["function"], "login")
        self.assertEqual(report["login_http"][0]["path_hint"], "/sso-user/login")
        self.assertTrue(any("security.py" in f for f in report["token_hints"]["files_with_jwt_or_bearer"]))

    def test_protected_rules_cannot_use_placeholder_values(self):
        inv = self.write_json("inv.json", {"routes": [{"method": "GET", "path": "/x"}]})
        for placeholder in ("待定", "未决", " TODO ", "tBd", " 未确认 ", " UnKnOwN "):
            with self.subTest(placeholder=placeholder):
                policy = self.write_json("policy.json", {"rules": [{
                    "method": "GET", "path": "/x", "access": "protected",
                    "roles": ["admin", placeholder], "object_scope": placeholder,
                    "fields": placeholder,
                }]})
                result = self.run_tool("check_policy_coverage.py", inv, policy)
                self.assertNotEqual(result.returncode, 0)
                for field in ("roles", "object_scope", "fields"):
                    self.assertIn(field, result.stderr)


if __name__ == "__main__":
    unittest.main()
