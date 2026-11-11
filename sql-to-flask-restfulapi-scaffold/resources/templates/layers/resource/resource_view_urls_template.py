#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 【AUTO-GENERATED】
# 本文件由 sql-to-flask-restfulapi-scaffold 生成，内容可被增量更新覆盖
from flask_restful import Api

from . import {{ blueprint_name }}
from .{{ other_resource_file_name }} import {{ class_name }}OtherResource

api = Api({{ blueprint_name }})

# View entity exposes collection query route only.
api.add_resource({{ class_name }}OtherResource, "{{ url_collection }}", endpoint="{{ endpoint_name }}Query")
