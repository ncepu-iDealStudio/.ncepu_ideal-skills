"""检查 sql-to-springboot-restfulapi-scaffold 自身是否自洽。

不渲染目标项目。校验「已有项目增量更新」的策略、规范、模板标记与各文档引用是否齐全，
并守住本技能的两条既定边界：不生成测试代码、不改 application.properties 的 ddl-auto。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2]
LAYERS = SKILL_ROOT / "resources" / "templates" / "layers"

REQUIRED_CHANGE_TYPES = (
    "add_table",
    "add_column",
    "drop_column",
    "rename_column",
    "modify_column_type",
    "modify_nullable",
    "modify_default",
    "modify_unique",
    "add_managed_field",
    "change_soft_delete_field",
    "change_primary_key",
    "add_foreign_key",
    "drop_foreign_key",
    "comment_only",
    "rename_table",
    "drop_table",
)

AUTO_GENERATED_TEMPLATES = (
    "entity/EntityTemplate.java",
    "repository/RepositoryTemplate.java",
    "dto/request/RequestTemplate.java",
    "dto/response/ResponseTemplate.java",
)

PROTECTED_TEMPLATES = (
    "service/ServiceTemplate.java",
    "controller/ControllerTemplate.java",
)


def check_incremental(errors: list[str]) -> None:
    """校验增量更新相关的资源、策略结构、模板标记与文档引用。"""
    config = SKILL_ROOT / "resources" / "config" / "incremental_change_policy.json"
    spec = SKILL_ROOT / "resources" / "specifications" / "incremental_update.md"
    for path in (config, spec):
        if not path.is_file():
            errors.append(f"缺少增量更新资源: {path.relative_to(SKILL_ROOT)}")
    if not config.is_file():
        return

    try:
        policy = json.loads(config.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"incremental_change_policy.json 无法解析: {exc}")
        return

    for key in (
        "framework_notes",
        "modes",
        "mode_detection",
        "baseline_snapshot",
        "file_roles",
        "change_types",
        "minimal_merge_protocol",
        "hand_written_protection",
        "registration_and_idempotency",
        "migration",
        "verification",
        "report",
    ):
        if key not in policy:
            errors.append(f"incremental_change_policy.json 缺少 {key}")

    for mode in ("greenfield", "add_table", "alter_table", "drop_table"):
        if mode not in policy.get("modes", {}):
            errors.append(f"incremental_change_policy.json 缺少运行模式 {mode}")
    for change in REQUIRED_CHANGE_TYPES:
        if change not in policy.get("change_types", {}):
            errors.append(f"incremental_change_policy.json 缺少变更类型 {change}")
    for change in ("add_column", "drop_column", "modify_column_type", "change_soft_delete_field"):
        entry = policy.get("change_types", {}).get(change, {})
        if not entry.get("minimal_merge_required"):
            errors.append(f"变更类型 {change} 缺少 Service 最小合并要求")
        if not entry.get("breaks_compile_if_skipped"):
            errors.append(f"变更类型 {change} 未标注编译破坏风险")

    notes = policy.get("framework_notes", {})
    for key in ("no_central_route_registry", "no_test_generation", "ddl_auto", "status_field", "compile_coupling"):
        if key not in notes:
            errors.append(f"incremental_change_policy.json 缺少 framework_notes.{key}")
    if "none" not in str(notes.get("ddl_auto", "")):
        errors.append("framework_notes.ddl_auto 未锁定 ddl-auto=none")
    if not policy.get("minimal_merge_protocol", {}).get("steps"):
        errors.append("incremental_change_policy.json 缺少最小合并协议步骤")
    if "不生成测试代码" not in str(policy.get("verification", {}).get("no_generated_tests", "")):
        errors.append("incremental_change_policy.json 未声明不生成测试代码")
    if not policy.get("hand_written_protection", {}).get("rules"):
        errors.append("incremental_change_policy.json 缺少骨架/手写保护规则")
    if not policy.get("registration_and_idempotency", {}).get("dedupe"):
        errors.append("incremental_change_policy.json 缺少幂等规则")
    if policy.get("registration_and_idempotency", {}).get("central_registry") != "none":
        errors.append("Spring 技能不应声明中央路由注册表")

    if spec.is_file() and len(spec.read_text(encoding="utf-8")) < 500:
        errors.append("incremental_update.md 内容过短，疑似占位")

    for relative in AUTO_GENERATED_TEMPLATES:
        path = LAYERS / relative
        if not path.is_file():
            errors.append(f"缺少层模板: {relative}")
        elif "【AUTO-GENERATED】" not in path.read_text(encoding="utf-8"):
            errors.append(f"层模板 {relative} 缺少 【AUTO-GENERATED】 标记")
    for relative in PROTECTED_TEMPLATES:
        path = LAYERS / relative
        if not path.is_file():
            errors.append(f"缺少层模板: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        if "【AUTO-GENERATED / 手写保护区】" not in text:
            errors.append(f"层模板 {relative} 缺少手写保护区标记")
        if "手写业务代码区" not in text:
            errors.append(f"层模板 {relative} 缺少手写业务代码区标记")

    references = {
        SKILL_ROOT / "SKILL.md": (
            "incremental_change_policy.json",
            "incremental_update.md",
            "alter_table",
            "add_table",
            "步骤 3.2",
            "步骤 3.3",
            "最小合并协议",
        ),
        SKILL_ROOT / "README.md": (
            "已有项目的增量更新",
            "alter_table",
            "incremental_change_policy.json",
            "不生成测试代码",
        ),
        SKILL_ROOT / "resources" / "specifications" / "coding_standards.md": (
            "## 8. 已有项目增量变更规范",
            "incremental_change_policy.json",
        ),
    }
    for path, needles in references.items():
        if not path.is_file():
            errors.append(f"缺少文档: {path.relative_to(SKILL_ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{path.relative_to(SKILL_ROOT)} 未引用增量内容: {needle}")

    skill = SKILL_ROOT / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        if "只生成新增表的5个文件" in text:
            errors.append("SKILL.md 仍写着「只生成新增表的5个文件」（应为 6 个按表文件）")
        if "不生成测试代码" not in text:
            errors.append("SKILL.md 未声明不生成测试代码")

    readme = SKILL_ROOT / "README.md"
    if readme.is_file() and "ddl-auto" not in readme.read_text(encoding="utf-8"):
        errors.append("README.md 未提示 ddl-auto 边界")


def main() -> int:
    errors: list[str] = []
    check_incremental(errors)
    if errors:
        print("\n".join(errors))
        return 1
    print("sql-to-springboot-restfulapi-scaffold consistency ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
