"""
课程基本信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CourseBase(BaseModel):
    """
    课程基本信息基础模型
    """

    course_id: str | None = Field(
        None,
        max_length=20,
        description="课程编号",
    )

    course_name: str | None = Field(
        None,
        max_length=50,
        description="课程名称",
    )

    teacher_id: str | None = Field(
        None,
        max_length=15,
        description="任课教师编号",
    )

    credit: float | None = Field(
        None,
        description="学分",
    )




class CourseCreate(CourseBase):
    """
    课程基本信息创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "course_id": "demo_course_id",

                "course_name": "demo_course_name",

                "teacher_id": "demo_teacher_id",

                "credit": 1.0,

            }
        }


class CourseUpdate(BaseModel):
    """
    课程基本信息更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    course_id: str | None = Field(
        default=None,
        max_length=20,
        description="课程编号",
    )



    course_name: str | None = Field(
        default=None,
        max_length=50,
        description="课程名称",
    )



    teacher_id: str | None = Field(
        default=None,
        max_length=15,
        description="任课教师编号",
    )



    credit: float | None = Field(
        default=None,
        description="学分",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "course_id": "demo_course_id",



                "course_name": "demo_course_name",



                "teacher_id": "demo_teacher_id",



                "credit": 1.0,


            }
        }




class CourseResponse(BaseModel):
    """
    课程基本信息响应模型
    """

    auto_id: int

    course_id: str | None

    course_name: str | None

    teacher_id: str | None

    credit: float | None

    is_delete: bool | None

    add_time: datetime | None


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "course_id": "demo_course_id",

                "course_name": "demo_course_name",

                "teacher_id": "demo_teacher_id",

                "credit": 1.0,

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }