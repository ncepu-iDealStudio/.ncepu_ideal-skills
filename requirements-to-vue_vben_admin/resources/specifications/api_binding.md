# 已有工程：按接口文档对接真实数据

适用：vue-vben-admin v5 里**已经有**本技能生成的页面和 `apps/web-antd/src/api/`，用户再提供接口文档，要求表格、表单改用真实数据。

从需求生成页面不走本文。本文也不实现后端，不新增菜单。

---

## 1. 先判定，再动手

骨架已存在，当目录里**同时**有：

- `apps/web-antd/src/api/` 下本技能生成的模块文件
- 对应的 `apps/web-antd/src/views/<module>/<page>/list.vue` 与 `data.ts`

没有这些文件就停。不要在 `.vue` 里写 `axios` 或 `fetch`。继续用 `#/api/request` 的 `requestClient`。

| 场景 | 判定 | 动作 |
| --- | --- | --- |
| **对接已有函数** | `api/<module>/<page>.ts` 里已有 list / create / update / delete | 用文档匹配这些函数，在函数内映射 |
| **文档多出接口** | 文档有接口，但没有对应页面或函数 | 不生成页面，不改路由。列入本次未对接 |
| **文档对不上** | 路径、字段或包络无法唯一对应 | 停下来问，不猜 |

一次只对接用户这次文档覆盖的函数。没提到的模块继续走原来的 mock。

---

## 2. 接受的文档，以及先读什么

不要求用户转换成某一种格式。以下都可以：

- OpenAPI / Swagger 的 JSON 或 YAML
- Markdown、Apifox 导出
- 用户粘贴的「方法 + 路径 + 查询参数 + 请求体 + 响应示例」

先读现有页面真正用到的名字，再和文档配对：

- `data.ts` 里列的 `field`、搜索项和表单的 `fieldName`
- `list.vue` 的 `proxyConfig.ajax.query` 传给列表函数的参数，以及它期望的返回形状
- `modules/form.vue` 提交时拿到的表单值

文档里页面用不到的字段，不写进 `data.ts`，也不加列。

---

## 3. 禁止事项

- 禁止改 `data.ts` 的 `field` / `fieldName` 去迁就后端字段名
- 禁止改路由、菜单，禁止按文档新增页面
- 禁止直接使用 `axios`。只通过已有的 `requestClient`
- 禁止重写 `#/api/request` 的登录、刷新令牌或拦截器。vben 自己的认证保持原样
- 禁止把整个应用的 `VITE_GLOB_API_URL` 改掉，除非用户明确说生成的这些模块和 vben 自带接口使用同一个基地址。没写基地址就停下来问
- 禁止删掉无关模块的 `apps/backend-mock` 路由
- 禁止在路径、主字段或分页字段仍有歧义时改该函数

---

## 4. 映射只写在 api 函数里

`SystemUser` 这类 namespace 类型继续描述页面列和表单。文档字段名不同时，在 `api/<module>/<page>.ts` 里进出各映射一次。

列表函数必须仍返回 `list.vue` 已经在用的形状。本技能的列表约定是 `{ items, total }`。文档若是 `{ code, data: { records, total } }`，由 `requestClient` 按项目既有方式解包；解包后的列表再映射成 `items`。不要改 `list.vue` 的 `query`。

```ts
interface UserRow {
  user_id: string
  user_name: string
  account_status: 0 | 1
}

export async function getUserList(params: Recordable<any>) {
  const raw = await requestClient.get<{ records: UserRow[]; total: number }>(
    '/system/users',
    {
      params: {
        page: params.page,
        size: params.pageSize,
        keyword: params.name,
      },
    },
  )
  return {
    items: raw.records.map((row) => ({
      id: row.user_id,
      name: row.user_name,
      status: row.account_status,
    })),
    total: raw.total,
  }
}
```

查询参数名以文档为准，写在这次 `params` 里。页面仍传 `page`、`pageSize` 和表单字段名。文档没写分页字段名时停下来问。

新增和编辑：在 `form.vue` 的提交处调用**已经存在**的 `createXxx` / `updateXxx`，传入 `formApi.getValues()` 的结果。生成阶段这里是 `TODO: 对接真实接口 create/update`，或注释写着先不接真实接口。请求体字段名的转换写在这两个 api 函数内，不写在表单里。删除同理，仍调用已有的 `deleteXxx`。

文档要求的额外请求头，只有现有 `requestClient` 还没带、且文档写明每个业务请求都要带时，才在该函数的请求配置里附加那一个头。文档没写凭证从哪里来，就停下来问，不要新做登录页。

---

## 5. mock 怎么处理

`pnpm dev:antd` 默认会把请求打到 `apps/backend-mock`。某个函数改到真实路径之后：

- 若 `backend-mock` 仍注册了同一路径，真实服务不会被命中。不要悄悄删掉 mock。停下来问：这次是只让这些已对接路径走文档里的服务器，还是整个 dev 仍先用 mock。
- 用户确认走真实服务器后，只去掉**已对接路径**对应的 mock 路由。其他模块的 mock 保留。
- 没对接的函数不要改，继续由原来的 mock 提供数据。

---

## 6. 停下来问

遇到下面任一情况，先问用户，不改该函数，也不改表单提交：

- 现有函数在文档里找不到唯一的路径
- 页面上的主键或主标题列在响应里没有对应字段
- 列表返回形状无法稳妥变成 `{ items, total }`
- 分页或搜索字段的文档参数名没写清
- 成功与失败的包络和现有 `requestClient` 不一致，且项目里看不出该怎么解
- 基地址、鉴权头或凭证来源没写清

能对上的函数可以先做。对不上的函数保持 mock，并在结果里列出原因。

---

## 7. 改完怎么汇报

说明：

- 哪些 api 函数已改路径，以及文档字段如何对应到现有 `field` / `fieldName`
- `form.vue` 的提交是否已接到已有的 create / update
- 哪些模块仍走 mock，以及原因
- 文档里有、但这次没有接的接口
- `data.ts`、路由和 `list.vue` 的列没有因为字段名不同而被改掉
