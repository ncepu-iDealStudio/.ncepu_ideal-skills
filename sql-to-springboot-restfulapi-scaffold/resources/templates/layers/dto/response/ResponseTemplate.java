/**
 * 【AUTO-GENERATED】由 sql-to-springboot-scaffold 生成；表结构变更时技能会重生成。
 * 敏感字段按 type_mappings.json 排除；本类由 Lombok @AllArgsConstructor 生成全参构造，
 * 字段增删时必须同步 Service.mapToResponse() 的构造参数，否则编译失败。
 */
package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
{% for import in additional_imports %}
{{ import }}
{% endfor %}

@Data
@NoArgsConstructor
@AllArgsConstructor
public class {{className}}Response {

{# ===== 响应 DTO 包含所有业务字段，排除：密码等敏感字段 ===== #}
{% for field in responseFields %}
    {% if field.comment %}
    {{field.comment}}
    {% endif %}
    private {{field.javaType}} {{field.fieldName}};

{% endfor %}
}
