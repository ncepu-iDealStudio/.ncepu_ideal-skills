#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.ssoUserController import SsoUserController
from utils import commons
from utils.response_code import RET


class SsoUserOtherResource(Resource):

    @classmethod
    def sensitive_update(cls, userID):
        if not userID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('password', location='form', required=False, help='password参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['userID'] = userID

        res = SsoUserController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
