#!/usr/bin/env python3
"""Collect account-table, login, role, and token evidence from a FastAPI project.

This is a preflight helper for skill gates. It does not decide pass/fail and
does not modify the target project.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PASSWORD_NAMES = frozenset(
    {
        "password",
        "passwd",
        "pwd",
        "password_hash",
        "hashed_password",
        "pass_hash",
        "passwordhash",
        "hashedpassword",
        "passhash",
    }
)
ACCOUNT_NAMES = frozenset(
    {
        "account",
        "username",
        "user_name",
        "login_name",
        "loginname",
        "email",
        "phone",
    }
)
ROLE_NAMES = frozenset(
    {
        "user_type",
        "usertype",
        "role",
        "role_id",
        "role_name",
        "is_admin",
        "user_role",
        "account_type",
    }
)
LOGIN_FN = re.compile(r"\b(login|signin|sign_in|authenticate)\b", re.I)
TOKEN_HINT = re.compile(
    r"\b(jwt|JSONWebToken|create_access_token|Bearer|OAuth2PasswordBearer|"
    r"access_token|Authorization)\b",
    re.I,
)
COL_PY = re.compile(
    r"""^\s*([A-Za-z_][\w]*)\s*=\s*Column\(\s*(?:['"]([\w]+)['"]\s*,)?""",
    re.M,
)
TABLENAME = re.compile(r"""__tablename__\s*=\s*['"]([^'"]+)['"]""")
SQL_TABLE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([A-Za-z_]\w*)`?",
    re.I,
)
SQL_COL = re.compile(r"`?([A-Za-z_]\w*)`?\s+(?:VARCHAR|CHAR|TEXT|TINYTEXT|MEDIUMTEXT|LONGTEXT|BLOB)", re.I)
SEED_NAME = re.compile(r"(seed|bootstrap|init[_-]?admin|create[_-]?admin)", re.I)
ADMIN_ENV = re.compile(
    r"^[ \t]*(INITIAL_ADMIN_USERNAME|INITIAL_ADMIN_PASSWORD|"
    r"ADMIN_USERNAME|ADMIN_INITIAL_PASSWORD)\s*=",
    re.M,
)
INSERT_INTO = re.compile(r"INSERT\s+INTO\s+`?([A-Za-z_]\w*)`?", re.I)
SESSION_STRONG = re.compile(
    r"(refresh|session|revok|jti|idle_expires|device|token_version|last_active)",
    re.I,
)
SESSION_WEAK = re.compile(r"(expires_at|expires)", re.I)
RESET_STRONG = re.compile(r"(reset_token|password_reset|verification_token|otp)", re.I)
USED_MARK = re.compile(r"(used_at|consumed_at)", re.I)
TOKEN_HASH = re.compile(r"token_hash", re.I)
NON_RESET_TOKEN = re.compile(r"(refresh|access|session)", re.I)
COOKIE_HINT = re.compile(
    r"(set_cookie|delete_cookie|httponly|samesite|Cookie\()", re.I
)
SET_COOKIE = re.compile(r"(set_cookie|delete_cookie)", re.I)
COOKIE_PARAM = re.compile(r"\bCookie\s*\(", re.I)
CREDENTIAL_BODY_FIELDS = ("refresh_token", "device_name")
REFRESH_ROUTE = re.compile(r"(refresh|renew)", re.I)
LOGOUT_ROUTE = re.compile(r"(logout|signout|sign_out|revoke)", re.I)
RESET_ROUTE = re.compile(
    r"(password/reset|forgot|reset_password|reset-password)", re.I
)
LIFECYCLE_FN = re.compile(
    r"^\s*(?:async\s+)?def\s+"
    r"(refresh|rotate|logout|revoke|reset_password|forgot_password)\s*\(",
    re.I | re.M,
)
SQL_KEYWORDS = frozenset(
    {
        "PRIMARY",
        "UNIQUE",
        "KEY",
        "CONSTRAINT",
        "INDEX",
        "FOREIGN",
        "CHECK",
        "ENGINE",
        "DEFAULT",
        "CHARSET",
        "COLLATE",
        "COMMENT",
        "AUTO_INCREMENT",
    }
)

# 数据权限模型识别规则：只收集证据，是否成立由 SKILL 门禁 6 判定。
AUTHZ_PROFILES = (
    {
        "id": "object_ownership",
        "name": "对象归属与水平越权",
        "table_re": r"(^|_)(ownership|owner)$",
        "field_re": r"^(owner|owner_[a-z0-9_]*|created_by|creator[a-z0-9_]*|author_id|uploader[a-z0-9_]*)$",
        "required_controls": [
            "创建由服务端绑定归属，忽略或拒绝客户端提交",
            "详情/更新/删除先按服务端原对象归属判定",
            "列表在分页与计数前按归属过滤",
            "Update 排除归属/状态等无权字段",
        ],
        "acceptance_cases": [
            "本人读/改/删成功",
            "他人读/改/删被拒且数据不变",
            "列表只含本人",
            "创建/更新篡改归属无效",
        ],
    },
    {
        "id": "tenant_isolation",
        "name": "多租户隔离",
        "table_re": r"^tenant$",
        "field_re": r"^tenant(_id|_code|_name|_status)?$|_tenant_id$",
        "required_controls": [
            "所有查询的 tenant_id 来自已认证主体",
            "跨租户读/改/删按约定 403/404",
            "租户禁用/归档后普通成员被拒",
            "列表计数按租户过滤",
        ],
        "acceptance_cases": [
            "同租户读写成功",
            "跨租户读写被拒且数据不变",
            "篡改 tenant_id 无效",
            "租户禁用后 401/403",
        ],
    },
    {
        "id": "org_scope",
        "name": "组织/部门数据范围",
        "table_re": r"^(org_unit|organization|organizations|department|departments|org_member)$",
        "field_re": r"^(org_unit_id|org_id|organization_id|department_id|dept_id|parent_org_unit_id|parent_org_id|org_type)$",
        "required_controls": [
            "从服务端组织树计算可见范围（含下级）",
            "校验 org_member 的 valid_from/valid_to/status",
            "外部合作组织与内部组织隔离",
            "请求中的组织标识不能扩大范围",
        ],
        "acceptance_cases": [
            "本人/本部门/下级范围可见",
            "跨部门被拒",
            "外部与内部互访被拒",
            "组织调整后按新范围",
            "临时成员到期/移除后被拒",
        ],
    },
    {
        "id": "project_rebac",
        "name": "项目成员与关系权限",
        "table_re": r"^(project|project_member)$",
        "field_re": r"^(project_id|parent_project_id|member_role)$",
        "required_controls": [
            "按 project_member.member_role 执行动作矩阵",
            "成员移除/status=0 后立即失效",
            "嵌套项目继承查看，编辑/删除仍需子项目成员",
            "检测项目循环嵌套并返回 409",
        ],
        "acceptance_cases": [
            "成员按角色可操作",
            "非成员被拒",
            "Viewer 编辑、Editor 删除被拒",
            "移除成员后立即失效",
            "循环嵌套 409",
        ],
    },
    {
        "id": "acl_grant",
        "name": "资源 ACL 与授权",
        "table_re": r"(_grant|grants)$",
        "field_re": r"^(grantee_user_id|grantee_id|can_view|can_edit|can_reshare|granted_at|revoked_at)$",
        "required_controls": [
            "按 can_view/can_edit 判定动作",
            "校验 valid_to 与 status，撤销/过期立即失效",
            "can_reshare=0 时禁止再次分享",
            "授权/撤销写审计",
        ],
        "acceptance_cases": [
            "直接授权可读/可编辑",
            "撤销/过期后失效",
            "越权动作被拒",
            "禁止转分享被拒",
        ],
    },
    {
        "id": "share_lifecycle",
        "name": "分享与生命周期",
        "table_re": r"(_share|shares)$",
        "field_re": r"^(share_token|share_token_hash|max_access_count|access_count|allow_download|allow_reshare|visitor_user_id)$",
        "required_controls": [
            "校验令牌摘要、密码哈希、有效期与访问次数",
            "allow_download/allow_reshare 限制对应动作",
            "资源冻结/归档/删除限制分享与访问",
            "分享访问结果写审计",
        ],
        "acceptance_cases": [
            "有效分享可访问",
            "错误密码/次数用尽/过期/撤销被拒",
            "禁止下载被拒",
            "冻结/归档/删除状态限制生效",
        ],
    },
    {
        "id": "classification",
        "name": "资源密级与访问限制",
        "table_re": r"^(classification|classification_level)$",
        "field_re": r"^(classification|classification_level_id|security_level|requires_approval|requires_mfa)$",
        "required_controls": [
            "密级规则强制决定查看/下载/分享",
            "机密需已通过审批，绝密还需 MFA",
            "管理员不能自动绕过密级",
            "密级变更后下一次请求即时生效",
        ],
        "acceptance_cases": [
            "公开/内部可读",
            "机密无审批被拒、有审批通过",
            "绝密无 MFA 被拒且禁止下载/分享",
            "管理员访问绝密同样受限",
        ],
    },
    {
        "id": "abac_policy",
        "name": "ABAC 属性策略",
        "table_re": r"^abac_policy(_action|_version)?$",
        "field_re": r"^(condition_json|missing_attribute_behavior|policy_snapshot|policy_code)$",
        "required_controls": [
            "统一策略引擎输入主体/资源/动作/上下文",
            "显式拒绝优先于允许，按 priority 排序",
            "属性缺失按策略默认，环境属性服务端采集",
            "策略修改前保存版本，决策记录命中规则与原因",
        ],
        "acceptance_cases": [
            "同部门/满足条件的允许生效",
            "显式拒绝压过允许",
            "属性缺失按默认拒绝",
            "客户端伪造属性被忽略",
            "版本快照与恢复",
        ],
    },
    {
        "id": "field_level",
        "name": "字段级权限与脱敏",
        "table_re": r"^field_policy$",
        "field_re": r"^(field_code|access_mode|mask_pattern)$",
        "required_controls": [
            "按角色/字段四态（可见/只读/脱敏/隐藏）投影",
            "列表、详情、导出共用同一投影函数",
            "只读字段不可写，隐藏字段提交应拒绝或剔除",
            "导出权限独立校验",
        ],
        "acceptance_cases": [
            "详情隐藏/脱敏正确",
            "列表同样过滤",
            "无导出权限被拒",
            "只读字段修改被拒",
            "策略变更即时生效",
        ],
    },
    {
        "id": "approval_temp_grant",
        "name": "审批与临时授权",
        "table_re": r"^(access_request|approval_task|approval_request)$",
        "field_re": r"^(applicant_user_id|approver_user_id|step_no|task_status|decided_at)$",
        "required_controls": [
            "申请人不能审批自己的申请",
            "单人/双人审批，双人需两个不同审批人",
            "临时授权必须有 valid_to，到期/撤销立即失效",
            "执行前复核申请人当前权限，重复执行 409",
        ],
        "acceptance_cases": [
            "提交申请 201",
            "自审批 403",
            "双人审批未齐不生效",
            "到期/撤销后失效",
            "重复执行 409",
        ],
    },
    {
        "id": "high_risk_break_glass",
        "name": "高危操作、MFA 与紧急访问",
        "table_re": r"^(high_risk_operation|break_glass_request|user_mfa|mfa_binding)$",
        "field_re": r"^(mfa_verified|secret_ciphertext|review_status|operation_type|executed_at|reviewed_by_user_id)$",
        "required_controls": [
            "审批通过前不得执行，执行前 Step-up MFA",
            "双人审批且发起人不能自批",
            "执行前复核权限与账号状态，重复执行 409",
            "Break-glass 必须有原因/范围/有效期并事后审查",
        ],
        "acceptance_cases": [
            "未 MFA 403",
            "单审批仍不可执行",
            "双人审批 + MFA 后成功",
            "重复执行 409",
            "Break-glass 到期/撤销失效",
        ],
    },
    {
        "id": "sod",
        "name": "职责分离与权限撤销",
        "table_re": r"^sod_rule$",
        "field_re": r"^(role_a_id|role_b_id|enforcement)$",
        "required_controls": [
            "互斥角色不能同时授予，禁止分配返回 409",
            "仅告警规则允许但写冲突记录",
            "撤销/禁用角色后下一次请求立即失效",
            "客户端提交角色参数无效",
        ],
        "acceptance_cases": [
            "非互斥角色正常分配",
            "冲突分配 409 或告警记录",
            "撤销后依赖该角色的接口 403",
            "客户端伪造角色无效",
        ],
    },
    {
        "id": "audit_decision",
        "name": "审计与授权决策",
        "table_re": r"^(audit_event|audit_log|authorization_decision|login_attempt|login_log)$",
        "field_re": r"^(is_auditor|deny_reason|matched_rule)$",
        "required_controls": [
            "每次访问决策写 authorization_decision",
            "登录/权限变更/拒绝访问写 audit_event",
            "拒绝原因区分无允许规则与显式拒绝",
            "审计只追加，只有审计员/管理员可查，不含秘密",
        ],
        "acceptance_cases": [
            "允许与拒绝均留痕",
            "普通用户查审计 403",
            "更新/删除审计被拒且记录不变",
            "记录不含密码/令牌/密钥",
        ],
    },
    {
        "id": "service_account",
        "name": "服务账号、API Key 与委托",
        "table_re": r"^(service_account|api_key|delegation)$",
        "field_re": r"^(key_hash|key_digest|scopes|delegator_user_id|delegatee_user_id)$",
        "required_controls": [
            "服务账号不继承用户/管理员权限",
            "API Key 只存摘要，过期/撤销/禁用后 401",
            "scopes 限制动作，超范围 403",
            "委托不越权、有有效期、撤销即时失效",
        ],
        "acceptance_cases": [
            "范围内 API Key 可访问",
            "超 scope 403",
            "过期/撤销 401",
            "委托越权被拒",
            "委托到期/撤销失效",
        ],
    },
    {
        "id": "scenario_library",
        "name": "鉴权场景库",
        "table_re": r"^auth_scenario$",
        "field_re": r"^(expected_decision|subject_snapshot|resource_snapshot|context_json|scenario_code)$",
        "required_controls": [
            "场景包含主体/资源/动作/上下文/期望决策",
            "执行场景调用统一鉴权入口并比对实际决策",
            "停用场景不执行，差异记录原因",
            "不预置漏洞或攻击脚本，不修改业务数据",
        ],
        "acceptance_cases": [
            "期望与实际一致时通过",
            "期望拒绝但实际允许标记失败",
            "停用场景不执行",
            "按分类查询正确",
        ],
    },
    {
        "id": "behavior_config",
        "name": "鉴权行为配置",
        "table_re": r"^platform_config$",
        "field_re": r"^(config_key|config_value|value_type)$",
        "required_controls": [
            "配置覆盖默认拒绝/允许、跨范围语义、属性缺失、字段返回方式",
            "仅管理员可改，按 value_type 校验",
            "修改后对后续请求生效，客户端不能覆盖",
            "变更审计含前后值，缺失时用安全默认",
        ],
        "acceptance_cases": [
            "默认拒绝生效",
            "切换默认允许后按新值",
            "跨范围 403/404 可配置",
            "非管理员修改 403",
            "非法值 400/422 且配置不变",
        ],
    },
)

SCOPE_FIELD_PATTERNS = {
    "ownership": r"^(owner|owner_[a-z0-9_]*|created_by|creator[a-z0-9_]*|author_id|uploader[a-z0-9_]*)$",
    "tenant": r"^tenant(_id|_code|_name)?$|_tenant_id$",
    "org": r"^(org_unit_id|org_id|organization_id|department_id|dept_id|parent_org_unit_id|parent_org_id)$",
    "project": r"^(project_id|parent_project_id)$",
    "role_status": r"^(role|role_id|role_code|is_admin|user_type|status|state|is_active|enabled|locked|classification|classification_level_id|security_level)$",
}


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _is_password(name: str) -> bool:
    n = name.lower()
    compact = _norm(name)
    if n in PASSWORD_NAMES or compact in PASSWORD_NAMES:
        return True
    return compact.endswith("password") and "policy" not in compact and "hint" not in compact


def _is_account(name: str) -> bool:
    return name.lower() in ACCOUNT_NAMES or _norm(name) in ACCOUNT_NAMES


def _is_role(name: str) -> bool:
    return name.lower() in ROLE_NAMES or _norm(name) in ROLE_NAMES


def _iter_files(root: Path, rel: str, suffix: str):
    base = root / rel
    if not base.is_dir():
        return
    for path in base.rglob(f"*{suffix}"):
        if "__pycache__" in path.parts or path.name.startswith("test_"):
            continue
        yield path


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def scan_models(root: Path) -> list[dict]:
    found = []
    for path in _iter_files(root, "models", ".py"):
        if path.name in {"base.py", "__init__.py"}:
            continue
        text = _read(path)
        table_m = TABLENAME.search(text)
        table = table_m.group(1) if table_m else path.stem
        cols = []
        for match in COL_PY.finditer(text):
            attr, db_name = match.group(1), match.group(2)
            cols.append(db_name or attr)
        passwords = [c for c in cols if _is_password(c)]
        if not passwords:
            continue
        found.append(
            {
                "table": table,
                "file": str(path.relative_to(root)).replace("\\", "/"),
                "password_fields": passwords,
                "account_fields": [c for c in cols if _is_account(c)],
                "role_fields": [c for c in cols if _is_role(c)],
            }
        )
    return found


def scan_sql(root: Path) -> list[dict]:
    found = []
    sql_dirs = [root / "sql", root / "database"]
    files = []
    for folder in sql_dirs:
        if folder.is_dir():
            files.extend(folder.rglob("*.sql"))
    for path in files:
        text = _read(path)
        current = None
        acc: dict[str, list[str]] = {}
        for line in text.splitlines():
            tm = SQL_TABLE.search(line)
            if tm:
                current = tm.group(1)
                acc.setdefault(current, [])
                continue
            if current:
                for col in SQL_COL.findall(line):
                    acc[current].append(col)
        rel = str(path.relative_to(root)).replace("\\", "/")
        for table, cols in acc.items():
            passwords = [c for c in cols if _is_password(c)]
            if not passwords:
                continue
            found.append(
                {
                    "table": table,
                    "file": rel,
                    "password_fields": passwords,
                    "account_fields": [c for c in cols if _is_account(c)],
                    "role_fields": [c for c in cols if _is_role(c)],
                }
            )
    return found


def scan_service_login(root: Path) -> list[dict]:
    hits = []
    for path in _iter_files(root, "service", ".py"):
        if path.name in {"dependencies.py", "__init__.py"}:
            continue
        text = _read(path)
        for match in re.finditer(
            r"^\s*(?:async\s+)?def\s+(login|signin|sign_in|authenticate)\s*\(",
            text,
            re.M | re.I,
        ):
            hits.append(
                {
                    "file": str(path.relative_to(root)).replace("\\", "/"),
                    "function": match.group(1),
                }
            )
    return hits


def _join_path(prefix: str, path_part: str) -> str:
    if not prefix:
        full = path_part or "/"
    elif path_part.startswith("/"):
        full = prefix.rstrip("/") + path_part
    elif path_part:
        full = prefix.rstrip("/") + "/" + path_part
    else:
        full = prefix
    return full if full.startswith("/") else "/" + full


def scan_http_login(root: Path) -> list[dict]:
    hits = []
    seen = set()
    for folder in ("api", "app"):
        for path in _iter_files(root, folder, ".py"):
            text = _read(path)
            rel = str(path.relative_to(root)).replace("\\", "/")
            prefix_m = re.search(r"""APIRouter\(\s*prefix\s*=\s*['"]([^'"]+)['"]""", text)
            prefix = prefix_m.group(1) if prefix_m else ""
            matched_route = False
            for match in re.finditer(
                r"""@(?:router|app)\.(post|get|put|patch)\(\s*['"]([^'"]*)['"]""",
                text,
                re.I,
            ):
                method, path_part = match.group(1).upper(), match.group(2)
                full = _join_path(prefix, path_part)
                if not (LOGIN_FN.search(full) or re.search(r"/token(?:/|$)", full, re.I)):
                    continue
                key = (rel, method, full)
                if key in seen:
                    continue
                seen.add(key)
                matched_route = True
                hits.append(
                    {
                        "file": rel,
                        "method": method,
                        "path_hint": full,
                        "evidence": "route decorator path",
                    }
                )
            if not matched_route and re.search(
                r"def\s+(login|signin|sign_in|authenticate)\s*\(", text, re.I
            ):
                key = (rel, None, None)
                if key not in seen:
                    seen.add(key)
                    hits.append(
                        {
                            "file": rel,
                            "method": None,
                            "path_hint": None,
                            "evidence": "function name matches login",
                        }
                    )
    return hits


def scan_token_hints(root: Path) -> dict:
    files = []
    for rel in ("api", "service", "core", "utils", "middleware", "app"):
        files.extend(_iter_files(root, rel, ".py"))
    mentions = []
    for path in files:
        text = _read(path)
        if TOKEN_HINT.search(text):
            mentions.append(str(path.relative_to(root)).replace("\\", "/"))
    return {"files_with_jwt_or_bearer": mentions}


def scan_role_signals(root: Path, account_tables: list[dict]) -> list[dict]:
    signals = []
    for item in account_tables:
        for field in item.get("role_fields") or []:
            signals.append(
                {
                    "table": item.get("table"),
                    "file": item.get("file"),
                    "field": field,
                }
            )
    return signals


def scan_initial_admin(root: Path, account_tables: list[dict]) -> dict:
    """Collect evidence for an initial-admin seed/bootstrap entry point.

    Only lists evidence; whether it is enough is decided by the skill gate.
    """
    account_names = {str(item.get("table", "")).lower() for item in account_tables}
    candidates: list[dict] = []

    for folder in ("scripts", "database", "sql", "migrations", "alembic", "deploy"):
        base = root / folder
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            if path.suffix.lower() not in {".py", ".sql"}:
                continue
            text = _read(path)
            evidence = None
            if SEED_NAME.search(path.stem):
                evidence = "文件名含 seed/bootstrap/admin 初始化"
            elif re.search(
                r"INITIAL_ADMIN|ADMIN_USERNAME|ADMIN_INITIAL_PASSWORD", text
            ):
                evidence = "引用 INITIAL_ADMIN / ADMIN_USERNAME"
            else:
                for table in INSERT_INTO.findall(text):
                    if table.lower() in account_names:
                        evidence = f"包含 INSERT INTO {table}"
                        break
            if evidence:
                candidates.append(
                    {
                        "file": str(path.relative_to(root)).replace("\\", "/"),
                        "evidence": evidence,
                    }
                )

    env_keys: list[str] = []
    env_example = root / ".env.example"
    if env_example.is_file():
        env_keys = sorted({m.group(1) for m in ADMIN_ENV.finditer(_read(env_example))})

    return {"seed_candidates": candidates, "env_keys": env_keys}


def _collect_model_tables(root: Path) -> list[dict]:
    """List every model table with its column names (no password filter)."""
    rows: list[dict] = []
    for path in _iter_files(root, "models", ".py"):
        if path.name in {"base.py", "__init__.py"}:
            continue
        text = _read(path)
        table_m = TABLENAME.search(text)
        table = table_m.group(1) if table_m else path.stem
        cols = []
        for match in COL_PY.finditer(text):
            attr, db_name = match.group(1), match.group(2)
            cols.append(db_name or attr)
        if cols:
            rows.append(
                {
                    "table": table,
                    "file": str(path.relative_to(root)).replace("\\", "/"),
                    "fields": cols,
                }
            )
    return rows


def _collect_sql_tables(root: Path) -> list[dict]:
    """List every SQL table with its column names (no password filter)."""
    rows: list[dict] = []
    files = []
    for folder in (root / "sql", root / "database"):
        if folder.is_dir():
            files.extend(folder.rglob("*.sql"))
    for path in files:
        text = _read(path)
        current = None
        acc: dict[str, list[str]] = {}
        for line in text.splitlines():
            tm = SQL_TABLE.search(line)
            if tm:
                current = tm.group(1)
                acc.setdefault(current, [])
                continue
            if current:
                for col in re.findall(r"`?([A-Za-z_]\w*)`?\s+(?:[A-Za-z]+)", line):
                    if col.upper() not in SQL_KEYWORDS:
                        acc[current].append(col)
        rel = str(path.relative_to(root)).replace("\\", "/")
        for table, cols in acc.items():
            rows.append({"table": table, "file": rel, "fields": cols})
    return rows


def _schema_body_fields(text: str) -> list[dict]:
    """List schema classes that declare refresh_token / device_name fields."""
    hits: list[dict] = []
    pattern = re.compile(
        r"^class\s+(\w+)[^\n]*:\s*\n((?:[ \t]+[^\n]*\n|\s*\n)*)", re.M
    )
    for match in pattern.finditer(text):
        block = match.group(2)
        fields = [
            field
            for field in CREDENTIAL_BODY_FIELDS
            if re.search(rf"^[ \t]+{field}\s*:", block, re.M)
        ]
        if fields:
            hits.append({"class": match.group(1), "fields": fields})
    return hits


def scan_token_lifecycle(root: Path) -> dict:
    """Collect session / refresh / reset / cookie evidence (no pass/fail decision)."""
    tables = _collect_model_tables(root) + _collect_sql_tables(root)
    session_tables: list[dict] = []
    reset_tables: list[dict] = []

    for row in tables:
        fields = row.get("fields") or []
        has_token = any("token" in f.lower() for f in fields)
        strong = {f for f in fields if RESET_STRONG.search(f)}
        weak = {
            f
            for f in fields
            if USED_MARK.search(f)
            or (TOKEN_HASH.search(f) and not NON_RESET_TOKEN.search(f))
        }
        if strong:
            reset_hits = sorted(strong | weak)
        elif has_token:
            reset_hits = sorted(weak)
        else:
            reset_hits = []
        if reset_hits:
            reset_tables.append(
                {"table": row["table"], "file": row["file"], "fields": reset_hits}
            )
            continue

        strong = [f for f in fields if SESSION_STRONG.search(f)]
        weak = [f for f in fields if SESSION_WEAK.search(f)]
        if strong:
            session_tables.append(
                {
                    "table": row["table"],
                    "file": row["file"],
                    "fields": sorted(set(strong + weak)),
                }
            )
        elif weak:
            session_tables.append(
                {"table": row["table"], "file": row["file"], "fields": weak}
            )

    refresh_endpoints: list[dict] = []
    logout_endpoints: list[dict] = []
    reset_endpoints: list[dict] = []
    cookie_files: set[str] = set()
    set_cookie_files: set[str] = set()
    cookie_param_files: set[str] = set()
    seen = set()

    for folder in ("api", "app"):
        for path in _iter_files(root, folder, ".py"):
            text = _read(path)
            rel = str(path.relative_to(root)).replace("\\", "/")
            if COOKIE_HINT.search(text):
                cookie_files.add(rel)
            if SET_COOKIE.search(text):
                set_cookie_files.add(rel)
            if COOKIE_PARAM.search(text):
                cookie_param_files.add(rel)
            prefix_m = re.search(
                r"""APIRouter\(\s*prefix\s*=\s*['"]([^'"]+)['"]""", text
            )
            prefix = prefix_m.group(1) if prefix_m else ""
            for match in re.finditer(
                r"""@(?:router|app)\.(post|get|put|patch)\(\s*['"]([^'"]*)['"]""",
                text,
                re.I,
            ):
                method, path_part = match.group(1).upper(), match.group(2)
                full = _join_path(prefix, path_part)
                key = (rel, method, full)
                if key in seen:
                    continue
                seen.add(key)
                row = {"file": rel, "method": method, "path_hint": full}
                if REFRESH_ROUTE.search(full):
                    refresh_endpoints.append(row)
                elif LOGOUT_ROUTE.search(full):
                    logout_endpoints.append(row)
                elif RESET_ROUTE.search(full):
                    reset_endpoints.append(row)

    service_methods: list[dict] = []
    for path in _iter_files(root, "service", ".py"):
        text = _read(path)
        rel = str(path.relative_to(root)).replace("\\", "/")
        for match in LIFECYCLE_FN.finditer(text):
            service_methods.append({"file": rel, "function": match.group(1)})

    for path in _iter_files(root, "core", ".py"):
        text = _read(path)
        if COOKIE_HINT.search(text):
            cookie_files.add(str(path.relative_to(root)).replace("\\", "/"))

    credential_body_fields: list[dict] = []
    for path in _iter_files(root, "schemas", ".py"):
        rel = str(path.relative_to(root)).replace("\\", "/")
        for hit in _schema_body_fields(_read(path)):
            credential_body_fields.append({"file": rel, **hit})

    return {
        "session_tables": session_tables,
        "reset_token_tables": reset_tables,
        "refresh_endpoints": refresh_endpoints,
        "logout_endpoints": logout_endpoints,
        "reset_endpoints": reset_endpoints,
        "cookie_files": sorted(cookie_files),
        "set_cookie_files": sorted(set_cookie_files),
        "cookie_param_files": sorted(cookie_param_files),
        "credential_body_fields": credential_body_fields,
        "service_methods": service_methods,
    }


def _dedupe_evidence(items: list[dict]) -> list[dict]:
    seen = set()
    result = []
    for item in items:
        key = (item["table"], item["file"], item["signal"])
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def scan_authorization(tables: list[dict]) -> dict:
    """按表/字段线索收集数据权限模型证据（不做通过判定）。"""
    evidence: dict[str, list[dict]] = {}
    scope_rows: list[dict] = []

    for row in tables:
        table = str(row.get("table") or "")
        file = str(row.get("file") or "")
        fields = [str(field) for field in (row.get("fields") or [])]
        if not table:
            continue

        for profile in AUTHZ_PROFILES:
            hits = []
            if profile.get("table_re") and re.search(profile["table_re"], table, re.I):
                hits.append({"table": table, "file": file, "signal": "table_name"})
            for field in fields:
                if profile.get("field_re") and re.search(profile["field_re"], field, re.I):
                    hits.append(
                        {"table": table, "file": file, "signal": f"field:{field}"}
                    )
            if hits:
                evidence.setdefault(profile["id"], []).extend(hits)

        row_scope = {}
        for category, pattern in SCOPE_FIELD_PATTERNS.items():
            matched = sorted({field for field in fields if re.search(pattern, field, re.I)})
            if matched:
                row_scope[category] = matched
        if row_scope:
            scope_rows.append({"table": table, "file": file, **row_scope})

    profiles = []
    for profile in AUTHZ_PROFILES:
        hits = _dedupe_evidence(evidence.get(profile["id"], []))
        if not hits:
            continue
        profiles.append(
            {
                "id": profile["id"],
                "name": profile["name"],
                "confidence": (
                    "table"
                    if any(hit["signal"] == "table_name" for hit in hits)
                    else "field"
                ),
                "evidence": hits,
                "required_controls": list(profile["required_controls"]),
                "acceptance_cases": list(profile["acceptance_cases"]),
                "reference": "references/authorization-models.md",
            }
        )

    return {
        "authorization_profiles": profiles,
        "scope_fields": scope_rows,
        "authorization_notes": [
            "本段只列证据；模型是否成立、范围是否合理由 SKILL 门禁 6 与需求/用户规则判定。",
            "字段名相同不代表语义相同：owner/user_id 可能是创建者、审核者、收件人或转移目标；"
            "证据不足时先停问或按更小权限处理。",
            "scope_fields 中的 ownership/tenant/org/project/role_status 字段不得由客户端在创建或更新时直接赋值。",
            "同一资源命中多个模型时，按 references/authorization-models.md 第五节的组合优先级求值。",
        ],
    }


def build_report(root: Path) -> dict:
    models = scan_models(root)
    sql = scan_sql(root)
    tables = models or sql
    if models and sql:
        known = {m["table"].lower() for m in models}
        for row in sql:
            if row["table"].lower() not in known:
                tables.append(row)
    login_service = scan_service_login(root)
    login_http = scan_http_login(root)
    all_tables = _collect_model_tables(root) + _collect_sql_tables(root)
    authorization = scan_authorization(all_tables)
    return {
        "project_root": str(root),
        "account_tables": tables,
        "login_service": login_service,
        "login_http": login_http,
        "role_signals": scan_role_signals(root, tables),
        "initial_admin": scan_initial_admin(root, tables),
        "token_lifecycle": scan_token_lifecycle(root),
        "token_hints": scan_token_hints(root),
        "authorization_profiles": authorization["authorization_profiles"],
        "scope_fields": authorization["scope_fields"],
        "authorization_notes": authorization["authorization_notes"],
        "notes": [
            "本报告只列证据，是否通过门禁由 SKILL 规则判定。",
            "有 JWT 工具不等于已有登录接口。",
            "Bearer test-token 测试夹具不等于令牌鉴权合格。",
            "有账号表与登录接口不等于系统可用：还需要可登录的初始管理员"
            "（种子脚本 / 初始化 SQL / 迁移）；只有 fixture 或启动时自动 INSERT 不算合格入口。",
            "有会话/刷新/重置结构但只有访问令牌，属于鉴权体系不完整；"
            "判定级别与实现要求见 references/token-lifecycle.md。",
            "Cookie 模式：刷新令牌应由 Set-Cookie 下发、刷新接口只从 Cookie 读取；"
            "Schema 中出现 refresh_token/device_name 需人工判定：请求体不应有，"
            "响应体不应有 refresh_token（device_name 可在响应中用于展示）。",
            "authorization_profiles 是数据权限模型线索，不是已实现的授权；"
            "门禁 6 与 references/authorization-models.md 要求逐模型实现控制点并验收。",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="FastAPI 鉴权预检：账号表 / 登录 / 角色 / 令牌线索 / 数据权限模型"
    )
    parser.add_argument("project_root", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not root.is_dir():
        print(f"项目目录不存在: {root}", file=sys.stderr)
        return 2
    report = build_report(root)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
