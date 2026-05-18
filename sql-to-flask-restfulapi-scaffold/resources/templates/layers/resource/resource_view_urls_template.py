#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import {{ blueprint_name }}
from .{{ other_resource_file_name }} import {{ class_name }}OtherResource

api = Api({{ blueprint_name }})

# View entity exposes collection query route only.
api.add_resource({{ class_name }}OtherResource, "{{ url_collection }}", endpoint="{{ endpoint_name }}Query")
