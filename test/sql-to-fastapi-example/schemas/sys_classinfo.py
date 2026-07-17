"""
班级信息（classinfo）数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class SysClassinfoBase(BaseModel):
    """
    班级信息（classinfo）基础模型
    """

    class_id: str | None = Field(
        None,
        max_length=10,
        description="班级ID",
    )

    college_id: str | None = Field(
        None,
        max_length=20,
        description="所属学院",
    )

    class_name: str | None = Field(
        None,
        max_length=20,
        description="班级名称",
    )




class SysClassinfoCreate(SysClassinfoBase):
    """
    班级信息（classinfo）创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "class_id": "demo_class",

                "college_id": "demo_college_id",

                "class_name": "demo_class_name",

            }
        }


class SysClassinfoUpdate(BaseModel):
    """
    班级信息（classinfo）更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    class_id: str | None = Field(
        default=None,
        max_length=10,
        description="班级ID",
    )



    college_id: str | None = Field(
        default=None,
        max_length=20,
        description="所属学院",
    )



    class_name: str | None = Field(
        default=None,
        max_length=20,
        description="班级名称",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "class_id": "demo_class",



                "college_id": "demo_college_id",



                "class_name": "demo_class_name",


            }
        }




class SysClassinfoResponse(BaseModel):
    """
    班级信息（classinfo）响应模型
    """

    auto_id: int

    class_id: str | None

    college_id: str | None

    class_name: str | None

    is_deleted: bool | None

    add_time: datetime | None


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "auto_id": 1,

                "class_id": "demo_class",

                "college_id": "demo_college_id",

                "class_name": "demo_class_name",

                "is_deleted": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }