# coding: utf-8
# 【AUTO-GENERATED】
# 本文件由 sql-to-flask-restfulapi-scaffold 生成，内容可被增量更新覆盖
from models import db


# Read-only view mapping template
{{ view_table_name_var }} = db.Table(
    "{{ table_name_raw }}",
    {{ view_columns_block }}
)
