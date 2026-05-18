#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.course import Course
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class CourseController(Course,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        courseID = GenerateID.create_random_id()
        
        try:
            model = Course(
                courseID=courseID,
                courseName=kwargs.get('courseName'),
                teacherID=kwargs.get('teacherID'),
                credit=kwargs.get('credit'),
                addTime=kwargs.get('addTime'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'courseID': model.courseID,
                
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
            if kwargs.get('courseID'):
                filter_list.append(cls.courseID == kwargs['courseID'])
            else:
                if kwargs.get('courseName'):
                    filter_list.append(cls.courseName == kwargs.get('courseName'))
                if kwargs.get('teacherID'):
                    filter_list.append(cls.teacherID == kwargs.get('teacherID'))
                if kwargs.get('credit') is not None:
                    filter_list.append(cls.credit == kwargs.get('credit'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            course_info = db.session.query(cls).filter(*filter_list)
            
            count = course_info.count()
            pages = math.ceil(count / size)
            course_info = course_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(course_info)
            results = cls.to_dict(course_info)
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
            if kwargs.get('courseID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('courseID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.courseID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('courseName'):
                    filter_list.append(cls.courseName == kwargs.get('courseName'))
                if kwargs.get('teacherID'):
                    filter_list.append(cls.teacherID == kwargs.get('teacherID'))
                if kwargs.get('credit') is not None:
                    filter_list.append(cls.credit == kwargs.get('credit'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'courseID': []
            }
            for query_model in res.all():
                results['courseID'].append(query_model.courseID)

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
            filter_list.append(cls.courseID == kwargs.get('courseID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'courseID': res.first().courseID,
                
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
        param_list = kwargs.get('CourseList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            courseID = GenerateID.create_random_id()
            
            model = Course(
                courseID=courseID,
                courseName=param_dict.get('courseName'),
                teacherID=param_dict.get('teacherID'),
                credit=param_dict.get('credit'),
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
                added_record['courseID'] = model.courseID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
