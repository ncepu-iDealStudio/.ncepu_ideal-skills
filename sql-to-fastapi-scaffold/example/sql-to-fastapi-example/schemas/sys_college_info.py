"""
学院信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SysCollegeInfoBase(BaseModel):
    college_id: Optional[str] = Field(None, max_length=20, description="学院ID编码--业务主键")
    college_name: Optional[str] = Field(None, max_length=50, description="学院名称")
    is_delete: Optional[bool] = Field(None, description="是否删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")


class SysCollegeInfoCreate(SysCollegeInfoBase):
    auto_id: int = Field(..., description="自增序号")


class SysCollegeInfoUpdate(BaseModel):
    college_id: Optional[str] = Field(None, max_length=20, description="学院ID编码--业务主键")
    college_name: Optional[str] = Field(None, max_length=50, description="学院名称")
    is_delete: Optional[bool] = Field(None, description="是否删除")

    class Config:
        extra = "forbid"


class SysCollegeInfoResponse(BaseModel):
    auto_id: int
    college_id: Optional[str] = None
    college_name: Optional[str] = None
    is_delete: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True