#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math

from app import db
from models.v_student_course_score import t_v_student_course_score
from utils import commons
from utils.loggings import loggings
from utils.response_code import RET, error_map_EN


class VStudentCourseScoreService(object):

    @classmethod
    def joint_query(cls, **kwargs):
    
        page = int(kwargs.get('Page', 1))
        size = int(kwargs.get('Size', 10))

        filter_list = []
    
        if kwargs.get('studentID') is not None:
            filter_list.append(t_v_student_course_score.columns['studentID'] == kwargs.get('studentID'))
        if kwargs.get('classID') is not None:
            filter_list.append(t_v_student_course_score.columns['classID'] == kwargs.get('classID'))
        if kwargs.get('collegeID') is not None:
            filter_list.append(t_v_student_course_score.columns['collegeID'] == kwargs.get('collegeID'))
        if kwargs.get('studentName') is not None:
            filter_list.append(t_v_student_course_score.columns['studentName'] == kwargs.get('studentName'))
        if kwargs.get('phoneNumber') is not None:
            filter_list.append(t_v_student_course_score.columns['phoneNumber'] == kwargs.get('phoneNumber'))
        if kwargs.get('className') is not None:
            filter_list.append(t_v_student_course_score.columns['className'] == kwargs.get('className'))

        try:
            vstudentcoursescore_info = db.session.query(t_v_student_course_score).filter(*filter_list)
            
            count = vstudentcoursescore_info.count()
            pages = math.ceil(count / size)
            vstudentcoursescore_info = vstudentcoursescore_info.limit(size).offset((page - 1) * size).all()
            results = commons.query_to_dict(vstudentcoursescore_info)

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
    
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
            
        finally:
            db.session.close()
