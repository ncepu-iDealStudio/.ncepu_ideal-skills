"""API v1路由包

此文件由 SQL-to-FastAPI-Scaffold 自动生成

注册v1版本下的所有子路由并导出
"""

from fastapi import APIRouter

v1_router = APIRouter()

from api.v1.admin.adminResource import router as AdminRouter
v1_router.include_router(AdminRouter)

from api.v1.course.courseResource import router as CourseRouter
v1_router.include_router(CourseRouter)

from api.v1.course_arrangement.course_arrangementResource import router as CourseArrangementRouter
v1_router.include_router(CourseArrangementRouter)

from api.v1.sso_user.sso_userResource import router as SsoUserRouter
v1_router.include_router(SsoUserRouter)

from api.v1.student.studentResource import router as StudentRouter
v1_router.include_router(StudentRouter)

from api.v1.student_selected_course.student_selected_courseResource import router as StudentSelectedCourseRouter
v1_router.include_router(StudentSelectedCourseRouter)

from api.v1.sys_class.sys_classResource import router as SysClassRouter
v1_router.include_router(SysClassRouter)

from api.v1.sys_classinfo.sys_classinfoResource import router as SysClassinfoRouter
v1_router.include_router(SysClassinfoRouter)

from api.v1.sys_college.sys_collegeResource import router as SysCollegeRouter
v1_router.include_router(SysCollegeRouter)

from api.v1.sys_department.sys_departmentResource import router as SysDepartmentRouter
v1_router.include_router(SysDepartmentRouter)

from api.v1.teacher.teacherResource import router as TeacherRouter
v1_router.include_router(TeacherRouter)

__all__ = ["v1_router"]
