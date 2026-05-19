#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.adminController import AdminController
from utils import commons
from utils.response_code import RET


class AdminOtherResource(Resource):

    @classmethod
    def sensitive_update(cls, admin_id):
        if not admin_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('phone', location='form', required=False, help='phone参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['admin_id'] = admin_id

        res = AdminController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
