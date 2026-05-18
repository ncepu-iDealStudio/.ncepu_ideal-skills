#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

student_blueprint = Blueprint('student', __name__)

from . import urls
