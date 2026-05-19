# coding: utf-8
from . import db, BaseModel


class SysDepartmentInfo(db.Model):
    __tablename__ = 'sys_departmentInfo'

    autoID = db.Column(db.BigInteger, primary_key=True)
    departmentID = db.Column(db.BigInteger, info='学院下属的教研室(研究所)ID')
    parentDepartmentID = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue(), info='父级部门ID')
    collegeID = db.Column(db.String(20, 'utf8_general_ci'), info='学院ID编码--业务主键')
    departmentName = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), info='教研室(研究所)名称')
    departmentType = db.Column(db.Integer, server_default=db.FetchedValue(), info='部门类型:\r\n1--教研室；\r\n2-研究所；\r\n3 实验中心；\r\n4-办公室；\r\n5-其他')
    isDeleted = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否被删除   0 -未被删除  1 - 被删除')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
