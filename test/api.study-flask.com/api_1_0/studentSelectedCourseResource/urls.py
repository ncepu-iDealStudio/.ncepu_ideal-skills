#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import studentselectedcourse_blueprint
from api_1_0.studentSelectedCourseResource.studentSelectedCourseResource import StudentSelectedCourseResource
from api_1_0.studentSelectedCourseResource.studentSelectedCourseOtherResource import StudentSelectedCourseOtherResource

api = Api(studentselectedcourse_blueprint)

api.add_resource(StudentSelectedCourseResource, '/student-selected-course/<autoID>', '/student-selected-course', endpoint='StudentSelectedCourse')

