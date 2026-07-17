"""
班级信息数据模型

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


class SysClass(BaseModel):
    """
    班级信息
    """

    __tablename__ = "sys_class"


    class_id = Column(
        "classID",
        String(10),
        primary_key=True,
        nullable=False,
        comment="班级ID--业务主键",
    )

    college_id = Column(
        "collegeID",
        String(20),
        nullable=True,
        comment="所属学院",
    )

    class_name = Column(
        "className",
        String(20),
        nullable=True,
        comment="班级名称",
    )

    is_delete = Column(
        "isDelete",
        Boolean,
        nullable=True,
        default=False,
        comment="是否被删除  0 - 未删除  1 - 已删除",
    )

    add_time = Column(
        "addTime",
        DateTime,
        nullable=True,
        comment="记录添加时间",
    )

