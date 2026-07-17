"""
学院数据模型

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


class SysCollege(BaseModel):
    """
    学院
    """

    __tablename__ = "sys_college"


    college_id = Column(
        "collegeID",
        String(20),
        primary_key=True,
        nullable=False,
        comment="学院ID编码--业务主键",
    )

    college_name = Column(
        "collegeName",
        String(50),
        nullable=True,
        comment="学院名称",
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

