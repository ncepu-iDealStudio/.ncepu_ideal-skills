"""
学生基本信息数据模型

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


class Student(BaseModel):
    """
    学生基本信息
    """

    __tablename__ = "student"


    auto_id = Column(
        "autoID",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="自增字段",
    )

    student_id = Column(
        "studentID",
        String(20),
        nullable=False,
        unique=True,
        comment="学号，业务主键",
    )

    user_id = Column(
        "userID",
        String(22),
        nullable=True,
        comment="关联 sso_user.userID（逻辑外键）",
    )

    class_id = Column(
        "classID",
        String(10),
        nullable=True,
        comment="所属班级ID",
    )

    college_id = Column(
        "collegeID",
        String(20),
        nullable=True,
        comment="所属学院",
    )

    name = Column(
        "name",
        String(20),
        nullable=False,
        comment="学生姓名",
    )

    phone_number = Column(
        "phoneNumber",
        String(500),
        nullable=True,
        comment="手机号码",
    )

    age = Column(
        "age",
        Integer,
        nullable=True,
        comment="年龄",
    )

    gender = Column(
        "gender",
        String(10),
        nullable=True,
        comment="性别：男/女/其他",
    )

    is_delete = Column(
        "isDelete",
        Boolean,
        nullable=False,
        default=False,
        comment="软删除：0未删 1已删",
    )

    add_time = Column(
        "addTime",
        DateTime,
        nullable=False,
        comment="创建时间",
    )



    @property
    def masked_phone_number(self) -> str:
        """脱敏后的手机号码"""
        if self.phone_number and len(self.phone_number) >= 11:
            return f"{self.phone_number[:3]}****{self.phone_number[-4:]}"
        return "****"
