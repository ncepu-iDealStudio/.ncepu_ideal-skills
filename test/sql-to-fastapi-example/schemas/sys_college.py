"""
学院数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class SysCollegeBase(BaseModel):
    """
    学院基础模型
    """

    college_id: str = Field(
        ...,
        max_length=20,
        description="学院ID编码--业务主键",
    )

    college_name: str | None = Field(
        None,
        max_length=50,
        description="学院名称",
    )




class SysCollegeCreate(SysCollegeBase):
    """
    学院创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "college_id": "demo_college_id",

                "college_name": "demo_college_name",

            }
        }


class SysCollegeUpdate(BaseModel):
    """
    学院更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    college_id: str | None = Field(
        default=None,
        max_length=20,
        description="学院ID编码--业务主键",
    )



    college_name: str | None = Field(
        default=None,
        max_length=50,
        description="学院名称",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "college_id": "demo_college_id",



                "college_name": "demo_college_name",


            }
        }




class SysCollegeResponse(BaseModel):
    """
    学院响应模型
    """

    college_id: str

    college_name: str | None

    is_delete: bool | None

    add_time: datetime | None


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "college_id": "demo_college_id",

                "college_name": "demo_college_name",

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }