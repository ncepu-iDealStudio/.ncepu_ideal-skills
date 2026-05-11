"""
用户账号信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class SsoUserBase(BaseModel):
    user_id: Optional[str] = Field(None, max_length=22, description="用户ID")
    account: Optional[str] = Field(None, max_length=255, description="登录账号-默认为手机号")
    password: Optional[str] = Field(None, max_length=255, description="密码")
    user_type: Optional[int] = Field(None, ge=1, le=3, description="账号类型：1--学生；2--老师；3--管理人员")
    status: Optional[int] = Field(None, ge=0, le=1, description="账号的状态：1--可用；0--锁定")
    add_time: Optional[datetime] = Field(None, description="记录添加时间")

    @field_validator("account")
    @classmethod
    def validate_account(cls, v):
        if v is not None:
            import re
            if re.match(r"^1[3-9]\d{9}$", v):
                pass
        return v


class SsoUserCreate(SsoUserBase):
    auto_id: int = Field(..., description="自增序号")


class SsoUserUpdate(BaseModel):
    user_id: Optional[str] = Field(None, max_length=22, description="用户ID")
    account: Optional[str] = Field(None, max_length=255, description="登录账号-默认为手机号")
    password: Optional[str] = Field(None, max_length=255, description="密码")
    user_type: Optional[int] = Field(None, ge=1, le=3, description="账号类型：1--学生；2--老师；3--管理人员")
    status: Optional[int] = Field(None, ge=0, le=1, description="账号的状态：1--可用；0--锁定")

    class Config:
        extra = "forbid"


class SsoUserResponse(BaseModel):
    auto_id: int
    user_id: Optional[str] = None
    account: Optional[str] = None
    password: Optional[str] = None
    user_type: Optional[int] = None
    status: Optional[int] = None
    add_time: Optional[datetime] = None

    class Config:
        from_attributes = True