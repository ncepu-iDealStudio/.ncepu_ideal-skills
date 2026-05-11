"""
学生选课情况业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.student_selected_course import StudentSelectedCourse
from schemas.student_selected_course import StudentSelectedCourseCreate, StudentSelectedCourseUpdate, StudentSelectedCourseResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class StudentSelectedCourseService:
    """
    学生选课情况服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: StudentSelectedCourseCreate) -> StudentSelectedCourseResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = StudentSelectedCourse(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return StudentSelectedCourseResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(StudentSelectedCourse).filter(StudentSelectedCourse.is_delete == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [StudentSelectedCourseResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> StudentSelectedCourseResponse:
        obj = self.db.query(StudentSelectedCourse).filter(
            StudentSelectedCourse.auto_id == auto_id,
            StudentSelectedCourse.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学生选课记录不存在")

        return StudentSelectedCourseResponse.model_validate(obj)

    def update(self, auto_id: int, data: StudentSelectedCourseUpdate) -> StudentSelectedCourseResponse:
        obj = self.db.query(StudentSelectedCourse).filter(
            StudentSelectedCourse.auto_id == auto_id,
            StudentSelectedCourse.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学生选课记录不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return StudentSelectedCourseResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(StudentSelectedCourse).filter(
            StudentSelectedCourse.auto_id == auto_id,
            StudentSelectedCourse.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学生选课记录不存在")

        setattr(obj, "is_delete", True)
        self.db.commit()