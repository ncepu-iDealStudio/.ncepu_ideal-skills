#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.student_selected_course import StudentSelectedCourse
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class StudentSelectedCourseController(StudentSelectedCourse,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        
        try:
            model = StudentSelectedCourse(
                studentID=kwargs.get('studentID'),
                courseID=kwargs.get('courseID'),
                score=kwargs.get('score'),
                addTime=kwargs.get('addTime'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'autoID': model.autoID,
                
            }
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # get
    @classmethod
    def get(cls, **kwargs):
        try:
            filter_list = [cls.isDelete == 0]
            if kwargs.get('autoID'):
                filter_list.append(cls.autoID == kwargs['autoID'])
            else:
                if kwargs.get('autoID') is not None:
                    filter_list.append(cls.autoID == kwargs.get('autoID'))
                if kwargs.get('studentID'):
                    filter_list.append(cls.studentID == kwargs.get('studentID'))
                if kwargs.get('courseID'):
                    filter_list.append(cls.courseID == kwargs.get('courseID'))
                if kwargs.get('score') is not None:
                    filter_list.append(cls.score == kwargs.get('score'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            student_selected_course_info = db.session.query(cls).filter(*filter_list)
            
            count = student_selected_course_info.count()
            pages = math.ceil(count / size)
            student_selected_course_info = student_selected_course_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(student_selected_course_info)
            results = cls.to_dict(student_selected_course_info)
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'totalCount': count, 'totalPage': pages, 'data': results}
            
        except Exception as e:
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # delete
    @classmethod
    def delete(cls, **kwargs):
        try:
            filter_list = [cls.isDelete == 0]
            if kwargs.get('autoID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('autoID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.autoID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('autoID') is not None:
                    filter_list.append(cls.autoID == kwargs.get('autoID'))
                if kwargs.get('studentID'):
                    filter_list.append(cls.studentID == kwargs.get('studentID'))
                if kwargs.get('courseID'):
                    filter_list.append(cls.courseID == kwargs.get('courseID'))
                if kwargs.get('score') is not None:
                    filter_list.append(cls.score == kwargs.get('score'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'autoID': []
            }
            for query_model in res.all():
                results['autoID'].append(query_model.autoID)

            res.update({'isDelete': 1})
            db.session.commit()

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
    
    # update
    @classmethod
    def update(cls, **kwargs):
        try:
            
            
            filter_list = [cls.isDelete == 0]
            filter_list.append(cls.autoID == kwargs.get('autoID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'autoID': res.first().autoID,
                
                }
                
                res.update(kwargs)
                db.session.commit()
            else:
                results = {
                    'error': 'data dose not exist'
                }

            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}

        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()

    # batch add
    @classmethod
    def add_list(cls, **kwargs):
        param_list = kwargs.get('StudentSelectedCourseList')
        model_list = []
        for param_dict in param_list:
            
            model = StudentSelectedCourse(
                studentID=param_dict.get('studentID'),
                courseID=param_dict.get('courseID'),
                score=param_dict.get('score'),
                addTime=param_dict.get('addTime'),
                
            )
            model_list.append(model)
        
        try:
            db.session.add_all(model_list)
            db.session.commit()
            results = {
                'added_records': [],
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            for model in model_list:
                added_record = {}
                added_record['autoID'] = model.autoID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
