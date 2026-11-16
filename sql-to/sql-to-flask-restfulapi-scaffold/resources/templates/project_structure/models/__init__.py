#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
