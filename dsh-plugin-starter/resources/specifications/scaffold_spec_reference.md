# 生成器 spec 参考（scaffold_plugin.py 的输入契约）

模型的职责是：**需求 → 这份 spec → 一条命令**。业务代码由模型随后在生成出的 `capability.ts` 里补齐。

---

## 1. 完整示例

```json
{
  "plugin": {
    "packageName": "@your-scope/dsh-notebook",
    "slug": "dsh-notebook",
    "type": "dual-face",
    "version": "0.1.0",
    "license": "MIT",
    "author": "Your Name <you@example.com>",
    "repoUrl": "https://github.com/your-scope/dsh-notebook",
    "displayNameZh": "笔记本",
    "displayNameEn": "Notebook",
    "descriptionZh": "在 DSH 设置页里记录与管理笔记。",
    "descriptionEn": "Manage notes from a DSH settings section."
  },
  "capability": {
    "summary": "笔记的增删查",
    "toolName": "notebook_search",
    "toolDescription": "在用户笔记里搜索关键词。当用户问『我之前记过什么』时使用。",
    "routePrefix": "/notebook",
    "parameters": [
      { "name": "query", "type": "string", "required": true, "description": "搜索关键词" },
      { "name": "limit", "type": "number", "required": false, "description": "返回条数，默认 10" }
    ]
  }
}
```

---

## 2. 字段表

### `plugin`

| 字段 | 必需 | 默认 | 规则 |
|---|---|---|---|
| `packageName` | ✅ | —— | `^@scope/dsh-xxx$`；不能用 `@deepseek-ai`；最后一段 = `slug` |
| `slug` | 建议 | 由包名推导 | `^dsh-[a-z0-9-]+$` |
| `type` | ✅ | `tool-only` | `tool-only` / `route-only` / `dual-face` / `interceptor` |
| `version` | | `0.1.0` | SemVer |
| `license` | | `MIT` | |
| `author` | | 空 | 写进 `package.json.author` |
| `repoUrl` | | 空 | 写进 `package.json.repository` |
| `displayNameZh` / `displayNameEn` | | 等于 slug | 设置页标题、locale title |
| `descriptionZh` / `descriptionEn` | | 自动兜底 | `package.json.description` 用英文，README 用中文 |

### `capability`

| 字段 | 适用类型 | 说明 |
|---|---|---|
| `summary` | 全部 | 一句话说明这个插件提供什么能力 |
| `toolName` | `tool-only` 必填 | snake_case，模型可见；`run_code` 禁用 |
| `toolDescription` | `tool-only` | 从模型视角写「何时使用」，会进入工具描述 |
| `routePrefix` | `route-only` / `dual-face` 必填 | 形如 `/notebook`，无尾斜杠 |
| `parameters` | `tool-only` | 参数数组；为空时自动补一个 `input: string` |

参数 `type` 仅支持：`string` / `number` / `boolean` / `string[]`。
（需要 `enum`、对象嵌套等复杂 schema 时，生成后直接改 `src/index.ts` 的 `parameters`。）

---

## 3. 类型与必需字段的对应关系

| type | 必需 spec 字段 | 生成内容 | 有无 Client |
|---|---|---|---|
| `tool-only` | `capability.toolName` | `src/index.ts`（defineTool）+ `capability.ts` | 无 |
| `route-only` | `capability.routePrefix` | `src/index.ts`（routes）+ `capability.ts` | 无 |
| `dual-face` | `capability.routePrefix` | 同上 + `src/client/index.ts`（设置页） | 有 |
| `interceptor` | 无 | `src/index.ts`（tools/pre-execute）+ `capability.ts` | 无 |

所有类型都会额外生成：`package.json`、`tsconfig.json`、`tsdown.config.ts`、`cordis.patch.yml`、`README.md`、**`DEVELOPMENT.md`（初学者开发指南）**、`.gitignore`。

---

## 4. 命令行

```bash
# spec 驱动（推荐）
python resources/tools/scaffold_plugin.py --spec spec.json --out ./dsh-notebook

# 参数直给（快速起步）
python resources/tools/scaffold_plugin.py \
  --type dual-face \
  --name @me/dsh-notebook \
  --route /notebook \
  --display-zh "笔记本" --display-en "Notebook" \
  --desc-zh "在设置页管理笔记" \
  --out ./dsh-notebook

# 只看将生成哪些文件
python resources/tools/scaffold_plugin.py --spec spec.json --out ./x --dry-run

# 目标目录非空时覆盖
python resources/tools/scaffold_plugin.py --spec spec.json --out ./x --force
```

CLI 参数优先于 spec 文件；`--dry-run` 不写盘。

---

## 5. 生成后必须做的事（模型自查）

1. 打开 `src/capability.ts`，把 demo 实现替换成真实业务逻辑（保持纯函数、不 import DSH API）。
2. 需要多个工具/路由时，按 `DEVELOPMENT.md` 第 5 章的模式追加注册块。
3. 跑 `validate_plugin.py`，确保 0 错误。
4. 提示用户：`pnpm install && pnpm typecheck && pnpm build`，然后 `dsh plugin --profile web add .`。
