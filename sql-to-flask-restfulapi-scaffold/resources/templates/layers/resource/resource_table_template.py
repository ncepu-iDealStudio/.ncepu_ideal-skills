#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import jsonify, request

from service.{{ class_name }}Service import {{ class_name }}Service
from utils import commons
from utils.response_code import RET, error_map_EN


class {{ class_name }}Resource(Resource):

    @classmethod
    def get(cls, {{ route_param_name }}=None):
        kwargs = request.args.to_dict(flat=True)
        if {{ route_param_name }} is not None:
            kwargs["{{ primary_key_field }}"] = {{ route_param_name }}

        kwargs = commons.put_remove_none(**kwargs)
        res = {{ class_name }}Service.get(**kwargs)
        return jsonify(**res)

    @classmethod
    def post(cls):
        payload = request.get_json(silent=True)
        if not payload:
            payload = request.form.to_dict(flat=True)
        payload = commons.put_remove_none(**(payload or {}))

        res = {{ class_name }}Service.add(**payload)
        return jsonify(**res)

    @classmethod
    def put(cls, {{ route_param_name }}):
        if {{ route_param_name }} is None:
            return jsonify(code=RET.PARAMERR, message=error_map_EN.get(RET.PARAMERR, "Parameter error"), data={"error": "primary key is required"})

        payload = request.get_json(silent=True)
        if not payload:
            payload = request.form.to_dict(flat=True)
        payload = commons.put_remove_none(**(payload or {}))
        payload["{{ primary_key_field }}"] = {{ route_param_name }}

        res = {{ class_name }}Service.update(**payload)
        return jsonify(**res)

    @classmethod
    def delete(cls, {{ route_param_name }}=None):
        kwargs = {}
        if {{ route_param_name }} is not None:
            kwargs["{{ primary_key_field }}"] = {{ route_param_name }}
        else:
            kwargs.update(request.args.to_dict(flat=True))

        kwargs = commons.put_remove_none(**kwargs)
        res = {{ class_name }}Service.delete(**kwargs)
        return jsonify(**res)
