#!/usr/bin/env python
# -*- coding:utf-8 -*- 

from flask_restful import Resource, reqparse
from flask import jsonify

from controller.courseArrangementController import CourseArrangementController
from utils import commons
from utils.response_code import RET, error_map_EN
import json


class CourseArrangementResource(Resource):

    # get
    @classmethod
    def get(cls, autoID=None):
        if autoID:
            kwargs = {
                'autoID': autoID
            }

            res = CourseArrangementController.get(**kwargs)
            if res['code'] == RET.OK:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])
            else:
                return jsonify(code=res['code'], message=res['message'], data=res['data'])

        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('courseID', location='args', required=False, help='courseID参数类型不正确或缺失')
        parser.add_argument('termID', location='args', required=False, help='termID参数类型不正确或缺失')
        parser.add_argument('classTime', location='args', required=False, help='classTime参数类型不正确或缺失')
        parser.add_argument('count', location='args', required=False, help='count参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('addTime', location='args', required=False, help='addTime参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        res = CourseArrangementController.get(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalPage=res['totalPage'], totalCount=res['totalCount'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data']) 

    
    # delete
    @classmethod
    def delete(cls, autoID=None):
        if autoID:
            kwargs = {
                'autoID': autoID
            }

        else:
            return jsonify(code=RET.PARAMERR, message=error_map_EN[RET.PARAMERR], data='id不能为空')

        res = CourseArrangementController.delete(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # put
    @classmethod
    def put(cls, autoID):
        if not autoID:
            return jsonify(code=RET.NODATA, message='primary key missed', error='primary key missed')

        parser = reqparse.RequestParser()
        parser.add_argument('courseID', location='form', required=False, help='courseID参数类型不正确或缺失')
        parser.add_argument('termID', location='form', required=False, help='termID参数类型不正确或缺失')
        parser.add_argument('classTime', location='form', required=False, help='classTime参数类型不正确或缺失')
        parser.add_argument('count', location='form', required=False, help='count参数类型不正确或缺失')
        parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
        
        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        kwargs['autoID'] = autoID

        res = CourseArrangementController.update(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])

    
    # add
    @classmethod
    def post(cls):
        '''
        CourseArrangementList: Pass in values in JSON format to batch add
        eg.[{k1:v1,k2:v2,...},...]
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('CourseArrangementList', type=str, location='form', required=False, help='CourseArrangementList参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)

        if kwargs.get('CourseArrangementList'):
            kwargs['CourseArrangementList'] = json.loads(kwargs['CourseArrangementList'])
            for data in kwargs['CourseArrangementList']:
                for key in []:
                    data.pop(key, None)
            res = CourseArrangementController.add_list(**kwargs)

        else:
            parser.add_argument('courseID', location='form', required=False, help='courseID参数类型不正确或缺失')
            parser.add_argument('termID', location='form', required=False, help='termID参数类型不正确或缺失')
            parser.add_argument('classTime', location='form', required=False, help='classTime参数类型不正确或缺失')
            parser.add_argument('count', location='form', required=False, help='count参数类型不正确或缺失')
            parser.add_argument('addTime', location='form', required=False, help='addTime参数类型不正确或缺失')
            
            kwargs = parser.parse_args()
            kwargs = commons.put_remove_none(**kwargs)

            res = CourseArrangementController.add(**kwargs)

        return jsonify(code=res['code'], message=res['message'], data=res['data'])
