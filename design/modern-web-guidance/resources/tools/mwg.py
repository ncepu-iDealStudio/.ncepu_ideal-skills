#!/usr/bin/env python3
"""modern-web-guidance 本地检索 CLI（零依赖、完全离线、无遥测）。

替代上游的 `npx -y modern-web-guidance@latest ...`：
    python3 resources/tools/mwg.py search "<2-5 词查询>"
    python3 resources/tools/mwg.py retrieve "<id>[,<id>...]"
    python3 resources/tools/mwg.py list [分类]
    python3 resources/tools/mwg.py categories

检索基于 build_index.py 生成的 guides_index.json（关键词加权 + 前缀匹配），
不联网、不调用任何外部服务。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX_FILE = HERE.parent / "guides_index.json"
GUIDES_DIR = HERE.parent / "guides"

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#.\-]*")

# 中文/口语查询 → 英文检索词映射。让中文用户不必先自行翻译。
# 键是中文词，值是会被追加到查询里的英文同义词（可多个）。
ZH_MAP: dict[str, str] = {
    "对话框": "dialog modal",
    "弹窗": "dialog modal popover",
    "模态": "modal dialog",
    "确认": "confirm dialog",
    "抽屉": "drawer navigation-drawer",
    "导航": "navigation navbar",
    "菜单": "menu",
    "表格": "table",
    "数据表": "table responsive-table",
    "表单": "form",
    "校验": "validation validate-input",
    "验证": "validation",
    "自动填充": "autofill",
    "登录": "sign-in passkey",
    "注册": "sign-up passkey",
    "暗色": "dark-mode",
    "深色": "dark-mode",
    "主题": "theme color-scheme dark-mode",
    "颜色": "color oklch contrast",
    "布局": "layout grid flexbox",
    "网格": "grid subgrid",
    "弹性": "flexbox",
    "容器查询": "container-queries",
    "响应式": "responsive-design",
    "动画": "animation transitions view-transitions",
    "过渡": "view-transitions transitions",
    "滚动": "scroll scroll-driven-animations",
    "视差": "parallax scroll",
    "提示": "tooltip popover hovercard",
    "气泡": "tooltip popover",
    "轮播": "carousel",
    "标签页": "tabs",
    "下拉": "select dropdown",
    "选择器": "select custom-select",
    "轮播图": "carousel",
    "进度": "progress progress-ring",
    "加载": "spinner loading skeleton",
    "图片": "image image-optimization",
    "字体": "typography font",
    "排版": "typography text",
    "无障碍": "accessibility a11y screen-reader",
    "可访问性": "accessibility a11y",
    "键盘": "keyboard focus accessibility",
    "焦点": "focus focus-visible",
    "性能": "performance",
    "首屏": "lcp performance",
    "交互延迟": "inp performance",
    "布局偏移": "cls performance",
    "预加载": "preload speculative-loading",
    "懒加载": "lazy-load",
    "安全": "security",
    "加密": "encryption client-side-encryption",
    "签名": "digital-signatures",
    "清理": "sanitize sanitize-untrusted-html trusted-types",
    "注入": "sanitize trusted-types xss",
    "密码": "passkey password",
    "通行密钥": "passkey passkeys",
    "组件": "web-components custom-elements",
    "自定义元素": "custom-elements web-components",
    "影子": "shadow-dom",
    "日期": "date calendar timezone",
    "时区": "timezone calendar",
    "日历": "calendar",
    "翻译": "translator built-in-ai",
    "摘要": "summarizer built-in-ai",
    "人工智能": "language-model built-in-ai prompt-api",
    "大模型": "language-model prompt-api",
    "本地模型": "language-model built-in-ai",
    "悬浮": "hovercard tooltip popover",
    "滚动条": "scrollbar",
    "锚点": "anchor-positioning",
    "定位": "anchor-positioning popover",
    "弹层": "popover top-layer",
    "遮罩": "backdrop dialog",
    "开关": "switch",
    "滑块": "slider",
    "复选框": "checkbox",
    "单选": "radio checkbox",
    "手风琴": "accordion",
    "折叠": "accordion details",
    "提示框": "toast toast-notifications",
    "吐司": "toast persistent-toast-notifications",
    "引导": "app-tours persistent-app-tours",
    "拖拽": "drag-and-drop drag",
    "排序": "sortable-table dynamic-sort",
    "搜索": "search-hidden-content",
    "分享": "share",
    "图标": "icons",
    "徽标": "badge icons",
    "波纹": "visual-effects",
    "滤镜": "visual-effects shaders",
    "画布": "canvas webgl",
    "渐变": "visual-effects color",
    "阴影": "visual-effects box-shadow",
    "毛玻璃": "visual-effects backdrop-filter",
    "扩展": "chrome-extensions",
    "缓存": "storage service-worker",
    "离线": "service-worker pwa",
    "推送": "notifications service-worker",
    "工作线程": "service-worker",
    "警告": "security validate-origins",
    "跨域": "cors validate-origins",
}

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is",
    "it", "of", "on", "or", "that", "the", "this", "to", "use", "using", "with",
    "when", "which", "how", "what", "why", "do", "does", "not", "your", "you",
    "into", "can", "if", "its", "their", "they", "these", "than", "then", "also",
    "more", "most", "some", "such", "over", "under", "each", "any", "all",
    "about", "after", "before", "between", "within", "via", "per",
}


def load_index() -> dict:
    if not INDEX_FILE.exists():
        sys.exit(
            f"索引不存在：{INDEX_FILE}\n"
            f"请先运行：python3 {HERE / 'build_index.py'}"
        )
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


def expand_query(query: str) -> str:
    """把中文词映射成英文同义词，追加到查询后面。"""
    extras: list[str] = []
    for zh, en in ZH_MAP.items():
        if zh in query:
            extras.append(en)
    return " ".join([query] + extras)


def tokenize(text: str) -> list[str]:
    out: list[str] = []
    for m in TOKEN_RE.finditer(text.lower()):
        t = m.group(0).strip(".-+#")
        if len(t) >= 2 and t not in STOPWORDS and not t.isdigit():
            out.append(t)
    return out


def score_guide(guide: dict, qtokens: list[str]) -> tuple[float, list[str]]:
    if not qtokens:
        return 0.0, []
    title = guide["title"].lower()
    gid = guide["id"].lower().replace("-", " ")
    kws = set(guide.get("keywords", []))
    summary = guide.get("summary", "").lower()
    cat = guide["category"].lower().replace("-", " ")

    matched: list[str] = []
    score = 0.0
    exact_id = guide["id"].lower()
    for qt in qtokens:
        hit = False
        # id 命中权重最高（用户常按能力名检索）
        if qt == exact_id or (len(qt) > 3 and qt in exact_id):
            score += 12.0
            hit = True
        # 标题命中
        if qt in title:
            score += 8.0
            hit = True
        # 关键词精确命中
        if qt in kws:
            score += 5.0
            hit = True
        else:
            # 关键词前缀命中（如 "dialog" 命中 "dialogs"）
            for kw in guide.get("keywords", []):
                if kw.startswith(qt) or (len(qt) > 3 and qt.startswith(kw)):
                    score += 2.0
                    hit = True
                    break
        if qt in gid:
            score += 3.0
            hit = True
        if qt in summary:
            score += 2.0
            hit = True
        if qt in cat:
            score += 1.0
            hit = True
        if hit:
            matched.append(qt)
    # 覆盖率奖励：命中查询词越全，越相关
    score += 6.0 * (len(matched) / len(qtokens))
    return score, matched


def cmd_search(query: str, top: int, as_json: bool) -> int:
    idx = load_index()
    expanded = expand_query(query)
    qtokens = tokenize(expanded)
    scored: list[tuple[float, dict, list[str]]] = []
    for g in idx["guides"]:
        s, matched = score_guide(g, qtokens)
        if s > 0:
            scored.append((s, g, matched))
    scored.sort(key=lambda x: (-x[0], x[1]["id"]))

    results = [
        {
            "id": g["id"],
            "category": g["category"],
            "title": g["title"],
            "summary": g["summary"][:160],
            "score": round(s, 1),
        }
        for s, g, _ in scored[:top]
    ]

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0 if results else 2

    if not results:
        print(f'未找到与「{query}」相关的指南。')
        print("建议：换成更具体的 HTML/CSS/UI 组件名词（dialog / modal / popover / table / form），")
        print("或运行 `python3 resources/tools/mwg.py categories` 浏览全部主题。")
        return 2

    print(f'查询「{query}」→ {len(results)} 条结果（共 {idx["meta"]["guide_count"]} 份指南）：\n')
    for r in results:
        print(f'  [{r["score"]:>5}] {r["id"]}  ({r["category"]})')
        print(f'          {r["title"]}')
        if r["summary"]:
            print(f'          {r["summary"][:120]}')
    print("\n下一步：python3 resources/tools/mwg.py retrieve \"<id>\"")
    return 0


def cmd_retrieve(ids: str) -> int:
    idx = load_index()
    by_id = {g["id"]: g for g in idx["guides"]}
    wanted = [x.strip() for x in ids.split(",") if x.strip()]
    missing = [x for x in wanted if x not in by_id]
    if missing:
        print(f"以下 id 不存在：{', '.join(missing)}", file=sys.stderr)
        print("可用 id 见：python3 resources/tools/mwg.py list", file=sys.stderr)
        return 1
    for i, wid in enumerate(wanted):
        g = by_id[wid]
        path = GUIDES_DIR / g["path"]
        if not path.exists():
            print(f"指南文件缺失：{path}", file=sys.stderr)
            return 1
        if i:
            print("\n" + "=" * 72 + "\n")
        print(f'<!-- id: {wid} | category: {g["category"]} | source: {g["path"]} -->\n')
        # 全文输出，绝不截断（大文件也完整打印，交给调用方的文件读取工具处理）
        content = path.read_text(encoding="utf-8")
        sys.stdout.write(content)
        if not content.endswith("\n"):
            print()
    return 0


def cmd_list(category: str | None, as_json: bool) -> int:
    idx = load_index()
    guides = idx["guides"]
    if category:
        guides = [g for g in guides if g["category"] == category]
        if not guides:
            print(f"没有分类「{category}」。可用分类：", file=sys.stderr)
            print("  " + ", ".join(idx["categories"]), file=sys.stderr)
            return 1
    if as_json:
        print(json.dumps(guides, ensure_ascii=False, indent=2))
        return 0
    current = None
    for g in sorted(guides, key=lambda x: (x["category"], x["id"])):
        if g["category"] != current:
            current = g["category"]
            print(f'\n### {current}（{idx["categories"].get(current, 0)}）')
        print(f'  {g["id"]:<40} {g["title"]}')
    print(f'\n共 {len(guides)} 份指南。')
    return 0


def cmd_categories() -> int:
    idx = load_index()
    print(f'指南总数：{idx["meta"]["guide_count"]}  来源：{idx["meta"]["source"]}\n')
    for cat, n in idx["categories"].items():
        print(f'  {cat:<18} {n:>3} 份')
    print("\n浏览某分类：python3 resources/tools/mwg.py list <分类>")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="mwg.py",
        description="modern-web-guidance 本地检索工具（离线、零依赖）",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search", help="按能力/组件检索指南（返回 id 与描述）")
    p.add_argument("query", help='2-5 词的动作导向查询，如 "light dismiss dialog"')
    p.add_argument("-n", "--top", type=int, default=8, help="返回条数（默认 8）")
    p.add_argument("--json", action="store_true", help="以 JSON 输出")

    p = sub.add_parser("retrieve", help="按 id 取回指南全文（可逗号分隔多个）")
    p.add_argument("ids", help='指南 id，如 "dialog" 或 "dialog,forms"')

    p = sub.add_parser("list", help="列出全部指南或某分类")
    p.add_argument("category", nargs="?", default=None)
    p.add_argument("--json", action="store_true", help="以 JSON 输出")

    sub.add_parser("categories", help="列出全部分类与计数")

    args = ap.parse_args()
    if args.cmd == "search":
        return cmd_search(args.query, args.top, args.json)
    if args.cmd == "retrieve":
        return cmd_retrieve(args.ids)
    if args.cmd == "list":
        return cmd_list(args.category, args.json)
    if args.cmd == "categories":
        return cmd_categories()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
