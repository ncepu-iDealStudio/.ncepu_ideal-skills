#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import math
import json

from sqlalchemy import or_

from app import db
from models.sso_user import SsoUser
from utils import commons
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings
from models import BaseModel


class SsoUserController(SsoUser,BaseModel):

    # add
    @classmethod
    def add(cls, **kwargs):
        from utils.generate_id import GenerateID
        userID = GenerateID.create_random_id()
        
        try:
            model = SsoUser(
                userID=userID,
                account=kwargs.get('account'),
                password=kwargs.get('password'),
                userType=kwargs.get('userType'),
                status=kwargs.get('status'),
                addTime=kwargs.get('addTime'),
                
            )
            db.session.add(model)
            db.session.commit()
            results = {
                'add_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'userID': model.userID,
                
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
            filter_list = []
            if kwargs.get('userID'):
                filter_list.append(cls.userID == kwargs['userID'])
            else:
                if kwargs.get('account'):
                    filter_list.append(cls.account == kwargs.get('account'))
                if kwargs.get('password'):
                    filter_list.append(cls.password == kwargs.get('password'))
                if kwargs.get('userType') is not None:
                    filter_list.append(cls.userType == kwargs.get('userType'))
                if kwargs.get('status') is not None:
                    filter_list.append(cls.status == kwargs.get('status'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                

            page = int(kwargs.get('Page', 1))
            size = int(kwargs.get('Size', 10))
            
            sso_user_info = db.session.query(cls).filter(*filter_list)
            
            count = sso_user_info.count()
            pages = math.ceil(count / size)
            sso_user_info = sso_user_info.limit(size).offset((page - 1) * size).all()
   
            #results = commons.query_to_dict(sso_user_info)
            results = cls.to_dict(sso_user_info)
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
            filter_list = []
            if kwargs.get('userID'):
                primary_key_list = []
                for primary_key in str(kwargs.get('userID')).replace(' ', '').split(','):
                    primary_key_list.append(cls.userID == primary_key)
                filter_list.append(or_(*primary_key_list))
                
            else:
                if kwargs.get('account'):
                    filter_list.append(cls.account == kwargs.get('account'))
                if kwargs.get('password'):
                    filter_list.append(cls.password == kwargs.get('password'))
                if kwargs.get('userType') is not None:
                    filter_list.append(cls.userType == kwargs.get('userType'))
                if kwargs.get('status') is not None:
                    filter_list.append(cls.status == kwargs.get('status'))
                if kwargs.get('addTime'):
                    filter_list.append(cls.addTime == kwargs.get('addTime'))
                
            res = db.session.query(cls).filter(*filter_list).with_for_update()

            results = {
                'delete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'userID': []
            }
            for query_model in res.all():
                results['userID'].append(query_model.userID)

            res.delete()
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
            
            
            filter_list = []
            filter_list.append(cls.userID == kwargs.get('userID'))
            
            res = db.session.query(cls).filter(*filter_list).with_for_update()
            if res.first():
                results = {
                    'update_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'userID': res.first().userID,
                
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
        param_list = kwargs.get('SsoUserList')
        model_list = []
        for param_dict in param_list:
            from utils.generate_id import GenerateID
            userID = GenerateID.create_random_id()
            
            model = SsoUser(
                userID=userID,
                account=param_dict.get('account'),
                password=param_dict.get('password'),
                userType=param_dict.get('userType'),
                status=param_dict.get('status'),
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
                added_record['userID'] = model.userID
                
                results['added_records'].append(added_record)
                
            return {'code': RET.OK, 'message': error_map_EN[RET.OK], 'data': results}
            
        except Exception as e:
            db.session.rollback()
            loggings.exception(1, e)
            return {'code': RET.DBERR, 'message': error_map_EN[RET.DBERR], 'data': {'error': str(e)}}
        finally:
            db.session.close()
