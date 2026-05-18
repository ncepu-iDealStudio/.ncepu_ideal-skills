#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint


v_student_course_score_blueprint = Blueprint("v_student_course_score", __name__)

from . import urls
