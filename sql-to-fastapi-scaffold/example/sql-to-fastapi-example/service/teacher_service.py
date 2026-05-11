"""
教师业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.teacher import Teacher
from schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class TeacherService:
    """
    教师服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: TeacherCreate) -> TeacherResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = Teacher(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return TeacherResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(Teacher).filter(Teacher.is_delete == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [TeacherResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> TeacherResponse:
        obj = self.db.query(Teacher).filter(
            Teacher.auto_id == auto_id,
            Teacher.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("教师不存在")

        return TeacherResponse.model_validate(obj)

    def update(self, auto_id: int, data: TeacherUpdate) -> TeacherResponse:
        obj = self.db.query(Teacher).filter(
            Teacher.auto_id == auto_id,
            Teacher.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("教师不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return TeacherResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(Teacher).filter(
            Teacher.auto_id == auto_id,
            Teacher.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("教师不存在")

        setattr(obj, "is_delete", True)
        self.db.commit()