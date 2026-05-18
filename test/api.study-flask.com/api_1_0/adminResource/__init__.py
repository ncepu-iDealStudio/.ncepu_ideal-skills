#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__)

from . import urls
