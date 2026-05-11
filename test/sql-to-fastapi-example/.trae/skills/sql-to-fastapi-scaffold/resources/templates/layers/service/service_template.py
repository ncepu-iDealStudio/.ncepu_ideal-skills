"""
{{table_comment}}业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from models.{{table_name}} import {{class_name}}
from schemas.{{table_name}} import {{class_name}}Create, {{class_name}}Update, {{class_name}}Response
from utils.custom_exceptions import BadRequestException, NotFoundException


class {{class_name}}Service:
    """
    {{table_comment}}服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: {{class_name}}Create) -> {{class_name}}Response:
        """
        创建{{table_comment}}记录
        """
        {% for pk in primary_keys %}
        existing = self.db.query({{class_name}}).filter(
            {{class_name}}.{{pk.name}} == data.{{pk.name}}
        ).first()
        if existing:
            raise BadRequestException("{{pk.comment}}已存在")
        {% endfor %}

        {% for fk in foreign_keys %}
        {% if fk.check_existence %}
        if data.{{fk.field_name}}:
            pass
        {% endif %}
        {% endfor %}

        obj = {{class_name}}(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return {{class_name}}Response.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        """
        获取{{table_comment}}记录列表
        """
        {% if soft_delete_field %}
        query = self.db.query({{class_name}}).filter(
            {{class_name}}.{{soft_delete_field}} == False
        )
        {% else %}
        query = self.db.query({{class_name}})
        {% endif %}

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [{{class_name}}Response.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, {{primary_key_param}}: {{primary_key_type}}) -> {{class_name}}Response:
        """
        获取{{table_comment}}记录详情
        """
        {% if soft_delete_field %}
        obj = self.db.query({{class_name}}).filter(
            {{class_name}}.{{primary_key_param}} == {{primary_key_param}},
            {{class_name}}.{{soft_delete_field}} == False
        ).first()
        {% else %}
        obj = self.db.query({{class_name}}).filter(
            {{class_name}}.{{primary_key_param}} == {{primary_key_param}}
        ).first()
        {% endif %}

        if not obj:
            raise NotFoundException("{{table_comment}}不存在")

        return {{class_name}}Response.model_validate(obj)

    def update(
        self,
        {{primary_key_param}}: {{primary_key_type}},
        data: {{class_name}}Update
    ) -> {{class_name}}Response:
        """
        更新{{table_comment}}记录
        """
        {% if soft_delete_field %}
        obj = self.db.query({{class_name}}).filter(
            {{class_name}}.{{primary_key_param}} == {{primary_key_param}},
            {{class_name}}.{{soft_delete_field}} == False
        ).first()
        {% else %}
        obj = self.db.query({{class_name}}).filter(
            {{class_name}}.{{primary_key_param}} == {{primary_key_param}}
        ).first()
        {% endif %}

        if not obj:
            raise NotFoundException("{{table_comment}}不存在")

        {% for fk in foreign_keys %}
        {% if fk.check_existence %}
        if data.{{fk.field_name}} is not None:
            pass
        {% endif %}
        {% endfor %}

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return {{class_name}}Response.model_validate(obj)

    def delete(self, {{primary_key_param}}: {{primary_key_type}}) -> None:
        """
        删除{{table_comment}}记录
        """
        {% if soft_delete_field %}
        obj = self.db.query({{class_name}}).filter(
            {{class_name}}.{{primary_key_param}} == {{primary_key_param}},
            {{class_name}}.{{soft_delete_field}} == False
        ).first()

        if not obj:
            raise NotFoundException("{{table_comment}}不存在")

        setattr(obj, {{soft_delete_field}}, True)
        self.db.commit()
        {% else %}
        obj = self.db.query({{class_name}}).filter(
            {{class_name}}.{{primary_key_param}} == {{primary_key_param}}
        ).first()

        if not obj:
            raise NotFoundException("{{table_comment}}不存在")

        self.db.delete(obj)
        self.db.commit()
        {% endif %}
