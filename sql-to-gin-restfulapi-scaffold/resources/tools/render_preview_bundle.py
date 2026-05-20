#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Render preview bundle for all entities and emit a manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from render_utils import build_fields_block, build_go_imports, ensure_parent, render_template


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "layers"
OUTPUT_DIR = ROOT / "demo_output" / "bundle_preview"


def render_model(entity: dict) -> str:
    model_tpl = TEMPLATES / "model" / (
        "model_view_template.go" if entity["entity_kind"] == "view" else "model_table_template.go"
    )
    imports = []
    for field in entity.get("fields", []):
        if field.get("go_type") == "time.Time":
            imports.append("time")
    return render_template(
        model_tpl,
        {
            "entity_name": entity["entity_name"],
            "table_name_raw": entity["table_name_raw"],
            "imports_block": build_go_imports(imports),
            "fields_block": build_fields_block(entity.get("fields", [])),
        },
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python render_preview_bundle.py <context_json_path>")
        return 1

    ctx_path = Path(sys.argv[1])
    data = json.loads(ctx_path.read_text(encoding="utf-8"))

    manifest: list[str] = []
    for entity in data.get("entities", []):
        content = render_model(entity)
        out = OUTPUT_DIR / "models" / f"{entity['entity_name']}.go"
        ensure_parent(out)
        out.write_text(content, encoding="utf-8")
        manifest.append(str(out.relative_to(ROOT)).replace('\\\\', '/'))

    manifest_file = OUTPUT_DIR / "manifest.json"
    ensure_parent(manifest_file)
    manifest_file.write_text(json.dumps({"files": manifest}, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"bundle files: {len(manifest)}")
    print(f"manifest: {manifest_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
