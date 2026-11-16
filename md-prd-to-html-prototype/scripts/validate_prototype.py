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
