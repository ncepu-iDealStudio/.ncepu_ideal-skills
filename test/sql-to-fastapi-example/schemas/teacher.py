"""
教师数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class TeacherBase(BaseModel):
    """
    教师基础模型
    """

    teacher_id: str = Field(
        ...,
        max_length=15,
        description="教工号",
    )

    user_id: str = Field(
        ...,
        max_length=22,
        description="对应的用户表ID",
    )

    department_id: int | None = Field(
        None,
        description="所属的教研室(研究所)ID",
    )

    name: str = Field(
        ...,
        max_length=50,
        description="姓名",
    )

    email: str | None = Field(
        None,
        max_length=100,
        description="邮箱",
    )

    phone: str | None = Field(
        None,
        max_length=20,
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



class TeacherCreate(TeacherBase):
    """
    教师创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "teacher_id": "demo_teacher_id",

                "user_id": "demo_user_id",

                "department_id": 1,

                "name": "demo_name",

                "email": "user@example.com",

                "phone": "13800138000",

                "office_address": "demo_office_address",

            }
        }


class TeacherUpdate(BaseModel):
    """
    教师更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    teacher_id: str | None = Field(
        default=None,
        max_length=15,
        description="教工号",
    )



    user_id: str | None = Field(
        default=None,
        max_length=22,
        description="对应的用户表ID",
    )



    department_id: int | None = Field(
        default=None,
        description="所属的教研室(研究所)ID",
    )



    name: str | None = Field(
        default=None,
        max_length=50,
        description="姓名",
    )



    email: str | None = Field(
        default=None,
        max_length=100,
        description="邮箱",
    )



    phone: str | None = Field(
        default=None,
        max_length=20,
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


                "teacher_id": "demo_teacher_id",



                "user_id": "demo_user_id",



                "department_id": 1,



                "name": "demo_name",



                "email": "user@example.com",



                "phone": "13800138000",



                "office_address": "demo_office_address",


            }
        }




class TeacherResponse(BaseModel):
    """
    教师响应模型
    """

    auto_id: int

    teacher_id: str

    user_id: str

    department_id: int | None

    name: str

    email: str | None

    phone: str | None

    office_address: str | None

    is_delete: bool

    add_time: datetime

    update_time: datetime


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "teacher_id": "demo_teacher_id",

                "user_id": "demo_user_id",

                "department_id": 1,

                "name": "demo_name",

                "email": "user@example.com",

                "phone": "13800138000",

                "office_address": "demo_office_address",

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

                "update_time": "2026-01-01T00:00:00",

            }
        }