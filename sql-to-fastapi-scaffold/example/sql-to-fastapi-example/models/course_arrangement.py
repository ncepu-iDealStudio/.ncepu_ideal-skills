"""
课程安排数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from models import Base


class CourseArrangement(Base):
    """
    课程安排
    """
    __tablename__ = "course_arrangement"

    auto_id = Column("autoID", Integer, primary_key=True, nullable=False, comment="自增序号")
    course_id = Column("courseID", String(20), nullable=True, comment="课程编号")
    term_id = Column("termID", String(50), nullable=True, comment="学期ID")
    class_time = Column("classTime", String(20), nullable=True, comment="上课时间：1-2；3-4；5-6；7-8；")
    count = Column("count", Integer, nullable=True, comment="课程容量-可选人数")
    is_delete = Column("isDelete", Boolean, default=False, nullable=True, comment="是否删除")
    add_time = Column("addTime", DateTime, default=datetime.now, nullable=True, comment="记录添加时间")