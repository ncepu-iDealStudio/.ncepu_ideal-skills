"""Tests for the local read-only HTTP probe; no project or database required."""
import contextlib
import io
import json
import os
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import http_auth_probe as probe


class Handler(BaseHTTPRequestHandler):
    login_count = 0
    redirect_followed = 0

    def log_message(self, *_args):
        pass

    def reply(self, code, value):
        raw = json.dumps(value).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        if self.path != "/login":
            self.reply(404, {"code": 404})
            return
        type(self).login_count += 1
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if data == {"account": "example-user", "password": "example-password"}:
            self.reply(200, {"data": {"access_token": "example-token"}})
        else:
            self.reply(401, {"code": 401})

    def do_GET(self):
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/must-not-follow")
            self.end_headers()
        elif self.path == "/must-not-follow":
            type(self).redirect_followed += 1
            self.reply(200, {"code": 200})
        elif self.path == "/server-error":
            self.reply(500, {"code": 500})
        elif self.path == "/leak":
            self.reply(200, {"code": 200, "nested": {"password": "test-secret"}})
        elif self.headers.get("Authorization") == "Bearer example-token":
            self.reply(200, {"code": 200, "data": {"id": 1}})
        else:
            self.reply(401, {"code": 401})


class HttpProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def config(self):
        return {"base_url": f"http://localhost:{self.server.server_port}",
                "login": {"path": "/login", "format": "json", "account_field": "account",
                          "password_field": "password", "token_path": "data.access_token"},
                "identities": {"alice": {"account_env": "PROBE_TEST_USER", "password_env": "PROBE_TEST_PASSWORD"}},
                "cases": [
                    {"name": "anonymous", "method": "GET", "path": "/resource", "identity": "anonymous",
                     "expect": {"status": 401, "json_equals": {"code": 401}, "forbidden_fields": ["password"]}},
                    {"name": "invalid", "method": "GET", "path": "/resource", "identity": "invalid",
                     "expect": {"status": 401, "json_equals": {"code": 401}, "forbidden_fields": ["password"]}},
                    {"name": "authorized", "method": "GET", "path": "/resource", "identity": "alice",
                     "expect": {"status": 200, "json_equals": {"code": 200, "data.id": 1}, "forbidden_fields": ["password"]}}]}

    def run_probe(self, cfg):
        out = io.StringIO()
        with patch.dict(os.environ, {"PROBE_TEST_USER": "example-user", "PROBE_TEST_PASSWORD": "example-password"}):
            with contextlib.redirect_stdout(out):
                result = probe.run(cfg)
        return result, out.getvalue()

    def test_login_and_positive_negative_controls_do_not_echo_secrets(self):
        result, out = self.run_probe(self.config())
        self.assertEqual(result, 0)
        self.assertIn("3 passed, 0 failed", out)
        for secret in ("example-token", "example-user", "example-password"):
            self.assertNotIn(secret, out)

    def test_rejects_empty_cases_external_hosts_writes_and_no_assertions(self):
        cfg = self.config()
        cfg["cases"] = []
        with self.assertRaises(probe.ProbeError):
            self.run_probe(cfg)
        cfg = self.config()
        cfg["base_url"] = "http://example.com"
        with self.assertRaises(probe.ProbeError):
            self.run_probe(cfg)
        cfg = self.config()
        cfg["cases"][0]["method"] = "POST"
        with self.assertRaises(probe.ProbeError):
            self.run_probe(cfg)
        cfg = self.config()
        cfg["cases"][0]["expect"]["json_equals"] = {}
        with self.assertRaises(probe.ProbeError):
            self.run_probe(cfg)
        cfg = self.config()
        cfg["cases"][0]["expect"]["status"] = 500
        with self.assertRaises(probe.ProbeError):
            self.run_probe(cfg)

    def test_error_leak_and_redirect_never_pass(self):
        for path, status, code in [("/server-error", 401, 401), ("/leak", 200, 200), ("/redirect", 200, 200)]:
            cfg = self.config()
            cfg["cases"] = [{"name": "negative", "method": "GET", "path": path, "identity": "anonymous",
                             "expect": {"status": status, "json_equals": {"code": code}, "forbidden_fields": ["password"]}}]
            result, out = self.run_probe(cfg)
            self.assertEqual(result, 1)
            self.assertIn("FAIL negative", out)
            self.assertNotIn("test-secret", out)
        self.assertEqual(Handler.redirect_followed, 0)


if __name__ == "__main__":
    unittest.main()
