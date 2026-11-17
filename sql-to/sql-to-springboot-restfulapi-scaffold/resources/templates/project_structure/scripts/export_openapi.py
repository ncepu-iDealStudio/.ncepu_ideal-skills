"""导出 Spring Boot 项目的接口文档。

写出两份文件，都覆盖同名旧文件：
- docs/openapi.json  给 Apifox / Apipost 按 OpenAPI 导入
- docs/api.md        给人阅读，不要把它当接口定义导入

在项目根目录执行：python scripts/export_openapi.py

应用已启动、且 /api-docs 对得上当前 Controller 时，用 springdoc 的结果。
否则按 Controller 与 Request/Response DTO 生成，不连接数据库。
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JAVA = ROOT / "src" / "main" / "java"
PROPS = ROOT / "src" / "main" / "resources" / "application.properties"
DOCS = ROOT / "docs"
METHODS = ("get", "post", "put", "patch", "delete")

SCALAR = {
    "String": {"type": "string"},
    "Integer": {"type": "integer", "format": "int32"},
    "int": {"type": "integer", "format": "int32"},
    "Long": {"type": "integer", "format": "int64"},
    "long": {"type": "integer", "format": "int64"},
    "Short": {"type": "integer", "format": "int32"},
    "short": {"type": "integer", "format": "int32"},
    "Boolean": {"type": "boolean"},
    "boolean": {"type": "boolean"},
    "Double": {"type": "number", "format": "double"},
    "double": {"type": "number", "format": "double"},
    "Float": {"type": "number", "format": "float"},
    "float": {"type": "number", "format": "float"},
    "BigDecimal": {"type": "number"},
    "LocalDateTime": {"type": "string", "format": "date-time"},
    "LocalDate": {"type": "string", "format": "date"},
    "LocalTime": {"type": "string", "format": "time"},
    "Date": {"type": "string", "format": "date-time"},
}


def read_properties(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def api_settings(props: dict[str, str]) -> tuple[str, str, str]:
    port = props.get("server.port") or "8080"
    context = props.get("server.servlet.context-path") or ""
    docs_path = props.get("springdoc.api-docs.path") or "/v3/api-docs"
    if context and not context.startswith("/"):
        context = "/" + context
    if context == "/":
        context = ""
    if not docs_path.startswith("/"):
        docs_path = "/" + docs_path
    return port, context, docs_path


def fetch_live(url: str) -> dict | None:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if response.status != 200:
                return None
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None
    if not isinstance(payload, dict) or "paths" not in payload:
        return None
    return payload


def live_matches(spec: dict, prefixes: list[str]) -> bool:
    if not prefixes:
        return False
    paths = spec.get("paths") or {}
    for prefix in prefixes:
        if not any(path == prefix or path.startswith(prefix + "/") for path in paths):
            return False
    return True


def annotate_spec(spec: dict) -> dict:
    info = spec.setdefault("info", {})
    note = (
        "脚手架生成的业务接口默认不要求登录。"
        "导入 Apifox 或 Apipost 时选择 OpenAPI / Swagger，上传本文件。"
    )
    description = (info.get("description") or "").strip()
    if "Apifox" not in description:
        info["description"] = f"{description}\n\n{note}".strip()
    return spec


def _java_type_schema(java_type: str, known: set[str]) -> dict:
    text = re.sub(r"\s+", "", java_type)
    list_match = re.fullmatch(r"(?:List|Set)<(.+)>", text)
    if list_match:
        return {"type": "array", "items": _java_type_schema(list_match.group(1), known)}
    if text in SCALAR:
        return dict(SCALAR[text])
    simple = text.split(".")[-1]
    if simple in SCALAR:
        return dict(SCALAR[simple])
    if simple in known:
        return {"$ref": f"#/components/schemas/{simple}"}
    return {"type": "string"}


def parse_dto(path: Path) -> tuple[str, dict]:
    text = path.read_text(encoding="utf-8")
    class_match = re.search(r"public\s+class\s+(\w+)", text)
    name = class_match.group(1) if class_match else path.stem
    properties: dict[str, dict] = {}
    required: list[str] = []
    pending_required = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("@") and any(
            mark in stripped for mark in ("NotNull", "NotBlank", "NotEmpty")
        ):
            pending_required = True
            continue
        field = re.match(r"private\s+(?!static)([\w.<>, ?]+)\s+(\w+)\s*(?:=|;)", stripped)
        if not field:
            if stripped and not stripped.startswith("@") and not stripped.startswith("*") and not stripped.startswith("/"):
                pending_required = False
            continue
        java_type, field_name = field.group(1).strip(), field.group(2)
        if field_name == "serialVersionUID":
            pending_required = False
            continue
        properties[field_name] = {"java_type": java_type}
        if pending_required:
            required.append(field_name)
        pending_required = False
    return name, {"properties": properties, "required": required}


def _annotation_value(text: str, name: str) -> str:
    match = re.search(rf'{name}\s*=\s*"([^"]*)"', text)
    if match:
        return match.group(1)
    match = re.search(rf'{name}\s*\(\s*"([^"]*)"', text)
    return match.group(1) if match else ""


def _mapping(annotations: str) -> tuple[str, str] | None:
    for method, annotation in (
        ("get", "GetMapping"),
        ("post", "PostMapping"),
        ("put", "PutMapping"),
        ("patch", "PatchMapping"),
        ("delete", "DeleteMapping"),
    ):
        match = re.search(rf"@{annotation}\b(\([^)]*\))?", annotations)
        if not match:
            continue
        body = match.group(1) or ""
        path = _annotation_value(body, "value") or _annotation_value(body, "path")
        if not path:
            quoted = re.search(r'"([^"]*)"', body)
            path = quoted.group(1) if quoted else ""
        return method, path
    return None


def _scan_closer(text: str, open_index: int, open_char: str, close_char: str) -> int:
    depth = 0
    index = open_index
    quote = ""
    while index < len(text):
        char = text[index]
        if quote:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = ""
            index += 1
            continue
        if char in ("'", '"'):
            quote = char
            index += 1
            continue
        if char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return len(text) - 1


def parse_controller(path: Path) -> tuple[str, list[dict]]:
    text = path.read_text(encoding="utf-8")
    class_mapping = ""
    class_match = re.search(
        r"@RequestMapping\s*\((.*?)\)\s*(?:@\w+\s*(?:\([^)]*\))?\s*)*public\s+class",
        text,
        re.S,
    )
    if class_match:
        body = class_match.group(1)
        class_mapping = _annotation_value(body, "value") or _annotation_value(body, "path")
        if not class_mapping:
            quoted = re.search(r'"([^"]*)"', body)
            class_mapping = quoted.group(1) if quoted else ""
    tag = ""
    tag_match = re.search(r'@Tag\s*\(\s*name\s*=\s*"([^"]*)"', text)
    if tag_match:
        tag = tag_match.group(1)

    operations = []
    class_at = text.find("public class")
    region_start = text.find("{", class_at) + 1 if class_at >= 0 else 0
    for match in re.finditer(r"public\s+([\w.<>, ?]+)\s+(\w+)\s*\(", text):
        annotation_text = text[region_start : match.start()]
        paren = match.end() - 1
        close_paren = _scan_closer(text, paren, "(", ")")
        brace = text.find("{", close_paren)
        region_start = _scan_closer(text, brace, "{", "}") + 1 if brace >= 0 else close_paren + 1
        mapped = _mapping(annotation_text)
        if not mapped:
            continue
        method, sub_path = mapped
        params_start = match.end() - 1
        depth = 0
        params = []
        buffer = []
        for index in range(params_start, len(text)):
            char = text[index]
            if char == "(":
                depth += 1
                if depth == 1:
                    continue
            elif char == ")":
                depth -= 1
                if depth == 0:
                    chunk = "".join(buffer).strip()
                    if chunk:
                        params.append(chunk)
                    break
                buffer.append(char)
                continue
            if depth == 1 and char == "," and buffer.count("(") == buffer.count(")"):
                params.append("".join(buffer).strip())
                buffer = []
                continue
            if depth >= 1:
                buffer.append(char)
        operations.append(
            {
                "method": method,
                "class_path": class_mapping,
                "sub_path": sub_path,
                "summary": _annotation_value(annotation_text, "summary") or match.group(2),
                "return_type": match.group(1).strip(),
                "name": match.group(2),
                "params": params,
                "tag": tag,
                "secured": "@PreAuthorize" in annotation_text,
            }
        )
    return class_mapping, operations


def _join_path(class_path: str, sub_path: str) -> str:
    left = "/" + class_path.strip("/") if class_path else ""
    right = "/" + sub_path.strip("/") if sub_path else ""
    path = (left + right) or "/"
    return re.sub(r"/{2,}", "/", path)


def _wrapper_name(data_name: str | None) -> str:
    return f"ApiResponse{data_name}" if data_name else "ApiResponse"


def build_from_sources(props: dict[str, str]) -> tuple[dict, list[str]]:
    port, context, _docs_path = api_settings(props)
    if not JAVA.is_dir():
        empty = annotate_spec(
            {
                "openapi": "3.0.3",
                "info": {"title": props.get("spring.application.name") or "API", "version": "1.0.0"},
                "servers": [{"url": f"http://127.0.0.1:{port}{context}", "description": "本地"}],
                "paths": {},
                "components": {"schemas": {}},
            }
        )
        return empty, []
    dto_files = list(JAVA.rglob("*Request.java")) + list(JAVA.rglob("*Response.java"))
    dtos: dict[str, dict] = {}
    for path in dto_files:
        if path.name == "ApiResponse.java":
            continue
        name, schema = parse_dto(path)
        dtos[name] = schema
    known = set(dtos)

    paths: dict[str, dict] = {}
    prefixes: list[str] = []
    wrappers: dict[str, dict] = {}
    for path in sorted(JAVA.rglob("*Controller.java")):
        class_path, operations = parse_controller(path)
        if class_path:
            prefixes.append(_join_path(class_path, ""))
        for operation in operations:
            url = _join_path(operation["class_path"], operation["sub_path"])
            data_schema, data_name = _response_data(operation["return_type"], known)
            wrapper = _wrapper_name(data_name)
            wrappers[wrapper] = _api_response_schema(data_schema)
            op: dict = {
                "tags": [operation["tag"]] if operation["tag"] else [],
                "summary": operation["summary"],
                "operationId": operation["name"],
                "parameters": _parameters(operation["params"]),
                "responses": {
                    "201" if operation["method"] == "post" and not operation["sub_path"] else "200": {
                        "description": "成功",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{wrapper}"}
                            }
                        },
                    }
                },
            }
            if not op["tags"]:
                op.pop("tags")
            body_name = _request_body_name(operation["params"], known)
            if body_name:
                op["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{body_name}"}
                        }
                    },
                }
            if operation["secured"]:
                op["security"] = [{"bearerAuth": []}]
            paths.setdefault(url, {})[operation["method"]] = op

    schemas = {}
    for name, dto in dtos.items():
        properties = {}
        for field_name, meta in dto["properties"].items():
            properties[field_name] = _java_type_schema(meta["java_type"], known)
        schema: dict = {"type": "object", "properties": properties}
        if dto["required"]:
            schema["required"] = dto["required"]
        schemas[name] = schema
    schemas.update(wrappers)
    components: dict = {"schemas": schemas}
    secured = any(
        operation.get("security")
        for item in paths.values()
        for operation in item.values()
    )
    if secured:
        components["securitySchemes"] = {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    title = props.get("spring.application.name") or "API"
    return annotate_spec(
        {
            "openapi": "3.0.3",
            "info": {"title": title, "version": "1.0.0"},
            "servers": [{"url": f"http://127.0.0.1:{port}{context}", "description": "本地"}],
            "paths": paths,
            "components": components,
        }
    ), prefixes


def _response_data(return_type: str, known: set[str]) -> tuple[dict, str | None]:
    text = re.sub(r"\s+", "", return_type)
    page = re.search(r"Page<(\w+)>", text)
    if page:
        item = page.group(1)
        item_schema = {"$ref": f"#/components/schemas/{item}"} if item in known else {"type": "object"}
        name = f"Page{item}"
        return (
            {
                "type": "object",
                "properties": {
                    "content": {"type": "array", "items": item_schema},
                    "totalElements": {"type": "integer", "format": "int64"},
                    "totalPages": {"type": "integer"},
                    "size": {"type": "integer"},
                    "number": {"type": "integer"},
                },
            },
            name,
        )
    inner = re.search(r"ApiResponse<(\w+)>", text)
    if inner and inner.group(1) not in {"Void", "void"}:
        name = inner.group(1)
        schema = {"$ref": f"#/components/schemas/{name}"} if name in known else {"type": "object"}
        return schema, name
    return {"nullable": True}, None


def _api_response_schema(data_schema: dict) -> dict:
    return {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "message": {"type": "string"},
            "data": data_schema,
            "timestamp": {"type": "string", "format": "date-time"},
        },
    }


def _parameters(params: list[str]) -> list[dict]:
    result = []
    for param in params:
        if "@RequestBody" in param:
            continue
        location = "path" if "@PathVariable" in param else "query" if "@RequestParam" in param else ""
        if not location:
            continue
        default = _annotation_value(param, "defaultValue")
        required = location == "path" or "required = false" not in param and "required=false" not in param
        if default and "@RequestParam" in param and "required" not in param:
            required = False
        cleaned = re.sub(r"@\w+(?:\s*\((?:[^()]|\([^()]*\))*\))?", " ", param)
        type_match = re.search(r"([\w.<>, ?]+)\s+(\w+)\s*$", cleaned.strip())
        if not type_match:
            continue
        schema = _java_type_schema(type_match.group(1), set())
        if default:
            schema = dict(schema)
            schema["default"] = default
        item = {"name": type_match.group(2), "in": location, "required": required, "schema": schema}
        description = _annotation_value(param, "description")
        if description:
            item["description"] = description
        result.append(item)
    return result


def _request_body_name(params: list[str], known: set[str]) -> str:
    for param in params:
        if "@RequestBody" not in param:
            continue
        match = re.search(r"@RequestBody\s+([\w.]+)", param)
        if not match:
            continue
        name = match.group(1).split(".")[-1]
        if name in known:
            return name
    return ""


def _ref_name(schema: dict | None) -> str:
    if not schema:
        return ""
    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[-1]
    for key in ("anyOf", "allOf", "oneOf"):
        for item in schema.get(key) or []:
            name = _ref_name(item)
            if name:
                return name
    items = schema.get("items")
    if isinstance(items, dict):
        return _ref_name(items)
    return schema.get("type") or ""


def render_markdown(spec: dict) -> str:
    info = spec.get("info") or {}
    lines = [
        f"# {info.get('title') or 'API'}",
        "",
        "这份文档给人阅读和评审。导入 Apifox 或 Apipost 时，选择 OpenAPI / Swagger，上传同目录的 `openapi.json`。不要把本文件当作接口定义导入。",
        "",
        "当前脚手架的业务接口默认不要求登录。某一条接口下面写了「鉴权」的，才是代码里已经加了登录约束；重新导出后以代码为准。",
        "",
        "## 接口",
        "",
    ]
    found = False
    for path, item in (spec.get("paths") or {}).items():
        for method in METHODS:
            operation = item.get(method)
            if not operation:
                continue
            found = True
            lines.append(f"### {method.upper()} `{path}`")
            lines.append("")
            summary = operation.get("summary") or operation.get("operationId") or ""
            if summary:
                lines.append(summary)
                lines.append("")
            security = operation.get("security")
            lines.append(f"- 鉴权：{security if security else '无'}")
            for param in operation.get("parameters") or []:
                required = "必填" if param.get("required") else "可选"
                desc = param.get("description") or ""
                lines.append(f"- 参数 `{param.get('name')}`（{param.get('in')}，{required}）{desc}")
            body = ((operation.get("requestBody") or {}).get("content") or {}).get("application/json") or {}
            body_name = _ref_name(body.get("schema"))
            if body_name:
                lines.append(f"- 请求体：`{body_name}`")
            responses = []
            for code, response in (operation.get("responses") or {}).items():
                content = (response or {}).get("content") or {}
                json_body = content.get("application/json") or {}
                name = _ref_name(json_body.get("schema"))
                responses.append(f"{code} {name}".strip())
            if responses:
                lines.append("- 响应：" + "、".join(responses))
            lines.append("")
    if not found:
        lines.append("当前项目没有可导出的业务接口。")
        lines.append("")
    schemas = ((spec.get("components") or {}).get("schemas")) or {}
    if schemas:
        lines.append("## 数据模型")
        lines.append("")
        for name, schema in schemas.items():
            lines.append(f"### `{name}`")
            lines.append("")
            props = schema.get("properties") or {}
            required = set(schema.get("required") or [])
            if not props:
                lines.append("无字段。")
                lines.append("")
                continue
            for prop, meta in props.items():
                kind = _ref_name(meta) or meta.get("type") or ""
                mark = "必填" if prop in required else "可选"
                lines.append(f"- `{prop}` {kind}（{mark}）")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    props = read_properties(PROPS)
    spec, prefixes = build_from_sources(props)
    port, context, docs_path = api_settings(props)
    live_url = f"http://127.0.0.1:{port}{context}{docs_path}"
    live = fetch_live(live_url)
    source = "controller 与 DTO"
    if live and live_matches(live, prefixes):
        spec = annotate_spec(live)
        if not spec.get("servers"):
            spec["servers"] = [{"url": f"http://127.0.0.1:{port}{context}", "description": "本地"}]
        source = f"已启动的应用 {live_url}"
    if not spec.get("paths"):
        print("没有找到 Controller，未写出接口文档")
        return 1
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "openapi.json").write_text(
        json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (DOCS / "api.md").write_text(render_markdown(spec), encoding="utf-8")
    print(f"source: {source}")
    print("wrote docs/openapi.json")
    print("wrote docs/api.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
