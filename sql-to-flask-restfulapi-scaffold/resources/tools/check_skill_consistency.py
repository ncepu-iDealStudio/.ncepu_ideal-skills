#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""检查 sql-to-flask-restfulapi-scaffold 自身是否自洽。

不渲染目标项目。校验内容：
1. 资源目录完整性（config / specifications / templates / tools）
2. 增量策略文件的结构完整性（运行模式、变更类型、手写保护、注册幂等）
3. 增量规范文档存在且非占位
4. 路由注册模板保留 marker 区块（幂等追加的前提）
5. 层模板保留手写标记（覆盖策略的前提）
6. SKILL.md 引用了增量策略与规范文档
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DIRS = ["config", "specifications", "templates", "tools", "static"]

REQUIRED_POLICY_KEYS = [
    "version",
    "modes",
    "mode_detection",
    "baseline_snapshot",
    "file_roles",
    "change_types",
    "hand_written_protection",
    "registration",
    "migration",
    "verification",
    "report",
]

# 必须支持的运行模式
REQUIRED_MODES = ["greenfield", "add_table", "alter_table", "drop_table"]

# 必须覆盖的变更类型（覆盖常见 DDL 变更）
REQUIRED_CHANGE_TYPES = [
    "add_table",
    "add_column",
    "drop_column",
    "rename_column",
    "modify_column_type",
    "modify_nullable",
    "change_primary_key",
    "add_status_flag",
    "change_soft_delete_field",
]

# 必须声明为「禁止自动执行」的高危变更
BLOCKED_FROM_AUTO = ["rename_table", "drop_table"]

INCREMENTAL_DOC = SKILL_ROOT / "resources" / "specifications" / "incremental_update.md"
POLICY = SKILL_ROOT / "resources" / "config" / "incremental_change_policy.json"
ROUTER_INIT = SKILL_ROOT / "resources" / "templates" / "project_structure" / "api_1_0" / "__init__.py"


def check_dirs(errors: list[str]) -> None:
    res = SKILL_ROOT / "resources"
    for d in REQUIRED_DIRS:
        if not (res / d).is_dir():
            errors.append(f"缺少资源目录: resources/{d}")


def check_policy(errors: list[str]) -> dict:
    if not POLICY.exists():
        errors.append("缺少增量策略文件: resources/config/incremental_change_policy.json")
        return {}

    try:
        policy = json.loads(POLICY.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"incremental_change_policy.json 无法解析: {exc}")
        return {}

    for key in REQUIRED_POLICY_KEYS:
        if key not in policy:
            errors.append(f"incremental_change_policy.json 缺少键: {key}")

    modes = policy.get("modes", {})
    for mode in REQUIRED_MODES:
        if mode not in modes:
            errors.append(f"incremental_change_policy.json 缺少运行模式: {mode}")

    change_types = policy.get("change_types", {})
    for ct in REQUIRED_CHANGE_TYPES:
        if ct not in change_types:
            errors.append(f"incremental_change_policy.json 缺少变更类型: {ct}")

    # 高危变更必须声明需用户确认或被禁止自动执行
    for ct in BLOCKED_FROM_AUTO:
        entry = change_types.get(ct, {})
        if not entry.get("blocked_from_auto") and not entry.get("requires_user_confirmation"):
            errors.append(f"高危变更 {ct} 未声明 blocked_from_auto 或 requires_user_confirmation")

    # 每个变更类型都要有验证项
    for name, entry in change_types.items():
        if not entry.get("verify"):
            errors.append(f"变更类型 {name} 缺少 verify 验证清单")

    # 手写保护
    protection = policy.get("hand_written_protection", {})
    if not protection.get("rules"):
        errors.append("incremental_change_policy.json 缺少 hand_written_protection.rules")

    # 注册幂等
    registration = policy.get("registration", {})
    if not registration.get("dedupe"):
        errors.append("incremental_change_policy.json 缺少 registration.dedupe（幂等规则）")
    if not registration.get("append_only_markers"):
        errors.append("incremental_change_policy.json 缺少 registration.append_only_markers")

    return policy


def check_incremental_doc(errors: list[str]) -> None:
    if not INCREMENTAL_DOC.exists():
        errors.append("缺少增量规范文档: resources/specifications/incremental_update.md")
        return
    text = INCREMENTAL_DOC.read_text(encoding="utf-8")
    if len(text) < 2000:
        errors.append("incremental_update.md 内容过短，疑似占位")


def check_router_markers(errors: list[str]) -> None:
    """路由注册文件必须保留 marker，否则无法幂等追加。"""
    if not ROUTER_INIT.exists():
        errors.append(f"缺少路由注册模板: {ROUTER_INIT.relative_to(SKILL_ROOT)}")
        return

    text = ROUTER_INIT.read_text(encoding="utf-8")
    for marker in ["AUTO_IMPORTS_START", "AUTO_IMPORTS_END", "AUTO_REGISTRY_START", "AUTO_REGISTRY_END"]:
        if marker not in text:
            errors.append(f"api_1_0/__init__.py 缺少 marker: {marker}（幂等追加依赖它）")


def check_layer_markers(errors: list[str], policy: dict) -> None:
    """校验层模板是否带生成/手写标记，供覆盖策略识别。"""
    layers = SKILL_ROOT / "resources" / "templates" / "layers"
    if not layers.is_dir():
        errors.append("缺少 templates/layers 目录")
        return

    file_roles = policy.get("file_roles", {})
    # 至少要能识别出 service 是手写文件
    service_role = None
    for key, val in file_roles.items():
        if "service" in key.lower():
            service_role = val
            break

    if service_role is None:
        errors.append("file_roles 中缺少 service 层的归属定义")
    elif service_role.get("ownership") != "hand_written":
        errors.append("service 层应定义 ownership=hand_written（保护手写代码）")


def check_skill_md(errors: list[str]) -> None:
    skill_md = SKILL_ROOT / "SKILL.md"
    if not skill_md.exists():
        errors.append("缺少 SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    checks = [
        ("incremental_change_policy.json", "SKILL.md 未引用增量策略文件"),
        ("incremental_update.md", "SKILL.md 未引用增量规范文档"),
        ("alter_table", "SKILL.md 未说明 alter_table 模式"),
        ("add_table", "SKILL.md 未说明 add_table 模式"),
    ]
    for needle, msg in checks:
        if needle not in text:
            errors.append(msg)


def main() -> int:
    errors: list[str] = []

    check_dirs(errors)
    policy = check_policy(errors)
    check_incremental_doc(errors)
    check_router_markers(errors)
    check_layer_markers(errors, policy)
    check_skill_md(errors)

    if errors:
        print("技能自洽校验失败：")
        for err in errors:
            print(f"  ❌ {err}")
        return 1

    print("sql-to-flask-restfulapi-scaffold consistency ok")
    print(f"  - 运行模式: {len(policy.get('modes', {}))}")
    print(f"  - 变更类型: {len(policy.get('change_types', {}))}")
    print(f"  - 文件归属规则: {len(policy.get('file_roles', {}))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
