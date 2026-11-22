#!/usr/bin/env python3
"""Check that the final route inventory matches the endpoint-surface plan.

The plan declares every route as ``keep`` or ``remove`` with a reason. This tool
only verifies consistency between the plan and the actual registered routes; it
does not prove authorization is enforced.
"""

import argparse
import json
import sys
from pathlib import Path


METHODS = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"})
ACTIONS = frozenset({"keep", "remove"})
PLACEHOLDERS = frozenset({"待定", "未决", "todo", "tbd", "未确认", "unknown"})


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复 JSON 键: {key!r}")
        result[key] = value
    return result


def _load(path):
    with path.open("r", encoding="utf-8-sig") as source:
        return json.load(source, object_pairs_hook=_unique_object)


def _route_key(item, label, index):
    if not isinstance(item, dict):
        raise ValueError(f"{label}[{index}] 必须为对象")
    method, path = item.get("method"), item.get("path")
    if not isinstance(method, str) or method not in METHODS:
        raise ValueError(f"{label}[{index}] 的 method 必须为大写 HTTP 方法")
    if not isinstance(path, str) or not path.startswith("/") or path != path.strip():
        raise ValueError(f"{label}[{index}] 的 path 必须为以 / 开头的完整路径")
    return method, path


def _meaningful(value):
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value.strip().casefold() not in PLACEHOLDERS
    )


def compare(inventory, surface):
    if not isinstance(inventory, dict) or not isinstance(inventory.get("routes"), list):
        raise ValueError("库存 JSON 必须包含 routes 数组")
    if not isinstance(surface, dict) or not isinstance(surface.get("routes"), list):
        raise ValueError("处置 JSON 必须包含 routes 数组")
    if not inventory["routes"]:
        raise ValueError("库存 routes 不能为空；空清单无法证明接口面")

    errors = []
    actual = set()
    for index, item in enumerate(inventory["routes"]):
        key = _route_key(item, "routes", index)
        if key in actual:
            errors.append(f"重复库存路由: {key[0]} {key[1]}")
        actual.add(key)

    keep, remove = set(), set()
    for index, item in enumerate(surface["routes"]):
        key = _route_key(item, "处置", index)
        if key in keep or key in remove:
            errors.append(f"重复处置规则: {key[0]} {key[1]}")
        action = item.get("action")
        if action not in ACTIONS:
            errors.append(f"{key[0]} {key[1]}: action 必须是 keep 或 remove")
        if not _meaningful(item.get("reason")):
            errors.append(f"{key[0]} {key[1]}: reason 必须为非空且不能使用待定占位值")

        if action == "keep":
            keep.add(key)
            if key not in actual:
                errors.append(f"声明保留但未注册: {key[0]} {key[1]}")
        elif action == "remove":
            remove.add(key)
            if key in actual:
                errors.append(f"声明删除但仍注册: {key[0]} {key[1]}")

    for method, path in sorted(actual - keep - remove):
        errors.append(f"缺少处置: {method} {path}")

    return errors, len(actual), len(keep), len(remove)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="对账最终路由库存与 keep/remove 处置表；不验证鉴权是否生效。"
    )
    parser.add_argument("inventory", type=Path, help="包含 routes 数组的最终路由库存")
    parser.add_argument("surface", type=Path, help="包含 routes 数组的处置表（keep/remove）")
    args = parser.parse_args(argv)

    try:
        errors, actual_count, keep_count, remove_count = compare(
            _load(args.inventory), _load(args.surface)
        )
    except (OSError, ValueError, TypeError) as exc:
        print(f"检查失败: {exc}", file=sys.stderr)
        return 1

    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"接口面对账失败: {len(errors)} 项问题", file=sys.stderr)
        return 1

    print(
        f"接口面对账通过: 实际 {actual_count} 个路由，"
        f"保留 {keep_count} 个，移除 {remove_count} 个。"
    )
    print("注意：仅验证路由与处置表一致，不证明权限策略合理或鉴权已生效。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
