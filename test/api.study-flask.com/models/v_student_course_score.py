# coding: utf-8
from . import db, BaseModel


t_v_student_course_score = db.Table(
    'v_student_course_score',
    db.Column('autoID', db.Integer, server_default=db.FetchedValue()),
    db.Column('studentID', db.String(20)),
    db.Column('userID', db.String(22)),
    db.Column('classID', db.String(10)),
    db.Column('collegeID', db.String(20)),
    db.Column('studentName', db.String(20)),
    db.Column('phoneNumber', db.String(500)),
    db.Column('age', db.Integer),
    db.Column('agenda', db.String(10)),
    db.Column('isDelete', db.Integer, server_default=db.FetchedValue()),
    db.Column('className', db.String(20)),
    db.Column('courseID', db.String(15)),
    db.Column('score', db.Integer),
    db.Column('courseName', db.String(50)),
    db.Column('teacherID', db.String(15)),
    db.Column('teacherName', db.String(10)),
    db.Column('phone', db.String(15)),
    db.Column('email', db.String(50))
)
