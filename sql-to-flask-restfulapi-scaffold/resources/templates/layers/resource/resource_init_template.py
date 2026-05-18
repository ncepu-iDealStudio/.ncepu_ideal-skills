#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint


{{ blueprint_name }} = Blueprint("{{ endpoint_base }}", __name__)

from . import urls
