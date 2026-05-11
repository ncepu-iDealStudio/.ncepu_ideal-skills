"""
学院信息数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from sqlalchemy import Column, String, BigInteger, Boolean, DateTime
from models import Base


class SysCollegeInfo(Base):
    """
    学院信息
    """
    __tablename__ = "sys_collegeInfo"

    auto_id = Column("autoID", BigInteger, primary_key=True, nullable=False)
    college_id = Column("collegeID", String(20), nullable=True, comment="学院ID编码--业务主键")
    college_name = Column("collegeName", String(50), nullable=True, comment="学院名称")
    is_delete = Column("isDelete", Boolean, default=False, nullable=True, comment="是否删除")
    add_time = Column("addTime", DateTime, default=datetime.now, nullable=True, comment="记录添加时间")