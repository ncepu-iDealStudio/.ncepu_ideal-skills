# coding: utf-8
from models import db


# Read-only view mapping template
t_v_student_course_score = db.Table(
    "v_student_course_score",
    db.Column('studentID', db.String(20)),
    db.Column('courseName', db.String(50))
)
