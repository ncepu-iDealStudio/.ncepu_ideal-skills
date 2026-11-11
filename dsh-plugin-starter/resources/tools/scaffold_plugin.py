#!/usr/bin/env python3
"""DSH 插件起步项目生成器（Python 标准库，零第三方依赖）。

输入：一份插件 spec（JSON 文件）+ 插件类型
输出：一个可用 VSCode 打开、`pnpm install && pnpm build` 即可构建的 DSH 插件工程

用法：
    # 1) 推荐：用 spec 文件（模型根据需求澄清结果填写）
    python scaffold_plugin.py --spec my-plugin.json --out ./dsh-notebook

    # 2) 命令行直给（快速起步）
    python scaffold_plugin.py --type tool-only --name @me/dsh-foo --out ./dsh-foo \\
        --tool foo_run --desc-zh "把输入回显出来"

    # 3) 只预览将要生成的文件
    python scaffold_plugin.py --spec my-plugin.json --out ./x --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = SKILL_ROOT / "resources" / "templates"

PLUGIN_TYPES = ("tool-only", "route-only", "dual-face", "interceptor")

# 每种插件类型需要渲染哪些模板目录（dual-face = Host 用 route-only + 自己的 Client）
TYPE_TEMPLATE_DIRS = {
    "tool-only": ("tool-only",),
    "route-only": ("route-only",),
    "dual-face": ("route-only", "dual-face"),
    "interceptor": ("interceptor",),
}

TYPE_HINT = {
    "tool-only": "模型可调用的工具",
    "route-only": "HTTP 路由",
    "dual-face": "HTTP 路由 + 设置页界面",
    "interceptor": "工具执行拦截器",
}

# README 目录树里对 Host 文件的一句话说明
HOST_ROLE = {
    "tool-only": "注册工具（defineTool）",
    "route-only": "注册 HTTP 路由",
    "dual-face": "注册 HTTP 路由",
    "interceptor": "监听工具拦截事件",
}

PKG_RE = re.compile(r"^@[a-z0-9][a-z0-9._-]*/dsh-[a-z0-9][a-z0-9-]*$")
SLUG_RE = re.compile(r"^dsh-[a-z0-9][a-z0-9-]*$")
TOOL_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
ROUTE_RE = re.compile(r"^/[a-z0-9][a-z0-9-]*$")

PARAM_TYPES = {
    "string": ("string", "string"),
    "number": ("number", "number"),
    "boolean": ("boolean", "boolean"),
    "string[]": ("string[]", "string[]"),
}

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


class ScaffoldError(Exception):
    """spec 不合法或目标目录不可写时抛出。"""


# --------------------------------------------------------------------------- #
# spec 处理
# --------------------------------------------------------------------------- #
def default_spec() -> dict:
    return {
        "plugin": {
            "packageName": None,
            "slug": None,
            "type": "tool-only",
            "version": "0.1.0",
            "license": "MIT",
            "author": "",
            "repoUrl": "",
            "displayNameZh": None,
            "displayNameEn": None,
            "descriptionZh": "",
            "descriptionEn": "",
        },
        "capability": {
            "summary": "",
            "toolName": None,
            "toolDescription": "",
            "routePrefix": None,
            "parameters": [],
        },
    }


def deep_merge(base: dict, patch: dict) -> dict:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        elif value is not None:
            base[key] = value
    return base


def load_spec(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise ScaffoldError(f"spec 文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ScaffoldError(f"spec 不是合法 JSON：{path} → {exc}") from exc
    if not isinstance(data, dict):
        raise ScaffoldError("spec 顶层必须是对象")
    return data


def normalize_spec(spec: dict) -> dict:
    """补默认值、推导派生的命名，并做硬校验。"""
    plugin = spec["plugin"]
    capability = spec["capability"]

    package_name = (plugin.get("packageName") or "").strip()
    slug = (plugin.get("slug") or "").strip()

    if package_name == "" and slug != "":
        raise ScaffoldError(
            "缺少 plugin.packageName：DSH 要求包名带自己的命名空间，例如 @your-scope/" + slug
        )
    if package_name == "":
        raise ScaffoldError("缺少 plugin.packageName（例如 @your-scope/dsh-my-plugin）")
    if not PKG_RE.match(package_name):
        raise ScaffoldError(
            f"包名不合法：{package_name}；必须形如 @your-scope/dsh-xxx（小写、不能用官方 @deepseek-ai 命名空间）"
        )
    if package_name.startswith("@deepseek-ai/"):
        raise ScaffoldError("不允许占用官方 @deepseek-ai 命名空间，请换成自己的 scope")

    if slug == "":
        slug = package_name.split("/", 1)[1]
    if not SLUG_RE.match(slug):
        raise ScaffoldError(f"插件 id 不合法：{slug}；必须形如 dsh-xxx（小写短横线）")
    if package_name.split("/", 1)[1] != slug:
        raise ScaffoldError(
            f"包名的最后一段必须等于插件 id：{package_name} vs {slug}（包名是 DSH 的唯一注册键）"
        )

    plugin_type = (plugin.get("type") or "tool-only").strip()
    if plugin_type not in PLUGIN_TYPES:
        raise ScaffoldError(f"未知插件类型：{plugin_type}；可选：{', '.join(PLUGIN_TYPES)}")

    tool_name = (capability.get("toolName") or "").strip()
    route_prefix = (capability.get("routePrefix") or "").strip()

    if plugin_type in ("tool-only", "interceptor") and tool_name == "":
        if plugin_type == "tool-only":
            raise ScaffoldError("tool-only 类型必须提供 capability.toolName（模型可见的工具名，snake_case）")
    if tool_name != "" and not TOOL_RE.match(tool_name):
        raise ScaffoldError(f"工具名不合法：{tool_name}；必须是 snake_case，且不能是保留名 run_code")
    if tool_name == "run_code":
        raise ScaffoldError("run_code 是 DSH 保留的 Code Mode 传输名，不能注册成工具")

    if plugin_type in ("route-only", "dual-face"):
        if route_prefix == "":
            raise ScaffoldError("route-only / dual-face 类型必须提供 capability.routePrefix（例如 /notes）")
        if not ROUTE_RE.match(route_prefix):
            raise ScaffoldError(f"路由前缀不合法：{route_prefix}；必须形如 /notes（绝对路径、无尾斜杠）")
        if route_prefix.endswith("/"):
            raise ScaffoldError("路由前缀不能以 / 结尾")

    plugin["packageName"] = package_name
    plugin["slug"] = slug
    plugin["type"] = plugin_type
    plugin["version"] = (plugin.get("version") or "0.1.0").strip()
    plugin["license"] = (plugin.get("license") or "MIT").strip()
    plugin["displayNameZh"] = (plugin.get("displayNameZh") or slug).strip()
    plugin["displayNameEn"] = (plugin.get("displayNameEn") or slug).strip()
    plugin["descriptionZh"] = (plugin.get("descriptionZh") or f"{slug} —— DSH 插件").strip()
    plugin["descriptionEn"] = (plugin.get("descriptionEn") or f"{slug} — a DSH plugin").strip()

    capability["toolName"] = tool_name
    capability["routePrefix"] = route_prefix
    parameters = capability.get("parameters") or []
    if not isinstance(parameters, list):
        raise ScaffoldError("capability.parameters 必须是数组")
    for item in parameters:
        if not isinstance(item, dict) or not item.get("name"):
            raise ScaffoldError("capability.parameters 的每一项都必须包含 name")
        if item.get("type", "string") not in PARAM_TYPES:
            raise ScaffoldError(
                f"参数 {item.get('name')} 的类型 {item.get('type')} 不支持；可选：{', '.join(PARAM_TYPES)}"
            )
    if plugin_type == "tool-only" and len(parameters) == 0:
        parameters = [
            {
                "name": "input",
                "type": "string",
                "required": True,
                "description": "待处理的内容（替换成你的业务入参）",
            }
        ]
    capability["parameters"] = parameters
    capability["toolDescription"] = (
        capability.get("toolDescription") or "把输入原样回显，用于验证工具链路。当用户需要确认插件已生效时使用。"
    ).strip()
    capability["summary"] = (capability.get("summary") or plugin["descriptionZh"]).strip()

    return spec


# --------------------------------------------------------------------------- #
# 渲染
# --------------------------------------------------------------------------- #
def pascal_case(slug: str) -> str:
    body = slug[4:] if slug.startswith("dsh-") else slug
    return "".join(part.capitalize() for part in body.split("-") if part)


def quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def render_parameters_ts(parameters: list) -> str:
    lines = []
    for item in parameters:
        schema_type = PARAM_TYPES[item.get("type", "string")][0]
        required = item.get("required") is True
        desc = quote(item.get("description") or "")
        extra = f", description: '{desc}'" if desc else ""
        if schema_type == "string[]":
            lines.append(
                f"      {item['name']}: {{ type: 'array', items: {{ type: 'string' }}, "
                f"required: {'true' if required else 'false'}{extra} }},"
            )
        else:
            required_part = ", required: true" if required else ""
            lines.append(f"      {item['name']}: {{ type: '{schema_type}'{required_part}{extra} }},")
    return "\n".join(lines)


def render_input_fields(parameters: list) -> str:
    lines = []
    for item in parameters:
        ts_type = PARAM_TYPES[item.get("type", "string")][1]
        optional = "" if item.get("required") is True else "?"
        lines.append(f"  {item['name']}{optional}: {ts_type}")
    return "\n".join(lines) if lines else "  // 当前没有入参，按需补充"


def build_tokens(spec: dict) -> dict:
    plugin = spec["plugin"]
    capability = spec["capability"]
    slug = plugin["slug"]
    plugin_type = plugin["type"]
    params = capability["parameters"]

    package_name = plugin["packageName"]
    pascal = pascal_case(slug)
    camel = pascal[0].lower() + pascal[1:] if pascal else "capability"
    route_prefix = capability["routePrefix"] or "/plugin"
    env_prefix = slug.replace("-", "_").upper()

    author = (plugin.get("author") or "").strip()
    repo = (plugin.get("repoUrl") or "").strip()

    if plugin_type == "dual-face":
        host_purpose = (
            f"注册 {route_prefix} 前缀下的 HTTP POST 路由，供 src/client 的设置页用 fetch() 调用。"
        )
        client_tree = (
            "│   └── client/\n"
            "│       └── index.ts        # Client 半边：设置页区块（settings.section）\n"
        )
        client_artifact = " + lib/client.js"
        dev_lib_tree = "└── client.js        # Client 半边（CJS，浏览器用）\n"
        dev_files_extra = ', "lib/client.js", "lib/types/client/index.d.ts"'
        verify_steps = (
            "验证步骤（带界面）：\n\n"
            "1. `dsh web --port 3081` 重启 DSH。\n"
            f"2. 打开设置页，找到「{plugin['displayNameZh']}」区块。\n"
            f"3. 输入内容点「执行」，应看到 `{{ ok: true, value: ... }}` 结果（说明 Host 路由通）。\n"
        )
    elif plugin_type == "route-only":
        host_purpose = f"注册 {route_prefix} 前缀下的 HTTP POST 路由，由外部脚本 / 其他系统调用（本插件无界面）。"
        client_tree = ""
        client_artifact = ""
        dev_lib_tree = ""
        dev_files_extra = ""
        verify_steps = (
            "验证步骤（无界面，直接打路由）：\n\n"
            "```bash\n"
            f"curl -X POST http://127.0.0.1:3081{route_prefix}/ping\n"
            f"curl -X POST http://127.0.0.1:3081{route_prefix}/run -H 'content-type: application/json' -d '{{\"text\":\"hi\"}}'\n"
            "```\n"
        )
    elif plugin_type == "interceptor":
        host_purpose = "监听 tools/pre-execute 事件（waterfall），按策略拒绝或放行工具调用。"
        client_tree = ""
        client_artifact = ""
        dev_lib_tree = ""
        dev_files_extra = ""
        verify_steps = (
            "验证步骤（拦截器）：\n\n"
            "1. `dsh web --port 3081` 重启 DSH。\n"
            "2. 让 Agent 调用一个不在白名单里的工具，应收到拒绝原因。\n"
            f"3. 设置环境变量 {env_prefix}_ALLOW 放行后重试。\n"
        )
    else:
        host_purpose = f"向模型注册工具 {capability['toolName']}（defineTool），模型可直接调用。"
        client_tree = ""
        client_artifact = ""
        dev_lib_tree = ""
        dev_files_extra = ""
        verify_steps = (
            "验证步骤（tool 型）：\n\n"
            "1. `dsh web --port 3081` 重启 DSH。\n"
            f"2. 让 Agent 调用工具 `{capability['toolName']}`，观察调用入参与返回。\n"
        )

    tokens = {
        "PKG_NAME": package_name,
        "SLUG": slug,
        "SLUG_UPPER": slug.replace("-", "_").upper(),
        "SLUG_UNDERSCORE": slug.replace("-", "_"),
        "PASCAL": pascal,
        "CAMEL": camel,
        "VERSION": plugin["version"],
        "LICENSE": plugin["license"],
        "AUTHOR": author,
        "AUTHOR_LINE": f'\n  "author": {json.dumps(author, ensure_ascii=False)},' if author else "",
        "REPO_URL": repo,
        "REPO_LINE": (
            f'\n  "repository": {{ "type": "git", "url": {json.dumps(repo, ensure_ascii=False)} }},'
            if repo
            else ""
        ),
        "DISPLAY_ZH": plugin["displayNameZh"],
        "DISPLAY_EN": plugin["displayNameEn"],
        "DESCRIPTION_ZH": plugin["descriptionZh"],
        "DESCRIPTION_EN": plugin["descriptionEn"],
        "TYPE": plugin_type,
        "TYPE_HINT": TYPE_HINT[plugin_type],
        "HOST_ROLE": HOST_ROLE[plugin_type],
        "HOST_PURPOSE": host_purpose,
        "TOOL_NAME": capability["toolName"] or "my_tool",
        "TOOL_DESCRIPTION": quote(capability["toolDescription"]),
        "PARAMETERS_TS": render_parameters_ts(params),
        "INPUT_FIELDS": render_input_fields(params),
        "ROUTE_PREFIX": route_prefix,
        "ENV_PREFIX": slug.replace("-", "_").upper(),
        "PLACEHOLDER_ZH": "输入要交给插件处理的内容",
        "PLACEHOLDER_EN": "Text to process",
        "CREATED_AT": date.today().isoformat(),
        "YEAR": str(date.today().year),
        "CLIENT_TREE": client_tree,
        "CLIENT_ARTIFACT": client_artifact,
        "DEV_LIB_TREE": dev_lib_tree,
        "DEV_FILES_EXTRA": dev_files_extra,
        "VERIFY_STEPS": verify_steps,
        # 由 scaffold() 填充：按类型渲染的《开发指南》扩展章节
        "DEV_TYPE_SECTION": "",
    }
    tokens.update(build_manifest_tokens(plugin, plugin_type))
    return tokens


def build_type_section(spec: dict, tokens: dict) -> str:
    """把 sections/<type>.md.tpl 渲染成《开发指南》第 5 章的内容。"""
    plugin_type = spec["plugin"]["type"]
    path = TEMPLATE_ROOT / "sections" / f"{plugin_type}.md.tpl"
    if not path.is_file():
        raise ScaffoldError(f"缺少类型章节模板：{path}")
    return render_text(path.read_text(encoding="utf-8"), tokens, path.name)


def build_manifest_tokens(plugin: dict, plugin_type: str) -> dict:
    """package.json / tsconfig.json / tsdown.config.ts 里与类型相关的片段。"""
    has_client = plugin_type == "dual-face"
    package_name = plugin["packageName"]

    dsh_packages = {
        "tool-only": ["@deepseek-ai/dsh-tools"],
        "interceptor": ["@deepseek-ai/dsh-tools"],
        "route-only": ["@deepseek-ai/dsh-host-webserver"],
        "dual-face": [
            "@deepseek-ai/dsh-host-webserver",
            "@deepseek-ai/dsh-client-runtime",
            "@deepseek-ai/dsh-client-ui-slots",
            "@deepseek-ai/dsh-client-ui-settings",
            "@deepseek-ai/dsh-client-locale",
        ],
    }[plugin_type]

    peer_lines = "".join(f',\n    "{name}": "^0.1.0-rc.7"' for name in dsh_packages)
    if has_client:
        peer_lines += ',\n    "react": "^18.2.0"'

    # devDependencies 的模板里 cordis 之后已经带逗号，这里续写时不重复加
    dev_lines = "".join(f'\n    "{name}": "^0.1.0-rc.7",' for name in dsh_packages)

    client_export = (
        f'\n    "./client": {{ "types": "./lib/types/client/index.d.ts", "default": "./lib/client.js" }},'
        if has_client
        else ""
    )
    client_file = '\n    "lib/client.js",' if has_client else ""

    dsh_client_block = ""
    if has_client:
        inject_lines = ",\n".join(
            f'        "{name}"'
            for name in (
                "@deepseek-ai/dsh-client-runtime",
                "@deepseek-ai/dsh-client-ui-slots",
                "@deepseek-ai/dsh-client-ui-settings",
                "@deepseek-ai/dsh-client-locale",
            )
        )
        dsh_client_block = (
            ',\n    "client": {\n      "inject": [\n'
            + inject_lines
            + '\n      ],\n      "platform": "web",\n      "immediately": true\n    }'
        )

    client_target = ""
    if has_client:
        client_target = (
            "\n\n"
            "  {\n"
            "    name: `${PLUGIN_ID}/client`,\n"
            "    entry: { client: 'src/client/index.ts' },\n"
            "    outDir: 'lib',\n"
            "    format: 'cjs',\n"
            "    platform: 'browser',\n"
            "    target: 'es2022',\n"
            "    dts: true,\n"
            "    clean: false,\n"
            "    deps: {\n"
            "      // DSH 模块表只认 react 与 @deepseek-ai/dsh-*，其余依赖必须内联\n"
            "      neverBundle: (id) => id === 'react' || id.startsWith('@deepseek-ai/dsh-'),\n"
            "      alwaysBundle: (id) => id !== 'react' && !id.startsWith('@deepseek-ai/dsh-'),\n"
            "    },\n"
            "    outputOptions: {\n"
            "      entryFileNames: 'client.js',\n"
            "      banner: `window.__ModuleLoader__.load({ id: ${JSON.stringify(PLUGIN_ID)}, factory: (require) => {`,\n"
            "      footer: 'return module.exports; } });',\n"
            "      intro: 'var module = { exports: {} }; var exports = module.exports;',\n"
            "    },\n"
            "  },"
        )

    ts_paths = ""
    if has_client:
        ts_paths = (
            ',\n    "baseUrl": ".",\n    "paths": {\n      '
            + json.dumps(package_name + "/client")
            + ': ["./src/client/index.ts"]\n    }'
        )

    return {
        "CLIENT_EXPORT": client_export,
        "CLIENT_FILE": client_file,
        "DSH_CLIENT_BLOCK": dsh_client_block,
        "PEER_DEPS": peer_lines,
        "DEV_DEPS": dev_lines,
        "DEV_REACT": '\n    "@types/react": "~18.3.1",\n    "react": "^18.2.0",' if has_client else "",
        "CLIENT_TARGET": client_target,
        "TS_PATHS": ts_paths,
    }


def render_text(text: str, tokens: dict, where: str) -> str:
    def substitute(match: re.Match) -> str:
        key = match.group(1)
        if key not in tokens:
            raise ScaffoldError(f"模板 {where} 使用了未定义的占位符 {{{{{key}}}}}")
        return str(tokens[key])

    rendered = TOKEN_RE.sub(substitute, text)
    if "{{" in rendered and TOKEN_RE.search(rendered):
        raise ScaffoldError(f"模板 {where} 渲染后仍有未替换的占位符")
    return rendered


def target_name(name: str) -> str:
    """gitignore.tpl → .gitignore；其余 .tpl 去掉后缀。"""
    if name == "gitignore.tpl":
        return ".gitignore"
    return name[:-4] if name.endswith(".tpl") else name


def collect_templates(plugin_type: str) -> list:
    files = []
    for dir_name in ("common",) + TYPE_TEMPLATE_DIRS[plugin_type]:
        base = TEMPLATE_ROOT / dir_name
        if not base.is_dir():
            raise ScaffoldError(f"模板目录缺失：{base}")
        for path in sorted(base.rglob("*")):
            if path.is_file():
                files.append((path, path.relative_to(base).as_posix()))
    return files


def scaffold(spec: dict, out_dir: Path, force: bool = False, dry_run: bool = False) -> list:
    plugin = spec["plugin"]
    tokens = build_tokens(spec)
    tokens["DEV_TYPE_SECTION"] = build_type_section(spec, tokens)

    if out_dir.exists() and any(out_dir.iterdir()) and not force:
        raise ScaffoldError(f"目标目录非空：{out_dir}（确认覆盖请加 --force）")

    written = []
    for source, relative in collect_templates(plugin["type"]):
        relative = target_name_path(relative)
        destination = out_dir / relative
        raw = source.read_text(encoding="utf-8")
        text = render_text(raw, tokens, source.name)
        written.append(destination)
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    return written


def target_name_path(relative: str) -> str:
    parts = relative.split("/")
    parts[-1] = target_name(parts[-1])
    return "/".join(parts)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="按 spec 生成 DSH 插件起步项目（支持 tool-only / route-only / dual-face / interceptor）",
    )
    parser.add_argument("--spec", type=Path, help="插件 spec JSON 文件")
    parser.add_argument("--out", type=Path, help="输出目录（默认 ./<插件id>）")
    parser.add_argument("--type", dest="plugin_type", choices=PLUGIN_TYPES, help="插件类型")
    parser.add_argument("--name", help="包名，例如 @your-scope/dsh-my-plugin")
    parser.add_argument("--slug", help="插件 id，例如 dsh-my-plugin（可由包名推导）")
    parser.add_argument("--tool", help="工具名（tool-only 用，snake_case）")
    parser.add_argument("--tool-desc", help="工具描述（写给模型看的）")
    parser.add_argument("--route", help="路由前缀，例如 /notes")
    parser.add_argument("--display-zh", help="中文显示名")
    parser.add_argument("--display-en", help="英文显示名")
    parser.add_argument("--desc-zh", help="中文描述")
    parser.add_argument("--desc-en", help="英文描述")
    parser.add_argument("--version", help="版本号，默认 0.1.0")
    parser.add_argument("--license", help="许可证，默认 MIT")
    parser.add_argument("--author", help="作者")
    parser.add_argument("--repo", help="仓库地址")
    parser.add_argument("--force", action="store_true", help="目标目录非空时覆盖同名文件")
    parser.add_argument("--dry-run", action="store_true", help="只打印将生成的文件，不写盘")
    return parser


def spec_from_args(args: argparse.Namespace) -> dict:
    spec = default_spec()
    if args.spec is not None:
        deep_merge(spec, load_spec(args.spec))

    plugin = spec["plugin"]
    capability = spec["capability"]
    overrides = {
        "packageName": args.name,
        "slug": args.slug,
        "type": args.plugin_type,
        "version": args.version,
        "license": args.license,
        "author": args.author,
        "repoUrl": args.repo,
        "displayNameZh": args.display_zh,
        "displayNameEn": args.display_en,
        "descriptionZh": args.desc_zh,
        "descriptionEn": args.desc_en,
    }
    for key, value in overrides.items():
        if value is not None:
            plugin[key] = value

    capability_overrides = {
        "toolName": args.tool,
        "toolDescription": args.tool_desc,
        "routePrefix": args.route,
    }
    for key, value in capability_overrides.items():
        if value is not None:
            capability[key] = value

    return spec


def print_summary(spec: dict, out_dir: Path, written: list, dry_run: bool) -> None:
    plugin = spec["plugin"]
    print("=" * 66)
    print(f"DSH 插件起步项目{'（预览）' if dry_run else '已生成'}")
    print("=" * 66)
    print(f"包名        : {plugin['packageName']}")
    print(f"插件 id     : {plugin['slug']}")
    print(f"类型        : {plugin['type']}（{TYPE_HINT[plugin['type']]}）")
    print(f"输出目录    : {out_dir}")
    print("-" * 66)
    for path in written:
        try:
            print("  " + path.relative_to(out_dir).as_posix())
        except ValueError:
            print("  " + str(path))
    print("-" * 66)
    if dry_run:
        print("以上为预览，未写入磁盘。去掉 --dry-run 即可生成。")
        return
    validator = Path(__file__).with_name("validate_plugin.py")
    print("下一步：")
    print(f"  1) cd {out_dir}")
    print("  2) pnpm install")
    print("  3) pnpm typecheck && pnpm build")
    print(f"  4) python \"{validator}\" \"{out_dir}\"")
    print(f"  5) dsh plugin --profile web add \"{out_dir}\"  &&  dsh web --port 3081")
    print("=" * 66)


def main(argv: list | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        spec = normalize_spec(spec_from_args(args))
        out_dir = args.out or Path(spec["plugin"]["slug"])
        written = scaffold(spec, out_dir, force=args.force, dry_run=args.dry_run)
    except ScaffoldError as exc:
        print(f"[scaffold] 失败：{exc}", file=sys.stderr)
        return 2
    print_summary(spec, out_dir, written, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
