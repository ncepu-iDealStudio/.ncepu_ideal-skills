"""
课程安排业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.course_arrangement import CourseArrangement
from schemas.course_arrangement import CourseArrangementCreate, CourseArrangementUpdate, CourseArrangementResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class CourseArrangementService:
    """
    课程安排服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CourseArrangementCreate) -> CourseArrangementResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = CourseArrangement(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return CourseArrangementResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(CourseArrangement).filter(CourseArrangement.is_delete == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [CourseArrangementResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> CourseArrangementResponse:
        obj = self.db.query(CourseArrangement).filter(
            CourseArrangement.auto_id == auto_id,
            CourseArrangement.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("课程安排不存在")

        return CourseArrangementResponse.model_validate(obj)

    def update(self, auto_id: int, data: CourseArrangementUpdate) -> CourseArrangementResponse:
        obj = self.db.query(CourseArrangement).filter(
            CourseArrangement.auto_id == auto_id,
            CourseArrangement.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("课程安排不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return CourseArrangementResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(CourseArrangement).filter(
            CourseArrangement.auto_id == auto_id,
            CourseArrangement.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("课程安排不存在")

        setattr(obj, "is_delete", True)
        self.db.commit()