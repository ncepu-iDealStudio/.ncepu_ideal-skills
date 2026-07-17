"""
教研室与研究所部门信息数据验证模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class SysDepartmentBase(BaseModel):
    """
    教研室与研究所部门信息基础模型
    """

    department_id: int = Field(
        ...,
        description="部门ID：学院下属的教研室(研究所)ID",
    )

    parent_department_id: int = Field(
        ...,
        description="父级部门ID",
    )

    college_id: str | None = Field(
        None,
        max_length=20,
        description="学院ID编码--业务主键",
    )

    department_name: str | None = Field(
        None,
        max_length=255,
        description="教研室(研究所)名称",
    )

    department_type: int | None = Field(
        None,
        description="部门类型:1教研室;2研究所;3实验中心;4办公室;5其他",
    )




class SysDepartmentCreate(SysDepartmentBase):
    """
    教研室与研究所部门信息创建模型
    """

    class Config:
        json_schema_extra = {
            "example": {

                "department_id": 1,

                "parent_department_id": 1,

                "college_id": "demo_college_id",

                "department_name": "demo_department_name",

                "department_type": 1,

            }
        }


class SysDepartmentUpdate(BaseModel):
    """
    教研室与研究所部门信息更新模型

    注意：状态/标识位字段不在此模型中，请使用专用改状态接口。
    """


    department_id: int | None = Field(
        default=None,
        description="部门ID：学院下属的教研室(研究所)ID",
    )



    parent_department_id: int | None = Field(
        default=None,
        description="父级部门ID",
    )



    college_id: str | None = Field(
        default=None,
        max_length=20,
        description="学院ID编码--业务主键",
    )



    department_name: str | None = Field(
        default=None,
        max_length=255,
        description="教研室(研究所)名称",
    )



    department_type: int | None = Field(
        default=None,
        description="部门类型:1教研室;2研究所;3实验中心;4办公室;5其他",
    )



    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {


                "department_id": 1,



                "parent_department_id": 1,



                "college_id": "demo_college_id",



                "department_name": "demo_department_name",



                "department_type": 1,


            }
        }




class SysDepartmentResponse(BaseModel):
    """
    教研室与研究所部门信息响应模型
    """

    department_id: int

    parent_department_id: int

    college_id: str | None

    department_name: str | None

    department_type: int | None

    is_delete: bool

    add_time: datetime | None


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {

                "department_id": 1,

                "parent_department_id": 1,

                "college_id": "demo_college_id",

                "department_name": "demo_department_name",

                "department_type": 1,

                "is_delete": False,

                "add_time": "2026-01-01T00:00:00",

            }
        }