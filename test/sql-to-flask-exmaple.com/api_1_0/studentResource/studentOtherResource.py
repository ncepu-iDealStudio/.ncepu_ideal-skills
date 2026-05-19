#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.studentController import StudentController
from utils import commons
from utils.response_code import RET


class StudentOtherResource(Resource):

    @classmethod
    def sensitive_update(cls, studentID):
        if not studentID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('phoneNumber', location='form', required=False, help='phoneNumber参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['studentID'] = studentID

        res = StudentController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
