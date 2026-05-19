#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

ssouser_blueprint = Blueprint('ssoUser', __name__)

from . import urls
