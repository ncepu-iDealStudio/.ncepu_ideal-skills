#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.courseController import CourseController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class CourseResource(Resource):

    # get
    @classmethod
    def get(cls, courseID=None):
        if courseID:
            kwargs = {
                'courseID': courseID
            }

            res = CourseController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('courseID', location='args', required=False, help='courseID参数类型不正确或缺失')
        parser.add_argument('courseName', location='args', required=False, help='courseName参数类型不正确或缺失')
        parser.add_argument('teacherID', location='args', required=False, help='teacherID参数类型不正确或缺失')
        parser.add_argument('credit', location='args', required=False, help='credit参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('addTime', location='args', required=False, help='addTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = CourseController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, courseID=None):
        if courseID:
            kwargs = {
                'courseID': courseID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = CourseController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, courseID):
        if not courseID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('courseName', location='form', required=False, help='courseName参数类型不正确或缺失')
        parser.add_argument('teacherID', location='form', required=False, help='teacherID参数类型不正确或缺失')
        parser.add_argument('credit', location='form', required=False, help='credit参数类型不正确或缺失')
        parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['courseID'] = courseID

        res = CourseController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        CourseList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('CourseList', type=str, location='form', required=False, help='CourseList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('CourseList'):
            kwargs['CourseList'] = json.loads(kwargs['CourseList'])
            for data in kwargs['CourseList']:
                for key in []:
                    data.pop(key, None)
            res = CourseController.add_list(**kwargs)

        else:
            parser.add_argument('courseName', location='form', required=False, help='courseName参数类型不正确或缺失')
            parser.add_argument('teacherID', location='form', required=False, help='teacherID参数类型不正确或缺失')
            parser.add_argument('credit', location='form', required=False, help='credit参数类型不正确或缺失')
            parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = CourseController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
