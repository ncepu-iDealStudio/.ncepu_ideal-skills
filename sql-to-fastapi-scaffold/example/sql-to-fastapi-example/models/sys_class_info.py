"""
班级信息数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from models import Base


class SysClassInfo(Base):
    """
    班级信息
    """
    __tablename__ = "sys_classInfo"

    auto_id = Column("autoID", Integer, primary_key=True, nullable=False)
    class_id = Column("classID", String(10), nullable=True, comment="班级ID")
    college_id = Column("collegeID", String(20), nullable=True, comment="所属学院")
    class_name = Column("className", String(20), nullable=True, comment="班级名称")
    is_deleted = Column("isDeleted", Boolean, default=False, nullable=True, comment="是否被删除  0 - 未删除  1 - 已删除")
    add_time = Column("addTime", DateTime, default=datetime.now, nullable=True, comment="记录添加时间")