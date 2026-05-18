# coding: utf-8
from . import db, BaseModel


class SsoUser(db.Model):
    __tablename__ = 'sso_user'

    autoID = db.Column(db.BigInteger, primary_key=True)
    userID = db.Column(db.String(22, 'utf8mb4_general_ci'), info='用户ID')
    account = db.Column(db.String(255, 'utf8mb4_general_ci'), info='登录账号-默认为手机号')
    password = db.Column(db.String(255, 'utf8mb4_general_ci'), info='密码')
    userType = db.Column(db.Integer, info='账号类型：1--学生；2--老师；3--管理人员')
    status = db.Column(db.Integer, info='账号的状态：1--可用；0--锁定')
    addTime = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
