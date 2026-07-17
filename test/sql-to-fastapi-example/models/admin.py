"""
管理员数据模型

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


class Admin(BaseModel):
    """
    管理员
    """

    __tablename__ = "admin"


    auto_id = Column(
        "auto_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="自增主键",
    )

    admin_id = Column(
        "admin_id",
        BigInteger,
        nullable=True,
        comment="管理员用户ID",
    )

    user_id = Column(
        "user_id",
        String(22),
        nullable=True,
        comment="对应的用户表ID",
    )

    department_id = Column(
        "department_id",
        BigInteger,
        nullable=True,
        comment="所属的部门ID",
    )

    name = Column(
        "name",
        String(10),
        nullable=True,
        comment="姓名",
    )

    email = Column(
        "email",
        String(50),
        nullable=True,
        comment="邮箱",
    )

    phone = Column(
        "phone",
        String(100),
        nullable=True,
        comment="电话",
    )

    office_address = Column(
        "office_address",
        String(255),
        nullable=True,
        comment="办公地址",
    )

    is_delete = Column(
        "is_delete",
        Boolean,
        nullable=True,
        default=False,
        comment="是否删除",
    )

    add_time = Column(
        "add_time",
        DateTime,
        nullable=True,
        comment="记录添加时间",
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
