#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

studentselectedcourse_blueprint = Blueprint('studentSelectedCourse', __name__)

from . import urls
