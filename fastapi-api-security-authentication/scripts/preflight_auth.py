#!/usr/bin/env python3
"""Collect account-table, login, role, and token evidence from a FastAPI project.

This is a preflight helper for skill gates. It does not decide pass/fail and
does not modify the target project.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PASSWORD_NAMES = frozenset(
    {
        "password",
        "passwd",
        "pwd",
        "password_hash",
        "hashed_password",
        "pass_hash",
        "passwordhash",
        "hashedpassword",
        "passhash",
    }
)
ACCOUNT_NAMES = frozenset(
    {
        "account",
        "username",
        "user_name",
        "login_name",
        "loginname",
        "email",
        "phone",
    }
)
ROLE_NAMES = frozenset(
    {
        "user_type",
        "usertype",
        "role",
        "role_id",
        "role_name",
        "is_admin",
        "user_role",
        "account_type",
    }
)
LOGIN_FN = re.compile(r"\b(login|signin|sign_in|authenticate)\b", re.I)
TOKEN_HINT = re.compile(
    r"\b(jwt|JSONWebToken|create_access_token|Bearer|OAuth2PasswordBearer|"
    r"access_token|Authorization)\b",
    re.I,
)
COL_PY = re.compile(
    r"""^\s*([A-Za-z_][\w]*)\s*=\s*Column\(\s*(?:['"]([\w]+)['"]\s*,)?""",
    re.M,
)
TABLENAME = re.compile(r"""__tablename__\s*=\s*['"]([^'"]+)['"]""")
SQL_TABLE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([A-Za-z_]\w*)`?",
    re.I,
)
SQL_COL = re.compile(r"`?([A-Za-z_]\w*)`?\s+(?:VARCHAR|CHAR|TEXT|TINYTEXT|MEDIUMTEXT|LONGTEXT|BLOB)", re.I)


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _is_password(name: str) -> bool:
    n = name.lower()
    compact = _norm(name)
    if n in PASSWORD_NAMES or compact in PASSWORD_NAMES:
        return True
    return compact.endswith("password") and "policy" not in compact and "hint" not in compact


def _is_account(name: str) -> bool:
    return name.lower() in ACCOUNT_NAMES or _norm(name) in ACCOUNT_NAMES


def _is_role(name: str) -> bool:
    return name.lower() in ROLE_NAMES or _norm(name) in ROLE_NAMES


def _iter_files(root: Path, rel: str, suffix: str):
    base = root / rel
    if not base.is_dir():
        return
    for path in base.rglob(f"*{suffix}"):
        if "__pycache__" in path.parts or path.name.startswith("test_"):
            continue
        yield path


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def scan_models(root: Path) -> list[dict]:
    found = []
    for path in _iter_files(root, "models", ".py"):
        if path.name in {"base.py", "__init__.py"}:
            continue
        text = _read(path)
        table_m = TABLENAME.search(text)
        table = table_m.group(1) if table_m else path.stem
        cols = []
        for match in COL_PY.finditer(text):
            attr, db_name = match.group(1), match.group(2)
            cols.append(db_name or attr)
        passwords = [c for c in cols if _is_password(c)]
        if not passwords:
            continue
        found.append(
            {
                "table": table,
                "file": str(path.relative_to(root)).replace("\\", "/"),
                "password_fields": passwords,
                "account_fields": [c for c in cols if _is_account(c)],
                "role_fields": [c for c in cols if _is_role(c)],
            }
        )
    return found


def scan_sql(root: Path) -> list[dict]:
    found = []
    sql_dirs = [root / "sql", root / "database"]
    files = []
    for folder in sql_dirs:
        if folder.is_dir():
            files.extend(folder.rglob("*.sql"))
    for path in files:
        text = _read(path)
        current = None
        acc: dict[str, list[str]] = {}
        for line in text.splitlines():
            tm = SQL_TABLE.search(line)
            if tm:
                current = tm.group(1)
                acc.setdefault(current, [])
                continue
            if current:
                for col in SQL_COL.findall(line):
                    acc[current].append(col)
        rel = str(path.relative_to(root)).replace("\\", "/")
        for table, cols in acc.items():
            passwords = [c for c in cols if _is_password(c)]
            if not passwords:
                continue
            found.append(
                {
                    "table": table,
                    "file": rel,
                    "password_fields": passwords,
                    "account_fields": [c for c in cols if _is_account(c)],
                    "role_fields": [c for c in cols if _is_role(c)],
                }
            )
    return found


def scan_service_login(root: Path) -> list[dict]:
    hits = []
    for path in _iter_files(root, "service", ".py"):
        if path.name in {"dependencies.py", "__init__.py"}:
            continue
        text = _read(path)
        for match in re.finditer(
            r"^\s*(?:async\s+)?def\s+(login|signin|sign_in|authenticate)\s*\(",
            text,
            re.M | re.I,
        ):
            hits.append(
                {
                    "file": str(path.relative_to(root)).replace("\\", "/"),
                    "function": match.group(1),
                }
            )
    return hits


def _join_path(prefix: str, path_part: str) -> str:
    if not prefix:
        full = path_part or "/"
    elif path_part.startswith("/"):
        full = prefix.rstrip("/") + path_part
    elif path_part:
        full = prefix.rstrip("/") + "/" + path_part
    else:
        full = prefix
    return full if full.startswith("/") else "/" + full


def scan_http_login(root: Path) -> list[dict]:
    hits = []
    seen = set()
    for folder in ("api", "app"):
        for path in _iter_files(root, folder, ".py"):
            text = _read(path)
            rel = str(path.relative_to(root)).replace("\\", "/")
            prefix_m = re.search(r"""APIRouter\(\s*prefix\s*=\s*['"]([^'"]+)['"]""", text)
            prefix = prefix_m.group(1) if prefix_m else ""
            matched_route = False
            for match in re.finditer(
                r"""@(?:router|app)\.(post|get|put|patch)\(\s*['"]([^'"]*)['"]""",
                text,
                re.I,
            ):
                method, path_part = match.group(1).upper(), match.group(2)
                full = _join_path(prefix, path_part)
                if not (LOGIN_FN.search(full) or re.search(r"/token(?:/|$)", full, re.I)):
                    continue
                key = (rel, method, full)
                if key in seen:
                    continue
                seen.add(key)
                matched_route = True
                hits.append(
                    {
                        "file": rel,
                        "method": method,
                        "path_hint": full,
                        "evidence": "route decorator path",
                    }
                )
            if not matched_route and re.search(
                r"def\s+(login|signin|sign_in|authenticate)\s*\(", text, re.I
            ):
                key = (rel, None, None)
                if key not in seen:
                    seen.add(key)
                    hits.append(
                        {
                            "file": rel,
                            "method": None,
                            "path_hint": None,
                            "evidence": "function name matches login",
                        }
                    )
    return hits


def scan_token_hints(root: Path) -> dict:
    files = []
    for rel in ("api", "service", "core", "utils", "middleware", "app"):
        files.extend(_iter_files(root, rel, ".py"))
    mentions = []
    for path in files:
        text = _read(path)
        if TOKEN_HINT.search(text):
            mentions.append(str(path.relative_to(root)).replace("\\", "/"))
    return {"files_with_jwt_or_bearer": mentions}


def scan_role_signals(root: Path, account_tables: list[dict]) -> list[dict]:
    signals = []
    for item in account_tables:
        for field in item.get("role_fields") or []:
            signals.append(
                {
                    "table": item.get("table"),
                    "file": item.get("file"),
                    "field": field,
                }
            )
    return signals


def build_report(root: Path) -> dict:
    models = scan_models(root)
    sql = scan_sql(root)
    tables = models or sql
    if models and sql:
        known = {m["table"].lower() for m in models}
        for row in sql:
            if row["table"].lower() not in known:
                tables.append(row)
    login_service = scan_service_login(root)
    login_http = scan_http_login(root)
    return {
        "project_root": str(root),
        "account_tables": tables,
        "login_service": login_service,
        "login_http": login_http,
        "role_signals": scan_role_signals(root, tables),
        "token_hints": scan_token_hints(root),
        "notes": [
            "本报告只列证据，是否通过门禁由 SKILL 规则判定。",
            "有 JWT 工具不等于已有登录接口。",
            "Bearer test-token 测试夹具不等于令牌鉴权合格。",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="FastAPI 鉴权预检：账号表 / 登录 / 角色 / 令牌线索")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not root.is_dir():
        print(f"项目目录不存在: {root}", file=sys.stderr)
        return 2
    report = build_report(root)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
