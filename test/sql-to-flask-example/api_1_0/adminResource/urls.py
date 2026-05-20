#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import admin_blueprint
from api_1_0.adminResource.adminResource import AdminResource
from api_1_0.adminResource.adminOtherResource import AdminOtherResource

api = Api(admin_blueprint)

api.add_resource(AdminResource, '/admin/<admin_id>', '/admin', endpoint='Admin')


@admin_blueprint.route('/admin/update/<admin_id>', methods=['PUT'], endpoint='AdminUpdate')
def update(admin_id):
    return AdminOtherResource.sensitive_update(admin_id)
