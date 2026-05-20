#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

vstudentcoursescore_blueprint = Blueprint('vStudentCourseScore', __name__)

from . import urls
