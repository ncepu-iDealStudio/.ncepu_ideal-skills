#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import jsonify, request

from service.StudentService import StudentService
from utils import commons
from utils.response_code import RET, error_map_EN


class StudentResource(Resource):

    @classmethod
    def get(cls, student_id=None):
        kwargs = request.args.to_dict(flat=True)
        if student_id is not None:
            kwargs["studentID"] = student_id

        kwargs = commons.put_remove_none(**kwargs)
        res = StudentService.get(**kwargs)
        return jsonify(**res)

    @classmethod
    def post(cls):
        payload = request.get_json(silent=True)
        if not payload:
            payload = request.form.to_dict(flat=True)
        payload = commons.put_remove_none(**(payload or {}))

        res = StudentService.add(**payload)
        return jsonify(**res)

    @classmethod
    def put(cls, student_id):
        if student_id is None:
            return jsonify(code=RET.PARAMERR, message=error_map_EN.get(RET.PARAMERR, "Parameter error"), data={"error": "primary key is required"})

        payload = request.get_json(silent=True)
        if not payload:
            payload = request.form.to_dict(flat=True)
        payload = commons.put_remove_none(**(payload or {}))
        payload["studentID"] = student_id

        res = StudentService.update(**payload)
        return jsonify(**res)

    @classmethod
    def delete(cls, student_id=None):
        kwargs = {}
        if student_id is not None:
            kwargs["studentID"] = student_id
        else:
            kwargs.update(request.args.to_dict(flat=True))

        kwargs = commons.put_remove_none(**kwargs)
        res = StudentService.delete(**kwargs)
        return jsonify(**res)
