#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import jsonify

from service.VStudentCourseScoreService import VStudentCourseScoreService


class VStudentCourseScoreOtherResource(Resource):

    @classmethod
    def query(cls):
        res = VStudentCourseScoreService.query()
        return jsonify(**res)
