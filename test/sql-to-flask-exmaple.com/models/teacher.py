# coding: utf-8
from . import db, BaseModel


class Teacher(db.Model):
    __tablename__ = 'teacher'

    autoID = db.Column(db.Integer, primary_key=True)
    teacherID = db.Column(db.String(15, 'utf8mb4_general_ci'), info='教工号')
    userID = db.Column(db.String(22, 'utf8mb4_general_ci'), info='对应的用户表ID')
    departmentID = db.Column(db.BigInteger, index=True, info='所属的教研室(研究所)ID')
    name = db.Column(db.String(10, 'utf8mb4_general_ci'), info='姓名')
    email = db.Column(db.String(50, 'utf8mb4_general_ci'), info='邮箱')
    phone = db.Column(db.String(15, 'utf8mb4_general_ci'), info='电话')
    officeAddress = db.Column(db.String(255, 'utf8mb4_general_ci'), info='办公地址')
    isDelete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
