"""
依赖注入容器

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from sqlalchemy.orm import Session
from fastapi import Depends
from core.database import get_db


def get_admin_service(db: Session = Depends(get_db)):
    from service.admin_service import AdminService
    return AdminService(db)


def get_course_service(db: Session = Depends(get_db)):
    from service.course_service import CourseService
    return CourseService(db)


def get_course_arrangement_service(db: Session = Depends(get_db)):
    from service.course_arrangement_service import CourseArrangementService
    return CourseArrangementService(db)


def get_sso_user_service(db: Session = Depends(get_db)):
    from service.sso_user_service import SsoUserService
    return SsoUserService(db)


def get_student_service(db: Session = Depends(get_db)):
    from service.student_service import StudentService
    return StudentService(db)


def get_student_selected_course_service(db: Session = Depends(get_db)):
    from service.student_selected_course_service import StudentSelectedCourseService
    return StudentSelectedCourseService(db)


def get_sys_class_info_service(db: Session = Depends(get_db)):
    from service.sys_class_info_service import SysClassInfoService
    return SysClassInfoService(db)


def get_sys_college_info_service(db: Session = Depends(get_db)):
    from service.sys_college_info_service import SysCollegeInfoService
    return SysCollegeInfoService(db)


def get_sys_department_info_service(db: Session = Depends(get_db)):
    from service.sys_department_info_service import SysDepartmentInfoService
    return SysDepartmentInfoService(db)


def get_teacher_service(db: Session = Depends(get_db)):
    from service.teacher_service import TeacherService
    return TeacherService(db)