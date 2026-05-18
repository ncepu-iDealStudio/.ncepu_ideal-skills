#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import {{ blueprint_name }}
from .{{ resource_file_name }} import {{ class_name }}Resource
from .{{ other_resource_file_name }} import {{ class_name }}OtherResource

api = Api({{ blueprint_name }})

# Main CRUD routes (table entity)
api.add_resource({{ class_name }}Resource, "{{ url_item }}", "{{ url_collection }}", endpoint="{{ endpoint_name }}")

# Compatibility route for placeholder other resource
@{{ blueprint_name }}.route("{{ other_route }}", methods=["PUT"], endpoint="{{ endpoint_name }}Update")
def update({{ route_param_name }}):
    return {{ class_name }}OtherResource.sensitive_update({{ route_param_name }})
