# coding: utf-8
# 【AUTO-GENERATED】
# 本文件由 sql-to-flask-restfulapi-scaffold 生成，内容可被增量更新覆盖
from models import db


# Read-only view mapping template
t_v_student_course_score = db.Table(
    "v_student_course_score",
    db.Column('studentID', db.String(20)),
    db.Column('courseName', db.String(50))
)
