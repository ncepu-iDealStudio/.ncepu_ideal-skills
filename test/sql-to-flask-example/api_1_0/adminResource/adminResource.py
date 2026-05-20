#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.adminController import AdminController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class AdminResource(Resource):

    # get
    @classmethod
    def get(cls, admin_id=None):
        if admin_id:
            kwargs = {
                'admin_id': admin_id
            }

            res = AdminController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('auto_id', location='args', required=False, help='auto_id参数类型不正确或缺失')
        parser.add_argument('admin_id', location='args', required=False, help='admin_id参数类型不正确或缺失')
        parser.add_argument('user_id', location='args', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('department_id', location='args', required=False, help='department_id参数类型不正确或缺失')
        parser.add_argument('name', location='args', required=False, help='name参数类型不正确或缺失')
        parser.add_argument('email', location='args', required=False, help='email参数类型不正确或缺失')
        parser.add_argument('phone', location='args', required=False, help='phone参数类型不正确或缺失')
        parser.add_argument('office_address', location='args', required=False, help='office_address参数类型不正确或缺失')
        parser.add_argument('is_delete', location='args', required=False, help='is_delete参数类型不正确或缺失')
        parser.add_argument('add_time', location='args', required=False, help='add_time参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = AdminController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, admin_id=None):
        if admin_id:
            kwargs = {
                'admin_id': admin_id
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = AdminController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, admin_id):
        if not admin_id:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
        parser.add_argument('department_id', location='form', required=False, help='department_id参数类型不正确或缺失')
        parser.add_argument('name', location='form', required=False, help='name参数类型不正确或缺失')
        parser.add_argument('email', location='form', required=False, help='email参数类型不正确或缺失')
        parser.add_argument('office_address', location='form', required=False, help='office_address参数类型不正确或缺失')
        parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['admin_id'] = admin_id

        res = AdminController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        AdminList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('AdminList', type=str, location='form', required=False, help='AdminList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('AdminList'):
            kwargs['AdminList'] = json.loads(kwargs['AdminList'])
            for data in kwargs['AdminList']:
                for key in ['phone']:
                    data.pop(key, None)
            res = AdminController.add_list(**kwargs)

        else:
            parser.add_argument('user_id', location='form', required=False, help='user_id参数类型不正确或缺失')
            parser.add_argument('department_id', location='form', required=False, help='department_id参数类型不正确或缺失')
            parser.add_argument('name', location='form', required=False, help='name参数类型不正确或缺失')
            parser.add_argument('email', location='form', required=False, help='email参数类型不正确或缺失')
            parser.add_argument('office_address', location='form', required=False, help='office_address参数类型不正确或缺失')
            parser.add_argument('add_time', location='form', required=False, help='add_time参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = AdminController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
