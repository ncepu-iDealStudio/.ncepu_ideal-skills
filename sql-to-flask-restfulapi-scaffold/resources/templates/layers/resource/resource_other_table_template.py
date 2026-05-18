#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import jsonify


class {{ class_name }}OtherResource(Resource):

    @classmethod
    def sensitive_update(cls, {{ route_param_name }}):
        # Placeholder endpoint kept for compatibility with target structure.
        return jsonify(code=0, message="OK", data={"{{ route_param_name }}": {{ route_param_name }}})
