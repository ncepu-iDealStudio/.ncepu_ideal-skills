"""
管理员数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class AdminBase(BaseModel):
    """
    管理员基础模型
    """

    admin_id: int | None = Field(
        None,
        description="管理员用户ID",
    )

    user_id: str | None = Field(
        None,
        max_length=22,
        description="对应的用户表ID",
    )

    department_id: int | None = Field(
        None,
        description="所属的部门ID",
    )

    name: str | None = Field(
        None,
        max_length=10,
        description="姓名",
    )

    email: str | None = Field(
        None,
        max_length=50,
        description="邮箱",
    )

    phone: str | None = Field(
        None,
        max_length=100,
        description="电话",
    )

    office_address: str | None = Field(
        None,
        max_length=255,
        description="办公地址",
    )



    @field_validator("email")
    @classmethod
    def validate_email(cls, v):

        if v is not None:
            import re
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
                raise ValueError("邮箱格式不正确")

        return v


    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):

        if v is not None:
            import re
            if not re.match(r"^1[3-9]\d{9}$", v):
                raise ValueError("手机号格式不正确")

        return v



class AdminCreate(AdminBase):
    """
    管理员创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "admin_id": 1,

                "user_id": "demo_user_id",

                "department_id": 1,

                "name": "demo_name",

                "email": "user@example.com",

                "phone": "13800138000",

                "office_address": "demo_office_address",

            }
        }


class AdminUpdate(BaseModel):
    """
    管理员更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    admin_id: int | None = Field(
        default=None,
        description="管理员用户ID",
    )



    user_id: str | None = Field(
        default=None,
        max_length=22,
        description="对应的用户表ID",
    )



    department_id: int | None = Field(
        default=None,
        description="所属的部门ID",
    )



    name: str | None = Field(
        default=None,
        max_length=10,
        description="姓名",
    )



    email: str | None = Field(
        default=None,
        max_length=50,
        description="邮箱",
    )



    phone: str | None = Field(
        default=None,
        max_length=100,
        description="电话",
    )



    office_address: str | None = Field(
        default=None,
        max_length=255,
        description="办公地址",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "admin_id": 1,



                "user_id": "demo_user_id",



                "department_id": 1,



                "name": "demo_name",



                "email": "user@example.com",



                "phone": "13800138000",



                "office_address": "demo_office_address",


            }
        }




class AdminResponse(BaseModel):
    """
    管理员响应模型
    """

    auto_id: int

    admin_id: int | None

    user_id: str | None

    department_id: int | None

    name: str | None

    email: str | None

    phone: str | None

    office_address: str | None

    is_delete: bool | None

    add_time: datetime | None


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "admin_id": 1,

                "user_id": "demo_user_id",

                "department_id": 1,

                "name": "demo_name",

                "email": "user@example.com",

                "phone": "13800138000",

                "office_address": "demo_office_address",

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }