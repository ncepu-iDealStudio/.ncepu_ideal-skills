# {{SLUG}} 的 bundle patch：把插件行插入 profile 的插件清单。
# 安装：dsh plugin --profile web add {{PKG_NAME}}
- insert:
    - id: {{SLUG}}
      name: '{{PKG_NAME}}'
