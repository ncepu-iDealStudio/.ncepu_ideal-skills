"""
教研室与研究所信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SysDepartmentInfoBase(BaseModel):
    department_id: Optional[int] = Field(None, description="学院下属的教研室(研究所)ID")
    parent_department_id: int = Field(default=0, description="父级部门ID")
    college_id: Optional[str] = Field(None, max_length=20, description="学院ID编码--业务主键")
    department_name: Optional[str] = Field(None, max_length=255, description="教研室(研究所)名称")
    department_type: Optional[int] = Field(None, ge=1, le=5, description="部门类型: 1--教研室；2-研究所；3 实验中心；4-办公室；5-其他")
    is_deleted: Optional[bool] = Field(None, description="是否被删除   0 -未被删除  1 - 被删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")


class SysDepartmentInfoCreate(SysDepartmentInfoBase):
    auto_id: int = Field(..., description="自增序号")


class SysDepartmentInfoUpdate(BaseModel):
    department_id: Optional[int] = Field(None, description="学院下属的教研室(研究所)ID")
    parent_department_id: Optional[int] = Field(default=0, description="父级部门ID")
    college_id: Optional[str] = Field(None, max_length=20, description="学院ID编码--业务主键")
    department_name: Optional[str] = Field(None, max_length=255, description="教研室(研究所)名称")
    department_type: Optional[int] = Field(None, ge=1, le=5, description="部门类型: 1--教研室；2-研究所；3 实验中心；4-办公室；5-其他")
    is_deleted: Optional[bool] = Field(None, description="是否被删除   0 -未被删除  1 - 被删除")

    class Config:
        extra = "forbid"


class SysDepartmentInfoResponse(BaseModel):
    auto_id: int
    department_id: Optional[int] = None
    parent_department_id: Optional[int] = None
    college_id: Optional[str] = None
    department_name: Optional[str] = None
    department_type: Optional[int] = None
    is_deleted: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True