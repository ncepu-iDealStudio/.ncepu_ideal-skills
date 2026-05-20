#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.sysDepartmentInfoController import SysDepartmentInfoController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class SysDepartmentInfoResource(Resource):

    # get
    @classmethod
    def get(cls, departmentID=None):
        if departmentID:
            kwargs = {
                'departmentID': departmentID
            }

            res = SysDepartmentInfoController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('departmentID', location='args', required=False, help='departmentID参数类型不正确或缺失')
        parser.add_argument('parentDepartmentID', location='args', required=False, help='parentDepartmentID参数类型不正确或缺失')
        parser.add_argument('collegeID', location='args', required=False, help='collegeID参数类型不正确或缺失')
        parser.add_argument('departmentName', location='args', required=False, help='departmentName参数类型不正确或缺失')
        parser.add_argument('departmentType', location='args', required=False, help='departmentType参数类型不正确或缺失')
        parser.add_argument('isDeleted', location='args', required=False, help='isDeleted参数类型不正确或缺失')
        parser.add_argument('addTime', location='args', required=False, help='addTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = SysDepartmentInfoController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, departmentID=None):
        if departmentID:
            kwargs = {
                'departmentID': departmentID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = SysDepartmentInfoController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, departmentID):
        if not departmentID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('parentDepartmentID', location='form', required=False, help='parentDepartmentID参数类型不正确或缺失')
        parser.add_argument('collegeID', location='form', required=False, help='collegeID参数类型不正确或缺失')
        parser.add_argument('departmentName', location='form', required=False, help='departmentName参数类型不正确或缺失')
        parser.add_argument('departmentType', location='form', required=False, help='departmentType参数类型不正确或缺失')
        parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['departmentID'] = departmentID

        res = SysDepartmentInfoController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        SysDepartmentInfoList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('SysDepartmentInfoList', type=str, location='form', required=False, help='SysDepartmentInfoList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('SysDepartmentInfoList'):
            kwargs['SysDepartmentInfoList'] = json.loads(kwargs['SysDepartmentInfoList'])
            for data in kwargs['SysDepartmentInfoList']:
                for key in []:
                    data.pop(key, None)
            res = SysDepartmentInfoController.add_list(**kwargs)

        else:
            parser.add_argument('parentDepartmentID', location='form', required=False, help='parentDepartmentID参数类型不正确或缺失')
            parser.add_argument('collegeID', location='form', required=False, help='collegeID参数类型不正确或缺失')
            parser.add_argument('departmentName', location='form', required=False, help='departmentName参数类型不正确或缺失')
            parser.add_argument('departmentType', location='form', required=False, help='departmentType参数类型不正确或缺失')
            parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = SysDepartmentInfoController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
