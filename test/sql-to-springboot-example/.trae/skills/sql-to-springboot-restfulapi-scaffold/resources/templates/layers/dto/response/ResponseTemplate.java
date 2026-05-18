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
