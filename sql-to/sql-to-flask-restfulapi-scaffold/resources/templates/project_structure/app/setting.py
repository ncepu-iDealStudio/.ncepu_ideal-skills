#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Application settings template."""

import os
from configparser import ConfigParser
from urllib import parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")


class Settings(object):
    CONFIG = ConfigParser()

    @classmethod
    def get_setting(cls, run_mode):
        cls.CONFIG.read(os.path.join(CONFIG_DIR, run_mode + "_config.conf"), encoding="utf-8")
        cls.SECRET_KEY = cls.CONFIG["BASIC"].get("secret_key", "")

        dialect = cls.CONFIG["DATABASE"].get("dialect", "mysql")
        driver = cls.CONFIG["DATABASE"].get("driver", "pymysql")
        username = cls.CONFIG["DATABASE"].get("username", "root")
        password = cls.CONFIG["DATABASE"].get("password", "")
        host = cls.CONFIG["DATABASE"].get("host", "127.0.0.1")
        port = cls.CONFIG["DATABASE"].get("port", "3306")
        database = cls.CONFIG["DATABASE"].get("database", "test")

        cls.SQLALCHEMY_DATABASE_URI = (
            f"{dialect}+{driver}://{username}:{parse.quote_plus(password)}@{host}:{port}/{database}?charset=utf8"
        )
        cls.SQLALCHEMY_TRACK_MODIFICATIONS = cls.CONFIG["DATABASE"].getboolean(
            "sqlalchemy_track_modifications", fallback=False
        )
        return cls
