"""
课程安排数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CourseArrangementBase(BaseModel):
    course_id: Optional[str] = Field(None, max_length=20, description="课程编号")
    term_id: Optional[str] = Field(None, max_length=50, description="学期ID")
    class_time: Optional[str] = Field(None, max_length=20, description="上课时间：1-2；3-4；5-6；7-8；")
    count: Optional[int] = Field(None, ge=0, description="课程容量-可选人数")
    is_delete: Optional[bool] = Field(None, description="是否删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")


class CourseArrangementCreate(CourseArrangementBase):
    auto_id: int = Field(..., description="自增序号")


class CourseArrangementUpdate(BaseModel):
    course_id: Optional[str] = Field(None, max_length=20, description="课程编号")
    term_id: Optional[str] = Field(None, max_length=50, description="学期ID")
    class_time: Optional[str] = Field(None, max_length=20, description="上课时间：1-2；3-4；5-6；7-8；")
    count: Optional[int] = Field(None, ge=0, description="课程容量-可选人数")
    is_delete: Optional[bool] = Field(None, description="是否删除")

    class Config:
        extra = "forbid"


class CourseArrangementResponse(BaseModel):
    auto_id: int
    course_id: Optional[str] = None
    term_id: Optional[str] = None
    class_time: Optional[str] = None
    count: Optional[int] = None
    is_delete: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True