#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Render a minimal single-entity demo output using template_context_example.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTEXT_FILE = ROOT / "resources" / "config" / "template_context_example.json"
TEMPLATE_ROOT = ROOT / "resources" / "templates" / "layers"
OUT_ROOT = ROOT / "resources" / "demo_output" / "student_demo"


def render_text(template_text: str, replacements: dict) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace("{{ " + key + " }}", str(value))
    return rendered


def build_fields_block(fields):
    lines = []
    for field in fields:
        name = field["field_name_raw"]
        sa_type = field["sqlalchemy_type"]
        nullable = "True" if field.get("nullable", True) else "False"
        is_pk = "True" if field.get("is_primary_key", False) else "False"
        lines.append(
            f"{name} = db.Column({sa_type}, primary_key={is_pk}, nullable={nullable})"
        )
    return "\n    ".join(lines)


def main() -> int:
    ctx = json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))
    entity = next(e for e in ctx["entities"] if e["entity_kind"] == "table" and e["module_name"] == "student")

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "models").mkdir(exist_ok=True)
    (OUT_ROOT / "controller").mkdir(exist_ok=True)
    (OUT_ROOT / "service").mkdir(exist_ok=True)
    (OUT_ROOT / "api_1_0" / f"{entity['resource_slug']}Resource").mkdir(parents=True, exist_ok=True)

    replacements = {
        "class_name": entity["class_name"],
        "module_name": entity["module_name"],
        "table_name_raw": entity["table_name_raw"],
        "fields_block": build_fields_block(entity["fields"]),
        "primary_key_field": entity["primary_key_field"],
        "route_param_name": entity["route_param_name"],
        "soft_delete_field": entity.get("soft_delete_field", ""),
        "soft_delete_inactive_value": entity.get("soft_delete_inactive_value", 0),
        "soft_delete_active_value": entity.get("soft_delete_active_value", 1),
        "blueprint_name": f"{entity['endpoint_base']}_blueprint",
        "resource_file_name": f"{entity['resource_slug']}Resource",
        "other_resource_file_name": f"{entity['resource_slug']}OtherResource",
        "endpoint_name": entity["class_name"],
        "url_collection": entity["url_collection"],
        "url_item": entity["url_item"],
        "other_route": f"{entity['url_collection']}/update/<{entity['route_param_name']}>",
        "endpoint_base": entity["endpoint_base"],
    }

    file_map = {
        TEMPLATE_ROOT / "model" / "model_table_template.py": OUT_ROOT / "models" / f"{entity['module_name']}.py",
        TEMPLATE_ROOT / "controller" / "controller_table_template.py": OUT_ROOT / "controller" / f"{entity['class_name']}Controller.py",
        TEMPLATE_ROOT / "service" / "service_table_template.py": OUT_ROOT / "service" / f"{entity['class_name']}Service.py",
        TEMPLATE_ROOT / "resource" / "resource_table_template.py": OUT_ROOT / "api_1_0" / f"{entity['resource_slug']}Resource" / f"{entity['resource_slug']}Resource.py",
        TEMPLATE_ROOT / "resource" / "resource_other_table_template.py": OUT_ROOT / "api_1_0" / f"{entity['resource_slug']}Resource" / f"{entity['resource_slug']}OtherResource.py",
        TEMPLATE_ROOT / "resource" / "resource_init_template.py": OUT_ROOT / "api_1_0" / f"{entity['resource_slug']}Resource" / "__init__.py",
        TEMPLATE_ROOT / "resource" / "resource_urls_template.py": OUT_ROOT / "api_1_0" / f"{entity['resource_slug']}Resource" / "urls.py",
    }

    for src, dst in file_map.items():
        text = src.read_text(encoding="utf-8")
        dst.write_text(render_text(text, replacements), encoding="utf-8")

    print(f"Demo rendered to: {OUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
