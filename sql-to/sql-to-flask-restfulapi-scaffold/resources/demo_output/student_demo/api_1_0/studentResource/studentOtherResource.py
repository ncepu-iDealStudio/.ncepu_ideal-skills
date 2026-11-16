#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import jsonify


class StudentOtherResource(Resource):

    @classmethod
    def sensitive_update(cls, auto_id):
        # Placeholder endpoint kept for compatibility with target structure.
        return jsonify(code=0, message="OK", data={"auto_id": auto_id})
