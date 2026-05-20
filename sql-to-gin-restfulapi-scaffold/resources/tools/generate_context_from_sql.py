#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Generate template context JSON from MySQL DDL for gin scaffold."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def to_pascal(name: str) -> str:
    parts = re.split(r"[_\-\s]+", name)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


def to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.replace("-", "_").lower()


def load_mapping(config_path: Path) -> dict:
    return json.loads(config_path.read_text(encoding="utf-8"))


def map_type(raw_sql_type: str, mapping: dict) -> tuple[str, str]:
    sql_upper = raw_sql_type.strip().upper()
    if sql_upper.startswith("TINYINT(1)"):
        return "bool", "bool"

    base = sql_upper.split("(")[0].strip()
    for rule in mapping.get("type_mappings", []):
        for item in rule.get("sql_types", []):
            item_upper = item.upper()
            if item_upper == sql_upper or item_upper == base:
                return rule.get("gorm_type", "string"), rule.get("go_type", "string")
    return "string", "string"


def parse_default(rest: str) -> str | int | float | None:
    m = re.search(r"DEFAULT\s+([^\s,]+|'[^']*')", rest, flags=re.I)
    if not m:
        return None
    val = m.group(1).strip()
    if val.startswith("'") and val.endswith("'"):
        return val[1:-1]
    if re.fullmatch(r"-?\d+", val):
        return int(val)
    if re.fullmatch(r"-?\d+\.\d+", val):
        return float(val)
    return val


def parse_comment(rest: str) -> str:
    m = re.search(r"COMMENT\s+'([^']*)'", rest, flags=re.I)
    return m.group(1) if m else ""


def parse_primary_key(table_body: str) -> str:
    m = re.search(r"PRIMARY\s+KEY\s*\(`([^`]+)`\)", table_body, flags=re.I)
    return m.group(1) if m else ""


def parse_table_fields(table_body: str, pk: str, mapping: dict, soft_delete_candidates: list[str]) -> list[dict]:
    fields: list[dict] = []
    for raw_line in table_body.splitlines():
        line = raw_line.strip().rstrip(",")
        if not line.startswith("`"):
            continue
        m = re.match(r"`([^`]+)`\s+([^\s]+(?:\([^)]*\))?)\s*(.*)", line)
        if not m:
            continue

        col = m.group(1)
        sql_type_raw = m.group(2)
        rest = m.group(3)
        gorm_type, go_type = map_type(sql_type_raw, mapping)

        is_pk = col == pk
        is_auto_inc = "AUTO_INCREMENT" in rest.upper()
        nullable = "NOT NULL" not in rest.upper()
        is_soft_delete = col in soft_delete_candidates

        gorm_items = [f"column:{col}", f"type:{sql_type_raw.lower()}"]
        if is_pk:
            gorm_items.append("primaryKey")
        if not nullable:
            gorm_items.append("not null")
        default_val = parse_default(rest)
        if default_val is not None:
            gorm_items.append(f"default:{default_val}")

        field = {
            "field_name_raw": col,
            "go_field_name": to_pascal(col),
            "sql_type_raw": sql_type_raw,
            "gorm_type": gorm_type,
            "go_type": go_type,
            "gorm_tag": ";".join(gorm_items) + ";",
            "json_tag": col,
            "form_tag": col,
            "nullable": nullable,
            "is_primary_key": is_pk,
            "is_auto_increment": is_auto_inc,
            "is_soft_delete_field": is_soft_delete,
            "default_value": default_val,
            "comment": parse_comment(rest),
            "in_get_filter": True,
            "in_post_payload": (not is_pk or not is_auto_inc) and not is_soft_delete,
            "in_put_payload": (not is_pk) and not is_soft_delete,
        }
        fields.append(field)
    return fields


def parse_tables(sql: str, mapping: dict, soft_delete_candidates: list[str]) -> list[dict]:
    table_pattern = re.compile(
        r"CREATE\s+TABLE\s+`(?P<name>[^`]+)`\s*\((?P<body>.*?)\)\s*ENGINE=",
        flags=re.I | re.S,
    )
    entities: list[dict] = []
    for match in table_pattern.finditer(sql):
        table_name = match.group("name")
        body = match.group("body")
        pk = parse_primary_key(body)
        fields = parse_table_fields(body, pk, mapping, soft_delete_candidates)

        pk_field = next((f for f in fields if f["field_name_raw"] == pk), None)
        pk_type = pk_field["go_type"] if pk_field else "string"
        route_param = to_snake(pk) if pk else "id"
        entity_name = to_pascal(table_name)
        soft_field = next((f["field_name_raw"] for f in fields if f["is_soft_delete_field"]), "")

        entities.append(
            {
                "entity_kind": "table",
                "table_name_raw": table_name,
                "module_name": table_name,
                "entity_name": entity_name,
                "resource_slug": to_snake(table_name),
                "router_init_func": f"Init{entity_name}RouterGroup",
                "url_collection": f"/{to_snake(table_name)}",
                "url_item": f"/{to_snake(table_name)}/:{route_param}" if pk else "",
                "route_param_name": route_param if pk else "",
                "primary_key_field": pk,
                "primary_key_type": pk_type,
                "supports_crud": True,
                "supports_query": True,
                "has_soft_delete": bool(soft_field),
                "soft_delete_field": soft_field,
                "soft_delete_active_value": 1,
                "soft_delete_inactive_value": 0,
                "fields": fields,
            }
        )
    return entities


def parse_view_fields(sql: str, view_name: str) -> list[dict]:
    view_stmt = re.search(
        rf"CREATE(?:\s+ALGORITHM\s*=\s*[^\s]+\s+SQL\s+SECURITY\s+[^\s]+)?\s+VIEW\s+`{re.escape(view_name)}`\s+AS\s+select\s+(.*?)\s+from\s+",
        sql,
        flags=re.I | re.S,
    )
    if not view_stmt:
        return []

    select_part = view_stmt.group(1)
    alias_matches = re.findall(r"AS\s+`([^`]+)`", select_part, flags=re.I)
    fields = []
    for alias in alias_matches:
        fields.append(
            {
                "field_name_raw": alias,
                "go_field_name": to_pascal(alias),
                "sql_type_raw": "varchar(255)",
                "gorm_type": "string",
                "go_type": "string",
                "gorm_tag": f"column:{alias};type:varchar(255);",
                "json_tag": alias,
                "form_tag": alias,
                "nullable": True,
                "is_primary_key": False,
                "is_auto_increment": False,
                "is_soft_delete_field": False,
                "default_value": None,
                "comment": "",
                "in_get_filter": True,
                "in_post_payload": False,
                "in_put_payload": False,
            }
        )
    return fields


def parse_views(sql: str) -> list[dict]:
    view_names = re.findall(
        r"CREATE(?:\s+ALGORITHM\s*=\s*[^\s]+\s+SQL\s+SECURITY\s+[^\s]+)?\s+VIEW\s+`([^`]+)`",
        sql,
        flags=re.I,
    )
    entities: list[dict] = []
    for view_name in view_names:
        entity_name = to_pascal(view_name)
        fields = parse_view_fields(sql, view_name)
        entities.append(
            {
                "entity_kind": "view",
                "table_name_raw": view_name,
                "module_name": view_name,
                "entity_name": entity_name,
                "resource_slug": to_snake(view_name),
                "router_init_func": f"Init{entity_name}RouterGroup",
                "url_collection": f"/{to_snake(view_name)}/list",
                "url_item": "",
                "route_param_name": "",
                "primary_key_field": "",
                "primary_key_type": "",
                "supports_crud": False,
                "supports_query": True,
                "has_soft_delete": False,
                "fields": fields,
            }
        )
    return entities


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python generate_context_from_sql.py <sql_path> <output_context_path> [project_name] [module_name]")
        return 1

    sql_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    project_name = sys.argv[3] if len(sys.argv) > 3 else "study_flask_api"
    module_name = sys.argv[4] if len(sys.argv) > 4 else "study_flask_api"

    if not sql_path.exists():
        print(f"ERROR: sql file not found: {sql_path}")
        return 2

    cfg_path = Path(__file__).resolve().parents[1] / "config" / "type_mappings.json"
    mapping = load_mapping(cfg_path)
    soft_delete_candidates = mapping.get("soft_delete_field_candidates", [])

    sql = sql_path.read_text(encoding="utf-8")
    tables = parse_tables(sql, mapping, soft_delete_candidates)
    views = parse_views(sql)
    entities = tables + views

    context = {
        "project": {
            "project_name": project_name,
            "module_name": module_name,
            "generator_name": "sql-to-gin-restfulapi-scaffold",
            "api_group": "api",
            "api_version_package": "api_1_0",
            "sql_source_type": "file",
            "sql_source_path": str(sql_path).replace("\\", "/"),
        },
        "options": {
            "first_scaffold": True,
            "overwrite_strategy": "merge",
            "conflict_policy": "warn",
            "security_profile": "standard",
            "generate_view_resource": True,
            "supports_batch_add": False,
        },
        "entities": entities,
        "diagnostics": {
            "parse_errors": [],
            "fallback_warnings": [],
            "conflict_warnings": [],
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "output": str(out_path),
                "tables": len(tables),
                "views": len(views),
                "entities": len(entities),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
