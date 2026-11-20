# 插件清单契约（manifest）

DSH 没有单一「manifest 文件」。插件的「身份 + 装配声明」分散在四个文件里，**以包名为唯一键**互相钉死。任何一处不一致，症状都是「装了但不生效」，而且不报错。

---

## 1. 包名是唯一键

```json
"name": "@your-scope/dsh-notebook"
```

同一个字符串必须出现在：

| 位置 | 字段 | 不一致的后果 |
| --- | --- | --- |
| `package.json` | `name` | —— |
| `tsdown.config.ts` | `const PLUGIN_ID` | Client bundle 的注册 id 错，浏览器侧加载不到 |
| `cordis.patch.yml` | `name` | 插件行插不进 profile 的装配层 |
| `tsconfig.json` | `paths` 的键（`<包名>/client`） | 仅类型解析失效（编译期报错，容易发现） |
| 运行期 | `window.__ModuleLoader__.load({ id })` | 由 tsdown 从 `PLUGIN_ID` 生成，因此只需保证后者正确 |

---

## 2. `package.json` 必需字段

```json
{
  "name": "@your-scope/dsh-notebook",
  "version": "0.1.0",
  "type": "module",
  "main": "lib/index.mjs",
  "types": "lib/index.d.mts",
  "exports": {
    ".": { "types": "./lib/index.d.mts", "default": "./lib/index.mjs" },
    "./client": { "types": "./lib/types/client/index.d.ts", "default": "./lib/client.js" },
    "./package.json": "./package.json"
  },
  "files": ["lib/index.mjs", "lib/index.d.mts", "lib/client.js", "cordis.patch.yml"],
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" },
    "client": {
      "inject": [
        "@deepseek-ai/dsh-client-runtime",
        "@deepseek-ai/dsh-client-ui-slots",
        "@deepseek-ai/dsh-client-ui-settings",
        "@deepseek-ai/dsh-client-locale"
      ],
      "platform": "web",
      "immediately": true
    }
  },
  "peerDependencies": { "@deepseek-ai/cordis": "^4.0.1" }
}
```

### 字段逐条解释

| 字段 | 是否必需 | 说明 |
| --- | --- | --- |
| `type: "module"` | 必需 | Host 产物是 ESM |
| `main` / `types` / `exports["."]` | 必需 | Host 入口，指向 `lib/index.mjs` |
| `exports["./client"]` | 带界面必需 | Client 入口，DSH 模块系统按「包名 + `/client`」解析 |
| `files` | 必需 | **必须包含 `cordis.patch.yml`**，否则别人装了不会进清单 |
| `dsh.bundle.patch` | **必需（最易漏）** | 指向 bundle patch；缺了它 `dsh plugin add` 只当普通依赖 |
| `dsh.client` | 带界面必需 | 声明 Client 半边存在 |
| `dsh.client.inject` | 带界面必需 | **模块表依赖**（包名边），不是服务名 |
| `dsh.client.platform` / `immediately` | 建议 | `web`；`true` 表示首阶段预取 |
| `peerDependencies` | 必需 | 必须含 `@deepseek-ai/cordis`，否则运行期类型不匹配 |

> **两套 inject 不要混**：`package.json.dsh.client.inject` 填的是**包名**（模块表行）；`src/client/index.ts` 里 `export const inject` 填的是**服务名**（如 `slots`、`locale`）。两者都需要。

### 纯 Host 插件（tool-only / route-only / interceptor）

删掉 `exports["./client"]`、`files` 里的 `lib/client.js`、整个 `dsh.client`；`peerDependencies` 按用到的服务声明 `@deepseek-ai/dsh-tools` 或 `@deepseek-ai/dsh-host-webserver`。

---

## 3. `cordis.patch.yml`

```yaml
# bundle patch：把插件行插入 profile 的插件清单
- insert:
    - id: dsh-notebook            # 建议用插件 id
      name: '@your-scope/dsh-notebook'   # 必须等于包名
```

- `insert` 段不能省：DSH 靠它把插件行合并进 profile 的 bundle 层。
- `name` 与包名不一致 → 装了个空壳。
- `id` 是这一行的标识，建议与插件 id 一致，便于 `--dump-config` 检索。

---

## 4. 安装路径的三个 scope

| scope | 路径 | 用途 |
| --- | --- | --- |
| profile 安装 | `dsh plugin --profile web add <dir\|tgz\|github:user/repo>` | 正式安装，写进 profile 的 `package.json` + `dsh.profile.bundles` |
| 开发期覆盖 | `dsh --profile headless --patch ./dev.patch.yml` | 跳过安装，直接把源码挂进进程（路径相对 profile 目录解析） |
| 技能安装 | `<DSH_HOME>/skills/<name>/SKILL.md` | 不是插件；这是本仓库这种「技能」的安装方式 |

---

## 5. 自检

```bash
python resources/tools/validate_plugin.py <插件目录>
dsh --profile web --dump-config | grep <插件包名>
```

两条都过，才算「真的装上了」。`validate_plugin.py` 的第 2–9 项就是这个契约的可执行版本。
