#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.teacher import Teacher
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class TeacherController(Teacher,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        teacherID = GenerateID.create_custom_id()
        
        try:
            model = Teacher(
                teacherID=teacherID,
                userID=kwargs.get('userID'),
                departmentID=kwargs.get('departmentID'),
                name=kwargs.get('name'),
                email=kwargs.get('email'),
                phone=kwargs.get('phone'),
                officeAddress=kwargs.get('officeAddress'),
                addTime=kwargs.get('addTime'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'teacherID': model.teacherID,
                
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
            if kwargs.get('teacherID'):
                filter_list.append(cls.teacherID == kwargs['teacherID'])
            else:
                if kwargs.get('userID'):
                    filter_list.append(cls.userID == kwargs.get('userID'))
                if kwargs.get('departmentID') is not None:
                    filter_list.append(cls.departmentID == kwargs.get('departmentID'))
                if kwargs.get('name'):
                    filter_list.append(cls.name == kwargs.get('name'))
                if kwargs.get('email'):
                    filter_list.append(cls.email == kwargs.get('email'))
                if kwargs.get('phone'):
                    filter_list.append(cls.phone == kwargs.get('phone'))
                if kwargs.get('officeAddress'):
                    filter_list.append(cls.officeAddress == kwargs.get('officeAddress'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            teacher_info = db.session.query(cls).filter(*filter_list)
            
            count = teacher_info.count()
            pages = math.ceil(count / size)
            teacher_info = teacher_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(teacher_info)
            results = cls.to_dict(teacher_info)
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
            if kwargs.get('teacherID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('teacherID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.teacherID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('userID'):
                    filter_list.append(cls.userID == kwargs.get('userID'))
                if kwargs.get('departmentID') is not None:
                    filter_list.append(cls.departmentID == kwargs.get('departmentID'))
                if kwargs.get('name'):
                    filter_list.append(cls.name == kwargs.get('name'))
                if kwargs.get('email'):
                    filter_list.append(cls.email == kwargs.get('email'))
                if kwargs.get('phone'):
                    filter_list.append(cls.phone == kwargs.get('phone'))
                if kwargs.get('officeAddress'):
                    filter_list.append(cls.officeAddress == kwargs.get('officeAddress'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'teacherID': []
            }
            for query_model in res.all():
                results['teacherID'].append(query_model.teacherID)

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
            filter_list.append(cls.teacherID == kwargs.get('teacherID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'teacherID': res.first().teacherID,
                
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
        param_list = kwargs.get('TeacherList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            teacherID = GenerateID.create_custom_id()
            
            model = Teacher(
                teacherID=teacherID,
                userID=param_dict.get('userID'),
                departmentID=param_dict.get('departmentID'),
                name=param_dict.get('name'),
                email=param_dict.get('email'),
                phone=param_dict.get('phone'),
                officeAddress=param_dict.get('officeAddress'),
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
                added_record['teacherID'] = model.teacherID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
