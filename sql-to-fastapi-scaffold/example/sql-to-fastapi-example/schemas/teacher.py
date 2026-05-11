"""
教师数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class TeacherBase(BaseModel):
    teacher_id: Optional[str] = Field(None, max_length=15, description="教工号")
    user_id: Optional[str] = Field(None, max_length=22, description="对应的用户表ID")
    department_id: Optional[int] = Field(None, description="所属的教研室(研究所)ID")
    name: Optional[str] = Field(None, max_length=10, description="姓名")
    email: Optional[str] = Field(None, max_length=50, description="邮箱")
    phone: Optional[str] = Field(None, max_length=15, description="电话")
    office_address: Optional[str] = Field(None, max_length=255, description="办公地址")
    is_delete: Optional[bool] = Field(None, description="是否删除")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            import re
            if not re.match(r"^1[3-9]\d{9}$", v):
                raise ValueError("手机号格式不正确")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            import re
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
                raise ValueError("邮箱格式不正确")
        return v


class TeacherCreate(TeacherBase):
    auto_id: int = Field(..., description="自增序号")


class TeacherUpdate(BaseModel):
    teacher_id: Optional[str] = Field(None, max_length=15, description="教工号")
    user_id: Optional[str] = Field(None, max_length=22, description="对应的用户表ID")
    department_id: Optional[int] = Field(None, description="所属的教研室(研究所)ID")
    name: Optional[str] = Field(None, max_length=10, description="姓名")
    email: Optional[str] = Field(None, max_length=50, description="邮箱")
    phone: Optional[str] = Field(None, max_length=15, description="电话")
    office_address: Optional[str] = Field(None, max_length=255, description="办公地址")
    is_delete: Optional[bool] = Field(None, description="是否删除")

    class Config:
        extra = "forbid"


class TeacherResponse(BaseModel):
    auto_id: int
    teacher_id: Optional[str] = None
    user_id: Optional[str] = None
    department_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    office_address: Optional[str] = None
    is_delete: Optional[bool] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True