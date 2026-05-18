package com.security.apisecurity.dto.request;

import lombok.Data;
{% for import in additional_imports %}
{{ import }}
{% endfor %}
import jakarta.validation.constraints.*;

@Data
public class {{className}}Request {

{# ===== 请求 DTO 包含业务字段，排除：主键、自动生成字段（create_time、update_time）、软删除字段 ===== #}
{% for field in requestFields %}
    {% if field.comment %}
    {{field.comment}}
    {% endif %}
    {% if field.validation_annotation %}
    {{field.validation_annotation}}
    {% endif %}
    private {{field.javaType}}{% if field.nullable %} = null{% endif %};

{% endfor %}
    public {{className}}Request() {
    }
}
