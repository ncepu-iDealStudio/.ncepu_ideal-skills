"""
{{table_comment}}数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime, date, time
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class {{class_name}}Base(BaseModel):
    """
    {{table_comment}}基础模型
    """
    {% for field in non_primary_fields %}
    {{field.name}}: {{field.pydantic_type}}{% if not field.not_null %} | None{% endif %} = Field(
        {% if field.not_null %}...{% else %}None{% endif %},
        {% if field.max_length %}max_length={{field.max_length}},{% endif %}
        {% if field.ge %}ge={{field.ge}},{% endif %}
        {% if field.le %}le={{field.le}},{% endif %}
        description="{{field.comment}}"
    )
    {% endfor %}

    {% for validator in validators %}
    @field_validator("{{validator.field_name}}")
    @classmethod
    def validate_{{validator.field_name}}(cls, v):
        {% if validator.type == "phone" %}
        if v is not None:
            import re
            if not re.match(r"^1[3-9]\d{9}$", v):
                raise ValueError("手机号格式不正确")
        {% elif validator.type == "email" %}
        if v is not None:
            import re
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
                raise ValueError("邮箱格式不正确")
        {% elif validator.type == "gender" %}
        if v is not None and v not in ["男", "女", "其他"]:
            raise ValueError("性别只能是：男、女、其他")
        {% endif %}
        return v
    {% endfor %}


class {{class_name}}Create({{class_name}}Base):
    """
    {{table_comment}}创建模型
    """
    class Config:
        json_schema_extra = {
            "example": {
                {% for field in non_primary_fields %}
                "{{field.name}}": {{field.example}},
                {% endfor %}
            }
        }


class {{class_name}}Update(BaseModel):
    """
    {{table_comment}}更新模型
    """
    {% for field in non_primary_fields %}
    {{field.name}}: {{field.pydantic_type}} | None = Field(
        default=None,
        {% if field.max_length %}max_length={{field.max_length}},{% endif %}
        {% if field.ge %}ge={{field.ge}},{% endif %}
        {% if field.le %}le={{field.le}},{% endif %}
        description="{{field.comment}}"
    )
    {% endfor %}

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                {% for field in non_primary_fields %}
                "{{field.name}}": {{field.example}},
                {% endfor %}
            }
        }


class {{class_name}}Response(BaseModel):
    """
    {{table_comment}}响应模型
    """
    {% for field in all_fields %}
    {{field.name}}: {{field.pydantic_type}}{% if not field.not_null %} | None{% endif %}
    {% endfor %}

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                {% for field in all_fields %}
                "{{field.name}}": {{field.example}},
                {% endfor %}
            }
        }

