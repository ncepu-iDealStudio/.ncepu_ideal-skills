#!/usr/bin/env python3
"""Run a narrow, read-only HTTP authentication probe against an explicit local API.

Usage: python http_auth_probe.py cases.json

JSON structure (the credentials are environment variable *names*, never values):
  {"base_url":"http://127.0.0.1:8000",
   "login":{"path":"/api/v1/login", "format":"json",
            "account_field":"account", "password_field":"password",
            "token_path":"data.access_token"},
   "identities":{"student":{"account_env":"TEST_USER", "password_env":"TEST_PASS"}},
   "cases":[{"name":"anonymous-student", "method":"GET", "path":"/api/v1/student",
             "identity":"anonymous", "expect":{"status":401,
              "json_equals":{"code":401}, "forbidden_fields":["password"]}}]}

login and identities are optional unless a case names a login identity. Each
case must have an explicit HTTP status, at least one JSON value assertion and
at least one forbidden response-field name. Case statuses can be 2xx, 401 or
403; 404-based object hiding must be tested by the project's own tests with a
known-existing-object control. This tool cannot establish full route coverage,
object ownership, data isolation, or absence of database side effects.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

MAX_RESPONSE = 1024 * 1024
READ_METHODS = {"GET", "HEAD", "OPTIONS"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")


class ProbeError(Exception):
    """A safe-to-display validation or request failure."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProbeError("redirect rejected")


def safe_origin(value: Any) -> str:
    if not isinstance(value, str):
        raise ProbeError("base_url must be a local HTTP origin")
    try:
        u = urllib.parse.urlsplit(value)
        host = u.hostname
        port = u.port
    except ValueError as exc:
        raise ProbeError("invalid base_url") from exc
    if (u.scheme not in ("http", "https") or not host or u.username or u.password
            or u.path not in ("", "/") or u.query or u.fragment):
        raise ProbeError("base_url must be a local HTTP origin")
    if host.lower() == "localhost":
        host = "127.0.0.1"  # Avoid DNS resolution and rebinding.
    else:
        try:
            ip = ipaddress.ip_address(host)
        except ValueError as exc:
            raise ProbeError("base_url host must be 127.0.0.1, localhost or ::1") from exc
        if ip not in (ipaddress.ip_address("127.0.0.1"), ipaddress.ip_address("::1")):
            raise ProbeError("base_url host must be 127.0.0.1, localhost or ::1")
        host = f"[{ip}]" if ip.version == 6 else str(ip)
    return f"{u.scheme}://{host}" + (f":{port}" if port else "")


def safe_path(path: Any) -> str:
    if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
        raise ProbeError("case/login path must be a local absolute path")
    if "#" in path or "\\" in path or any(ord(c) < 32 for c in path):
        raise ProbeError("invalid case/login path")
    return path


def json_value(doc: Any, path: str) -> Any:
    for key in path.split("."):
        if not key or not isinstance(doc, dict) or key not in doc:
            raise ProbeError("expected JSON path is missing")
        doc = doc[key]
    return doc


def contains_forbidden(value: Any, fields: set[str]) -> bool:
    if isinstance(value, dict):
        return any(k in fields or contains_forbidden(v, fields) for k, v in value.items())
    if isinstance(value, list):
        return any(contains_forbidden(v, fields) for v in value)
    return False


def request(opener, origin: str, path: str, method: str, headers=None, body=None):
    req = urllib.request.Request(origin + safe_path(path), data=body,
                                 headers=headers or {}, method=method)
    try:
        try:
            resp = opener.open(req, timeout=5)
        except urllib.error.HTTPError as exc:
            resp = exc
        with resp:
            status = resp.status
            raw = resp.read(MAX_RESPONSE + 1)
        if 300 <= status < 400:
            raise ProbeError("redirect rejected")
        if len(raw) > MAX_RESPONSE:
            raise ProbeError("response exceeds size limit")
        return status, raw
    except ProbeError:
        raise
    except Exception as exc:
        raise ProbeError("request failed or timed out") from exc


def parse_json(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProbeError("response is not valid JSON") from exc


def validate(config: Any):
    if not isinstance(config, dict):
        raise ProbeError("configuration must be an object")
    origin = safe_origin(config.get("base_url"))
    cases = config.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ProbeError("at least one case is required")
    ids = config.get("identities", {})
    if not isinstance(ids, dict):
        raise ProbeError("identities must be an object")
    names = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ProbeError("case must be an object")
        name = case.get("name")
        if not isinstance(name, str) or not ID_PATTERN.fullmatch(name) or name in names:
            raise ProbeError("case names must be unique safe identifiers")
        names.add(name)
        if case.get("method") not in READ_METHODS:
            raise ProbeError("only GET, HEAD and OPTIONS case requests are allowed")
        safe_path(case.get("path"))
        identity = case.get("identity")
        if identity not in ("anonymous", "invalid") and identity not in ids:
            raise ProbeError("unknown identity")
        expect = case.get("expect")
        if not isinstance(expect, dict):
            raise ProbeError("case requires expect")
        status = expect.get("status")
        if isinstance(status, bool) or not isinstance(status, int) or not (200 <= status < 300 or status in (401, 403)):
            raise ProbeError("expected status must be 2xx, 401 or 403")
        assertions = expect.get("json_equals")
        fields = expect.get("forbidden_fields")
        if not isinstance(assertions, dict) or not assertions or not all(isinstance(k, str) and k for k in assertions):
            raise ProbeError("each case needs nonempty json_equals")
        if not isinstance(fields, list) or not fields or not all(isinstance(k, str) and k for k in fields):
            raise ProbeError("each case needs nonempty forbidden_fields")
        if case["method"] == "HEAD":
            raise ProbeError("HEAD responses have no JSON body; use project tests for HEAD")
    needed = {c["identity"] for c in cases} - {"anonymous", "invalid"}
    if needed:
        login = config.get("login")
        if not isinstance(login, dict):
            raise ProbeError("login configuration is required for named identities")
        safe_path(login.get("path"))
        if login.get("format") not in ("json", "form"):
            raise ProbeError("login format must be json or form")
        for k in ("account_field", "password_field", "token_path"):
            if not isinstance(login.get(k), str) or not login[k]:
                raise ProbeError("login field names and token_path are required")
        if login["account_field"] == login["password_field"]:
            raise ProbeError("login field names must differ")
        for name in needed:
            info = ids[name]
            if not isinstance(info, dict):
                raise ProbeError("identity configuration must be an object")
            for key in ("account_env", "password_env"):
                env_name = info.get(key)
                if not isinstance(env_name, str) or not env_name or not os.environ.get(env_name):
                    raise ProbeError("required identity environment variable is missing")
    return origin, cases, ids, needed


def run(config: Any) -> int:
    origin, cases, ids, needed = validate(config)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    tokens = {}
    for name in sorted(needed):
        login, identity = config["login"], ids[name]
        fields = {login["account_field"]: os.environ[identity["account_env"]],
                  login["password_field"]: os.environ[identity["password_env"]]}
        if login["format"] == "json":
            body, ct = json.dumps(fields).encode("utf-8"), "application/json"
        else:
            body, ct = urllib.parse.urlencode(fields).encode("utf-8"), "application/x-www-form-urlencoded"
        status, raw = request(opener, origin, login["path"], "POST", {"Content-Type": ct}, body)
        if not 200 <= status < 300:
            raise ProbeError("configured login failed")
        token = json_value(parse_json(raw), login["token_path"])
        if not isinstance(token, str) or not token or any(ord(c) < 33 or ord(c) > 126 for c in token):
            raise ProbeError("configured login did not return a usable token")
        tokens[name] = token
    failed = 0
    for case in cases:
        try:
            identity = case["identity"]
            token = tokens.get(identity) if identity not in ("anonymous", "invalid") else ("invalid-token-for-test" if identity == "invalid" else None)
            headers = {"Authorization": "Bearer " + token} if token else {}
            status, raw = request(opener, origin, case["path"], case["method"], headers)
            expect = case["expect"]
            if status != expect["status"]:
                raise ProbeError("HTTP status did not match")
            doc = parse_json(raw)
            for key, value in expect["json_equals"].items():
                if json_value(doc, key) != value:
                    raise ProbeError("JSON assertion did not match")
            if contains_forbidden(doc, set(expect["forbidden_fields"])):
                raise ProbeError("response contains a forbidden field")
            print(f"PASS {case['name']}")
        except ProbeError as exc:
            failed += 1
            print(f"FAIL {case['name']}: {exc}")
    print(f"Results: {len(cases) - failed} passed, {failed} failed; read-only probe, not full authorization coverage.")
    return 1 if failed else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("config", help="path to the JSON test config (credentials must be environment references)")
    args = parser.parse_args(argv)
    try:
        with open(args.config, encoding="utf-8") as handle:
            return run(json.load(handle))
    except (OSError, json.JSONDecodeError, ProbeError, TypeError, ValueError):
        print("ERROR: invalid configuration or login/request failed; check config and local service without exposing credentials.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
