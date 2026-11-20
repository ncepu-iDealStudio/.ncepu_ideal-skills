# {{DISPLAY_EN}} ({{PKG_NAME}})

{{DESCRIPTION_ZH}}

- 插件类型：`{{TYPE}}`
- 插件 id（注册键）：`{{SLUG}}`
- 包名：`{{PKG_NAME}}`

## 目录结构

```text
{{SLUG}}/
├── src/
│   ├── index.ts            # Host 半边：{{HOST_ROLE}}
│   ├── capability.ts       # 业务实现（唯一需要你「填空」的文件）
{{CLIENT_TREE}}├── cordis.patch.yml       # DSH 安装配置（bundle patch）
├── package.json            # dsh.bundle / dsh.client 声明
├── tsconfig.json
├── tsdown.config.ts        # 双目标构建配置
├── README.md               # 本文件：怎么装、怎么构建
└── DEVELOPMENT.md          # 开发指南：扩展功能、调试、打包发布（初学者从这里读起）
```

> 第一次开发请直接读 [`DEVELOPMENT.md`](./DEVELOPMENT.md)：它从「插件是什么」讲到「怎么打包发布」，
> 包含改代码 → 构建 → 装进 DSH → 调试的完整闭环，以及按插件类型给出的扩展步骤和踩坑表。

## 构建

```bash
pnpm install
pnpm typecheck            # tsc --noEmit
pnpm build                # tsdown → lib/index.mjs{{CLIENT_ARTIFACT}}
```

## 安装到 DSH 并验证

```bash
dsh plugin --profile web add .          # 本地目录安装
dsh web --port 3081                     # 重启后验证

dsh --profile web --dump-config | grep {{SLUG}}   # 确认真的进了装配
```

{{VERIFY_STEPS}}

## 发布

```bash
git init && git add . && git commit -m "feat: initial release"
# 先在 GitHub 建好仓库，再推送
git remote add origin git@github.com:<your-account>/{{SLUG}}.git
git push -u origin master
```

npm 发布（可选，包名自带 scope 时注意 `--access public`）：

```bash
pnpm build && pnpm pack
npm publish --access public
```

## 关键约束

1. **包名是唯一键**：`package.json.name`、`tsdown.config.ts` 的 `PLUGIN_ID`、`cordis.patch.yml` 的 `name`、`tsconfig.json` 的 `paths` 键、Client bundle 里的 `__ModuleLoader__` id 必须完全一致。
2. **`dsh.bundle.patch` 不能省**：缺了它，`dsh plugin add` 只把它当普通依赖，路由与设置页都不生效，而且不报错。
3. **`peerDependencies` 必须声明 `@deepseek-ai/cordis`**，否则运行期 cordis 类型不匹配。
4. 不要占用官方 `@deepseek-ai` 命名空间。

生成时间：{{CREATED_AT}}
