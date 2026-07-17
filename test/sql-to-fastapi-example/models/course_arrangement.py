"""
课程安排数据模型

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


class CourseArrangement(BaseModel):
    """
    课程安排
    """

    __tablename__ = "course_arrangement"


    auto_id = Column(
        "autoID",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="自增序号",
    )

    course_id = Column(
        "courseID",
        String(20),
        nullable=True,
        comment="课程编号",
    )

    term_id = Column(
        "termID",
        String(50),
        nullable=True,
        comment="学期ID",
    )

    class_time = Column(
        "classTime",
        String(20),
        nullable=True,
        comment="上课时间：1-2；3-4；5-6；7-8；",
    )

    count = Column(
        "count",
        Integer,
        nullable=True,
        comment="课程容量-可选人数",
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

