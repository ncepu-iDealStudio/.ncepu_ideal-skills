"""
教研室与研究所部门信息数据模型

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


class SysDepartment(BaseModel):
    """
    教研室与研究所部门信息
    """

    __tablename__ = "sys_department"


    department_id = Column(
        "departmentID",
        BigInteger,
        primary_key=True,
        nullable=False,
        comment="部门ID：学院下属的教研室(研究所)ID",
    )

    parent_department_id = Column(
        "parentDepartmentID",
        BigInteger,
        nullable=False,
        default=0,
        comment="父级部门ID",
    )

    college_id = Column(
        "collegeID",
        String(20),
        nullable=True,
        comment="学院ID编码--业务主键",
    )

    department_name = Column(
        "departmentName",
        String(255),
        nullable=True,
        comment="教研室(研究所)名称",
    )

    department_type = Column(
        "departmentType",
        Integer,
        nullable=True,
        default=1,
        comment="部门类型:1教研室;2研究所;3实验中心;4办公室;5其他",
    )

    is_delete = Column(
        "isDelete",
        Boolean,
        nullable=False,
        default=False,
        comment="是否被删除   0 -未被删除  1 - 被删除",
    )

    add_time = Column(
        "addTime",
        DateTime,
        nullable=True,
        comment="记录添加时间",
    )

