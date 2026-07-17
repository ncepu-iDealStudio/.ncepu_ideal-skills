"""
用户账号信息（登录中心）数据模型

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


class SsoUser(BaseModel):
    """
    用户账号信息（登录中心）
    """

    __tablename__ = "sso_user"


    auto_id = Column(
        "autoID",
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="物理主键，自增",
    )

    user_id = Column(
        "userID",
        String(22),
        nullable=False,
        unique=True,
        comment="用户业务ID，被业务表 userID 引用",
    )

    account = Column(
        "account",
        String(255),
        nullable=False,
        unique=True,
        comment="登录账号（手机号/邮箱/用户名）",
    )

    password = Column(
        "password",
        String(255),
        nullable=False,
        comment="密码哈希（新数据请用 bcrypt）",
    )

    user_type = Column(
        "userType",
        Integer,
        nullable=True,
        comment="账号类型：1学生 2教师 3管理员",
    )

    status = Column(
        "status",
        Integer,
        nullable=False,
        default=1,
        comment="账号状态：1-可用; 0--锁定",
    )

    add_time = Column(
        "addTime",
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )

