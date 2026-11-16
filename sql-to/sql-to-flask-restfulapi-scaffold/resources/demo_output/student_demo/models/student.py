# coding: utf-8
from models import db, BaseModel


class Student(BaseModel):
    __tablename__ = "student"

    # Fields rendered from SQL columns
    autoID = db.Column(db.Integer, primary_key=True, nullable=False, info="自增字段")
    studentID = db.Column(db.String(20), primary_key=False, nullable=True, info="学号")
    name = db.Column(db.String(20), primary_key=False, nullable=True, info="学生姓名")
    isDelete = db.Column(db.Integer, primary_key=False, nullable=True, default=0, info="是否删除")
