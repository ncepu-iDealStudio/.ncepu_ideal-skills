#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math

from sqlalchemy.inspection import inspect

from models.{{ module_name }} import {{ class_name }}
from models import db
from utils.response_code import RET, error_map_EN
from utils.loggings import loggings


class {{ class_name }}Controller({{ class_name }}):

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
            if hasattr(cls, "{{ soft_delete_field }}"):
                query = query.filter(getattr(cls, "{{ soft_delete_field }}") == {{ soft_delete_inactive_value }})

            if "{{ primary_key_field }}" in kwargs and kwargs.get("{{ primary_key_field }}") is not None:
                query = query.filter(getattr(cls, "{{ primary_key_field }}") == kwargs.get("{{ primary_key_field }}"))
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
            pk_value = kwargs.get("{{ primary_key_field }}")
            if pk_value is None:
                return {
                    "code": RET.PARAMERR,
                    "message": error_map_EN.get(RET.PARAMERR, "Parameter error"),
                    "data": {"error": "primary key is required"}
                }

            query = db.session.query(cls).filter(getattr(cls, "{{ primary_key_field }}") == pk_value)
            if hasattr(cls, "{{ soft_delete_field }}"):
                query = query.filter(getattr(cls, "{{ soft_delete_field }}") == {{ soft_delete_inactive_value }})

            model = query.first()
            if not model:
                return {
                    "code": RET.NODATA,
                    "message": error_map_EN.get(RET.NODATA, "No data"),
                    "data": {"error": "record not found"}
                }

            for key, value in kwargs.items():
                if key == "{{ primary_key_field }}" or value is None:
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
            pk_value = kwargs.get("{{ primary_key_field }}")
            if pk_value is None:
                return {
                    "code": RET.PARAMERR,
                    "message": error_map_EN.get(RET.PARAMERR, "Parameter error"),
                    "data": {"error": "primary key is required"}
                }

            query = db.session.query(cls).filter(getattr(cls, "{{ primary_key_field }}") == pk_value)
            model = query.first()
            if not model:
                return {
                    "code": RET.NODATA,
                    "message": error_map_EN.get(RET.NODATA, "No data"),
                    "data": {"error": "record not found"}
                }

            if hasattr(model, "{{ soft_delete_field }}"):
                setattr(model, "{{ soft_delete_field }}", {{ soft_delete_active_value }})
            else:
                db.session.delete(model)

            db.session.commit()
            return {
                "code": RET.OK,
                "message": error_map_EN.get(RET.OK, "OK"),
                "data": {"{{ primary_key_field }}": pk_value}
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
