"""
学生选课情况数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class StudentSelectedCourseBase(BaseModel):
    student_id: str = Field(..., max_length=20, description="学号")
    course_id: str = Field(..., max_length=15, description="课程编号")
    score: Optional[int] = Field(None, ge=0, le=100, description="成绩")
    is_delete: Optional[bool] = Field(None, description="是否删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")


class StudentSelectedCourseCreate(StudentSelectedCourseBase):
    auto_id: int = Field(..., description="自增序号字段")


class StudentSelectedCourseUpdate(BaseModel):
    student_id: Optional[str] = Field(None, max_length=20, description="学号")
    course_id: Optional[str] = Field(None, max_length=15, description="课程编号")
    score: Optional[int] = Field(None, ge=0, le=100, description="成绩")
    is_delete: Optional[bool] = Field(None, description="是否删除")

    class Config:
        extra = "forbid"


class StudentSelectedCourseResponse(BaseModel):
    auto_id: int
    student_id: str
    course_id: str
    score: Optional[int] = None
    is_delete: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True