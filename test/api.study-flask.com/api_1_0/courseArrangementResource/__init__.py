#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

coursearrangement_blueprint = Blueprint('courseArrangement', __name__)

from . import urls
