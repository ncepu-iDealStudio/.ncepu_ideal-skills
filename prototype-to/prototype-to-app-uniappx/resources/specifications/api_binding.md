# 已有工程：按接口文档对接真实数据

适用：目标目录**已经是**本技能生成的 uni-app x 工程（或同结构工程），用户提供接口文档，要求页面改用真实数据。

从零生成工程不走本文。本文也不实现后端。

---

## 1. 先判定，再动手

骨架已存在，当目录里**同时**有：

- `pages.json`
- `manifest.json`，且含 `"uni-app-x"`
- `services/api/`，且其中有业务接口文件（如 `skill.ts`）和 `request.ts`

没有 `services/api` 就停。不要在 `.uvue` 页面里写 `uni.request`。

| 场景 | 判定 | 动作 |
| --- | --- | --- |
| **对接已有函数** | 页面已经调用 `services/api` 里的某个函数 | 用文档匹配该函数，在函数内映射并改为 `request()` |
| **文档多出接口** | 文档有写接口、详情接口，但工程没有对应页面或函数 | 不生成页面，不新增函数。列入本次未对接 |
| **文档对不上** | 路径、字段或包络无法唯一对应 | 停下来问，不猜 |

一次只对接用户这次给出的文档所覆盖的函数。未提到的函数保持原来的 mock 分支。

---

## 2. 接受的文档，以及先读什么

不要求用户把文档转成某一种格式。以下都可以：

- OpenAPI / Swagger 的 JSON 或 YAML
- Markdown、Apifox 导出
- 用户粘贴的「方法 + 路径 + 请求参数 + 响应示例」

对每个**已经存在**的 `services/api` 函数，只提取这些信息：

| 项 | 用途 |
| --- | --- |
| HTTP 方法与路径 | 填入该函数的 `request({ url, method })` |
| 查询参数 / 路径参数 | 仅当页面已经把对应参数传给该函数 |
| 响应字段 | 映射到该函数已经返回的页面类型 |
| 包络 | 是否为 `{ code, message, data }` 或文档写明的其他外壳 |
| 成功码 | 调整 `request.ts` 里那一处判断 |
| 鉴权头 | 文档写明才加 |

先列页面真正用到的字段，再和响应字段配对。文档里页面用不到的字段不写进页面类型。

---

## 3. 禁止事项

- 禁止把全局 `USE_MOCK` 改成 `false`，除非页面调用的**每一个**函数都已映射完成
- 禁止改页面、组件的调用方式，禁止把后端字段名写进 `.uvue`
- 禁止在页面里直接 `uni.request`
- 禁止引入 axios 或其他 HTTP 客户端。继续用 `services/api/request.ts` 里的 `uni.request`
- 禁止为了一个请求头新建登录页、刷新令牌或通用拦截器
- 禁止把接口文档当成页面清单去加页面。新页面还必须注册 `pages.json`，本文不新增页面
- 禁止在路径、字段、包络或成功码仍有歧义时删掉该函数的 mock 分支

`USE_MOCK` 的默认值保持 `true`。已对接的函数不再走自己的 mock 分支；未对接的函数继续 `if (USE_MOCK)`。

---

## 4. 包络留在 request.ts，字段映射留在业务函数

`request<T>()` 只负责拼 `BASE_URL`、发 `uni.request`、按文档解开外壳并返回 `data`。它不认识 `Skill` 这种页面类型。

文档的成功码不是 `0`，或外壳字段不叫 `code` / `message` / `data` 时，只改 `request.ts` 里这一处判断，并改 `ApiResponse`。成功码以文档为准，不要沿用模板里的 `0`。

业务函数保持原来的签名和返回类型。下面以 `getSkillList(): Promise<Skill[]>` 为例。文档列表项字段是 `skill_id`、`skill_name`、`publisher_name`，外壳仍由 `request()` 解开，`request` 的泛型是原始项而不是 `Skill`。

```ts
interface SkillRow {
  skill_id: number
  skill_name: string
  publisher_name: string
  avatar_url?: string
  tag_list?: string[]
}

export async function getSkillList(page: number = 1, pageSize: number = 10): Promise<Skill[]> {
  const rows = await request<SkillRow[]>({
    url: '/skills',
    method: 'GET',
    data: { page, pageSize }
  })
  return rows.map(row => ({
    id: row.skill_id,
    title: row.skill_name,
    userName: row.publisher_name,
    avatar: row.avatar_url ?? '',
    tags: row.tag_list ?? []
  }))
}
```

同一文件里尚未对接的函数继续保留 `if (USE_MOCK)` 分支。

文档要求每个请求都带同一个请求头时，加在 `request.ts` 的 `header` 里，只加文档写明的那一个。只有单个接口需要时，通过该次 `request({ header })` 传入。文档没写凭证从哪里来，就停下来问，不要新做登录页。

缺少的可选展示字段用空字符串或空数组。缺少页面必需字段（如列表项 `id`、主标题）时停下来问。

设置 `BASE_URL` 为文档中的基地址。文档没写基地址时停下来问，不要猜域名。

---

## 5. 分页、筛选、详情

- 页面已经把 `page` 等参数传给现有函数，并且文档有对应查询参数时，把参数放进该函数已有的 `data`
- 页面没有分页或筛选交互时，不因为文档里有 `page`、`keyword` 就新做控件
- 文档有详情接口，但工程没有详情页、也没有对应的现有函数时，不新增详情页

---

## 6. 停下来问

遇到下面任一情况，先问用户，不改该函数的 mock 分支：

- 现有函数在文档里找不到唯一的路径
- 同一函数能对上多个路径
- 页面主字段在响应里没有对应字段
- 响应包络有两种以上解释
- 成功码没有写明
- 文档要求鉴权，但没写请求头名称，或没写凭证从哪里来
- 没写接口基地址

能对上的函数可以先做。对不上的函数保持 mock，并在结果里列出原因。

---

## 7. 改完怎么汇报

说明：

- 哪些函数已走 `request()`（路径、原始字段 → 页面字段）
- `BASE_URL` 和成功码取自文档的哪一处
- 哪些函数仍走 mock，以及原因
- 文档里有、但这次没有接的接口
- 页面调用方式没有改，全局 `USE_MOCK` 是否仍然为 `true`
