"""
管理员业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.admin import Admin
from schemas.admin import AdminCreate, AdminUpdate, AdminResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class AdminService:
    """
    管理员服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: AdminCreate) -> AdminResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = Admin(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return AdminResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(Admin).filter(Admin.is_delete == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [AdminResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> AdminResponse:
        obj = self.db.query(Admin).filter(
            Admin.auto_id == auto_id,
            Admin.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("管理员不存在")

        return AdminResponse.model_validate(obj)

    def update(self, auto_id: int, data: AdminUpdate) -> AdminResponse:
        obj = self.db.query(Admin).filter(
            Admin.auto_id == auto_id,
            Admin.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("管理员不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return AdminResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(Admin).filter(
            Admin.auto_id == auto_id,
            Admin.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("管理员不存在")

        setattr(obj, "is_delete", True)
        self.db.commit()