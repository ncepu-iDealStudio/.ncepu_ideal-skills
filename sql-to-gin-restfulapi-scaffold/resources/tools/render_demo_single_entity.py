#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Render a single entity model template for quick demo."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from render_utils import build_fields_block, build_go_imports, ensure_parent, render_template


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "layers"
OUTPUT_DIR = ROOT / "demo_output" / "single_entity"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python render_demo_single_entity.py <context_json_path> [entity_index]")
        return 1

    ctx_path = Path(sys.argv[1])
    entity_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    data = json.loads(ctx_path.read_text(encoding="utf-8"))
    entity = data["entities"][entity_idx]

    model_tpl = TEMPLATES / "model" / (
        "model_view_template.go" if entity["entity_kind"] == "view" else "model_table_template.go"
    )

    imports = []
    for field in entity.get("fields", []):
        if field.get("go_type") == "time.Time":
            imports.append("time")

    rendered = render_template(
        model_tpl,
        {
            "entity_name": entity["entity_name"],
            "table_name_raw": entity["table_name_raw"],
            "imports_block": build_go_imports(imports),
            "fields_block": build_fields_block(entity.get("fields", [])),
        },
    )

    output = OUTPUT_DIR / f"{entity['entity_name']}.go"
    ensure_parent(output)
    output.write_text(rendered, encoding="utf-8")
    print(f"rendered: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
