"""
学生基本信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class StudentBase(BaseModel):
    """
    学生基本信息基础模型
    """

    student_id: str = Field(
        ...,
        max_length=20,
        description="学号，业务主键",
    )

    user_id: str | None = Field(
        None,
        max_length=22,
        description="关联 sso_user.userID（逻辑外键）",
    )

    class_id: str | None = Field(
        None,
        max_length=10,
        description="所属班级ID",
    )

    college_id: str | None = Field(
        None,
        max_length=20,
        description="所属学院",
    )

    name: str = Field(
        ...,
        max_length=20,
        description="学生姓名",
    )

    phone_number: str | None = Field(
        None,
        max_length=500,
        description="手机号码",
    )

    age: int | None = Field(
        None,
        ge=0,
        le=150,
        description="年龄",
    )

    gender: str | None = Field(
        None,
        max_length=10,
        description="性别：男/女/其他",
    )



    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):

        if v is not None:
            import re
            if not re.match(r"^1[3-9]\d{9}$", v):
                raise ValueError("手机号格式不正确")

        return v


    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):

        if v is not None and v not in ["男", "女", "其他"]:
            raise ValueError("性别只能是：男、女、其他")

        return v



class StudentCreate(StudentBase):
    """
    学生基本信息创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "student_id": "demo_student_id",

                "user_id": "demo_user_id",

                "class_id": "demo_class",

                "college_id": "demo_college_id",

                "name": "demo_name",

                "phone_number": "13800138000",

                "age": 1,

                "gender": "男",

            }
        }


class StudentUpdate(BaseModel):
    """
    学生基本信息更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    student_id: str | None = Field(
        default=None,
        max_length=20,
        description="学号，业务主键",
    )



    user_id: str | None = Field(
        default=None,
        max_length=22,
        description="关联 sso_user.userID（逻辑外键）",
    )



    class_id: str | None = Field(
        default=None,
        max_length=10,
        description="所属班级ID",
    )



    college_id: str | None = Field(
        default=None,
        max_length=20,
        description="所属学院",
    )



    name: str | None = Field(
        default=None,
        max_length=20,
        description="学生姓名",
    )



    phone_number: str | None = Field(
        default=None,
        max_length=500,
        description="手机号码",
    )



    age: int | None = Field(
        default=None,
        ge=0,
        le=150,
        description="年龄",
    )



    gender: str | None = Field(
        default=None,
        max_length=10,
        description="性别：男/女/其他",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "student_id": "demo_student_id",



                "user_id": "demo_user_id",



                "class_id": "demo_class",



                "college_id": "demo_college_id",



                "name": "demo_name",



                "phone_number": "13800138000",



                "age": 1,



                "gender": "男",


            }
        }




class StudentResponse(BaseModel):
    """
    学生基本信息响应模型
    """

    auto_id: int

    student_id: str

    user_id: str | None

    class_id: str | None

    college_id: str | None

    name: str

    phone_number: str | None

    age: int | None

    gender: str | None

    is_delete: bool

    add_time: datetime


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "student_id": "demo_student_id",

                "user_id": "demo_user_id",

                "class_id": "demo_class",

                "college_id": "demo_college_id",

                "name": "demo_name",

                "phone_number": "13800138000",

                "age": 1,

                "gender": "男",

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }