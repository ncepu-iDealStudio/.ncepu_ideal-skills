#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import sysdepartmentinfo_blueprint
from api_1_0.sysDepartmentInfoResource.sysDepartmentInfoResource import SysDepartmentInfoResource
from api_1_0.sysDepartmentInfoResource.sysDepartmentInfoOtherResource import SysDepartmentInfoOtherResource

api = Api(sysdepartmentinfo_blueprint)

api.add_resource(SysDepartmentInfoResource, '/sysDepartmentInfo/<departmentID>', '/sysDepartmentInfo', endpoint='SysDepartmentInfo')

