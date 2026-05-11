"""
学生选课情况数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from models import Base


class StudentSelectedCourse(Base):
    """
    学生选课情况
    """
    __tablename__ = "student_selected_course"

    auto_id = Column("autoID", Integer, primary_key=True, nullable=False, comment="自增序号字段")
    student_id = Column("studentID", String(20), nullable=False, comment="学号")
    course_id = Column("courseID", String(15), nullable=False, comment="课程编号")
    score = Column("score", Integer, nullable=True, comment="成绩")
    is_delete = Column("isDelete", Boolean, default=False, nullable=True, comment="是否删除")
    add_time = Column("addTime", DateTime, default=datetime.now, nullable=True, comment="记录添加时间")