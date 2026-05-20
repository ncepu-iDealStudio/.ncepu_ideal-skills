#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from flask import jsonify

from service.vStudentCourseScoreService import VStudentCourseScoreService
from utils import commons
from utils.response_code import RET


class VStudentCourseScoreOtherResource(Resource):

    @classmethod
    def joint_query(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('autoID', location='args', required=False, help='autoID参数类型不正确或缺失')
        parser.add_argument('studentID', location='args', required=False, help='studentID参数类型不正确或缺失')
        parser.add_argument('userID', location='args', required=False, help='userID参数类型不正确或缺失')
        parser.add_argument('classID', location='args', required=False, help='classID参数类型不正确或缺失')
        parser.add_argument('collegeID', location='args', required=False, help='collegeID参数类型不正确或缺失')
        parser.add_argument('studentName', location='args', required=False, help='studentName参数类型不正确或缺失')
        parser.add_argument('phoneNumber', location='args', required=False, help='phoneNumber参数类型不正确或缺失')
        parser.add_argument('age', location='args', required=False, help='age参数类型不正确或缺失')
        parser.add_argument('agenda', location='args', required=False, help='agenda参数类型不正确或缺失')
        parser.add_argument('isDelete', location='args', required=False, help='isDelete参数类型不正确或缺失')
        parser.add_argument('className', location='args', required=False, help='className参数类型不正确或缺失')
        parser.add_argument('courseID', location='args', required=False, help='courseID参数类型不正确或缺失')
        parser.add_argument('score', location='args', required=False, help='score参数类型不正确或缺失')
        parser.add_argument('courseName', location='args', required=False, help='courseName参数类型不正确或缺失')
        parser.add_argument('teacherID', location='args', required=False, help='teacherID参数类型不正确或缺失')
        parser.add_argument('teacherName', location='args', required=False, help='teacherName参数类型不正确或缺失')
        parser.add_argument('phone', location='args', required=False, help='phone参数类型不正确或缺失')
        parser.add_argument('email', location='args', required=False, help='email参数类型不正确或缺失')
        
        parser.add_argument('Page', location='args', required=False, help='Page参数类型不正确或缺失')
        parser.add_argument('Size', location='args', required=False, help='Size参数类型不正确或缺失')

        kwargs = parser.parse_args()
        kwargs = commons.put_remove_none(**kwargs)
        
        res = VStudentCourseScoreService.joint_query(**kwargs)
        if res['code'] == RET.OK:
            return jsonify(code=res['code'], message=res['message'], data=res['data'], totalCount=res['totalCount'], totalPage=res['totalPage'])
        else:
            return jsonify(code=res['code'], message=res['message'], data=res['data'])
