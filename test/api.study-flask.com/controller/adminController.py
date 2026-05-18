#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.admin import Admin
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class AdminController(Admin,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        admin_id = GenerateID.create_random_id()
        
        try:
            model = Admin(
                admin_id=admin_id,
                user_id=kwargs.get('user_id'),
                department_id=kwargs.get('department_id'),
                name=kwargs.get('name'),
                email=kwargs.get('email'),
                phone=kwargs.get('phone'),
                office_address=kwargs.get('office_address'),
                add_time=kwargs.get('add_time'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'admin_id': model.admin_id,
                
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
            filter_list = [cls.is_delete == 0]
            if kwargs.get('admin_id'):
                filter_list.append(cls.admin_id == kwargs['admin_id'])
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('department_id') is not None:
                    filter_list.append(cls.department_id == kwargs.get('department_id'))
                if kwargs.get('name'):
                    filter_list.append(cls.name == kwargs.get('name'))
                if kwargs.get('email'):
                    filter_list.append(cls.email == kwargs.get('email'))
                if kwargs.get('phone'):
                    filter_list.append(cls.phone == kwargs.get('phone'))
                if kwargs.get('office_address'):
                    filter_list.append(cls.office_address == kwargs.get('office_address'))
                if kwargs.get('add_time'):
                    filter_list.append(cls.add_time == kwargs.get('add_time'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            admin_info = db.session.query(cls).filter(*filter_list)
            
            count = admin_info.count()
            pages = math.ceil(count / size)
            admin_info = admin_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(admin_info)
            results = cls.to_dict(admin_info)
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
            filter_list = [cls.is_delete == 0]
            if kwargs.get('admin_id'):
                primary_key_list = []
                for primary_key in str(kwargs.get('admin_id')).replace(' ', '').split(','):
                    primary_key_list.append(cls.admin_id == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('user_id'):
                    filter_list.append(cls.user_id == kwargs.get('user_id'))
                if kwargs.get('department_id') is not None:
                    filter_list.append(cls.department_id == kwargs.get('department_id'))
                if kwargs.get('name'):
                    filter_list.append(cls.name == kwargs.get('name'))
                if kwargs.get('email'):
                    filter_list.append(cls.email == kwargs.get('email'))
                if kwargs.get('phone'):
                    filter_list.append(cls.phone == kwargs.get('phone'))
                if kwargs.get('office_address'):
                    filter_list.append(cls.office_address == kwargs.get('office_address'))
                if kwargs.get('add_time'):
                    filter_list.append(cls.add_time == kwargs.get('add_time'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'admin_id': []
            }
            for query_model in res.all():
                results['admin_id'].append(query_model.admin_id)

            res.update({'is_delete': 1})
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
            
            
            filter_list = [cls.is_delete == 0]
            filter_list.append(cls.admin_id == kwargs.get('admin_id'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'admin_id': res.first().admin_id,
                
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
        param_list = kwargs.get('AdminList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            admin_id = GenerateID.create_random_id()
            
            model = Admin(
                admin_id=admin_id,
                user_id=param_dict.get('user_id'),
                department_id=param_dict.get('department_id'),
                name=param_dict.get('name'),
                email=param_dict.get('email'),
                phone=param_dict.get('phone'),
                office_address=param_dict.get('office_address'),
                add_time=param_dict.get('add_time'),
                
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
                added_record['admin_id'] = model.admin_id
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
