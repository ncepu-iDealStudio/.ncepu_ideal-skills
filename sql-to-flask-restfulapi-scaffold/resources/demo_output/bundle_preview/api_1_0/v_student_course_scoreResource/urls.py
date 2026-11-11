#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 【AUTO-GENERATED】
# 本文件由 sql-to-flask-restfulapi-scaffold 生成，内容可被增量更新覆盖
from flask_restful import Api

from . import v_student_course_score_blueprint
from .v_student_course_scoreOtherResource import VStudentCourseScoreOtherResource

api = Api(v_student_course_score_blueprint)

# View entity exposes collection query route only.
api.add_resource(VStudentCourseScoreOtherResource, "/v_student_course_score/query", endpoint="VStudentCourseScoreQuery")
