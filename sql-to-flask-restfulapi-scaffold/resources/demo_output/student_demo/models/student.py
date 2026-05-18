# coding: utf-8
from models import db, BaseModel


class Student(BaseModel):
    __tablename__ = "student"

    # Fields rendered from SQL columns
    studentID = db.Column(db.String(20), primary_key=False, nullable=True)
    name = db.Column(db.String(20), primary_key=False, nullable=True)
    isDelete = db.Column(db.Integer, primary_key=False, nullable=True)
