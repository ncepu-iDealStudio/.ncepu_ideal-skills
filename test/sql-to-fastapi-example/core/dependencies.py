"""
依赖注入（FastAPI Depends）

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- Resource 统一注入 get_{table}_service
- Service 内部组合 Repository；一般无需在 Resource 中注入 Repository
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session


def get_admin_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取管理员业务服务实例"""
    from service.admin_service import AdminService

    return AdminService(db)


def get_admin_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取管理员仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.admin_repository import AdminRepository

    return AdminRepository(db)


def get_course_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取课程基本信息业务服务实例"""
    from service.course_service import CourseService

    return CourseService(db)


def get_course_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取课程基本信息仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.course_repository import CourseRepository

    return CourseRepository(db)


def get_course_arrangement_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取课程安排业务服务实例"""
    from service.course_arrangement_service import CourseArrangementService

    return CourseArrangementService(db)


def get_course_arrangement_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取课程安排仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.course_arrangement_repository import CourseArrangementRepository

    return CourseArrangementRepository(db)


def get_sso_user_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取用户账号信息（登录中心）业务服务实例"""
    from service.sso_user_service import SsoUserService

    return SsoUserService(db)


def get_sso_user_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取用户账号信息（登录中心）仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.sso_user_repository import SsoUserRepository

    return SsoUserRepository(db)


def get_student_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取学生基本信息业务服务实例"""
    from service.student_service import StudentService

    return StudentService(db)


def get_student_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取学生基本信息仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.student_repository import StudentRepository

    return StudentRepository(db)


def get_student_selected_course_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取学生选课情况业务服务实例"""
    from service.student_selected_course_service import StudentSelectedCourseService

    return StudentSelectedCourseService(db)


def get_student_selected_course_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取学生选课情况仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.student_selected_course_repository import StudentSelectedCourseRepository

    return StudentSelectedCourseRepository(db)


def get_sys_class_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取班级信息业务服务实例"""
    from service.sys_class_service import SysClassService

    return SysClassService(db)


def get_sys_class_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取班级信息仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.sys_class_repository import SysClassRepository

    return SysClassRepository(db)


def get_sys_classinfo_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取班级信息（classinfo）业务服务实例"""
    from service.sys_classinfo_service import SysClassinfoService

    return SysClassinfoService(db)


def get_sys_classinfo_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取班级信息（classinfo）仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.sys_classinfo_repository import SysClassinfoRepository

    return SysClassinfoRepository(db)


def get_sys_college_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取学院业务服务实例"""
    from service.sys_college_service import SysCollegeService

    return SysCollegeService(db)


def get_sys_college_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取学院仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.sys_college_repository import SysCollegeRepository

    return SysCollegeRepository(db)


def get_sys_department_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取教研室与研究所部门信息业务服务实例"""
    from service.sys_department_service import SysDepartmentService

    return SysDepartmentService(db)


def get_sys_department_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取教研室与研究所部门信息仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.sys_department_repository import SysDepartmentRepository

    return SysDepartmentRepository(db)


def get_teacher_service(
    db: AsyncSession = Depends(get_async_session),
):
    """获取教师业务服务实例"""
    from service.teacher_service import TeacherService

    return TeacherService(db)


def get_teacher_repository(
    db: AsyncSession = Depends(get_async_session),
):
    """获取教师仓储实例（一般由 Service 内部使用；特殊场景可注入）"""
    from repository.teacher_repository import TeacherRepository

    return TeacherRepository(db)


