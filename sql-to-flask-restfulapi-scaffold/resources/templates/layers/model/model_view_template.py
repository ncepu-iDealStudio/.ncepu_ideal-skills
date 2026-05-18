# coding: utf-8
from models import db


# Read-only view mapping template
{{ view_table_name_var }} = db.Table(
    "{{ table_name_raw }}",
    {{ view_columns_block }}
)
