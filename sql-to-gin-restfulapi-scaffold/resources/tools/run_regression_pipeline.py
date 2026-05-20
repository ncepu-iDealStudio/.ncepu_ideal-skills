#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Run end-to-end regression pipeline for gin scaffold skill."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def extract_sql_baseline(sql_path: Path) -> tuple[int, int]:
    text = sql_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    bt = "`"
    tables = [ln for ln in lines if ln.strip().upper().startswith(f"CREATE TABLE {bt}")]
    views = [
        ln
        for ln in lines
        if (f" VIEW {bt}" in ln.strip().upper()) and ("CREATE" in ln.strip().upper())
    ]
    return len(tables), len(views)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    skill_root = repo_root / "sql-to-gin-restfulapi-scaffold"
    tools = skill_root / "resources" / "tools"
    demo = skill_root / "resources" / "demo_output"
    tmpl_urls = skill_root / "resources" / "templates" / "project_structure" / "apis" / "api_1_0" / "urls.go"

    sql_path = repo_root / "test" / "study_flask_api.sql"
    context_path = demo / "generated_context_study_flask_api.json"
    merge_preview_path = demo / "urls_merge_preview.go"

    steps = [
        (
            "generate_context",
            [
                sys.executable,
                str(tools / "generate_context_from_sql.py"),
                str(sql_path),
                str(context_path),
                "study_flask_api",
                "study_flask_api",
            ],
        ),
        (
            "validate_context",
            [sys.executable, str(tools / "validate_template_context.py"), str(context_path)],
        ),
        (
            "preview_plan",
            [sys.executable, str(tools / "preview_generation_plan.py"), str(context_path)],
        ),
        (
            "render_bundle",
            [sys.executable, str(tools / "render_preview_bundle.py"), str(context_path)],
        ),
    ]

    report: dict[str, object] = {
        "pipeline": "sql-to-gin-regression",
        "ok": True,
        "steps": [],
    }

    for name, cmd in steps:
        code, output = run_cmd(cmd, repo_root)
        report["steps"].append(
            {
                "name": name,
                "exit_code": code,
                "ok": code == 0,
                "output": output,
            }
        )
        if code != 0:
            report["ok"] = False
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 1

    merge_preview_path.write_text(tmpl_urls.read_text(encoding="utf-8"), encoding="utf-8")

    merge_cmd = [
        sys.executable,
        str(tools / "merge_router_registry.py"),
        str(context_path),
        str(merge_preview_path),
    ]
    code, output = run_cmd(merge_cmd, repo_root)
    report["steps"].append(
        {
            "name": "merge_registry_preview",
            "exit_code": code,
            "ok": code == 0,
            "output": output,
        }
    )
    if code != 0:
        report["ok"] = False
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    snapshot_cmd = [
        sys.executable,
        str(tools / "check_snapshots.py"),
    ]
    code, output = run_cmd(snapshot_cmd, repo_root)
    report["steps"].append(
        {
            "name": "check_snapshots",
            "exit_code": code,
            "ok": code == 0,
            "output": output,
        }
    )
    if code != 0:
        report["ok"] = False
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    tables, views = extract_sql_baseline(sql_path)
    ctx = json.loads(context_path.read_text(encoding="utf-8"))
    sql_entities = tables + views
    context_entities = len(ctx.get("entities", []))
    coverage = round((context_entities * 100.0 / sql_entities), 2) if sql_entities else 0.0

    report["coverage"] = {
        "sql_tables": tables,
        "sql_views": views,
        "sql_entities": sql_entities,
        "context_entities": context_entities,
        "coverage_percent": coverage,
    }

    report_path = demo / "pipeline_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report["report_file"] = str(report_path)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
