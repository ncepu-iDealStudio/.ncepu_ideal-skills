# coding: utf-8
from . import db, BaseModel


class SysClassInfo(db.Model):
    __tablename__ = 'sys_classInfo'

    autoID = db.Column(db.Integer, primary_key=True)
    classID = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), info='班级ID')
    collegeID = db.Column(db.String(20, 'utf8_general_ci'), info='所属学院')
    className = db.Column(db.String(20), info='班级名称')
    isDeleted = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否被删除  0 - 未删除  1 - 已删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
