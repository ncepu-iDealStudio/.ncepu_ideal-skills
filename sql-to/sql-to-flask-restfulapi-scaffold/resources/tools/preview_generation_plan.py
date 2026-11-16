#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Preview generation plan from SQL DDL.

Extracts table/view names and prints a planned file summary.
"""

import re
import sys
from pathlib import Path

TABLE_RE = re.compile(r"^CREATE TABLE\s+`([^`]+)`", re.IGNORECASE)
VIEW_RE = re.compile(r"^CREATE\s+ALGORITHM\s*=.*?VIEW\s+`([^`]+)`", re.IGNORECASE)


def snake_case(name: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python preview_generation_plan.py <sql_file_path>")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: sql file not found: {path}")
        return 2

    tables = []
    views = []
    for line in path.read_text(encoding="utf-8").splitlines():
        t_match = TABLE_RE.match(line.strip())
        if t_match:
            tables.append(t_match.group(1))
            continue

        v_match = VIEW_RE.match(line.strip())
        if v_match:
            views.append(v_match.group(1))

    print(f"Tables: {len(tables)}")
    print(f"Views: {len(views)}")
    print()

    print("Planned files per table:")
    print("- models/{module}.py")
    print("- controller/{ClassName}Controller.py")
    print("- service/{ClassName}Service.py")
    print("- api_1_0/{resource}Resource/__init__.py")
    print("- api_1_0/{resource}Resource/{resource}Resource.py")
    print("- api_1_0/{resource}Resource/{resource}OtherResource.py")
    print("- api_1_0/{resource}Resource/urls.py")
    print()

    print("Table entities:")
    for name in tables:
        print(f"- {name} -> {snake_case(name)}")

    print()
    print("View entities:")
    for name in views:
        print(f"- {name} -> {snake_case(name)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
