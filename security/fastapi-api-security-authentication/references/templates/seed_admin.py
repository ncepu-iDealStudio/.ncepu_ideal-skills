"""初始管理员种子脚本模板（fastapi-api-security-authentication）。

复制到目标项目 ``scripts/seed_admin.py`` 后，按实际模型与角色设计调整 import 和字段。

用法::

    uv run python scripts/seed_admin.py
    uv run python scripts/seed_admin.py --reset-password
    FASTAPI_ENV=production uv run python scripts/seed_admin.py --allow-production

环境变量（写入项目根 ``.env``，不要提交）::

    INITIAL_ADMIN_USERNAME=...
    INITIAL_ADMIN_PASSWORD=...

安全约束：
- 不硬编码账号或口令；缺配置、口令过短、命中弱口令/占位值时非零退出且不写入。
- 幂等：账号存在则跳过；仅 ``--reset-password`` 时更新哈希。
- 不打印口令、哈希或连接串。
- 不在应用启动/lifespan 中自动执行，必须显式调用。
- 使用项目统一哈希工具（Argon2id），不自行实现加密。

若项目使用角色表（role / user_role）而非 ``is_admin`` 字段，请在写入账号后
同时写入最小管理员角色绑定，并保持同样的幂等判断。
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

MIN_PASSWORD_LENGTH = 12
WEAK_PASSWORDS = {
    "123456",
    "12345678",
    "password",
    "password123",
    "admin",
    "admin123",
    "root",
    "qwerty",
}
PLACEHOLDERS = {
    "",
    "change_me",
    "changeme",
    "your_password",
    "initial_admin_password",
    "<set-me>",
}


def _fail(message: str, code: int = 2) -> None:
    """配置/环境错误：标准错误输出并退出，不写出任何数据。"""
    print(f"[seed_admin] 失败：{message}", file=sys.stderr)
    raise SystemExit(code)


def _load_dotenv() -> None:
    """优先读取项目根 .env；未安装 python-dotenv 时改用进程环境。"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(PROJECT_ROOT / ".env")


def _read_config(allow_production: bool) -> tuple[str, str]:
    """读取并校验初始化配置。"""
    username = (os.getenv("INITIAL_ADMIN_USERNAME") or "").strip()
    password = os.getenv("INITIAL_ADMIN_PASSWORD") or ""

    if not username:
        _fail("缺少 INITIAL_ADMIN_USERNAME")
    if len(password) < MIN_PASSWORD_LENGTH:
        _fail(f"INITIAL_ADMIN_PASSWORD 至少 {MIN_PASSWORD_LENGTH} 位")
    normalized = password.strip().lower()
    if normalized in PLACEHOLDERS:
        _fail("INITIAL_ADMIN_PASSWORD 仍是占位值，请设置真实口令")
    if normalized in WEAK_PASSWORDS or normalized == username.lower():
        _fail("INITIAL_ADMIN_PASSWORD 强度不足（弱口令或与用户名相同）")

    from config import settings

    environment = getattr(settings, "environment", "development")
    environment = getattr(environment, "value", environment)
    if str(environment).lower() == "production" and not allow_production:
        _fail("生产环境需显式 --allow-production 才会写入管理员")
    return username, password


async def _seed(username: str, password: str, reset_password: bool) -> int:
    """幂等写入管理员账号。"""
    from sqlalchemy import select

    import models  # noqa: F401  确保 ORM 元数据已加载
    from core import database
    from models.app_user import AppUser  # TODO: 按项目实际模型调整
    from utils.security import SecurityUtil  # TODO: 使用项目统一哈希工具

    await database.create_database_pool()
    try:
        # 异步会话工厂在建池后才赋值，必须从模块属性动态读取
        async with database.AsyncSessionLocal() as db:
            user = await db.scalar(
                select(AppUser).where(AppUser.username == username)
            )

            if user is not None and not reset_password:
                print(f"[seed_admin] 账号已存在，跳过：{username}")
                return 0

            if user is not None:
                user.password_hash = SecurityUtil.hash_password(password)
                user.status = 1
                user.is_admin = True  # TODO: 角色表项目改为写入管理员角色绑定
                await db.commit()
                print(f"[seed_admin] 已重置管理员口令：{username}")
                return 0

            db.add(
                AppUser(
                    username=username,
                    password_hash=SecurityUtil.hash_password(password),
                    is_admin=True,  # TODO: 角色表项目改为写入管理员角色绑定
                    status=1,
                )
            )
            await db.commit()
            print(f"[seed_admin] 已创建管理员：{username}")
            return 0
    finally:
        await database.close_database_pool()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="初始化管理员账号（幂等）")
    parser.add_argument(
        "--reset-password",
        action="store_true",
        help="账号已存在时重置口令（默认跳过）",
    )
    parser.add_argument(
        "--allow-production",
        action="store_true",
        help="允许在生产环境执行",
    )
    args = parser.parse_args(argv)

    _load_dotenv()
    username, password = _read_config(args.allow_production)
    return asyncio.run(_seed(username, password, args.reset_password))


if __name__ == "__main__":
    raise SystemExit(main())
