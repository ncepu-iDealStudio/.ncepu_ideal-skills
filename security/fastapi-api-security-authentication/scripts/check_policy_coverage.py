#!/usr/bin/env python3
"""Compare a route inventory against declared policy; this does not test enforcement."""

import argparse
import json
import sys
from pathlib import Path


METHODS = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"})
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


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _meaningful(value):
    return _nonempty(value) and value.strip().casefold() not in PLACEHOLDERS


def compare(inventory, policy):
    if not isinstance(inventory, dict) or not isinstance(inventory.get("routes"), list):
        raise ValueError("库存 JSON 必须包含 routes 数组")
    if not isinstance(policy, dict) or not isinstance(policy.get("rules"), list):
        raise ValueError("策略 JSON 必须包含 rules 数组")
    if not inventory["routes"]:
        raise ValueError("库存 routes 不能为空；空清单无法证明覆盖")
    errors = []
    routes = set()
    for index, item in enumerate(inventory["routes"]):
        key = _route_key(item, "routes", index)
        if key in routes:
            errors.append(f"重复库存路由: {key[0]} {key[1]}")
        routes.add(key)
    rules = set()
    for index, item in enumerate(policy["rules"]):
        key = _route_key(item, "rules", index)
        if key in rules:
            errors.append(f"重复策略规则: {key[0]} {key[1]}")
        rules.add(key)
        access = item.get("access")
        if access not in ("public", "protected"):
            errors.append(f"{key[0]} {key[1]}: access 必须是 public 或 protected")
        elif access == "protected":
            roles = item.get("roles")
            if not isinstance(roles, list) or not roles or not all(_meaningful(role) for role in roles):
                errors.append(f"{key[0]} {key[1]}: protected 的 roles 必须为非空字符串数组且不能使用待定占位值")
            for field in ("object_scope", "fields"):
                if not _meaningful(item.get(field)):
                    errors.append(f"{key[0]} {key[1]}: protected 的 {field} 必须为非空字符串且不能使用待定占位值")
        if "fields" in item and not _nonempty(item["fields"]):
            errors.append(f"{key[0]} {key[1]}: fields 如提供必须为非空字符串")
    for method, path in sorted(routes - rules):
        errors.append(f"缺少策略: {method} {path}")
    for method, path in sorted(rules - routes):
        errors.append(f"库存中不存在的策略: {method} {path}")
    return errors, len(routes), len(rules)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="比较库存 routes 与策略 rules；此检查不验证权限策略是否正确或被实际执行。"
    )
    parser.add_argument("inventory", type=Path, help="包含 routes 数组的库存 JSON")
    parser.add_argument("policy", type=Path, help="包含 rules 数组的策略 JSON")
    args = parser.parse_args(argv)
    try:
        errors, route_count, rule_count = compare(_load(args.inventory), _load(args.policy))
    except (OSError, ValueError, TypeError) as exc:
        print(f"检查失败: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"策略对账失败: {len(errors)} 项问题", file=sys.stderr)
        return 1
    print(f"清单对账通过: {route_count} 个路由，{rule_count} 条规则。")
    print("注意：仅验证清单完整性，不证明策略合理或接口已执行鉴权。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
