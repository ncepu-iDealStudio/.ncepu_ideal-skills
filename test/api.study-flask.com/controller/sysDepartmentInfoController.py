#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.sys_departmentInfo import SysDepartmentInfo
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class SysDepartmentInfoController(SysDepartmentInfo,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        departmentID = GenerateID.create_random_id()
        
        try:
            model = SysDepartmentInfo(
                departmentID=departmentID,
                parentDepartmentID=kwargs.get('parentDepartmentID'),
                collegeID=kwargs.get('collegeID'),
                departmentName=kwargs.get('departmentName'),
                departmentType=kwargs.get('departmentType'),
                addTime=kwargs.get('addTime'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'departmentID': model.departmentID,
                
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
            if kwargs.get('departmentID'):
                filter_list.append(cls.departmentID == kwargs['departmentID'])
            else:
                if kwargs.get('parentDepartmentID') is not None:
                    filter_list.append(cls.parentDepartmentID == kwargs.get('parentDepartmentID'))
                if kwargs.get('collegeID'):
                    filter_list.append(cls.collegeID == kwargs.get('collegeID'))
                if kwargs.get('departmentName'):
                    filter_list.append(cls.departmentName == kwargs.get('departmentName'))
                if kwargs.get('departmentType') is not None:
                    filter_list.append(cls.departmentType == kwargs.get('departmentType'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            sys_departmentInfo_info = db.session.query(cls).filter(*filter_list)
            
            count = sys_departmentInfo_info.count()
            pages = math.ceil(count / size)
            sys_departmentInfo_info = sys_departmentInfo_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(sys_departmentInfo_info)
            results = cls.to_dict(sys_departmentInfo_info)
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
            if kwargs.get('departmentID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('departmentID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.departmentID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('parentDepartmentID') is not None:
                    filter_list.append(cls.parentDepartmentID == kwargs.get('parentDepartmentID'))
                if kwargs.get('collegeID'):
                    filter_list.append(cls.collegeID == kwargs.get('collegeID'))
                if kwargs.get('departmentName'):
                    filter_list.append(cls.departmentName == kwargs.get('departmentName'))
                if kwargs.get('departmentType') is not None:
                    filter_list.append(cls.departmentType == kwargs.get('departmentType'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'departmentID': []
            }
            for query_model in res.all():
                results['departmentID'].append(query_model.departmentID)

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
            filter_list.append(cls.departmentID == kwargs.get('departmentID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'departmentID': res.first().departmentID,
                
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
        param_list = kwargs.get('SysDepartmentInfoList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            departmentID = GenerateID.create_random_id()
            
            model = SysDepartmentInfo(
                departmentID=departmentID,
                parentDepartmentID=param_dict.get('parentDepartmentID'),
                collegeID=param_dict.get('collegeID'),
                departmentName=param_dict.get('departmentName'),
                departmentType=param_dict.get('departmentType'),
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
                added_record['departmentID'] = model.departmentID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
