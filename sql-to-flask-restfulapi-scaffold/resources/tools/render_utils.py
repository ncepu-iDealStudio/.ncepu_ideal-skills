#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Shared rendering helpers for scaffold demo scripts."""

from __future__ import annotations

from pathlib import Path


def render_text(template_text: str, replacements: dict) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace("{{ " + key + " }}", str(value))
    return rendered


def build_default_part(field: dict) -> str:
    if field.get("server_default_expr"):
        return ", server_default=db.FetchedValue()"

    if field.get("default_value") is not None:
        value = field["default_value"]
        if isinstance(value, str):
            return f", default='{value}'"
        return f", default={value}"

    return ""


def build_info_part(field: dict) -> str:
    comment = field.get("comment")
    if comment:
        return f", info=\"{comment}\""
    return ""


def build_model_field_line(field: dict) -> str:
    name = field["field_name_raw"]
    sa_type = field["sqlalchemy_type"]
    nullable = "True" if field.get("nullable", True) else "False"
    is_pk = "True" if field.get("is_primary_key", False) else "False"
    default_part = build_default_part(field)
    info_part = build_info_part(field)
    return f"{name} = db.Column({sa_type}, primary_key={is_pk}, nullable={nullable}{default_part}{info_part})"


def build_fields_block(fields: list[dict]) -> str:
    return "\n    ".join(build_model_field_line(field) for field in fields)


def render_model_table_template(template_path: Path, entity: dict, replacements: dict) -> str:
    """Render model table template using entity field list automatically.

    This keeps model field rendering deterministic and avoids relying on callers
    to manually assemble fields_block.
    """
    template_text = template_path.read_text(encoding="utf-8")
    merged = dict(replacements)
    merged["fields_block"] = build_fields_block(entity.get("fields", []))
    return render_text(template_text, merged)


def build_view_columns_block(fields: list[dict]) -> str:
    lines = []
    for field in fields:
        lines.append(f"db.Column('{field['field_name_raw']}', {field['sqlalchemy_type']})")
    return ",\n    ".join(lines)


def build_table_replacements(entity: dict) -> dict:
    return {
        "class_name": entity["class_name"],
        "module_name": entity["module_name"],
        "table_name_raw": entity["table_name_raw"],
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


def build_view_replacements(entity: dict) -> dict:
    return {
        "class_name": entity["class_name"],
        "module_name": entity["module_name"],
        "table_name_raw": entity["table_name_raw"],
        "view_table_name_var": f"t_{entity['module_name']}",
        "view_columns_block": build_view_columns_block(entity["fields"]),
        "blueprint_name": f"{entity['endpoint_base']}_blueprint",
        "other_resource_file_name": f"{entity['resource_slug']}OtherResource",
        "endpoint_name": entity["class_name"],
        "url_collection": entity["url_collection"],
        "endpoint_base": entity["endpoint_base"],
    }
