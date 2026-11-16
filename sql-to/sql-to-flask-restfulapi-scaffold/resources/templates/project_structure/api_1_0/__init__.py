#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Router registry template.

Entity routers will be appended during generation.
"""

# ==AUTO_IMPORTS_START==
# from .student_resource import student_blueprint
# ==AUTO_IMPORTS_END==

ROUTER_REGISTRY = [
    # ==AUTO_REGISTRY_START==
    # (student_blueprint, "/api_1_0"),
    # ==AUTO_REGISTRY_END==
]


def init_router(app):
    for blueprint, prefix in ROUTER_REGISTRY:
        app.register_blueprint(blueprint, url_prefix=prefix)

    return app
