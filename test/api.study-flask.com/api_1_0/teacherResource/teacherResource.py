#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.teacherController import TeacherController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class TeacherResource(Resource):

    # get
    @classmethod
    def get(cls, teacherID=None):
        if teacherID:
            kwargs = {
                'teacherID': teacherID
            }

            res = TeacherController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('teacherID', location='args', required=False, help='teacherID参数类型不正确或缺失')
        parser.add_argument('userID', location='args', required=False, help='userID参数类型不正确或缺失')
        parser.add_argument('departmentID', location='args', required=False, help='departmentID参数类型不正确或缺失')
        parser.add_argument('name', location='args', required=False, help='name参数类型不正确或缺失')
        parser.add_argument('email', location='args', required=False, help='email参数类型不正确或缺失')
        parser.add_argument('phone', location='args', required=False, help='phone参数类型不正确或缺失')
        parser.add_argument('officeAddress', location='args', required=False, help='officeAddress参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('addTime', location='args', required=False, help='addTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = TeacherController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, teacherID=None):
        if teacherID:
            kwargs = {
                'teacherID': teacherID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = TeacherController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, teacherID):
        if not teacherID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('userID', location='form', required=False, help='userID参数类型不正确或缺失')
        parser.add_argument('departmentID', location='form', required=False, help='departmentID参数类型不正确或缺失')
        parser.add_argument('name', location='form', required=False, help='name参数类型不正确或缺失')
        parser.add_argument('email', location='form', required=False, help='email参数类型不正确或缺失')
        parser.add_argument('officeAddress', location='form', required=False, help='officeAddress参数类型不正确或缺失')
        parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['teacherID'] = teacherID

        res = TeacherController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        TeacherList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('TeacherList', type=str, location='form', required=False, help='TeacherList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('TeacherList'):
            kwargs['TeacherList'] = json.loads(kwargs['TeacherList'])
            for data in kwargs['TeacherList']:
                for key in ['phone']:
                    data.pop(key, None)
            res = TeacherController.add_list(**kwargs)

        else:
            parser.add_argument('userID', location='form', required=False, help='userID参数类型不正确或缺失')
            parser.add_argument('departmentID', location='form', required=False, help='departmentID参数类型不正确或缺失')
            parser.add_argument('name', location='form', required=False, help='name参数类型不正确或缺失')
            parser.add_argument('email', location='form', required=False, help='email参数类型不正确或缺失')
            parser.add_argument('officeAddress', location='form', required=False, help='officeAddress参数类型不正确或缺失')
            parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = TeacherController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
