#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

sysdepartmentinfo_blueprint = Blueprint('sysDepartmentInfo', __name__)

from . import urls
