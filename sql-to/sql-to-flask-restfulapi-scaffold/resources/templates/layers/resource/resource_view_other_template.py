#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 【HAND-WRITTEN 占位】
# 本文件为手写文件，增量更新时绝不覆盖，仅输出人工待办
from flask_restful import Resource
from flask import jsonify

from service.{{ class_name }}Service import {{ class_name }}Service


class {{ class_name }}OtherResource(Resource):

    @classmethod
    def query(cls):
        res = {{ class_name }}Service.query()
        return jsonify(**res)
