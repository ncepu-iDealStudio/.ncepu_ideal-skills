#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import student_blueprint
from .studentResource import StudentResource
from .studentOtherResource import StudentOtherResource

api = Api(student_blueprint)

# Main CRUD routes (table entity)
api.add_resource(StudentResource, "/student/<auto_id>", "/student", endpoint="Student")

# Compatibility route for placeholder other resource
@student_blueprint.route("/student/update/<auto_id>", methods=["PUT"], endpoint="StudentUpdate")
def update(auto_id):
    return StudentOtherResource.sensitive_update(auto_id)
