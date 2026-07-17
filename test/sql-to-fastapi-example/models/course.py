"""
课程基本信息数据模型

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


class Course(BaseModel):
    """
    课程基本信息
    """

    __tablename__ = "course"


    auto_id = Column(
        "autoID",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="自增主键",
    )

    course_id = Column(
        "courseID",
        String(20),
        nullable=True,
        unique=True,
        comment="课程编号",
    )

    course_name = Column(
        "courseName",
        String(50),
        nullable=True,
        comment="课程名称",
    )

    teacher_id = Column(
        "teacherID",
        String(15),
        nullable=True,
        comment="任课教师编号",
    )

    credit = Column(
        "credit",
        Float,
        nullable=True,
        comment="学分",
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

