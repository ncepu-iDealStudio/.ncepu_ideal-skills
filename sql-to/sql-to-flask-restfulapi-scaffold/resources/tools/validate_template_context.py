#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Validate template context JSON for scaffold rendering."""

import json
import sys
from pathlib import Path

REQUIRED_ROOT = ["project", "options", "entities", "diagnostics"]
REQUIRED_ENTITY = [
    "entity_kind",
    "table_name_raw",
    "module_name",
    "class_name",
    "resource_slug",
    "endpoint_base",
    "url_collection",
    "supports_crud",
    "supports_query",
    "supports_other_resource",
    "fields",
]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python validate_template_context.py <context_json_path>")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: context file not found: {path}")
        return 2

    data = json.loads(path.read_text(encoding="utf-8"))

    errors = []
    for key in REQUIRED_ROOT:
        if key not in data:
            errors.append(f"Missing root key: {key}")

    entities = data.get("entities", [])
    if not isinstance(entities, list) or not entities:
        errors.append("entities must be a non-empty list")
    else:
        for index, entity in enumerate(entities):
            for key in REQUIRED_ENTITY:
                if key not in entity:
                    errors.append(f"entities[{index}] missing key: {key}")

    if errors:
        print("Context validation failed:")
        for err in errors:
            print(f"- {err}")
        return 3

    print("Context validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
