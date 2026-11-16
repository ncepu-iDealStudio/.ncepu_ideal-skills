#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Merge router imports and registry calls for apis/api_1_0/urls.go."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

AUTO_IMPORTS_START = "// ==AUTO_IMPORTS_START=="
AUTO_IMPORTS_END = "// ==AUTO_IMPORTS_END=="
AUTO_REGISTRY_START = "// ==AUTO_REGISTRY_START=="
AUTO_REGISTRY_END = "// ==AUTO_REGISTRY_END=="

IMPORT_PATTERN = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s+"([^"]+)"\s*$')
CALL_PATTERN = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\.(Init[a-zA-Z0-9_]+)\(Api\)\s*$')


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_marker_indices(lines: list[str], start_marker: str, end_marker: str) -> tuple[int, int] | None:
    try:
        start = next(i for i, line in enumerate(lines) if start_marker in line)
        end = next(i for i, line in enumerate(lines) if i > start and end_marker in line)
        return start, end
    except StopIteration:
        return None


def build_desired_items(context: dict) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    module_name = context["project"]["module_name"]
    entities = context.get("entities", [])

    import_items: list[tuple[str, str]] = []
    call_items: list[tuple[str, str]] = []

    for entity in entities:
        alias = entity.get("module_name", "").replace("-", "_")
        resource_slug = entity.get("resource_slug", "")
        router_init_func = entity.get("router_init_func", "")
        if not alias or not resource_slug or not router_init_func:
            continue

        import_path = f"{module_name}/apis/api_1_0/{resource_slug}"
        import_items.append((alias, import_path))
        call_items.append((alias, router_init_func))

    import_items = sorted(set(import_items), key=lambda x: (x[1], x[0]))
    call_items = sorted(set(call_items), key=lambda x: (x[0], x[1]))
    return import_items, call_items


def merge_import_block(lines: list[str], desired: list[tuple[str, str]]) -> tuple[list[str], dict]:
    diagnostics = {
        "inserted_imports_count": 0,
        "duplicate_imports_removed_count": 0,
        "import_merge_skipped": False,
        "import_skip_reason": "",
    }

    idx = find_marker_indices(lines, AUTO_IMPORTS_START, AUTO_IMPORTS_END)
    if not idx:
        diagnostics["import_merge_skipped"] = True
        diagnostics["import_skip_reason"] = "auto import markers missing"
        return lines, diagnostics

    start, end = idx
    current_block = lines[start + 1 : end]

    existing: list[tuple[str, str]] = []
    for line in current_block:
        match = IMPORT_PATTERN.match(line)
        if match:
            existing.append((match.group(1), match.group(2)))

    unique_existing = sorted(set(existing), key=lambda x: (x[1], x[0]))
    diagnostics["duplicate_imports_removed_count"] = len(existing) - len(unique_existing)

    existing_paths = {path for _, path in unique_existing}
    merged = list(unique_existing)
    for alias, path in desired:
        if path not in existing_paths:
            merged.append((alias, path))
            existing_paths.add(path)
            diagnostics["inserted_imports_count"] += 1

    merged = sorted(merged, key=lambda x: (x[1], x[0]))
    merged_lines = [f'\t{alias} "{path}"\n' for alias, path in merged]

    new_lines = lines[: start + 1] + merged_lines + lines[end:]
    return new_lines, diagnostics


def merge_registry_block(lines: list[str], desired: list[tuple[str, str]]) -> tuple[list[str], dict]:
    diagnostics = {
        "inserted_registry_entries_count": 0,
        "duplicate_registry_entries_removed_count": 0,
        "registry_merge_skipped": False,
        "registry_skip_reason": "",
    }

    idx = find_marker_indices(lines, AUTO_REGISTRY_START, AUTO_REGISTRY_END)
    if not idx:
        diagnostics["registry_merge_skipped"] = True
        diagnostics["registry_skip_reason"] = "auto registry markers missing"
        return lines, diagnostics

    start, end = idx
    current_block = lines[start + 1 : end]

    existing: list[tuple[str, str]] = []
    for line in current_block:
        match = CALL_PATTERN.match(line)
        if match:
            existing.append((match.group(1), match.group(2)))

    unique_existing = sorted(set(existing), key=lambda x: (x[0], x[1]))
    diagnostics["duplicate_registry_entries_removed_count"] = len(existing) - len(unique_existing)

    existing_set = set(unique_existing)
    merged = list(unique_existing)
    for alias, init_func in desired:
        entry = (alias, init_func)
        if entry not in existing_set:
            merged.append(entry)
            existing_set.add(entry)
            diagnostics["inserted_registry_entries_count"] += 1

    merged = sorted(merged, key=lambda x: (x[0], x[1]))
    merged_lines = [f"\t{alias}.{init_func}(Api)\n" for alias, init_func in merged]

    new_lines = lines[: start + 1] + merged_lines + lines[end:]
    return new_lines, diagnostics


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python merge_router_registry.py <context_json_path> <urls_go_path>")
        return 1

    context_path = Path(sys.argv[1])
    urls_path = Path(sys.argv[2])

    if not context_path.exists():
        print(f"ERROR: context file not found: {context_path}")
        return 2
    if not urls_path.exists():
        print(f"ERROR: urls.go file not found: {urls_path}")
        return 3

    context = read_json(context_path)
    import_items, call_items = build_desired_items(context)

    lines = urls_path.read_text(encoding="utf-8").splitlines(keepends=True)

    lines, import_diag = merge_import_block(lines, import_items)
    lines, registry_diag = merge_registry_block(lines, call_items)

    urls_path.write_text("".join(lines), encoding="utf-8")

    diagnostics = {
        **import_diag,
        **registry_diag,
        "target_file": str(urls_path),
    }
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
