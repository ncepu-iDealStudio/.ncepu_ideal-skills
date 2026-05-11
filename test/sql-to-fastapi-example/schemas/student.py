"""
学生基本信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class StudentBase(BaseModel):
    student_id: Optional[str] = Field(None, max_length=20, description="学号，业务主键")
    user_id: Optional[str] = Field(None, max_length=22, description="对应的用户表ID")
    class_id: Optional[str] = Field(None, max_length=10, description="所属班级ID")
    college_id: Optional[str] = Field(None, max_length=20, description="所属学院")
    name: Optional[str] = Field(None, max_length=20, description="学生姓名")
    phone_number: Optional[str] = Field(None, max_length=500, description="手机号码")
    age: Optional[int] = Field(None, ge=0, le=150, description="年龄")
    agenda: Optional[str] = Field(None, max_length=10, description="性别")
    is_delete: Optional[bool] = Field(None, description="是否删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if v is not None:
            import re
            if not re.match(r"^1[3-9]\d{9}$", v):
                raise ValueError("手机号格式不正确")
        return v

    @field_validator("agenda")
    @classmethod
    def validate_agenda(cls, v):
        if v is not None and v not in ["男", "女", "其他"]:
            raise ValueError("性别只能是：男、女、其他")
        return v


class StudentCreate(StudentBase):
    auto_id: int = Field(..., description="自增字段")


class StudentUpdate(BaseModel):
    student_id: Optional[str] = Field(None, max_length=20, description="学号，业务主键")
    user_id: Optional[str] = Field(None, max_length=22, description="对应的用户表ID")
    class_id: Optional[str] = Field(None, max_length=10, description="所属班级ID")
    college_id: Optional[str] = Field(None, max_length=20, description="所属学院")
    name: Optional[str] = Field(None, max_length=20, description="学生姓名")
    phone_number: Optional[str] = Field(None, max_length=500, description="手机号码")
    age: Optional[int] = Field(None, ge=0, le=150, description="年龄")
    agenda: Optional[str] = Field(None, max_length=10, description="性别")
    is_delete: Optional[bool] = Field(None, description="是否删除")

    class Config:
        extra = "forbid"


class StudentResponse(BaseModel):
    auto_id: int
    student_id: Optional[str] = None
    user_id: Optional[str] = None
    class_id: Optional[str] = None
    college_id: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None
    agenda: Optional[str] = None
    is_delete: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True