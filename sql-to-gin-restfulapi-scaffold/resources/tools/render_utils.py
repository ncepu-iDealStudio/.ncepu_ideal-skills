#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Shared rendering helpers for gin scaffold demo scripts."""

from __future__ import annotations

from pathlib import Path


def render_text(template_text: str, replacements: dict) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", str(value))
    return rendered


def read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_template(path: Path, replacements: dict) -> str:
    return render_text(read_template(path), replacements)


def build_go_imports(imports: list[str]) -> str:
    uniq = sorted(set(x for x in imports if x))
    if not uniq:
        return ""
    if len(uniq) == 1:
        return f'import "{uniq[0]}"'
    body = "\n".join(f'\t"{item}"' for item in uniq)
    return f"import (\n{body}\n)"


def build_fields_block(fields: list[dict]) -> str:
    lines = []
    for field in fields:
        line = (
            f"\t{field['go_field_name']} {field['go_type']} "
            f"`gorm:\"{field['gorm_tag']}\" json:\"{field['json_tag']}\" form:\"{field['form_tag']}\"`"
        )
        lines.append(line)
    return "\n".join(lines)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
