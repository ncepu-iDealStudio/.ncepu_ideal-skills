#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math

from sqlalchemy.inspection import inspect

from models.student import Student
from models import db
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class StudentController(Student):

    @staticmethod
    def _to_dict(model):
        return {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}

    @staticmethod
    def _normalize_pagination(page, size):
        page_val = int(page) if str(page).isdigit() else 1
        size_val = int(size) if str(size).isdigit() else 10
        page_val = max(page_val, 1)
        size_val = max(min(size_val, 100), 1)
        return page_val, size_val

    @classmethod
    def add(cls, **kwargs):
        try:
            model = cls(**kwargs)
            db.session.add(model)
            db.session.commit()
            return {
                "code": RET.OK,
                "message": error_map_EN.get(RET.OK, "OK"),
                "data": cls._to_dict(model)
            }
        except Exception as exc:
            db.session.rollback()
            loggings.exception(exc)
            return {
                "code": RET.DBERR,
                "message": error_map_EN.get(RET.DBERR, "Database error"),
                "data": {"error": str(exc)}
            }
        finally:
            db.session.close()

    @classmethod
    def get(cls, **kwargs):
        try:
            page_raw = kwargs.pop("Page", 1)
            size_raw = kwargs.pop("Size", 10)
            page, size = cls._normalize_pagination(page_raw, size_raw)

            query = db.session.query(cls)

            # Default soft-delete filter (enabled only when configured field exists).
            if hasattr(cls, "isDelete"):
                query = query.filter(getattr(cls, "isDelete") == 0)

            if "autoID" in kwargs and kwargs.get("autoID") is not None:
                query = query.filter(getattr(cls, "autoID") == kwargs.get("autoID"))
            else:
                for key, value in kwargs.items():
                    if value is None:
                        continue
                    if hasattr(cls, key):
                        query = query.filter(getattr(cls, key) == value)

            total_count = query.count()
            total_page = math.ceil(total_count / size) if total_count > 0 else 0
            rows = query.limit(size).offset((page - 1) * size).all()

            return {
                "code": RET.OK,
                "message": error_map_EN.get(RET.OK, "OK"),
                "data": [cls._to_dict(row) for row in rows],
                "totalCount": total_count,
                "totalPage": total_page,
            }
        except Exception as exc:
            loggings.exception(exc)
            return {
                "code": RET.DBERR,
                "message": error_map_EN.get(RET.DBERR, "Database error"),
                "data": {"error": str(exc)},
                "totalCount": 0,
                "totalPage": 0,
            }
        finally:
            db.session.close()

    @classmethod
    def update(cls, **kwargs):
        try:
            pk_value = kwargs.get("autoID")
            if pk_value is None:
                return {
                    "code": RET.PARAMERR,
                    "message": error_map_EN.get(RET.PARAMERR, "Parameter error"),
                    "data": {"error": "primary key is required"}
                }

            query = db.session.query(cls).filter(getattr(cls, "autoID") == pk_value)
            if hasattr(cls, "isDelete"):
                query = query.filter(getattr(cls, "isDelete") == 0)

            model = query.first()
            if not model:
                return {
                    "code": RET.NODATA,
                    "message": error_map_EN.get(RET.NODATA, "No data"),
                    "data": {"error": "record not found"}
                }

            for key, value in kwargs.items():
                if key == "autoID" or value is None:
                    continue
                if hasattr(model, key):
                    setattr(model, key, value)

            db.session.commit()
            return {
                "code": RET.OK,
                "message": error_map_EN.get(RET.OK, "OK"),
                "data": cls._to_dict(model)
            }
        except Exception as exc:
            db.session.rollback()
            loggings.exception(exc)
            return {
                "code": RET.DBERR,
                "message": error_map_EN.get(RET.DBERR, "Database error"),
                "data": {"error": str(exc)}
            }
        finally:
            db.session.close()

    @classmethod
    def delete(cls, **kwargs):
        try:
            pk_value = kwargs.get("autoID")
            if pk_value is None:
                return {
                    "code": RET.PARAMERR,
                    "message": error_map_EN.get(RET.PARAMERR, "Parameter error"),
                    "data": {"error": "primary key is required"}
                }

            query = db.session.query(cls).filter(getattr(cls, "autoID") == pk_value)
            model = query.first()
            if not model:
                return {
                    "code": RET.NODATA,
                    "message": error_map_EN.get(RET.NODATA, "No data"),
                    "data": {"error": "record not found"}
                }

            if hasattr(model, "isDelete"):
                setattr(model, "isDelete", 1)
            else:
                db.session.delete(model)

            db.session.commit()
            return {
                "code": RET.OK,
                "message": error_map_EN.get(RET.OK, "OK"),
                "data": {"autoID": pk_value}
            }
        except Exception as exc:
            db.session.rollback()
            loggings.exception(exc)
            return {
                "code": RET.DBERR,
                "message": error_map_EN.get(RET.DBERR, "Database error"),
                "data": {"error": str(exc)}
            }
        finally:
            db.session.close()
