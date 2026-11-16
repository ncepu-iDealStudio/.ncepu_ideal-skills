"""Flag candidate dangerous APIs. A hit is not a confirmed vulnerability.

Quoted literals in snippets are redacted. Secret-like filenames are reported
without reading their contents.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".gradle",
    ".idea",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
    "vendor",
    "venv",
}

CODE_EXTENSIONS = {
    ".cs",
    ".go",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".j2",
    ".jinja",
    ".kt",
    ".kts",
    ".php",
    ".properties",
    ".py",
    ".rb",
    ".ts",
    ".tsx",
    ".vue",
    ".xml",
    ".yaml",
    ".yml",
}

SECRET_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}

MAX_BYTES = 500_000

# (id, severity, regex). Patterns are candidate locators, not exploit checks.
RULES: list[tuple[str, str, re.Pattern[str]]] = [
    ("python-shell-true", "high", re.compile(r"shell\s*=\s*True")),
    ("python-pickle", "high", re.compile(r"pickle\.loads?\s*\(")),
    ("python-yaml-load", "high", re.compile(r"yaml\.load\s*\(")),
    ("tls-verify-disabled", "high", re.compile(r"verify\s*=\s*False|InsecureSkipVerify\s*:\s*true")),
    ("python-mark-safe", "medium", re.compile(r"mark_safe\s*\(")),
    ("template-safe-filter", "medium", re.compile(r"\|\s*safe\b")),
    ("react-dangerous-html", "medium", re.compile(r"dangerouslySetInnerHTML")),
    ("vue-v-html", "medium", re.compile(r"\bv-html\b")),
    ("dom-innerhtml", "medium", re.compile(r"\.innerHTML\s*=")),
    ("js-eval", "medium", re.compile(r"\beval\s*\(")),
    ("js-function-ctor", "medium", re.compile(r"new\s+Function\s*\(")),
    ("prisma-raw-unsafe", "high", re.compile(r"\$(?:queryRawUnsafe|executeRawUnsafe)")),
    ("sqlalchemy-f-string", "high", re.compile(r"text\(\s*f[\"']")),
    ("java-object-input", "critical", re.compile(r"new\s+ObjectInputStream\s*\(")),
    ("dotnet-binary-formatter", "critical", re.compile(r"new\s+BinaryFormatter\s*\(")),
    ("shell-via-sh", "high", re.compile(r"exec\.Command\(\s*\"sh\"\s*,\s*\"-c\"")),
    (
        "hardcoded-secret",
        "critical",
        re.compile(
            r"(?i)\b(?:password|passwd|secret|api_key|apikey|access_key|private_key)\b\s*[:=]\s*[\"'][^\"']{6,}[\"']"
        ),
    ),
]


def snippet(line: str) -> str:
    redacted = re.sub(r"(['\"])(?:\\.|(?!\1).){0,200}\1", "\\1***\\1", line.strip())
    return redacted[:180]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix == ".min.js" or path.name.endswith(".min.js"):
            continue
        yield path


def scan(root: Path) -> list[dict]:
    findings: list[dict] = []
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        if path.name in SECRET_FILENAMES or path.suffix == ".pem":
            findings.append(
                {
                    "rule": "secret-file",
                    "severity": "critical",
                    "path": rel,
                    "line": 0,
                    "snippet": "(file not read)",
                }
            )
            continue
        if path.suffix.lower() not in CODE_EXTENSIONS:
            continue
        if path.stat().st_size > MAX_BYTES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for rule_id, severity, pattern in RULES:
                if pattern.search(line):
                    findings.append(
                        {
                            "rule": rule_id,
                            "severity": severity,
                            "path": rel,
                            "line": lineno,
                            "snippet": snippet(line),
                        }
                    )
    return findings


def to_markdown(root: Path, findings: list[dict]) -> str:
    lines = [
        "# scan_sinks",
        "",
        f"target: {root}",
        f"findings: {len(findings)}",
        "",
        "Hits are candidates. Confirm that untrusted data reaches the API before treating one as a vulnerability.",
        "",
    ]
    if not findings:
        lines.append("No candidates.")
        return "\n".join(lines) + "\n"
    for item in findings:
        loc = item["path"] if item["line"] == 0 else f"{item['path']}:{item['line']}"
        lines.append(f"- [{item['severity']}] {item['rule']} {loc}")
        lines.append(f"  {item['snippet']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Flag candidate dangerous APIs in a project tree.")
    parser.add_argument("target", help="Project root to scan")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args(argv)
    root = Path(args.target)
    if not root.is_dir():
        print(f"target is not a directory: {root}", file=sys.stderr)
        return 2
    findings = scan(root.resolve())
    if args.json:
        json.dump(findings, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(to_markdown(root.resolve(), findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
