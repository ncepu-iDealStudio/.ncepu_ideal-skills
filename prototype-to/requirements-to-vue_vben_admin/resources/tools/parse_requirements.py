#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""把中文后台管理需求描述解析为 req_context.json（初稿）。

用法：
    python parse_requirements.py 需求.txt --out req_context.json
    python parse_requirements.py --text "系统管理模块包括：用户管理、角色管理" --out ctx.json
    python parse_requirements.py 需求.txt --out ctx.json --title "订单管理后台" --ui antd

设计说明：
    基于关键词匹配的启发式解析，输出结构化初稿供人工/模型核对。
    不追求 100% 准确，重点是省掉机械的拆解工作。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---- 关键词词典（与 config/module_mapping.json 保持同步）--------------------

MODULE_KEYWORDS = {
    "系统管理": ["系统管理", "系统设置", "权限中心", "基础配置", "后台管理"],
    "业务管理": ["业务管理", "业务中心", "运营管理", "交易管理"],
    "数据统计": ["数据统计", "统计分析", "数据中心", "报表中心", "数据分析"],
    "内容管理": ["内容管理", "文章管理", "资讯管理"],
    "用户中心": ["用户中心", "会员管理", "客户管理"],
    "财务管理": ["财务管理", "财务中心", "结算管理"],
    "运营管理": ["运营管理", "营销管理", "活动管理"],
}

MODULE_ICONS = {
    "系统管理": "lucide:settings",
    "业务管理": "lucide:briefcase",
    "数据统计": "lucide:chart-column",
    "内容管理": "lucide:file-text",
    "用户中心": "lucide:users",
    "财务管理": "lucide:wallet",
    "运营管理": "lucide:megaphone",
    "默认": "lucide:folder",
}

PAGE_ICONS = {
    "用户管理": "lucide:users",
    "角色管理": "lucide:shield-check",
    "权限管理": "lucide:key-round",
    "订单管理": "lucide:shopping-cart",
    "商品管理": "lucide:package",
    "库存管理": "lucide:warehouse",
    "销售数据分析": "lucide:trending-up",
    "用户行为分析": "lucide:activity",
    "类别管理": "lucide:tags",
    "部门管理": "lucide:network",
    "菜单管理": "lucide:list-tree",
    "默认": "lucide:circle",
}

# 页面类型关键词（顺序敏感：先具体后宽泛）
TYPE_KEYWORDS = [
    ("dashboard", ["分析", "统计", "报表", "看板", "概览", "趋势", "走势"]),
    ("tree", ["权限", "菜单", "组织", "部门", "分类", "层级"]),
    ("form", ["设置", "配置", "参数"]),
]

# 领域专属字段
DOMAIN_FIELDS = {
    "用户管理": [
        {"field": "account", "label": "账号", "type": "string", "column": True, "form": True, "required": True, "width": 160},
        {"field": "nickname", "label": "昵称", "type": "string", "column": True, "form": True, "width": 160},
        {"field": "email", "label": "邮箱", "type": "string", "column": True, "form": True, "width": 200},
        {"field": "phone", "label": "手机号", "type": "string", "column": True, "form": False, "width": 150},
    ],
    "角色管理": [
        {"field": "code", "label": "角色编码", "type": "string", "column": True, "form": True, "required": True, "width": 160},
        {"field": "description", "label": "描述", "type": "textarea", "column": True, "form": True},
    ],
    "订单管理": [
        {"field": "orderNo", "label": "订单号", "type": "string", "column": True, "form": False, "width": 200},
        {"field": "customerName", "label": "客户", "type": "string", "column": True, "form": True, "width": 160},
        {"field": "amount", "label": "金额", "type": "number", "column": True, "form": True, "width": 140},
        {"field": "orderTime", "label": "下单时间", "type": "datetime", "column": True, "form": False, "width": 200},
    ],
    "商品管理": [
        {"field": "sku", "label": "SKU", "type": "string", "column": True, "form": True, "width": 160},
        {"field": "category", "label": "分类", "type": "string", "column": True, "form": True, "width": 140},
        {"field": "price", "label": "价格", "type": "number", "column": True, "form": True, "width": 120},
        {"field": "stock", "label": "库存", "type": "number", "column": True, "form": False, "width": 100},
    ],
    "库存管理": [
        {"field": "productName", "label": "商品", "type": "string", "column": True, "form": True, "width": 200},
        {"field": "warehouse", "label": "仓库", "type": "string", "column": True, "form": True, "width": 160},
        {"field": "quantity", "label": "库存数量", "type": "number", "column": True, "form": True, "width": 120},
        {"field": "warningLine", "label": "预警线", "type": "number", "column": True, "form": True, "width": 120},
    ],
}

COMMON_CRUD_FIELDS = [
    {"field": "id", "label": "ID", "type": "string", "column": True, "form": False, "width": 200},
    {"field": "name", "label": "名称", "type": "string", "column": True, "form": True, "required": True, "width": 200},
    {"field": "status", "label": "状态", "type": "switch", "column": True, "form": True, "width": 100,
     "options": [{"label": "启用", "value": 1}, {"label": "禁用", "value": 0}]},
    {"field": "remark", "label": "备注", "type": "textarea", "column": False, "form": True},
    {"field": "createTime", "label": "创建时间", "type": "datetime", "column": True, "form": False, "width": 200},
]

DASHBOARD_FIELDS = [
    {"field": "overview", "label": "概览指标", "type": "statCards"},
    {"field": "trend", "label": "趋势图", "type": "lineChart"},
    {"field": "category", "label": "分类占比", "type": "pieChart"},
]

TREE_FIELDS = [
    {"field": "id", "label": "ID", "type": "string", "column": True, "width": 200},
    {"field": "name", "label": "名称", "type": "string", "column": True, "form": True, "required": True},
    {"field": "code", "label": "编码", "type": "string", "column": True, "form": True, "width": 200},
    {"field": "type", "label": "类型", "type": "tag", "column": True, "form": True, "width": 120},
]


# ---- 工具函数 --------------------------------------------------------------


def to_pascal(name: str) -> str:
    """中文名 -> PascalCase 英文标识。

    按「词」匹配而非按「字」：映射表的键是"用户""角色"这类双字词，
    逐字遍历永远匹配不上，会导致全部退化为默认值。
    """
    mapping = {
        "用户": "User", "角色": "Role", "权限": "Permission", "菜单": "Menu",
        "部门": "Dept", "组织": "Org", "订单": "Order", "商品": "Product",
        "库存": "Inventory", "仓库": "Warehouse", "销售": "Sales",
        "分析": "Analysis", "统计": "Statistics", "行为": "Behavior",
        "数据": "Data", "内容": "Content", "文章": "Article", "会员": "Member",
        "客户": "Customer", "财务": "Finance", "结算": "Settlement",
        "系统": "System", "业务": "Business", "运营": "Operation",
        "设置": "Setting", "配置": "Config", "管理": "", "中心": "",
        # 组合词优先（避免"数据统计"拆成 DataStatistics 这类冗长结果）
        "数据统计": "Statistics", "销售数据": "Sales", "销售数据分析": "SalesAnalysis",
        "用户行为": "UserBehavior", "用户行为分析": "UserBehaviorAnalysis",
        "系统管理": "System", "业务管理": "Business", "运营管理": "Operation",
    }
    parts: list[str] = []
    i = 0
    while i < len(name):
        matched = False
        # 优先匹配更长的词
        for length in (4, 3, 2, 1):   # 最长优先，支持"数据统计"这类组合词
            token = name[i:i + length]
            if token in mapping:
                if mapping[token]:
                    parts.append(mapping[token])
                i += length
                matched = True
                break
        if matched:
            continue
        ch = name[i]
        if ch.isascii() and ch.isalnum():
            parts.append(ch.upper() if not parts else ch)
        i += 1

    result = "".join(parts)
    if not result:
        result = "Item"
    # 保证首字母大写
    return result[0].upper() + result[1:]


def to_kebab(name: str) -> str:
    """中文名 -> kebab-case 路径段（按词匹配，同 to_pascal）"""
    mapping = {
        "用户": "user", "角色": "role", "权限": "permission", "菜单": "menu",
        "部门": "dept", "组织": "org", "订单": "order", "商品": "product",
        "库存": "inventory", "仓库": "warehouse", "销售": "sales",
        "分析": "analysis", "统计": "statistics", "行为": "behavior",
        "数据": "data", "内容": "content", "文章": "article", "会员": "member",
        "客户": "customer", "财务": "finance", "结算": "settlement",
        "系统": "system", "业务": "business", "运营": "operation",
        "管理": "", "中心": "",
        # 组合词优先
        "数据统计": "statistics", "销售数据分析": "sales-analysis",
        "销售数据": "sales", "用户行为分析": "user-behavior",
        "用户行为": "user-behavior", "系统管理": "system",
        "业务管理": "business", "运营管理": "operation",
    }
    parts: list[str] = []
    i = 0
    while i < len(name):
        matched = False
        for length in (4, 3, 2, 1):   # 最长优先，支持"数据统计"这类组合词
            token = name[i:i + length]
            if token in mapping:
                if mapping[token]:
                    parts.append(mapping[token])
                i += length
                matched = True
                break
        if matched:
            continue
        ch = name[i]
        if ch.isascii() and ch.isalnum():
            parts.append(ch.lower())
        i += 1

    # 去重相邻重复（如"用户用户"）
    dedup: list[str] = []
    for part in parts:
        if not dedup or dedup[-1] != part:
            dedup.append(part)
    return "-".join(dedup) or "item"


def detect_page_type(page_name: str) -> str:
    for ptype, words in TYPE_KEYWORDS:
        if any(w in page_name for w in words):
            return ptype
    return "crud"


def build_fields(page_name: str, page_type: str) -> list[dict]:
    if page_type == "dashboard":
        return [dict(f) for f in DASHBOARD_FIELDS]
    if page_type == "tree":
        return [dict(f) for f in TREE_FIELDS]
    if page_type == "form":
        return [dict(f) for f in COMMON_CRUD_FIELDS if f["form"]]

    # crud：领域字段 + 通用字段，去重
    fields: list[dict] = []
    seen: set[str] = set()
    for f in DOMAIN_FIELDS.get(page_name, []):
        fields.append(dict(f))
        seen.add(f["field"])
    for f in COMMON_CRUD_FIELDS:
        if f["field"] not in seen:
            fields.append(dict(f))
    return fields


# ---- 解析主体 --------------------------------------------------------------


def split_module_sections(text: str) -> list[tuple[str, str]]:
    """把需求文本切成 (模块名, 该模块的页面描述) 列表。"""
    # 统一分隔符
    normalized = text.replace("；", ";").replace("，", ",").replace("。", ".")
    sections: list[tuple[str, str]] = []

    # 逐个模块关键词定位
    positions: list[tuple[int, str]] = []
    for module, keywords in MODULE_KEYWORDS.items():
        for kw in keywords:
            idx = normalized.find(kw)
            if idx != -1:
                positions.append((idx, module))
                break

    if not positions:
        return [("功能模块", normalized)]

    positions.sort()
    for i, (idx, module) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(normalized)
        chunk = normalized[idx:end]
        sections.append((module, chunk))

    return sections


def extract_pages(chunk: str, module: str) -> list[str]:
    """从模块片段中提取页面名。

    注意：只能剥离「模块名整词」与引导词，不能做单字替换，
    否则会把「数据统计」的"数据"误当成模块词，导致
    「销售数据分析」被截断成「销售」。
    """
    cleaned = chunk

    # 只剥离「片段开头」的模块名，绝不做全文替换：
    # 否则「数据统计」的同义词含"数据分析"，会把页面名「销售数据分析」截断成「销售」
    candidates = sorted(set(MODULE_KEYWORDS.get(module, []) + [module]), key=len, reverse=True)
    for kw in candidates:
        if cleaned.lstrip().startswith(kw):
            lead = len(cleaned) - len(cleaned.lstrip())
            cleaned = cleaned[:lead] + cleaned[lead + len(kw):]
            break

    # 剥离引导词（同样按长度倒序，避免 "模块包括" 被 "包括" 先吃掉）
    fillers = sorted([
        "模块包含", "模块包括", "模块有", "包括", "包含", "功能",
        "：", ":", ";", "、", "，", ",", "。", ".",
    ], key=len, reverse=True)
    for filler in fillers:
        cleaned = cleaned.replace(filler, "\n")

    pages: list[str] = []
    for raw in re.split(r"[\n,;、]+", cleaned):
        item = raw.strip().strip("-—•*·0123456789. ")
        if not item or len(item) < 2:
            continue
        if item in pages:
            continue
        # 过滤掉明显不是页面的词
        if item in {"我", "需要", "实现", "一个", "后台", "管理系统", "以下"}:
            continue
        pages.append(item)

    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description="后台管理需求 -> req_context.json（启发式初稿）")
    parser.add_argument("input", nargs="?", help="需求文本文件路径")
    parser.add_argument("--text", help="直接传入需求文本")
    parser.add_argument("--out", default="req_context.json", help="输出 JSON 路径")
    parser.add_argument("--title", default="后台管理系统", help="系统标题")
    parser.add_argument("--ui", default="antd", choices=["antd", "ele", "naive", "tdesign"], help="UI 框架")
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"错误：文件不存在 {path}")
            return 2
        text = path.read_text(encoding="utf-8")
    else:
        print("用法: python parse_requirements.py <需求文件> 或 --text \"...\"")
        return 1

    sections = split_module_sections(text)

    modules: list[dict] = []
    order = 10
    assumptions: list[str] = []
    need_confirm: list[str] = []
    total_pages = 0

    for module_name, chunk in sections:
        pages = extract_pages(chunk, module_name)
        if not pages:
            continue

        module_en = to_pascal(module_name) or "Module"
        module_path = "/" + to_kebab(module_name)
        children: list[dict] = []

        for page_name in pages:
            ptype = detect_page_type(page_name)
            page_en = to_pascal(page_name)
            page_path = to_kebab(page_name)
            children.append({
                "name": page_name,
                "name_en": f"{module_en}{page_en}",
                "path": page_path,
                "full_path": f"{module_path}/{page_path}",
                "icon": PAGE_ICONS.get(page_name, PAGE_ICONS["默认"]),
                "type": ptype,
                "model": f"{module_en}{page_en}",
                "route_file": f"{to_kebab(module_name)}.ts",
                "view_dir": f"views/{to_kebab(module_name)}/{page_path}",
                "api_file": f"api/{to_kebab(module_name)}/{page_path}.ts",
                "fields": build_fields(page_name, ptype),
                "actions": ["create", "edit", "detail", "delete"] if ptype == "crud" else ["create", "edit", "delete"],
                "has_mock": True,
            })
            total_pages += 1
            if page_name not in DOMAIN_FIELDS and ptype == "crud":
                need_confirm.append(f"「{page_name}」的字段定义按通用模板推断，请确认实际字段")

        modules.append({
            "name": module_name,
            "name_en": module_en,
            "path": module_path,
            "icon": MODULE_ICONS.get(module_name, MODULE_ICONS["默认"]),
            "order": order,
            "children": children,
        })
        order += 10
        assumptions.append(f"「{module_name}」识别为一级菜单，含 {len(children)} 个页面")

    context = {
        "app": {
            "title": args.title,
            "ui": args.ui,
            "vben_version": "5.x",
        },
        "modules": modules,
        "stats": {
            "module_count": len(modules),
            "page_count": total_pages,
        },
        "diagnostics": {
            "parse_errors": [],
            "assumptions": assumptions,
            "need_confirm": need_confirm,
        },
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "output": str(out_path),
        "modules": len(modules),
        "pages": total_pages,
        "module_list": [
            {"name": m["name"], "pages": [c["name"] for c in m["children"]]}
            for m in modules
        ],
        "need_confirm_count": len(need_confirm),
        "note": "这是初稿，请核对 diagnostics.need_confirm 中的待确认项",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
