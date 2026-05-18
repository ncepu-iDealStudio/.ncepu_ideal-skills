#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Flask app factory template."""

from flask import Flask
from flask_session import Session

from .setting import Settings
from models import db


def create_app(run_mode):
    app = Flask(__name__)
    app.config.from_object(Settings.get_setting(run_mode))
    db.init_app(app)
    Session(app)

    from api_1_0 import init_router

    init_router(app)
    return app
