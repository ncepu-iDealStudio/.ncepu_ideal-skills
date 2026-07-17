"""
学生选课情况数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class StudentSelectedCourseBase(BaseModel):
    """
    学生选课情况基础模型
    """

    student_id: str = Field(
        ...,
        max_length=20,
        description="学号",
    )

    course_id: str = Field(
        ...,
        max_length=15,
        description="课程编号",
    )

    score: int | None = Field(
        None,
        description="成绩",
    )




class StudentSelectedCourseCreate(StudentSelectedCourseBase):
    """
    学生选课情况创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "student_id": "demo_student_id",

                "course_id": "demo_course_id",

                "score": 1,

            }
        }


class StudentSelectedCourseUpdate(BaseModel):
    """
    学生选课情况更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    student_id: str | None = Field(
        default=None,
        max_length=20,
        description="学号",
    )



    course_id: str | None = Field(
        default=None,
        max_length=15,
        description="课程编号",
    )



    score: int | None = Field(
        default=None,
        description="成绩",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "student_id": "demo_student_id",



                "course_id": "demo_course_id",



                "score": 1,


            }
        }




class StudentSelectedCourseResponse(BaseModel):
    """
    学生选课情况响应模型
    """

    auto_id: int

    student_id: str

    course_id: str

    score: int | None

    is_delete: bool | None

    add_time: datetime | None


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "student_id": "demo_student_id",

                "course_id": "demo_course_id",

                "score": 1,

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }