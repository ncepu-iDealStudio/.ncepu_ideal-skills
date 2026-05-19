#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.sys_classInfo import SysClassInfo
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class SysClassInfoController(SysClassInfo,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        classID = GenerateID.create_random_id()
        
        try:
            model = SysClassInfo(
                classID=classID,
                collegeID=kwargs.get('collegeID'),
                className=kwargs.get('className'),
                addTime=kwargs.get('addTime'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'classID': model.classID,
                
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
            filter_list = [cls.isDeleted == 0]
            if kwargs.get('classID'):
                filter_list.append(cls.classID == kwargs['classID'])
            else:
                if kwargs.get('collegeID'):
                    filter_list.append(cls.collegeID == kwargs.get('collegeID'))
                if kwargs.get('className'):
                    filter_list.append(cls.className == kwargs.get('className'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            sys_classInfo_info = db.session.query(cls).filter(*filter_list)
            
            count = sys_classInfo_info.count()
            pages = math.ceil(count / size)
            sys_classInfo_info = sys_classInfo_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(sys_classInfo_info)
            results = cls.to_dict(sys_classInfo_info)
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
            filter_list = [cls.isDeleted == 0]
            if kwargs.get('classID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('classID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.classID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('collegeID'):
                    filter_list.append(cls.collegeID == kwargs.get('collegeID'))
                if kwargs.get('className'):
                    filter_list.append(cls.className == kwargs.get('className'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'classID': []
            }
            for query_model in res.all():
                results['classID'].append(query_model.classID)

            res.update({'isDeleted': 1})
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
            
            
            filter_list = [cls.isDeleted == 0]
            filter_list.append(cls.classID == kwargs.get('classID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'classID': res.first().classID,
                
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
        param_list = kwargs.get('SysClassInfoList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            classID = GenerateID.create_random_id()
            
            model = SysClassInfo(
                classID=classID,
                collegeID=param_dict.get('collegeID'),
                className=param_dict.get('className'),
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
                added_record['classID'] = model.classID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
