"""
班级信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SysClassInfoBase(BaseModel):
    class_id: Optional[str] = Field(None, max_length=10, description="班级ID")
    college_id: Optional[str] = Field(None, max_length=20, description="所属学院")
    class_name: Optional[str] = Field(None, max_length=20, description="班级名称")
    is_deleted: Optional[bool] = Field(None, description="是否被删除  0 - 未删除  1 - 已删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")


class SysClassInfoCreate(SysClassInfoBase):
    auto_id: int = Field(..., description="自增序号")


class SysClassInfoUpdate(BaseModel):
    class_id: Optional[str] = Field(None, max_length=10, description="班级ID")
    college_id: Optional[str] = Field(None, max_length=20, description="所属学院")
    class_name: Optional[str] = Field(None, max_length=20, description="班级名称")
    is_deleted: Optional[bool] = Field(None, description="是否被删除  0 - 未删除  1 - 已删除")

    class Config:
        extra = "forbid"


class SysClassInfoResponse(BaseModel):
    auto_id: int
    class_id: Optional[str] = None
    college_id: Optional[str] = None
    class_name: Optional[str] = None
    is_deleted: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True