# coding: utf-8
from . import db, BaseModel


class Admin(db.Model):
    __tablename__ = 'admin'

    auto_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.BigInteger, info='管理员用户ID')
    user_id = db.Column(db.String(22, 'utf8mb4_0900_ai_ci'), info='对应的用户表ID')
    department_id = db.Column(db.BigInteger, info='所属的部门)ID')
    name = db.Column(db.String(10, 'utf8mb4_general_ci'), info='姓名')
    email = db.Column(db.String(50, 'utf8mb4_general_ci'), info='邮箱')
    phone = db.Column(db.String(100, 'utf8mb4_general_ci'), info='电话')
    office_address = db.Column(db.String(255, 'utf8mb4_general_ci'), info='办公地址')
    is_delete = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否删除')
    add_time = db.Column(db.DateTime, server_default=db.FetchedValue(), info='记录添加时间')
