"""业务认证 / 授权依赖（依赖 SsoUser，不属于通用 utils）

统一入口：
- get_current_sso_user / get_current_user：验 JWT 后从 DB 加载活跃用户
- get_current_active_user / require_admin|teacher|student：授权链

JWT 纯函数在 utils.auth；本模块只做 FastAPI Depends + 业务表查询。
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from models.sso_user import SsoUser
from utils.auth import jwt_authenticator
from utils.custom_exceptions import AuthenticationException, AuthorizationException
from utils.logger import log_security_event

security = HTTPBearer()


class PermissionChecker:
    """权限检查器（业务规则）"""

    @staticmethod
    def check_user_access_to_resource(
        current_user: SsoUser,
        resource_owner_id: str,
        resource_type: str = "general",
    ) -> bool:
        if current_user.user_type == 3:
            return True
        if current_user.user_id == resource_owner_id:
            return True
        log_security_event(
            "UNAUTHORIZED_RESOURCE_ACCESS",
            user_id=current_user.user_id,
            details={
                "resource_owner": resource_owner_id,
                "resource_type": resource_type,
                "user_type": current_user.user_type_name,
            },
        )
        return False

    @staticmethod
    def check_admin_permission(current_user: SsoUser) -> bool:
        if current_user.user_type != 3:
            log_security_event(
                "ADMIN_PERMISSION_DENIED",
                user_id=current_user.user_id,
                details={"user_type": current_user.user_type_name},
            )
            return False
        return True

    @staticmethod
    def check_teacher_permission(current_user: SsoUser) -> bool:
        if current_user.user_type not in (2, 3):
            log_security_event(
                "TEACHER_PERMISSION_DENIED",
                user_id=current_user.user_id,
                details={"user_type": current_user.user_type_name},
            )
            return False
        return True


async def get_current_sso_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session),
) -> SsoUser:
    """从 Bearer Token 加载活跃 SsoUser（业务认证依赖）。"""
    try:
        payload = jwt_authenticator.verify_token(credentials.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationException("令牌中缺少用户信息")

        user = await db.scalar(
            select(SsoUser).where(
                SsoUser.user_id == str(user_id),
                SsoUser.status == 1,
            )
        )
        if user is None:
            log_security_event("USER_NOT_FOUND_IN_TOKEN", user_id=str(user_id))
            raise AuthenticationException("用户不存在")
        if not user.is_active:
            log_security_event(
                "INACTIVE_USER_ACCESS",
                user_id=str(user_id),
                details={"status": user.status},
            )
            raise AuthenticationException("用户账号已被禁用")
        return user
    except AuthenticationException:
        raise
    except Exception as exc:
        log_security_event("AUTHENTICATION_ERROR", details={"error": str(exc)})
        raise AuthenticationException("身份验证失败") from exc


# 统一别名：业务路由请依赖本符号，勿再用 core.security.get_current_user
get_current_user = get_current_sso_user


async def get_current_active_user(
    current_user: SsoUser = Depends(get_current_sso_user),
) -> SsoUser:
    if not current_user.is_active:
        raise AuthenticationException("用户账号已被禁用")
    return current_user


async def require_admin(
    current_user: SsoUser = Depends(get_current_active_user),
) -> SsoUser:
    if not PermissionChecker.check_admin_permission(current_user):
        raise AuthorizationException("需要管理员权限")
    return current_user


async def require_teacher(
    current_user: SsoUser = Depends(get_current_active_user),
) -> SsoUser:
    if not PermissionChecker.check_teacher_permission(current_user):
        raise AuthorizationException("需要教师权限")
    return current_user


async def require_student(
    current_user: SsoUser = Depends(get_current_active_user),
) -> SsoUser:
    if current_user.user_type not in (1, 3):
        log_security_event(
            "STUDENT_PERMISSION_DENIED",
            user_id=current_user.user_id,
            details={"user_type": current_user.user_type_name},
        )
        raise AuthorizationException("需要学生权限")
    return current_user


def check_resource_ownership(resource_owner_id: str, resource_type: str = "general"):
    """返回校验资源归属的 Depends 可调用对象。"""

    async def _dependency(
        current_user: SsoUser = Depends(get_current_active_user),
    ) -> SsoUser:
        if not PermissionChecker.check_user_access_to_resource(
            current_user, resource_owner_id, resource_type
        ):
            raise AuthorizationException("您无权访问此资源")
        return current_user

    return _dependency
