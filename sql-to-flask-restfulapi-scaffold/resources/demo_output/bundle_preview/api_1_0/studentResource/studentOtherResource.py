#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 【HAND-WRITTEN 占位】
# 本文件为手写文件，增量更新时绝不覆盖，仅输出人工待办
from flask_restful import Resource
from flask import jsonify


class StudentOtherResource(Resource):

    @classmethod
    def sensitive_update(cls, auto_id):
        # Placeholder endpoint kept for compatibility with target structure.
        return jsonify(code=0, message="OK", data={"auto_id": auto_id})
