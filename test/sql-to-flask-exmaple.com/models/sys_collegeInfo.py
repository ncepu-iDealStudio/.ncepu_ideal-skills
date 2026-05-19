# coding: utf-8
from . import db, BaseModel


class SysCollegeInfo(db.Model):
    __tablename__ = 'sys_collegeInfo'

    autoID = db.Column(db.BigInteger, primary_key=True)
    collegeID = db.Column(db.String(20, 'utf8_general_ci'), info='学院ID编码--业务主键')
    collegeName = db.Column(db.String(50, 'utf8_general_ci'), info='学院名称')
    isDelete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
