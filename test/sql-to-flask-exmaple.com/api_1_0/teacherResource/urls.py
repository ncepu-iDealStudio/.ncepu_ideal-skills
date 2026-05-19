#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import teacher_blueprint
from api_1_0.teacherResource.teacherResource import TeacherResource
from api_1_0.teacherResource.teacherOtherResource import TeacherOtherResource

api = Api(teacher_blueprint)

api.add_resource(TeacherResource, '/teacher/<teacherID>', '/teacher', endpoint='Teacher')


@teacher_blueprint.route('/teacher/update/<teacherID>', methods=['PUT'], endpoint='TeacherUpdate')
def update(teacherID):
    return TeacherOtherResource.sensitive_update(teacherID)
