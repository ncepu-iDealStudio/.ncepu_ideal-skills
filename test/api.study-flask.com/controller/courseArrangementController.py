#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.course_arrangement import CourseArrangement
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class CourseArrangementController(CourseArrangement,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        
        try:
            model = CourseArrangement(
                courseID=kwargs.get('courseID'),
                termID=kwargs.get('termID'),
                classTime=kwargs.get('classTime'),
                count=kwargs.get('count'),
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
                if kwargs.get('courseID'):
                    filter_list.append(cls.courseID == kwargs.get('courseID'))
                if kwargs.get('termID'):
                    filter_list.append(cls.termID == kwargs.get('termID'))
                if kwargs.get('classTime'):
                    filter_list.append(cls.classTime == kwargs.get('classTime'))
                if kwargs.get('count') is not None:
                    filter_list.append(cls.count == kwargs.get('count'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            course_arrangement_info = db.session.query(cls).filter(*filter_list)
            
            count = course_arrangement_info.count()
            pages = math.ceil(count / size)
            course_arrangement_info = course_arrangement_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(course_arrangement_info)
            results = cls.to_dict(course_arrangement_info)
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
                if kwargs.get('courseID'):
                    filter_list.append(cls.courseID == kwargs.get('courseID'))
                if kwargs.get('termID'):
                    filter_list.append(cls.termID == kwargs.get('termID'))
                if kwargs.get('classTime'):
                    filter_list.append(cls.classTime == kwargs.get('classTime'))
                if kwargs.get('count') is not None:
                    filter_list.append(cls.count == kwargs.get('count'))
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
        param_list = kwargs.get('CourseArrangementList')
        model_list = []
        for param_dict in param_list:
            
            model = CourseArrangement(
                courseID=param_dict.get('courseID'),
                termID=param_dict.get('termID'),
                classTime=param_dict.get('classTime'),
                count=param_dict.get('count'),
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
