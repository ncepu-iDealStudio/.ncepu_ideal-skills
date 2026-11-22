# 路由库存与权限规则格式

这两个可选 JSON 是人工可审阅的对账材料，不是自动生成的授权实现。路径和方法来自目标应用；下面仅说明格式，**不是当前项目的权限决定**。权限可以来自用户规则、证据推断或[默认策略](default-policy.md)，应说明来源，不能把示例值冒充真实业务事实。

## 1. 路由库存

将目标应用的 OpenAPI 文档保存为 `openapi.json`，使用项目虚拟环境中的 Python 执行以下命令。`<skill目录>` 是本 Skill 的完整目录，输出文件放在本次任务的目标项目中；在 PowerShell 中保留引号：

```powershell
python "<skill目录>/scripts/route_inventory.py" openapi.json -o route-inventory.json
```

结果示例：

```json
{
  "routes": [
    {"method": "POST", "path": "/api/v1/auth/login"},
    {"method": "GET", "path": "/api/v1/example/{id}"}
  ]
}
```

OpenAPI 可能遗漏隐藏路由、文档端点及框架自动方法。检查目标应用实际注册的路由、`include_in_schema=False` 项以及 HEAD、OPTIONS 等；将需要归入规则清单的实际项按同样格式并入库存，并说明不适用的基础设施路由及其保护方式。不要对路径大小写、参数名或末尾斜杠自行合并。记录这一步的来源和实际覆盖范围。

## 2. 权限规则

新建 UTF-8 编码 `auth-policy.json`。受保护项的 `roles` 是**非空字符串数组**，`object_scope` 和 `fields` 是非空字符串；即使实际角色编码是数字，也要在此清单写成字符串，并记录其与项目真实编码的对应依据。`public` 不要求 `roles`，但仍应考虑输出字段。路径与库存必须完全一致。

```json
{
  "rules": [
    {
      "method": "POST",
      "path": "/api/v1/auth/login",
      "access": "public",
      "fields": "仅返回登录结果与凭证签发所需字段"
    },
    {
      "method": "GET",
      "path": "/api/v1/example/{id}",
      "access": "protected",
      "roles": ["example-role"],
      "object_scope": "仅有权访问已确认属于本主体的示例对象",
      "fields": "仅返回该角色允许读取的字段"
    }
  ]
}
```

示例中的 `example-role` 和对象规则是格式占位，不得照搬。单独记录规则来源和选择理由；证据不足时按默认策略设计，不能把推断当作已确认的历史数据归属。确实无法安全建立身份或关联时，记录受限范围和阻碍。此格式的 `protected` 规则要求非空角色，刻意对所有角色拒绝的接口请另行记录为受阻，不填写虚构角色来使检查通过。

## 3. 检查

```powershell
python "<skill目录>/scripts/check_policy_coverage.py" route-inventory.json auth-policy.json
```

工具检查清单格式、缺项、重复项与额外规则，并以非零退出码报告问题。它不会验证策略合理、字段陈述是否准确、代码是否生效，也不会实际发送接口请求。必须以真实正反测试及数据库状态验证鉴权。

## 4. 接口处置表（最小接口面）

用于门禁 5。对**最终实际注册路由**逐条声明保留或删除，并写业务理由；规则见[接口面最小化](endpoint-minimization.md)。

```json
{
  "routes": [
    {"method": "GET", "path": "/api/v1/account/{id}", "action": "keep",
     "reason": "查看账号详情，权限码 account:read"},
    {"method": "DELETE", "path": "/api/v1/account/{id}", "action": "remove",
     "reason": "账号改用禁用状态，不做硬删除"},
    {"method": "DELETE", "path": "/api/v1/audit-log/{id}", "action": "remove",
     "reason": "审计记录只读"}
  ]
}
```

- `action` 只能是 `keep` 或 `remove`；`reason` 必须非空且不能是待定占位。
- `keep` 必须存在于最终库存；`remove` 必须不存在。
- 需要收窄行为的端点仍标 `keep`，在 `reason` 里写明收窄后的业务动作。

```powershell
python "<skill目录>/scripts/route_inventory.py" openapi.json -o route-inventory.json
python "<skill目录>/scripts/check_endpoint_surface.py" route-inventory.json endpoint-surface.json
```

工具只验证「处置表与最终路由一致」，不验证删除是否破坏业务；被删端点仍需用真实请求确认 404/405。
