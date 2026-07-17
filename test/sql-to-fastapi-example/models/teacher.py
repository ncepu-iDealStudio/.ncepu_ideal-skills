"""
教师数据模型

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


class Teacher(BaseModel):
    """
    教师
    """

    __tablename__ = "teacher"


    auto_id = Column(
        "autoID",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="自增主键",
    )

    teacher_id = Column(
        "teacherID",
        String(15),
        nullable=False,
        unique=True,
        comment="教工号",
    )

    user_id = Column(
        "userID",
        String(22),
        nullable=False,
        comment="对应的用户表ID",
    )

    department_id = Column(
        "departmentID",
        BigInteger,
        nullable=True,
        comment="所属的教研室(研究所)ID",
    )

    name = Column(
        "name",
        String(50),
        nullable=False,
        comment="姓名",
    )

    email = Column(
        "email",
        String(100),
        nullable=True,
        comment="邮箱",
    )

    phone = Column(
        "phone",
        String(20),
        nullable=True,
        comment="电话",
    )

    office_address = Column(
        "officeAddress",
        String(255),
        nullable=True,
        comment="办公地址",
    )

    is_delete = Column(
        "isDelete",
        Boolean,
        nullable=False,
        default=False,
        comment="是否删除: 0--有效；1--已删除",
    )

    add_time = Column(
        "addTime",
        DateTime,
        nullable=False,
        comment="记录添加时间",
    )

    update_time = Column(
        "updateTime",
        DateTime,
        nullable=False,
        comment="记录更新时间",
    )



    @property
    def masked_email(self) -> str:
        """脱敏后的邮箱"""
        if self.email and len(self.email) >= 6:
            return f"{self.email[:3]}****{self.email[-4:]}"
        return "****"


    @property
    def masked_phone(self) -> str:
        """脱敏后的电话"""
        if self.phone and len(self.phone) >= 11:
            return f"{self.phone[:3]}****{self.phone[-4:]}"
        return "****"
