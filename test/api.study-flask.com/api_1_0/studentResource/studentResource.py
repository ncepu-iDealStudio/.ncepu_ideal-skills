#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.studentController import StudentController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class StudentResource(Resource):

    # get
    @classmethod
    def get(cls, studentID=None):
        if studentID:
            kwargs = {
                'studentID': studentID
            }

            res = StudentController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('studentID', location='args', required=False, help='studentID参数类型不正确或缺失')
        parser.add_argument('userID', location='args', required=False, help='userID参数类型不正确或缺失')
        parser.add_argument('classID', location='args', required=False, help='classID参数类型不正确或缺失')
        parser.add_argument('collegeID', location='args', required=False, help='collegeID参数类型不正确或缺失')
        parser.add_argument('name', location='args', required=False, help='name参数类型不正确或缺失')
        parser.add_argument('phoneNumber', location='args', required=False, help='phoneNumber参数类型不正确或缺失')
        parser.add_argument('age', location='args', required=False, help='age参数类型不正确或缺失')
        parser.add_argument('agenda', location='args', required=False, help='agenda参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('addTime', location='args', required=False, help='addTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = StudentController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, studentID=None):
        if studentID:
            kwargs = {
                'studentID': studentID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = StudentController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, studentID):
        if not studentID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('userID', location='form', required=False, help='userID参数类型不正确或缺失')
        parser.add_argument('classID', location='form', required=False, help='classID参数类型不正确或缺失')
        parser.add_argument('collegeID', location='form', required=False, help='collegeID参数类型不正确或缺失')
        parser.add_argument('name', location='form', required=False, help='name参数类型不正确或缺失')
        parser.add_argument('age', location='form', required=False, help='age参数类型不正确或缺失')
        parser.add_argument('agenda', location='form', required=False, help='agenda参数类型不正确或缺失')
        parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['studentID'] = studentID

        res = StudentController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        StudentList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('StudentList', type=str, location='form', required=False, help='StudentList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('StudentList'):
            kwargs['StudentList'] = json.loads(kwargs['StudentList'])
            for data in kwargs['StudentList']:
                for key in ['phoneNumber']:
                    data.pop(key, None)
            res = StudentController.add_list(**kwargs)

        else:
            parser.add_argument('userID', location='form', required=False, help='userID参数类型不正确或缺失')
            parser.add_argument('classID', location='form', required=False, help='classID参数类型不正确或缺失')
            parser.add_argument('collegeID', location='form', required=False, help='collegeID参数类型不正确或缺失')
            parser.add_argument('name', location='form', required=False, help='name参数类型不正确或缺失')
            parser.add_argument('age', location='form', required=False, help='age参数类型不正确或缺失')
            parser.add_argument('agenda', location='form', required=False, help='agenda参数类型不正确或缺失')
            parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = StudentController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
