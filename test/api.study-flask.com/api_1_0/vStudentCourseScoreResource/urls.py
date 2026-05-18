#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api
import json
from . import vstudentcoursescore_blueprint
from api_1_0.vStudentCourseScoreResource.vStudentCourseScoreOtherResource import VStudentCourseScoreOtherResource

api = Api(vstudentcoursescore_blueprint)


# joint query
@vstudentcoursescore_blueprint.route('/v-student-course-score/query', methods=['GET'], endpoint='VStudentCourseScoreQuery')
def VStudentCourseScore_query():
    return VStudentCourseScoreOtherResource.joint_query()

