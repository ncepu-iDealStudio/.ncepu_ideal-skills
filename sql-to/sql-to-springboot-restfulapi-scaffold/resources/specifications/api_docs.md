# 接口文档

生成或增量改完代码后，导出接口文档。不要按 SQL 另写一份 JSON，也不要手改导出结果来同步字段。

## 文件

| 文件 | 给谁 | 怎么来 |
|------|------|--------|
| `docs/openapi.json` | Apifox、Apipost | 运行 `scripts/export_openapi.py`，覆盖旧文件 |
| `docs/api.md` | 人阅读、评审 | 同一份 OpenAPI 转成 Markdown，覆盖旧文件 |
| `scripts/export_openapi.py` | 导出入口 | 模板原样拷入；目标项目里已有则不覆盖 |

导入 Apifox 或 Apipost 时选择 OpenAPI / Swagger，上传 `docs/openapi.json`。`docs/api.md` 不能当作接口定义导入。

## 内容从哪来

脚本先读 `application.properties` 里的端口、`server.servlet.context-path` 和 `springdoc.api-docs.path`。

1. 应用已经启动，并且 `/api-docs` 里的路径对得上当前 Controller 时，用 springdoc 的结果。手写端点、登录约束以运行中的应用为准。
2. 应用没启动，或文档对不上这些 Controller 时，按 `*Controller.java` 和 Request/Response DTO 生成。这一步不连接数据库，也不改 `application.properties`。

两种结果都是 OpenAPI。`servers` 带上 context-path，例如 `http://127.0.0.1:8080/api/v1`；路径是 Controller 上的映射，例如 `/students`。业务接口默认不声明鉴权。代码里写了 `@PreAuthorize` 的，导出后标在对应接口上。

本技能仍然只有 5 个脚手架 CRUD 端点，不因为导出而新增 `PATCH /{id}/status`。用户写在 Controller 里的自定义端点会跟着导出。

## 何时导出

`greenfield`、`add_table`、`alter_table` 在代码落盘后执行：

```text
python scripts/export_openapi.py
```

`drop_table` 只输出待删清单、不改代码，此时不导出。用户按清单改完代码后，再导出一次。

应用后来启动过，再执行一次脚本，就会改用 springdoc 的文档覆盖先前那份。

## 禁止

- 手改 `docs/openapi.json` 或 `docs/api.md` 来同步字段、路径或鉴权。
- 用 Markdown 代替 `openapi.json` 作为导入文件。
- 覆盖用户已经改过的 `scripts/export_openapi.py`。
- 为了导出去改 `pom.xml` 或 `application.properties`。
