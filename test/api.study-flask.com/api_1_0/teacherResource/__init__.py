#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

teacher_blueprint = Blueprint('teacher', __name__)

from . import urls
