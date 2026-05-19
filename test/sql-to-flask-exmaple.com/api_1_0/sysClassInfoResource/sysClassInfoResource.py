#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.sysClassInfoController import SysClassInfoController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class SysClassInfoResource(Resource):

    # get
    @classmethod
    def get(cls, classID=None):
        if classID:
            kwargs = {
                'classID': classID
            }

            res = SysClassInfoController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('classID', location='args', required=False, help='classID参数类型不正确或缺失')
        parser.add_argument('collegeID', location='args', required=False, help='collegeID参数类型不正确或缺失')
        parser.add_argument('className', location='args', required=False, help='className参数类型不正确或缺失')
        parser.add_argument('isDeleted', location='args', required=False, help='isDeleted参数类型不正确或缺失')
        parser.add_argument('addTime', location='args', required=False, help='addTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = SysClassInfoController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, classID=None):
        if classID:
            kwargs = {
                'classID': classID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = SysClassInfoController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, classID):
        if not classID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('collegeID', location='form', required=False, help='collegeID参数类型不正确或缺失')
        parser.add_argument('className', location='form', required=False, help='className参数类型不正确或缺失')
        parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['classID'] = classID

        res = SysClassInfoController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        SysClassInfoList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('SysClassInfoList', type=str, location='form', required=False, help='SysClassInfoList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('SysClassInfoList'):
            kwargs['SysClassInfoList'] = json.loads(kwargs['SysClassInfoList'])
            for data in kwargs['SysClassInfoList']:
                for key in []:
                    data.pop(key, None)
            res = SysClassInfoController.add_list(**kwargs)

        else:
            parser.add_argument('collegeID', location='form', required=False, help='collegeID参数类型不正确或缺失')
            parser.add_argument('className', location='form', required=False, help='className参数类型不正确或缺失')
            parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = SysClassInfoController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
