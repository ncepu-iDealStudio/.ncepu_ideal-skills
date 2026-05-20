#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import coursearrangement_blueprint
from api_1_0.courseArrangementResource.courseArrangementResource import CourseArrangementResource
from api_1_0.courseArrangementResource.courseArrangementOtherResource import CourseArrangementOtherResource

api = Api(coursearrangement_blueprint)

api.add_resource(CourseArrangementResource, '/course-arrangement/<autoID>', '/course-arrangement', endpoint='CourseArrangement')

