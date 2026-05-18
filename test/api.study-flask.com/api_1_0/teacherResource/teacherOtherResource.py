#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.teacherController import TeacherController
from utils import commons
from utils.response_code import RET


class TeacherOtherResource(Resource):

    @classmethod
    def sensitive_update(cls, teacherID):
        if not teacherID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('phone', location='form', required=False, help='phone参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['teacherID'] = teacherID

        res = TeacherController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
