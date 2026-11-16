#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 【AUTO-GENERATED】
# 本文件由 sql-to-flask-restfulapi-scaffold 生成，内容可被增量更新覆盖
from flask import Blueprint


student_blueprint = Blueprint("student", __name__)

from . import urls
