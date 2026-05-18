# coding: utf-8
from . import db, BaseModel


class Student(db.Model):
    __tablename__ = 'student'

    autoID = db.Column(db.Integer, primary_key=True, info='自增字段')
    studentID = db.Column(db.String(20, 'utf8mb4_general_ci'), info='学号，业务主键')
    userID = db.Column(db.String(22, 'utf8mb4_0900_ai_ci'), info='对应的用户表ID')
    classID = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), info='所属班级ID')
    collegeID = db.Column(db.String(20, 'utf8_general_ci'), info='所属学院')
    name = db.Column(db.String(20, 'utf8mb4_general_ci'), info='学生姓名')
    phoneNumber = db.Column(db.String(500, 'utf8mb4_general_ci'), info='手机号码')
    age = db.Column(db.Integer, info='年龄')
    agenda = db.Column(db.String(10, 'utf8mb4_general_ci'), info='性别')
    isDelete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
