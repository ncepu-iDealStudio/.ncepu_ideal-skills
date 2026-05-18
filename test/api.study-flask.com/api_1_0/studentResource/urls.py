#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import student_blueprint
from api_1_0.studentResource.studentResource import StudentResource
from api_1_0.studentResource.studentOtherResource import StudentOtherResource

api = Api(student_blueprint)

api.add_resource(StudentResource, '/student/<studentID>', '/student', endpoint='Student')


@student_blueprint.route('/student/update/<studentID>', methods=['PUT'], endpoint='StudentUpdate')
def update(studentID):
    return StudentOtherResource.sensitive_update(studentID)
