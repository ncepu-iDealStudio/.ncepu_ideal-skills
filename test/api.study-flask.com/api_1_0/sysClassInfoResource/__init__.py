#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

sysclassinfo_blueprint = Blueprint('sysClassInfo', __name__)

from . import urls
