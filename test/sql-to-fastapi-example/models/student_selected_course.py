"""
学生选课情况数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    BigInteger,
    String,
    Text,
    Numeric,
    Date,
    Time,
    JSON,
    ForeignKey,
    text,
)
from sqlalchemy.orm import relationship

from models.base import BaseModel


class StudentSelectedCourse(BaseModel):
    """
    学生选课情况
    """

    __tablename__ = "student_selected_course"


    auto_id = Column(
        "autoID",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="自增序号字段",
    )

    student_id = Column(
        "studentID",
        String(20),
        nullable=False,
        comment="学号",
    )

    course_id = Column(
        "courseID",
        String(15),
        nullable=False,
        comment="课程编号",
    )

    score = Column(
        "score",
        Integer,
        nullable=True,
        comment="成绩",
    )

    is_delete = Column(
        "isDelete",
        Boolean,
        nullable=True,
        default=False,
        comment="是否删除",
    )

    add_time = Column(
        "addTime",
        DateTime,
        nullable=True,
        comment="记录添加时间",
    )

