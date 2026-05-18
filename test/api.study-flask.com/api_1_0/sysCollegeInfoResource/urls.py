#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import syscollegeinfo_blueprint
from api_1_0.sysCollegeInfoResource.sysCollegeInfoResource import SysCollegeInfoResource
from api_1_0.sysCollegeInfoResource.sysCollegeInfoOtherResource import SysCollegeInfoOtherResource

api = Api(syscollegeinfo_blueprint)

api.add_resource(SysCollegeInfoResource, '/sysCollegeInfo/<collegeID>', '/sysCollegeInfo', endpoint='SysCollegeInfo')

