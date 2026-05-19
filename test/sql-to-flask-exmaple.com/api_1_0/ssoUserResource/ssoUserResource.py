#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.ssoUserController import SsoUserController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class SsoUserResource(Resource):

    # get
    @classmethod
    def get(cls, userID=None):
        if userID:
            kwargs = {
                'userID': userID
            }

            res = SsoUserController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('userID', location='args', required=False, help='userID参数类型不正确或缺失')
        parser.add_argument('account', location='args', required=False, help='account参数类型不正确或缺失')
        parser.add_argument('password', location='args', required=False, help='password参数类型不正确或缺失')
        parser.add_argument('userType', location='args', required=False, help='userType参数类型不正确或缺失')
        parser.add_argument('status', location='args', required=False, help='status参数类型不正确或缺失')
        parser.add_argument('addTime', location='args', required=False, help='addTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = SsoUserController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, userID=None):
        if userID:
            kwargs = {
                'userID': userID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = SsoUserController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, userID):
        if not userID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('account', location='form', required=False, help='account参数类型不正确或缺失')
        parser.add_argument('userType', location='form', required=False, help='userType参数类型不正确或缺失')
        parser.add_argument('status', location='form', required=False, help='status参数类型不正确或缺失')
        parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['userID'] = userID

        res = SsoUserController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        SsoUserList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('SsoUserList', type=str, location='form', required=False, help='SsoUserList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('SsoUserList'):
            kwargs['SsoUserList'] = json.loads(kwargs['SsoUserList'])
            for data in kwargs['SsoUserList']:
                for key in ['password']:
                    data.pop(key, None)
            res = SsoUserController.add_list(**kwargs)

        else:
            parser.add_argument('account', location='form', required=False, help='account参数类型不正确或缺失')
            parser.add_argument('userType', location='form', required=False, help='userType参数类型不正确或缺失')
            parser.add_argument('status', location='form', required=False, help='status参数类型不正确或缺失')
            parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = SsoUserController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
