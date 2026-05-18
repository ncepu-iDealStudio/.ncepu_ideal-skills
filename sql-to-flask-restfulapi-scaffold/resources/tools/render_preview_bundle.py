#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Render table and view entities from context and output a manifest."""

import json
from pathlib import Path

from render_utils import (
    build_table_replacements,
    build_view_replacements,
    render_model_table_template,
    render_text,
)

ROOT = Path(__file__).resolve().parents[2]
CONTEXT_FILE = ROOT / "resources" / "config" / "template_context_example.json"
TEMPLATE_ROOT = ROOT / "resources" / "templates" / "layers"
OUT_ROOT = ROOT / "resources" / "demo_output" / "bundle_preview"


def render_entity(entity: dict) -> list[str]:
    generated = []

    if entity["entity_kind"] == "table":
        replacements = build_table_replacements(entity)
        resource_dir = OUT_ROOT / "api_1_0" / f"{entity['resource_slug']}Resource"
        resource_dir.mkdir(parents=True, exist_ok=True)

        file_map = {
            TEMPLATE_ROOT / "model" / "model_table_template.py": OUT_ROOT / "models" / f"{entity['module_name']}.py",
            TEMPLATE_ROOT / "controller" / "controller_table_template.py": OUT_ROOT / "controller" / f"{entity['class_name']}Controller.py",
            TEMPLATE_ROOT / "service" / "service_table_template.py": OUT_ROOT / "service" / f"{entity['class_name']}Service.py",
            TEMPLATE_ROOT / "resource" / "resource_table_template.py": resource_dir / f"{entity['resource_slug']}Resource.py",
            TEMPLATE_ROOT / "resource" / "resource_other_table_template.py": resource_dir / f"{entity['resource_slug']}OtherResource.py",
            TEMPLATE_ROOT / "resource" / "resource_init_template.py": resource_dir / "__init__.py",
            TEMPLATE_ROOT / "resource" / "resource_urls_template.py": resource_dir / "urls.py",
        }
    else:
        replacements = build_view_replacements(entity)
        resource_dir = OUT_ROOT / "api_1_0" / f"{entity['resource_slug']}Resource"
        resource_dir.mkdir(parents=True, exist_ok=True)

        file_map = {
            TEMPLATE_ROOT / "model" / "model_view_template.py": OUT_ROOT / "models" / f"{entity['module_name']}.py",
            TEMPLATE_ROOT / "controller" / "controller_view_template.py": OUT_ROOT / "controller" / f"{entity['class_name']}Controller.py",
            TEMPLATE_ROOT / "service" / "service_view_template.py": OUT_ROOT / "service" / f"{entity['class_name']}Service.py",
            TEMPLATE_ROOT / "resource" / "resource_view_other_template.py": resource_dir / f"{entity['resource_slug']}OtherResource.py",
            TEMPLATE_ROOT / "resource" / "resource_init_template.py": resource_dir / "__init__.py",
            TEMPLATE_ROOT / "resource" / "resource_view_urls_template.py": resource_dir / "urls.py",
        }

    for src, dst in file_map.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if entity["entity_kind"] == "table" and src.name == "model_table_template.py":
            rendered = render_model_table_template(src, entity, replacements)
        else:
            text = src.read_text(encoding="utf-8")
            rendered = render_text(text, replacements)

        dst.write_text(rendered, encoding="utf-8")
        generated.append(str(dst.relative_to(OUT_ROOT)).replace("\\", "/"))

    return generated


def main() -> int:
    ctx = json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "models").mkdir(exist_ok=True)
    (OUT_ROOT / "controller").mkdir(exist_ok=True)
    (OUT_ROOT / "service").mkdir(exist_ok=True)

    manifest = {
        "project": ctx.get("project", {}),
        "summary": {
            "tables": 0,
            "views": 0,
            "generated_files": 0,
        },
        "entities": [],
    }

    for entity in ctx.get("entities", []):
        generated_files = render_entity(entity)
        if entity["entity_kind"] == "table":
            manifest["summary"]["tables"] += 1
        else:
            manifest["summary"]["views"] += 1

        manifest["summary"]["generated_files"] += len(generated_files)
        manifest["entities"].append(
            {
                "entity_kind": entity["entity_kind"],
                "module_name": entity["module_name"],
                "class_name": entity["class_name"],
                "generated_files": generated_files,
            }
        )

    manifest_file = OUT_ROOT / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Bundle preview rendered to: {OUT_ROOT}")
    print(f"Manifest: {manifest_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
