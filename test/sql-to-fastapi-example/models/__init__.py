"""Models包

此文件由 SQL-to-FastAPI-Scaffold 自动生成

导出共享的 Base / BaseModel 供所有模型使用
"""

from core.database import Base
from models.base import BaseModel

from models.admin import Admin  # noqa: F401
from models.course import Course  # noqa: F401
from models.course_arrangement import CourseArrangement  # noqa: F401
from models.sso_user import SsoUser  # noqa: F401
from models.student import Student  # noqa: F401
from models.student_selected_course import StudentSelectedCourse  # noqa: F401
from models.sys_class import SysClass  # noqa: F401
from models.sys_classinfo import SysClassinfo  # noqa: F401
from models.sys_college import SysCollege  # noqa: F401
from models.sys_department import SysDepartment  # noqa: F401
from models.teacher import Teacher  # noqa: F401

__all__ = ["Base", "BaseModel"]
