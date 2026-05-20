#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Validate template context JSON for gin scaffold rendering."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_ROOT = ["project", "options", "entities", "diagnostics"]
REQUIRED_ENTITY = [
    "entity_kind",
    "table_name_raw",
    "module_name",
    "entity_name",
    "resource_slug",
    "router_init_func",
    "url_collection",
    "supports_crud",
    "supports_query",
    "fields",
]
REQUIRED_FIELD = [
    "field_name_raw",
    "go_field_name",
    "sql_type_raw",
    "gorm_type",
    "go_type",
    "gorm_tag",
    "json_tag",
    "form_tag",
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

    errors: list[str] = []
    for key in REQUIRED_ROOT:
        if key not in data:
            errors.append(f"Missing root key: {key}")

    entities = data.get("entities", [])
    if not isinstance(entities, list) or not entities:
        errors.append("entities must be a non-empty list")
    else:
        for idx, entity in enumerate(entities):
            for key in REQUIRED_ENTITY:
                if key not in entity:
                    errors.append(f"entities[{idx}] missing key: {key}")
            fields = entity.get("fields", [])
            if not isinstance(fields, list):
                errors.append(f"entities[{idx}].fields must be list")
            for f_idx, field in enumerate(fields):
                for key in REQUIRED_FIELD:
                    if key not in field:
                        errors.append(f"entities[{idx}].fields[{f_idx}] missing key: {key}")

    if errors:
        print("Context validation failed:")
        for err in errors:
            print(f"- {err}")
        return 3

    print("Context validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
