#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Compare generated artifacts with snapshot baselines."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def stable_json_text(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compare_or_update(target: Path, snapshot: Path, update: bool) -> dict:
    result = {
        "target": str(target),
        "snapshot": str(snapshot),
        "exists": target.exists(),
        "snapshot_exists": snapshot.exists(),
        "ok": False,
        "updated": False,
        "reason": "",
        "target_hash": "",
        "snapshot_hash": "",
    }

    if not target.exists():
        result["reason"] = "target file missing"
        return result

    current_text = stable_json_text(target)
    result["target_hash"] = sha256_text(current_text)

    if not snapshot.exists():
        if update:
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(current_text, encoding="utf-8")
            result["snapshot_exists"] = True
            result["snapshot_hash"] = result["target_hash"]
            result["updated"] = True
            result["ok"] = True
            result["reason"] = "snapshot created"
            return result
        result["reason"] = "snapshot missing"
        return result

    snap_text = stable_json_text(snapshot)
    result["snapshot_hash"] = sha256_text(snap_text)

    if snap_text == current_text:
        result["ok"] = True
        result["reason"] = "match"
        return result

    if update:
        snapshot.write_text(current_text, encoding="utf-8")
        result["snapshot_hash"] = result["target_hash"]
        result["updated"] = True
        result["ok"] = True
        result["reason"] = "snapshot refreshed"
        return result

    result["reason"] = "content mismatch"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or update regression snapshots")
    parser.add_argument("--update", action="store_true", help="create/refresh snapshots")
    parser.add_argument(
        "--context",
        default="sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json",
        help="generated context json path",
    )
    parser.add_argument(
        "--manifest",
        default="sql-to-gin-restfulapi-scaffold/resources/demo_output/bundle_preview/manifest.json",
        help="generated manifest json path",
    )
    parser.add_argument(
        "--snapshot-dir",
        default="sql-to-gin-restfulapi-scaffold/resources/demo_output/snapshots",
        help="snapshot directory path",
    )
    args = parser.parse_args()

    context = Path(args.context)
    manifest = Path(args.manifest)
    snapshot_dir = Path(args.snapshot_dir)

    checks = [
        compare_or_update(context, snapshot_dir / "generated_context_study_flask_api.snapshot.json", args.update),
        compare_or_update(manifest, snapshot_dir / "bundle_manifest.snapshot.json", args.update),
    ]

    ok = all(item["ok"] for item in checks)
    output = {
        "ok": ok,
        "update_mode": args.update,
        "checks": checks,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
