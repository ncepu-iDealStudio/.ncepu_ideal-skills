"""API v1路由包

此文件由 SQL-to-FastAPI-Scaffold 自动生成

注册v1版本下的所有子路由并导出
"""

from fastapi import APIRouter

from api.v1.admin import router as AdminRouter
from api.v1.course import router as CourseRouter
from api.v1.course_arrangement import router as CourseArrangementRouter
from api.v1.sso_user import router as SsoUserRouter
from api.v1.student import router as StudentRouter
from api.v1.student_selected_course import router as StudentSelectedCourseRouter
from api.v1.sys_class_info import router as SysClassInfoRouter
from api.v1.sys_college_info import router as SysCollegeInfoRouter
from api.v1.sys_department_info import router as SysDepartmentInfoRouter
from api.v1.teacher import router as TeacherRouter

v1_router = APIRouter()

v1_router.include_router(AdminRouter)
v1_router.include_router(CourseRouter)
v1_router.include_router(CourseArrangementRouter)
v1_router.include_router(SsoUserRouter)
v1_router.include_router(StudentRouter)
v1_router.include_router(StudentSelectedCourseRouter)
v1_router.include_router(SysClassInfoRouter)
v1_router.include_router(SysCollegeInfoRouter)
v1_router.include_router(SysDepartmentInfoRouter)
v1_router.include_router(TeacherRouter)

__all__ = ["v1_router"]