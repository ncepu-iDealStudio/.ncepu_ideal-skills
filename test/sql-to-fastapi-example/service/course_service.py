"""
课程基本信息业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.course import Course
from schemas.course import CourseCreate, CourseUpdate, CourseResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class CourseService:
    """
    课程基本信息服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CourseCreate) -> CourseResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = Course(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return CourseResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(Course).filter(Course.is_delete == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [CourseResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> CourseResponse:
        obj = self.db.query(Course).filter(
            Course.auto_id == auto_id,
            Course.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("课程不存在")

        return CourseResponse.model_validate(obj)

    def update(self, auto_id: int, data: CourseUpdate) -> CourseResponse:
        obj = self.db.query(Course).filter(
            Course.auto_id == auto_id,
            Course.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("课程不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return CourseResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(Course).filter(
            Course.auto_id == auto_id,
            Course.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("课程不存在")

        setattr(obj, "is_delete", True)
        self.db.commit()