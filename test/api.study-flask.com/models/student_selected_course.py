# coding: utf-8
from . import db, BaseModel


class StudentSelectedCourse(db.Model):
    __tablename__ = 'student_selected_course'

    autoID = db.Column(db.Integer, primary_key=True, info='自增序号字段')
    studentID = db.Column(db.String(20, 'utf8mb4_general_ci'), nullable=False, info='学号')
    courseID = db.Column(db.String(15, 'utf8mb4_general_ci'), nullable=False, info='课程编号')
    score = db.Column(db.Integer, info='成绩')
    isDelete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
