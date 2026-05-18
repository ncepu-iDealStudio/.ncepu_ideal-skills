# coding: utf-8
from models import db, BaseModel


class {{ class_name }}(BaseModel):
    __tablename__ = "{{ table_name_raw }}"

    # Fields rendered from SQL columns
    {{ fields_block }}
