#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.student import Student
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class StudentController(Student,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        studentID = GenerateID.create_custom_id()
        
        try:
            model = Student(
                studentID=studentID,
                userID=kwargs.get('userID'),
                classID=kwargs.get('classID'),
                collegeID=kwargs.get('collegeID'),
                name=kwargs.get('name'),
                phoneNumber=kwargs.get('phoneNumber'),
                age=kwargs.get('age'),
                agenda=kwargs.get('agenda'),
                addTime=kwargs.get('addTime'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'studentID': model.studentID,
                
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
            if kwargs.get('studentID'):
                filter_list.append(cls.studentID == kwargs['studentID'])
            else:
                if kwargs.get('userID'):
                    filter_list.append(cls.userID == kwargs.get('userID'))
                if kwargs.get('classID'):
                    filter_list.append(cls.classID == kwargs.get('classID'))
                if kwargs.get('collegeID'):
                    filter_list.append(cls.collegeID == kwargs.get('collegeID'))
                if kwargs.get('name'):
                    filter_list.append(cls.name == kwargs.get('name'))
                if kwargs.get('phoneNumber'):
                    filter_list.append(cls.phoneNumber == kwargs.get('phoneNumber'))
                if kwargs.get('age') is not None:
                    filter_list.append(cls.age == kwargs.get('age'))
                if kwargs.get('agenda'):
                    filter_list.append(cls.agenda == kwargs.get('agenda'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            student_info = db.session.query(cls).filter(*filter_list)
            
            count = student_info.count()
            pages = math.ceil(count / size)
            student_info = student_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(student_info)
            results = cls.to_dict(student_info)
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
            if kwargs.get('studentID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('studentID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.studentID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('userID'):
                    filter_list.append(cls.userID == kwargs.get('userID'))
                if kwargs.get('classID'):
                    filter_list.append(cls.classID == kwargs.get('classID'))
                if kwargs.get('collegeID'):
                    filter_list.append(cls.collegeID == kwargs.get('collegeID'))
                if kwargs.get('name'):
                    filter_list.append(cls.name == kwargs.get('name'))
                if kwargs.get('phoneNumber'):
                    filter_list.append(cls.phoneNumber == kwargs.get('phoneNumber'))
                if kwargs.get('age') is not None:
                    filter_list.append(cls.age == kwargs.get('age'))
                if kwargs.get('agenda'):
                    filter_list.append(cls.agenda == kwargs.get('agenda'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'studentID': []
            }
            for query_model in res.all():
                results['studentID'].append(query_model.studentID)

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
            filter_list.append(cls.studentID == kwargs.get('studentID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'studentID': res.first().studentID,
                
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
        param_list = kwargs.get('StudentList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            studentID = GenerateID.create_custom_id()
            
            model = Student(
                studentID=studentID,
                userID=param_dict.get('userID'),
                classID=param_dict.get('classID'),
                collegeID=param_dict.get('collegeID'),
                name=param_dict.get('name'),
                phoneNumber=param_dict.get('phoneNumber'),
                age=param_dict.get('age'),
                agenda=param_dict.get('agenda'),
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
                added_record['studentID'] = model.studentID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
