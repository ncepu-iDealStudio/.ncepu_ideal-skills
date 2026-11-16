# coding: utf-8
# 【AUTO-GENERATED】
# 本文件由 sql-to-flask-restfulapi-scaffold 生成，内容可被增量更新覆盖
from models import db, BaseModel


class {{ class_name }}(BaseModel):
    __tablename__ = "{{ table_name_raw }}"

    # Fields rendered from SQL columns
    {{ fields_block }}
