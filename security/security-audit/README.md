# security-audit

审计已有代码的安全问题，并给出可复核的报告。改编自 [developer-agent-skills 的 security-audit](https://github.com/reddygopalkrishna/developer-agent-skills/tree/main/skills/security-audit)（MIT），见 `NOTICE`。

## 它做什么

- 按信任边界审查越权、注入、XSS、SSRF、认证与 JWT、密钥、反序列化、上传与路径、CSRF、响应头、依赖和日志
- 用 `scripts/scan_sinks.py` 标出危险 API 候选，再人工判定
- 对本仓库的 FastAPI / Flask / Gin / Spring Boot 脚手架给出落点

## 它不做什么

- 不实现 FastAPI 登录和对象权限。那是 `fastapi-api-security-authentication`
- 不对未授权系统做渗透
- 不在报告里写攻击步骤、载荷或密钥原文

## 用法

对 AI 说：请用 `security-audit` 审计这个项目。只读扫描：

```powershell
python security/security-audit/scripts/scan_sinks.py <目标项目根>
```

自测扫描脚本：

```powershell
python -m unittest security/security-audit/scripts/test_scan_sinks.py
```

从本仓库根目录执行。若当前目录已是 `scripts/`，则：

```powershell
python -m unittest test_scan_sinks.py
```
