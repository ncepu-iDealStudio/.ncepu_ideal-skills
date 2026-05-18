#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import sysclassinfo_blueprint
from api_1_0.sysClassInfoResource.sysClassInfoResource import SysClassInfoResource
from api_1_0.sysClassInfoResource.sysClassInfoOtherResource import SysClassInfoOtherResource

api = Api(sysclassinfo_blueprint)

api.add_resource(SysClassInfoResource, '/sysClassInfo/<classID>', '/sysClassInfo', endpoint='SysClassInfo')

