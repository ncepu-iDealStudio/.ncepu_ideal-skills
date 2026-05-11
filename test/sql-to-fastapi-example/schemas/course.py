"""
课程基本信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    course_id: Optional[str] = Field(None, max_length=20, description="课程编号")
    course_name: Optional[str] = Field(None, max_length=50, description="课程名称")
    teacher_id: Optional[str] = Field(None, max_length=15, description="任课教师编号")
    credit: Optional[float] = Field(None, ge=0, le=10, description="学分")
    is_delete: Optional[bool] = Field(None, description="是否删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")


class CourseCreate(CourseBase):
    auto_id: int = Field(..., description="自增序号")


class CourseUpdate(BaseModel):
    course_id: Optional[str] = Field(None, max_length=20, description="课程编号")
    course_name: Optional[str] = Field(None, max_length=50, description="课程名称")
    teacher_id: Optional[str] = Field(None, max_length=15, description="任课教师编号")
    credit: Optional[float] = Field(None, ge=0, le=10, description="学分")
    is_delete: Optional[bool] = Field(None, description="是否删除")

    class Config:
        extra = "forbid"


class CourseResponse(BaseModel):
    auto_id: int
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    teacher_id: Optional[str] = None
    credit: Optional[float] = None
    is_delete: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True