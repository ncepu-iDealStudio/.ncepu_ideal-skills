#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import course_blueprint
from api_1_0.courseResource.courseResource import CourseResource
from api_1_0.courseResource.courseOtherResource import CourseOtherResource

api = Api(course_blueprint)

api.add_resource(CourseResource, '/course/<courseID>', '/course', endpoint='Course')

