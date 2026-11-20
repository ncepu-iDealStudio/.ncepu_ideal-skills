#!/usr/bin/env python3
"""DSH 插件工程自检器（Python 标准库，零第三方依赖）。

对生成/手写的 DSH 插件目录做 18 项静态校验，覆盖「装了但不生效」的全部常见根因：
装配声明、包名一致性、Client bundle 格式、defineTool 契约、沙箱与主题约定。

用法：
    python validate_plugin.py <插件目录>
    python validate_plugin.py <插件目录> --quiet

退出码：0 = 通过（可能有警告）；1 = 存在错误。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PKG_RE = re.compile(r"^@[a-z0-9][a-z0-9._-]*/dsh-[a-z0-9][a-z0-9-]*$")
TOKEN_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")

SOURCE_SUFFIXES = (".ts", ".tsx", ".mts", ".cts", ".js", ".mjs")

OK = "OK"
FAIL = "FAIL"
WARN = "WARN"


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, level: str, title: str, detail: str = "") -> None:
        self.rows.append((level, title, detail))

    def ok(self, title: str, detail: str = "") -> None:
        self.add(OK, title, detail)

    def fail(self, title: str, detail: str = "") -> None:
        self.add(FAIL, title, detail)

    def warn(self, title: str, detail: str = "") -> None:
        self.add(WARN, title, detail)

    @property
    def errors(self) -> int:
        return sum(1 for level, _, _ in self.rows if level == FAIL)

    @property
    def warnings(self) -> int:
        return sum(1 for level, _, _ in self.rows if level == WARN)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def has_bom(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(3) == b"\xef\xbb\xbf"


def collect_sources(root: Path) -> list[Path]:
    src = root / "src"
    if not src.is_dir():
        return []
    return [
        path
        for path in src.rglob("*")
        if path.is_file() and path.suffix in SOURCE_SUFFIXES
    ]


def check(root: Path) -> Report:
    report = Report()

    # 1. 必需文件
    required = [
        "package.json",
        "tsconfig.json",
        "tsdown.config.ts",
        "cordis.patch.yml",
        "src/index.ts",
        "README.md",
        "DEVELOPMENT.md",
    ]
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        report.fail("目录结构", "缺少文件：" + "、".join(missing))
    else:
        report.ok("目录结构", "package.json / tsconfig / tsdown / cordis.patch.yml / src/index.ts 齐全")

    manifest: dict = {}
    manifest_path = root / "package.json"
    if manifest_path.is_file():
        try:
            manifest = read_json(manifest_path)
            report.ok("package.json 可解析")
        except json.JSONDecodeError as exc:
            report.fail("package.json 不是合法 JSON", str(exc))

    package_name = manifest.get("name", "") if manifest else ""
    if package_name:
        if PKG_RE.match(package_name):
            report.ok("包名格式", package_name)
        else:
            report.fail("包名格式", f"{package_name} 应形如 @your-scope/dsh-xxx")
        if package_name.startswith("@deepseek-ai/"):
            report.fail("命名空间", "不允许占用官方 @deepseek-ai 命名空间")
    slug = package_name.split("/", 1)[1] if "/" in package_name else package_name

    # 3. 入口指向
    if manifest:
        main_ok = manifest.get("main") == "lib/index.mjs"
        exports = manifest.get("exports") or {}
        root_export = exports.get(".") or {}
        export_ok = str(root_export.get("default", "")) == "./lib/index.mjs"
        if main_ok and export_ok:
            report.ok("Host 入口", "main / exports['.'] 指向 lib/index.mjs")
        else:
            report.fail(
                "Host 入口",
                f"main={manifest.get('main')} exports['.'].default={root_export.get('default')}，应指向 lib/index.mjs",
            )

    # 4. bundle patch 声明
    bundle_patch = ((manifest.get("dsh") or {}).get("bundle") or {}).get("patch") if manifest else None
    if bundle_patch is None:
        report.fail("dsh.bundle.patch", "缺失 → dsh plugin add 只当普通依赖，路由与设置页都不生效且不报错")
    else:
        patch_path = (root / bundle_patch).resolve()
        if patch_path.is_file():
            report.ok("dsh.bundle.patch", str(bundle_patch))
        else:
            report.fail("dsh.bundle.patch", f"{bundle_patch} 指向的文件不存在")

    # 5. cordis.patch.yml 内容
    patch_file = root / "cordis.patch.yml"
    if patch_file.is_file():
        patch_text = read_text(patch_file)
        if slug and f"id: {slug}" in patch_text:
            report.ok("cordis.patch.yml id", slug)
        else:
            report.warn("cordis.patch.yml id", f"未找到 `id: {slug}`，建议与插件 id 保持一致")
        if package_name and f"name: '{package_name}'" in patch_text or (
            package_name and f'name: "{package_name}"' in patch_text
        ):
            report.ok("cordis.patch.yml name", package_name)
        else:
            report.fail("cordis.patch.yml name", f"name 必须等于包名 {package_name}")
        if "insert:" not in patch_text:
            report.fail("cordis.patch.yml 结构", "缺少 insert: 段，插件不会进入 profile 的插件清单")

    # 6. tsdown PLUGIN_ID
    tsdown_file = root / "tsdown.config.ts"
    tsdown_text = read_text(tsdown_file) if tsdown_file.is_file() else ""
    if tsdown_text:
        match = re.search(r"PLUGIN_ID\s*=\s*['\"]([^'\"]+)['\"]", tsdown_text)
        if match is None:
            report.fail("tsdown PLUGIN_ID", "未找到 const PLUGIN_ID")
        elif match.group(1) != package_name:
            report.fail("tsdown PLUGIN_ID", f"{match.group(1)} ≠ 包名 {package_name}")
        else:
            report.ok("tsdown PLUGIN_ID", package_name)

    # 7. Client 目标与 wrapper
    dsh_client = (manifest.get("dsh") or {}).get("client") if manifest else None
    client_source = root / "src" / "client" / "index.ts"
    client_export = ((manifest.get("exports") or {}).get("./client") or {}) if manifest else {}
    if dsh_client is not None:
        problems = []
        if not client_source.is_file():
            problems.append("缺少 src/client/index.ts")
        if str(client_export.get("default", "")) != "./lib/client.js":
            problems.append("exports['./client'].default 应指向 ./lib/client.js")
        if "src/client/index.ts" not in tsdown_text:
            problems.append("tsdown.config.ts 缺少 client 目标")
        if "__ModuleLoader__" not in tsdown_text:
            problems.append("tsdown.config.ts 缺少 __ModuleLoader__ banner/footer 包装")
        if problems:
            report.fail("Client 半边装配", "；".join(problems))
        else:
            report.ok("Client 半边装配", "dsh.client + exports['./client'] + tsdown 双目标一致")
    else:
        if client_source.is_file():
            report.warn("Client 半边", "存在 src/client/index.ts 但 package.json 未声明 dsh.client，浏览器侧不会加载")

    # 8. tsconfig paths
    tsconfig_file = root / "tsconfig.json"
    if tsconfig_file.is_file() and dsh_client is not None:
        try:
            tsconfig = read_json(tsconfig_file)
            paths = (tsconfig.get("compilerOptions") or {}).get("paths") or {}
            expected = f"{package_name}/client"
            if expected in paths:
                report.ok("tsconfig paths", expected)
            else:
                report.warn("tsconfig paths", f"建议加 {expected} → ./src/client/index.ts")
        except json.JSONDecodeError as exc:
            report.fail("tsconfig.json 不是合法 JSON", str(exc))

    # 9. peerDependencies 必须声明 cordis
    peer = (manifest.get("peerDependencies") or {}) if manifest else {}
    if "@deepseek-ai/cordis" in peer:
        report.ok("peerDependencies", "@deepseek-ai/cordis 已声明")
    else:
        report.fail("peerDependencies", "缺 @deepseek-ai/cordis，运行期会出现 cordis 类型不匹配")

    # 10. 源码禁止使用 input_schema / 注册 run_code
    sources = collect_sources(root)
    if not sources:
        report.fail("源码目录", "src/ 下没有源码文件")
    joined = "\n".join(read_text(path) for path in sources)
    if "input_schema" in joined:
        report.fail("工具 schema 写法", "出现 input_schema：原生形状只有 {name, description, parameters}")
    else:
        report.ok("工具 schema 写法", "未使用 input_schema")
    if re.search(r"name:\s*['\"]run_code['\"]", joined):
        report.fail("保留工具名", "run_code 是 Code Mode 保留传输名，不能注册")
    else:
        report.ok("保留工具名", "未占用 run_code")

    # 11. defineTool 必须有 output
    host_source = root / "src" / "index.ts"
    host_text = read_text(host_source) if host_source.is_file() else ""
    if "defineTool(" in joined:
        for block_source in sources:
            text = read_text(block_source)
            if "defineTool(" not in text:
                continue
            if "output:" not in text:
                report.fail("defineTool 契约", f"{block_source.name} 缺少 output: {{schema, render}}（注册会失败）")
            elif "schema:" not in text or "render:" not in text:
                report.fail("defineTool 契约", f"{block_source.name} 的 output 必须同时有 schema 与 render")
            else:
                report.ok("defineTool 契约", f"{block_source.name} 具备 output.schema + render")
            if re.search(r"additionalProperties", text) is None:
                report.warn("JSON Schema", f"{block_source.name} 的 object schema 需显式写 additionalProperties: true/false")

    # 12. 路由必须包在 ctx.effect 里
    if "webServer.register" in joined:
        route_ok = True
        for block_source in sources:
            text = read_text(block_source)
            if "webServer.register" in text and "ctx.effect" not in text:
                report.fail("路由生命周期", f"{block_source.name} 的 register 未包在 ctx.effect 中，卸载时不会注销")
                route_ok = False
        if route_ok:
            report.ok("路由生命周期", "webServer.register 均在 ctx.effect 内")

    # 13. inject 声明
    if "export const inject" in host_text:
        names = re.search(r"export const inject\s*=\s*\[([^\]]*)\]", host_text)
        report.ok("inject 声明", (names.group(1).replace("'", "").strip() if names else "已声明"))
    elif "ctx.on(" in host_text:
        report.warn("inject 声明", "事件型插件可不需要 inject；若用到 tools/webServer 服务请补 inject")
    else:
        report.warn("inject 声明", "src/index.ts 未声明 inject，确认没有用 ctx.get 读取关键服务")

    # 14. BOM
    bom_files = [path.name for path in [manifest_path, tsconfig_file, patch_file] if path.is_file() and has_bom(path)]
    if bom_files:
        report.fail("UTF-8 BOM", "以下文件带 BOM，会导致 JSON/curl 输出异常：" + "、".join(bom_files))
    else:
        report.ok("编码", "配置与源码无 BOM")

    # 15. 未替换的占位符
    leftover = [
        path.name
        for path in ([manifest_path, patch_file, host_source] + sources)
        if path.is_file() and TOKEN_RE.search(read_text(path))
    ]
    if leftover:
        report.fail("占位符", "仍有未替换的 {{...}}：" + "、".join(sorted(set(leftover))))
    else:
        report.ok("占位符", "全部已替换")

    # 16. 已构建的产物是否合规
    client_bundle = root / "lib" / "client.js"
    if client_bundle.is_file():
        head = client_bundle.read_text(encoding="utf-8-sig")[:400]
        if "__ModuleLoader__.load(" not in head:
            report.fail("lib/client.js 格式", "开头不是 window.__ModuleLoader__.load(...)，浏览器侧加载不到")
        elif package_name and package_name not in head:
            report.fail("lib/client.js id", f"bundle 的 id 必须等于包名 {package_name}")
        else:
            report.ok("lib/client.js 格式", "ModuleLoader 包装与 id 正确")
    else:
        report.warn("构建产物", "lib/client.js 不存在（尚未 pnpm build，正常）")

    # 17. Client 侧硬编码颜色
    client_text = read_text(client_source) if client_source.is_file() else ""
    color_hits = HEX_COLOR_RE.findall(client_text)
    if color_hits:
        report.warn(
            "主题令牌",
            "Client 源码出现硬编码颜色（" + "、".join(sorted(set(color_hits))[:3]) + "），深色主题下会失效",
        )
    elif client_text:
        report.ok("主题令牌", "未发现硬编码颜色")

    # 18. 结构化错误
    if re.search(r"throw new Error\(", joined) and "ok: false" not in joined:
        report.warn("错误处理", "存在裸抛异常且未见 { ok: false, error } 结构化返回")
    else:
        report.ok("错误处理", "使用 { ok, error } 结构化返回")

    return report


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    quiet = "--quiet" in args
    args = [item for item in args if item != "--quiet"]
    root = Path(args[0]).resolve() if args else Path.cwd()

    if not root.is_dir():
        print(f"[validate] 目录不存在：{root}", file=sys.stderr)
        return 2

    report = check(root)
    print("=" * 68)
    print(f"DSH 插件自检：{root}")
    print("=" * 68)
    for level, title, detail in report.rows:
        if quiet and level == OK:
            continue
        mark = {OK: "[ OK ]", FAIL: "[FAIL]", WARN: "[WARN]"}[level]
        line = f"{mark} {title}"
        print(line + (f" —— {detail}" if detail else ""))
    print("-" * 68)
    total = len(report.rows)
    print(f"共 {total} 项：通过 {total - report.errors - report.warnings}，警告 {report.warnings}，错误 {report.errors}")
    if report.errors:
        print("结论：存在错误，先修上面 [FAIL] 项，再 pnpm build。")
        return 1
    print("结论：静态检查通过。别忘了跑 pnpm typecheck && pnpm build 做真正的编译验证。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
