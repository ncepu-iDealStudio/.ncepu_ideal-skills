"""
课程安排数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CourseArrangementBase(BaseModel):
    """
    课程安排基础模型
    """

    course_id: str | None = Field(
        None,
        max_length=20,
        description="课程编号",
    )

    term_id: str | None = Field(
        None,
        max_length=50,
        description="学期ID",
    )

    class_time: str | None = Field(
        None,
        max_length=20,
        description="上课时间：1-2；3-4；5-6；7-8；",
    )

    count: int | None = Field(
        None,
        description="课程容量-可选人数",
    )




class CourseArrangementCreate(CourseArrangementBase):
    """
    课程安排创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "course_id": "demo_course_id",

                "term_id": "demo_term_id",

                "class_time": "demo_class_time",

                "count": 1,

            }
        }


class CourseArrangementUpdate(BaseModel):
    """
    课程安排更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    course_id: str | None = Field(
        default=None,
        max_length=20,
        description="课程编号",
    )



    term_id: str | None = Field(
        default=None,
        max_length=50,
        description="学期ID",
    )



    class_time: str | None = Field(
        default=None,
        max_length=20,
        description="上课时间：1-2；3-4；5-6；7-8；",
    )



    count: int | None = Field(
        default=None,
        description="课程容量-可选人数",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "course_id": "demo_course_id",



                "term_id": "demo_term_id",



                "class_time": "demo_class_time",



                "count": 1,


            }
        }




class CourseArrangementResponse(BaseModel):
    """
    课程安排响应模型
    """

    auto_id: int

    course_id: str | None

    term_id: str | None

    class_time: str | None

    count: int | None

    is_delete: bool | None

    add_time: datetime | None


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "course_id": "demo_course_id",

                "term_id": "demo_term_id",

                "class_time": "demo_class_time",

                "count": 1,

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }