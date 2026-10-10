"""检查 sql-to-fastapi-restfulapi-scaffold 自身是否自洽。

不渲染目标项目。只确认骨架里没有已淘汰文件，命名规则与资源模板使用同一套前缀变量。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2]
STRUCTURE = SKILL_ROOT / "resources" / "templates" / "project_structure"

OBSOLETE = (
    "app/events.py",
    "app/router.py",
    "config/settings.py",
    "utils/loguru.py",
    "core/dependencies.py",
)


def main() -> int:
    errors: list[str] = []

    for relative in OBSOLETE:
        if (STRUCTURE / relative).exists():
            errors.append(f"淘汰文件仍在骨架中: {relative}")

    for path in STRUCTURE.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "{%" in text:
            errors.append(f"骨架 Python 含未渲染的 Jinja 控制块: {path.relative_to(SKILL_ROOT)}")

    rules = json.loads(
        (SKILL_ROOT / "resources" / "config" / "naming_rules.json").read_text(encoding="utf-8")
    )
    if "plural_rules" in json.dumps(rules):
        errors.append("naming_rules.json 仍包含 plural_rules")
    route = rules.get("route_prefix", {})
    if route.get("template_variable") != "route_prefix":
        errors.append("naming_rules.json 缺少 route_prefix.template_variable")
    if route.get("examples", {}).get("company_file") != "/company-file":
        errors.append("company_file 的路由前缀不是 /company-file")

    resource = (
        SKILL_ROOT / "resources" / "templates" / "layers" / "resource" / "resource_template.py"
    ).read_text(encoding="utf-8")
    if 'prefix="/{{route_prefix}}"' not in resource:
        errors.append("资源模板的 APIRouter 前缀未使用 route_prefix")
    if 'prefix="/{{resource_singular}}"' in resource:
        errors.append("资源模板仍把 resource_singular 当作 HTTP 前缀")

    readme = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    for label, text in (("README.md", readme), ("SKILL.md", skill)):
        if "create / get / update / delete" in text:
            errors.append(f"{label} 的 Repository 方法顺序仍是 create/get/update/delete")
        if "不生成的文件" in text and "Docker" in text:
            errors.append(f"{label} 仍把 Docker 列进不生成清单")
        for banned in ("events.py", "loguru.py", "config/settings.py"):
            if f"├── {banned}" in text or f"│   ├── {banned}" in text or f"│   └── {banned}" in text:
                errors.append(f"{label} 的目录树仍包含 {banned}")

    copilot = SKILL_ROOT / "docs" / "GitHub Copilot中使用sql-to-fastapi-restfulapi-scaffold技能.md"
    if not copilot.is_file():
        errors.append("缺少 FastAPI 的 Copilot 配置说明")
    flask_doc = SKILL_ROOT / "docs" / "GitHub Copilot中使用sql-to-flask-restfulapi-scaffold技能.md"
    if flask_doc.exists():
        errors.append("FastAPI 技能目录仍保留 Flask 的 Copilot 说明")

    if errors:
        print("\n".join(errors))
        return 1
    print("sql-to-fastapi-restfulapi-scaffold consistency ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
