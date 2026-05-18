#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import ssouser_blueprint
from api_1_0.ssoUserResource.ssoUserResource import SsoUserResource
from api_1_0.ssoUserResource.ssoUserOtherResource import SsoUserOtherResource

api = Api(ssouser_blueprint)

api.add_resource(SsoUserResource, '/ssoUser/<userID>', '/ssoUser', endpoint='SsoUser')


@ssouser_blueprint.route('/ssouser/update/<userID>', methods=['PUT'], endpoint='SsoUserUpdate')
def update(userID):
    return SsoUserOtherResource.sensitive_update(userID)
