"""
学生基本信息业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.student import Student
from schemas.student import StudentCreate, StudentUpdate, StudentResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class StudentService:
    """
    学生基本信息服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: StudentCreate) -> StudentResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = Student(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return StudentResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(Student).filter(Student.is_delete == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [StudentResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> StudentResponse:
        obj = self.db.query(Student).filter(
            Student.auto_id == auto_id,
            Student.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学生不存在")

        return StudentResponse.model_validate(obj)

    def update(self, auto_id: int, data: StudentUpdate) -> StudentResponse:
        obj = self.db.query(Student).filter(
            Student.auto_id == auto_id,
            Student.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学生不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return StudentResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(Student).filter(
            Student.auto_id == auto_id,
            Student.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学生不存在")

        setattr(obj, "is_delete", True)
        self.db.commit()