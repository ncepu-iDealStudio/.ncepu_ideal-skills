#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 【HAND-WRITTEN 占位】
# 本文件为手写文件，增量更新时绝不覆盖，仅输出人工待办
from flask_restful import Resource
from flask import jsonify

from service.VStudentCourseScoreService import VStudentCourseScoreService


class VStudentCourseScoreOtherResource(Resource):

    @classmethod
    def query(cls):
        res = VStudentCourseScoreService.query()
        return jsonify(**res)
