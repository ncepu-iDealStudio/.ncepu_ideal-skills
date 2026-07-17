"""
用户账号信息（登录中心）数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class SsoUserBase(BaseModel):
    """
    用户账号信息（登录中心）基础模型
    """

    user_id: str = Field(
        ...,
        max_length=22,
        description="用户业务ID，被业务表 userID 引用",
    )

    account: str = Field(
        ...,
        max_length=255,
        description="登录账号（手机号/邮箱/用户名）",
    )

    password: str = Field(
        ...,
        max_length=255,
        description="密码哈希（新数据请用 bcrypt）",
    )

    user_type: int | None = Field(
        None,
        description="账号类型：1学生 2教师 3管理员",
    )

    status: int = Field(
        ...,
        description="账号状态：1-可用; 0--锁定",
    )




class SsoUserCreate(SsoUserBase):
    """
    用户账号信息（登录中心）创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "user_id": "demo_user_id",

                "account": "demo_account",

                "password": "hashed_password_example",

                "user_type": 1,

                "status": 1,

            }
        }


class SsoUserUpdate(BaseModel):
    """
    用户账号信息（登录中心）更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    user_id: str | None = Field(
        default=None,
        max_length=22,
        description="用户业务ID，被业务表 userID 引用",
    )



    account: str | None = Field(
        default=None,
        max_length=255,
        description="登录账号（手机号/邮箱/用户名）",
    )



    password: str | None = Field(
        default=None,
        max_length=255,
        description="密码哈希（新数据请用 bcrypt）",
    )



    user_type: int | None = Field(
        default=None,
        description="账号类型：1学生 2教师 3管理员",
    )





    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "user_id": "demo_user_id",



                "account": "demo_account",



                "password": "hashed_password_example",



                "user_type": 1,




            }
        }



class SsoUserStatusUpdate(BaseModel):
    """
    用户账号信息（登录中心）状态/标识位更新模型（专用）
    """

    status: int = Field(
        ...,
        description="账号状态：1-可用; 0--锁定",
    )


    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {

                "status": 1,

            }
        }



class SsoUserResponse(BaseModel):
    """
    用户账号信息（登录中心）响应模型
    """

    auto_id: int

    user_id: str

    account: str

    password: str

    user_type: int | None

    status: int

    add_time: datetime


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "user_id": "demo_user_id",

                "account": "demo_account",

                "password": "hashed_password_example",

                "user_type": 1,

                "status": 1,

                "add_time": "2026-01-01T00:00:00",

            }
        }