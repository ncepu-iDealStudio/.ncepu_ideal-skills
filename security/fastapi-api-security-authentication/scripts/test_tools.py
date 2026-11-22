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

    def test_preflight_detects_initial_admin_seed(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        (scripts / "seed_admin.py").write_text(
            "from utils.security import SecurityUtil\n", encoding="utf-8"
        )
        (self.root / ".env.example").write_text(
            "INITIAL_ADMIN_USERNAME=\nINITIAL_ADMIN_PASSWORD=\n", encoding="utf-8"
        )
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        files = [item["file"] for item in report["initial_admin"]["seed_candidates"]]
        self.assertIn("scripts/seed_admin.py", files)
        self.assertIn("INITIAL_ADMIN_USERNAME", report["initial_admin"]["env_keys"])
        self.assertIn("INITIAL_ADMIN_PASSWORD", report["initial_admin"]["env_keys"])

    def test_preflight_reports_missing_initial_admin(self):
        (self.root / "service").mkdir()
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["initial_admin"]["seed_candidates"], [])
        self.assertEqual(report["initial_admin"]["env_keys"], [])

    def test_preflight_detects_token_lifecycle(self):
        models = self.root / "models"
        models.mkdir()
        (models / "app_user.py").write_text(
            "class AppUser:\n"
            "    __tablename__ = 'app_user'\n"
            "    username = Column('username', String(50))\n"
            "    password_hash = Column('password_hash', String(255))\n",
            encoding="utf-8",
        )
        (models / "session_record.py").write_text(
            "class SessionRecord:\n"
            "    __tablename__ = 'session_record'\n"
            "    refresh_token_hash = Column('refresh_token_hash', String(64))\n"
            "    revoked_at = Column('revoked_at', DateTime)\n"
            "    idle_expires_at = Column('idle_expires_at', DateTime)\n"
            "    device_name = Column('device_name', String(100))\n",
            encoding="utf-8",
        )
        (models / "reset_record.py").write_text(
            "class ResetRecord:\n"
            "    __tablename__ = 'reset_record'\n"
            "    token_hash = Column('token_hash', String(64))\n"
            "    used_at = Column('used_at', DateTime)\n"
            "    expires_at = Column('expires_at', DateTime)\n",
            encoding="utf-8",
        )
        api = self.root / "api"
        api.mkdir()
        (api / "auth.py").write_text(
            "router = APIRouter(prefix='/auth')\n"
            "@router.post('/refresh')\n"
            "async def refresh():\n    return {}\n"
            "@router.post('/logout')\n"
            "async def logout():\n    return {}\n"
            "@router.post('/password/reset')\n"
            "async def reset():\n    return {}\n",
            encoding="utf-8",
        )
        (api / "cookie.py").write_text(
            "def attach(response):\n"
            "    response.set_cookie('r', 'x', httponly=True, samesite='lax')\n",
            encoding="utf-8",
        )
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        life = json.loads(out.read_text(encoding="utf-8"))["token_lifecycle"]

        session_tables = [item["table"] for item in life["session_tables"]]
        reset_tables = [item["table"] for item in life["reset_token_tables"]]
        self.assertIn("session_record", session_tables)
        self.assertIn("reset_record", reset_tables)
        self.assertNotIn("app_user", session_tables)

        self.assertIn("/auth/refresh", [r["path_hint"] for r in life["refresh_endpoints"]])
        self.assertIn("/auth/logout", [r["path_hint"] for r in life["logout_endpoints"]])
        self.assertIn(
            "/auth/password/reset", [r["path_hint"] for r in life["reset_endpoints"]]
        )
        self.assertIn("api/cookie.py", life["cookie_files"])

    def test_preflight_reports_missing_lifecycle(self):
        models = self.root / "models"
        models.mkdir()
        (models / "app_user.py").write_text(
            "class AppUser:\n"
            "    __tablename__ = 'app_user'\n"
            "    username = Column('username', String(50))\n"
            "    password_hash = Column('password_hash', String(255))\n",
            encoding="utf-8",
        )
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        life = json.loads(out.read_text(encoding="utf-8"))["token_lifecycle"]
        self.assertEqual(life["session_tables"], [])
        self.assertEqual(life["reset_token_tables"], [])
        self.assertEqual(life["refresh_endpoints"], [])

    def test_preflight_reports_cookie_contract_signals(self):
        schemas = self.root / "schemas"
        schemas.mkdir()
        (schemas / "auth.py").write_text(
            "class TokenResponse(BaseModel):\n"
            "    access_token: str\n"
            "    refresh_token: str\n"
            "\n"
            "class LoginRequest(BaseModel):\n"
            "    username: str\n"
            "    device_name: str | None = None\n",
            encoding="utf-8",
        )
        api = self.root / "api"
        api.mkdir()
        (api / "auth.py").write_text(
            "def login(response):\n"
            "    response.set_cookie('refresh_token', 'x', httponly=True)\n"
            "\n"
            "async def refresh(refresh_token: str = Cookie(default=None)):\n"
            "    return {}\n",
            encoding="utf-8",
        )
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        life = json.loads(out.read_text(encoding="utf-8"))["token_lifecycle"]

        self.assertIn("api/auth.py", life["set_cookie_files"])
        self.assertIn("api/auth.py", life["cookie_param_files"])
        classes = {
            (item["class"], tuple(item["fields"]))
            for item in life["credential_body_fields"]
        }
        self.assertIn(("TokenResponse", ("refresh_token",)), classes)
        self.assertIn(("LoginRequest", ("device_name",)), classes)

    def test_preflight_detects_authorization_profiles(self):
        models = self.root / "models"
        models.mkdir()
        (models / "app_user.py").write_text(
            "class AppUser:\n"
            "    __tablename__ = 'app_user'\n"
            "    username = Column('username', String(50))\n"
            "    password_hash = Column('password_hash', String(255))\n",
            encoding="utf-8",
        )
        (models / "document.py").write_text(
            "class Document:\n"
            "    __tablename__ = 'document'\n"
            "    document_id = Column('document_id', BigInteger, primary_key=True)\n"
            "    owner_user_id = Column('owner_user_id', BigInteger)\n"
            "    tenant_id = Column('tenant_id', BigInteger)\n"
            "    status = Column('status', Integer)\n",
            encoding="utf-8",
        )
        (models / "resource_grant.py").write_text(
            "class ResourceGrant:\n"
            "    __tablename__ = 'resource_grant'\n"
            "    resource_grant_id = Column('resource_grant_id', BigInteger)\n"
            "    grantee_user_id = Column('grantee_user_id', BigInteger)\n"
            "    can_view = Column('can_view', Boolean)\n"
            "    can_edit = Column('can_edit', Boolean)\n",
            encoding="utf-8",
        )
        (models / "field_policy.py").write_text(
            "class FieldPolicy:\n"
            "    __tablename__ = 'field_policy'\n"
            "    field_policy_id = Column('field_policy_id', BigInteger)\n"
            "    field_code = Column('field_code', String(64))\n"
            "    access_mode = Column('access_mode', Integer)\n"
            "    mask_pattern = Column('mask_pattern', String(100))\n",
            encoding="utf-8",
        )
        (models / "access_request.py").write_text(
            "class AccessRequest:\n"
            "    __tablename__ = 'access_request'\n"
            "    access_request_id = Column('access_request_id', BigInteger)\n"
            "    applicant_user_id = Column('applicant_user_id', BigInteger)\n"
            "    status = Column('status', Integer)\n",
            encoding="utf-8",
        )
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))

        ids = {item["id"] for item in report["authorization_profiles"]}
        for expected in (
            "object_ownership",
            "tenant_isolation",
            "acl_grant",
            "field_level",
            "approval_temp_grant",
        ):
            self.assertIn(expected, ids)
        self.assertNotIn("sod", ids)

        by_table = {row["table"]: row for row in report["scope_fields"]}
        self.assertIn("owner_user_id", by_table["document"]["ownership"])
        self.assertIn("tenant_id", by_table["document"]["tenant"])
        self.assertIn("status", by_table["document"]["role_status"])

    def test_preflight_detects_sql_authorization_profiles(self):
        database = self.root / "database"
        database.mkdir()
        (database / "schema.sql").write_text(
            "CREATE TABLE org_unit (\n"
            "  org_unit_id BIGINT UNSIGNED NOT NULL,\n"
            "  parent_org_unit_id BIGINT UNSIGNED NULL,\n"
            "  org_type TINYINT UNSIGNED NOT NULL\n"
            ");\n"
            "CREATE TABLE document (\n"
            "  document_id BIGINT UNSIGNED NOT NULL,\n"
            "  org_unit_id BIGINT UNSIGNED NOT NULL,\n"
            "  status TINYINT UNSIGNED NOT NULL\n"
            ");\n",
            encoding="utf-8",
        )
        out = self.root / "preflight.json"
        result = self.run_tool("preflight_auth.py", self.root, "-o", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(out.read_text(encoding="utf-8"))
        ids = {item["id"] for item in report["authorization_profiles"]}
        self.assertIn("org_scope", ids)

    def test_endpoint_surface_valid_plan(self):
        inv = self.write_json("inv.json", {"routes": [{"method": "GET", "path": "/x"}]})
        plan = self.write_json("surface.json", {"routes": [
            {"method": "GET", "path": "/x", "action": "keep", "reason": "查看详情"},
            {"method": "DELETE", "path": "/x", "action": "remove", "reason": "改用状态禁用"},
        ]})
        result = self.run_tool("check_endpoint_surface.py", inv, plan)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("保留 1 个", result.stdout)

    def test_endpoint_surface_detects_leftover_removed_route(self):
        inv = self.write_json("inv.json", {"routes": [
            {"method": "GET", "path": "/x"}, {"method": "DELETE", "path": "/x"}
        ]})
        plan = self.write_json("surface.json", {"routes": [
            {"method": "GET", "path": "/x", "action": "keep", "reason": "查看详情"},
            {"method": "DELETE", "path": "/x", "action": "remove", "reason": "审计不可删除"},
        ]})
        result = self.run_tool("check_endpoint_surface.py", inv, plan)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("仍注册", result.stderr)

    def test_endpoint_surface_detects_missing_and_placeholder(self):
        inv = self.write_json("inv.json", {"routes": [
            {"method": "GET", "path": "/x"}, {"method": "POST", "path": "/y"}
        ]})
        plan = self.write_json("surface.json", {"routes": [
            {"method": "GET", "path": "/x", "action": "keep", "reason": "查看详情"},
            {"method": "GET", "path": "/z", "action": "keep", "reason": "待定"},
        ]})
        result = self.run_tool("check_endpoint_surface.py", inv, plan)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少处置", result.stderr)
        self.assertIn("未注册", result.stderr)
        self.assertIn("reason", result.stderr)

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
