#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Preview generated file plan from template context."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def build_plan(entity: dict) -> list[str]:
    name = entity["entity_name"]
    slug = entity["resource_slug"]
    files = [
        f"internal/models/{name}.go",
        f"internal/services/{name}.go",
        f"apis/api_1_0/{slug}/urls.go",
        f"apis/api_1_0/{slug}/{name}Resource.go",
    ]
    if entity.get("entity_kind") == "table":
        files.insert(1, f"internal/dao/{name}.go")
    return files


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python preview_generation_plan.py <context_json_path>")
        return 1

    ctx_path = Path(sys.argv[1])
    if not ctx_path.exists():
        print(f"ERROR: context file not found: {ctx_path}")
        return 2

    data = json.loads(ctx_path.read_text(encoding="utf-8"))
    entities = data.get("entities", [])
    print(f"entities: {len(entities)}")

    total = 0
    for entity in entities:
        print(f"\n[{entity['entity_kind']}] {entity['table_name_raw']}")
        plan = build_plan(entity)
        total += len(plan)
        for item in plan:
            print(f"- {item}")

    print(f"\nplanned files: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
