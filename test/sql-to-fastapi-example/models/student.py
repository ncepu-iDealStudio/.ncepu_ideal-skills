"""
学生基本信息数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from models import Base


class Student(Base):
    """
    学生基本信息
    """
    __tablename__ = "student"

    auto_id = Column("autoID", Integer, primary_key=True, nullable=False, comment="自增字段")
    student_id = Column("studentID", String(20), nullable=True, comment="学号，业务主键")
    user_id = Column("userID", String(22), nullable=True, comment="对应的用户表ID")
    class_id = Column("classID", String(10), nullable=True, comment="所属班级ID")
    college_id = Column("collegeID", String(20), nullable=True, comment="所属学院")
    name = Column("name", String(20), nullable=True, comment="学生姓名")
    phone_number = Column("phoneNumber", String(500), nullable=True, comment="手机号码")
    age = Column("age", Integer, nullable=True, comment="年龄")
    agenda = Column("agenda", String(10), nullable=True, comment="性别")
    is_delete = Column("isDelete", Boolean, default=False, nullable=True, comment="是否删除")
    add_time = Column("addTime", DateTime, default=datetime.now, nullable=True, comment="记录添加时间")

    @property
    def masked_phone_number(self) -> str:
        if self.phone_number and len(self.phone_number) >= 11:
            return f"{self.phone_number[:3]}****{self.phone_number[-4:]}"
        return "****"