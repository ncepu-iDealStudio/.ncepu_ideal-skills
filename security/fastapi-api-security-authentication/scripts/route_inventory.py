#!/usr/bin/env python3
"""Export method/path pairs from a *saved* OpenAPI JSON document.

This is a manifest helper, not an application runner or security scanner.
"""

import argparse
import json
import sys
from pathlib import Path


METHODS = frozenset({"get", "post", "put", "patch", "delete", "head", "options", "trace"})


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复 JSON 键: {key!r}")
        result[key] = value
    return result


def inventory(document):
    if not isinstance(document, dict) or not isinstance(document.get("paths"), dict):
        raise ValueError("OpenAPI 根对象必须包含 paths 对象")
    routes = []
    for path, item in document["paths"].items():
        if not isinstance(path, str) or not path.startswith("/"):
            raise ValueError(f"无效 OpenAPI 路径: {path!r}")
        if not isinstance(item, dict):
            raise ValueError(f"路径项必须是对象: {path}")
        if "$ref" in item:
            raise ValueError(f"路径项包含未解析的 $ref，请先解析: {path}")
        for method, operation in item.items():
            if method in METHODS:
                if not isinstance(operation, dict):
                    raise ValueError(f"操作必须是对象: {method.upper()} {path}")
                routes.append({"method": method.upper(), "path": path})
    if not routes:
        raise ValueError("未发现任何 OpenAPI 操作，不能生成空清单")
    routes.sort(key=lambda item: (item["path"], item["method"]))
    return {"routes": routes}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="从已保存的 OpenAPI JSON 提取操作清单；不会启动应用或探测接口。"
    )
    parser.add_argument("openapi", type=Path, help="本地 OpenAPI JSON 文件")
    parser.add_argument("-o", "--output", type=Path, help="输出 JSON 文件；不指定则写到 stdout")
    args = parser.parse_args(argv)
    try:
        with args.openapi.open("r", encoding="utf-8-sig") as source:
            document = json.load(source, object_pairs_hook=_unique_object)
        result = inventory(document)
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, ValueError, TypeError) as exc:
        print(f"生成清单失败: {exc}", file=sys.stderr)
        return 1
    print("提示：OpenAPI 可能遗漏隐藏路由、文档和其他已注册路由；须与运行时路由清单对账。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
