#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

syscollegeinfo_blueprint = Blueprint('sysCollegeInfo', __name__)

from . import urls
