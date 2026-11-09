# 可选本机 HTTP 鉴权探测

`scripts/http_auth_probe.py` 是小范围探测工具，不自动发现规则或生成业务用例。只连接明确提供的 `127.0.0.1`、`localhost` 或 `::1`，不跟随重定向，不使用代理；只发送 GET/OPTIONS 和配置的登录 POST。使用前确认目标服务和登录操作属于本次实验，且要访问的 GET/OPTIONS 确实不修改数据。工具不覆盖写操作、对象归属、数据库副作用或所有路由，不能作为完整验收。

配置文件示例（项目必须先建立独立测试账号；示例路径、字段和预期均需根据实际项目修改）：

```json
{
  "base_url": "http://127.0.0.1:8000",
  "login": {
    "path": "/api/v1/auth/login",
    "format": "json",
    "account_field": "account",
    "password_field": "password",
    "token_path": "data.access_token"
  },
  "identities": {
    "testuser": {
      "account_env": "AUTH_TEST_USER",
      "password_env": "AUTH_TEST_PASSWORD"
    }
  },
  "cases": [
    {
      "name": "anonymous-denied",
      "method": "GET",
      "path": "/api/v1/example/1",
      "identity": "anonymous",
      "expect": {"status": 401, "json_equals": {"code": 401}, "forbidden_fields": ["password", "password_hash"]}
    },
    {
      "name": "testuser-allowed",
      "method": "GET",
      "path": "/api/v1/example/1",
      "identity": "testuser",
      "expect": {"status": 200, "json_equals": {"code": 200, "data.id": 1}, "forbidden_fields": ["password", "password_hash"]}
    }
  ]
}
```

`account_env` 和 `password_env` 填的是当前进程环境变量名，不能写真实密码；应通过本地安全方式设置，不在命令行、日志或报告中输出值。`login.format` 支持 `json` 和 `form`。`identity` 可设为 `anonymous`、`invalid` 或已配置身份。每条用例必须包含具体的预期 HTTP 状态、至少一个 `json_equals` 路径断言和非空 `forbidden_fields`。允许的状态为 2xx、401、403；需要验证以 404 隐藏存在性、无 JSON 正文的 HEAD 或其他响应时，使用目标项目的测试实现。脚本对失败返回非零，不输出响应正文和令牌。

```powershell
python "<skill目录>/scripts/http_auth_probe.py" auth-probe.json
```

脚本只保证逐条执行及断言，不会检查正反场景是否足够、业务规则是否正确，也不会在失败时自动修复。模型应根据测试规范补充项目专属的真实写操作、数据库状态、隔离和完整覆盖测试。
