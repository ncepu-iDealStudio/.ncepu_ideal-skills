"""
教研室与研究所信息数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from sqlalchemy import Column, String, BigInteger, Integer, Boolean, DateTime
from models import Base


class SysDepartmentInfo(Base):
    """
    教研室与研究所信息
    """
    __tablename__ = "sys_departmentInfo"

    auto_id = Column("autoID", BigInteger, primary_key=True, nullable=False)
    department_id = Column("departmentID", BigInteger, nullable=True, comment="学院下属的教研室(研究所)ID")
    parent_department_id = Column("parentDepartmentID", BigInteger, default=0, nullable=False, comment="父级部门ID")
    college_id = Column("collegeID", String(20), nullable=True, comment="学院ID编码--业务主键")
    department_name = Column("departmentName", String(255), nullable=True, comment="教研室(研究所)名称")
    department_type = Column("departmentType", Integer, default=1, nullable=True, comment="部门类型: 1--教研室；2-研究所；3 实验中心；4-办公室；5-其他")
    is_deleted = Column("isDeleted", Boolean, default=False, nullable=False, comment="是否被删除   0 -未被删除  1 - 被删除")
    add_time = Column("addTime", DateTime, default=datetime.now, nullable=True, comment="记录添加时间")