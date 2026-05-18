# coding: utf-8
from . import db, BaseModel


class Course(db.Model):
    __tablename__ = 'course'

    autoID = db.Column(db.Integer, primary_key=True)
    courseID = db.Column(db.String(20, 'utf8mb4_general_ci'), info='课程编号')
    courseName = db.Column(db.String(50, 'utf8mb4_general_ci'), info='课程名称')
    teacherID = db.Column(db.String(15, 'utf8mb4_general_ci'), info='任课教师编号')
    credit = db.Column(db.Float, info='学分')
    isDelete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
