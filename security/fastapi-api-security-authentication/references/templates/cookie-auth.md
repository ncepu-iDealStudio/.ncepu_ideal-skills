# Cookie 认证实现模板（FastAPI，通用）

复制到目标项目后按实际命名调整。适用于「浏览器 + 刷新令牌 + 会话」场景：

- 刷新令牌只放 HttpOnly Cookie，响应体不返回；
- 刷新接口只从 Cookie 读；
- 设备名称从请求头获取，不从 body 获取。

不要把这些名字当成目标项目的既定事实，按已有配置与模型替换。

## 1. 配置

```python
# config/config_unified.py（追加到现有 BaseConfig）
refresh_cookie_name: str = "refresh_token"
refresh_cookie_path: str = "/api/v1/auth"   # 只随认证请求发送
refresh_cookie_samesite: str = "lax"        # 跨站前端再评估 none + CSRF
refresh_cookie_secure: bool = True          # 开发环境可覆盖为 false
```

`.env.example` 只放非敏感默认值：

```ini
REFRESH_COOKIE_NAME=refresh_token
REFRESH_COOKIE_PATH=/api/v1/auth
REFRESH_COOKIE_SAMESITE=lax
REFRESH_COOKIE_SECURE=true
```

## 2. Cookie 读写工具

```python
from fastapi import Response

from config import settings


def set_refresh_cookie(response: Response, raw_refresh: str, max_age: int) -> None:
    """写入刷新令牌 Cookie：HttpOnly + SameSite + Path 限定 + 生产 Secure。"""
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=raw_refresh,
        max_age=max_age,
        httponly=True,
        secure=bool(settings.refresh_cookie_secure),
        samesite=settings.refresh_cookie_samesite,
        path=settings.refresh_cookie_path,
        domain=None,
    )


def clear_refresh_cookie(response: Response) -> None:
    """登出/吊销时清空 Cookie，属性必须与写入时一致。"""
    response.delete_cookie(
        key=settings.refresh_cookie_name,
        path=settings.refresh_cookie_path,
        httponly=True,
        secure=bool(settings.refresh_cookie_secure),
        samesite=settings.refresh_cookie_samesite,
        domain=None,
    )
```

## 3. 设备名称来自请求头

```python
DEVICE_NAME_MAX_LENGTH = 100


def device_name_from_headers(
    user_agent: str | None,
    x_device_name: str | None = None,
) -> str:
    """设备名称只用于展示/审计；优先网关可信头，其次 User-Agent。

    不要从请求体读取；不要用于授权判断。
    """
    candidate = (x_device_name or user_agent or "").strip() or "unknown"
    return candidate[:DEVICE_NAME_MAX_LENGTH]
```

在路由里显式取头，不放进请求 Schema：

```python
from fastapi import Header

device = device_name_from_headers(
    user_agent=user_agent,
    x_device_name=x_device_name,
)
```

## 4. 登录：写 Cookie，响应体不含刷新令牌

```python
@router.post("/login", response_model=SuccessResponse[TokenResponse])
async def login(
    data: LoginRequest,
    request: Request,
    response: Response,
    user_agent: str | None = Header(default=None, alias="User-Agent"),
    x_device_name: str | None = Header(default=None, alias="X-Device-Name"),
    service: AuthService = Depends(get_auth_service),
):
    result = await service.login(
        username=data.username,
        password=data.password,
        source_ip=client_ip(request),
        device_name=device_name_from_headers(user_agent, x_device_name),
    )
    set_refresh_cookie(response, result.raw_refresh, result.refresh_max_age)
    return success_response(result.body_without_refresh, message="登录成功")
```

`LoginRequest` 不包含 `device_name`；`TokenResponse` 不包含 `refresh_token`：

```python
class LoginRequest(BaseModel):
    username: str
    password: str
    model_config = ConfigDict(extra="forbid")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile
    model_config = ConfigDict(extra="forbid")
```

## 5. 刷新：只从 Cookie 读

```python
from fastapi import Cookie


@router.post("/refresh", response_model=SuccessResponse[TokenResponse])
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=settings.refresh_cookie_name),
    user_agent: str | None = Header(default=None, alias="User-Agent"),
    x_device_name: str | None = Header(default=None, alias="X-Device-Name"),
    service: AuthService = Depends(get_auth_service),
):
    if not refresh_token:
        raise AuthenticationException("未授权或登录已失效")

    result = await service.refresh(
        raw_refresh=refresh_token,
        device_name=device_name_from_headers(user_agent, x_device_name),
    )
    set_refresh_cookie(response, result.raw_refresh, result.refresh_max_age)
    return success_response(result.body_without_refresh, message="刷新成功")
```

要求：

- 不定义 `RefreshRequest.refresh_token`，也不从 body/query 读取令牌；
- 旧令牌轮换后立即失效；重放触发会话吊销；
- 响应 `Set-Cookie` 必须是新值。

## 6. 登出：清 Cookie

```python
@router.post("/logout")
async def logout(
    response: Response,
    principal: Principal = Depends(require_authenticated),
    service: AuthService = Depends(get_auth_service),
):
    await service.logout(principal)
    clear_refresh_cookie(response)
    return success_response(None, message="已登出")
```

## 7. OpenAPI 与测试提示

- 刷新/登出声明 Cookie 方案（如 `APIKeyCookie`），避免文档暗示刷新令牌在 body。
- 测试至少覆盖：
  - 登录 `Set-Cookie` 含 HttpOnly / SameSite / Path / Max-Age，响应体无 `refresh_token`；
  - 刷新仅凭 Cookie 成功，且 `Set-Cookie` 更新；
  - 仅传 body、无 Cookie 的刷新返回 401/422；
  - body 带 `refresh_token` 或 `device_name` 被 422 拒绝；
  - 登出清空 Cookie；
  - 会话记录的设备名来自 `User-Agent` / `X-Device-Name`。
