# coding: utf-8
from . import db, BaseModel


class CourseArrangement(db.Model):
    __tablename__ = 'course_arrangement'

    autoID = db.Column(db.Integer, primary_key=True, info='自增序号')
    courseID = db.Column(db.String(20, 'utf8mb4_general_ci'), info='课程编号')
    termID = db.Column(db.String(50), info='学期ID')
    classTime = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), info='上课时间：1-2；3-4；5-6；7-8；')
    count = db.Column(db.Integer, info='课程容量-可选人数')
    isDelete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
