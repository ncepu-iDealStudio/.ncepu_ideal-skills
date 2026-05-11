"""
用户账号信息业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.sso_user import SsoUser
from schemas.sso_user import SsoUserCreate, SsoUserUpdate, SsoUserResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class SsoUserService:
    """
    用户账号信息服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SsoUserCreate) -> SsoUserResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = SsoUser(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return SsoUserResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(SsoUser)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [SsoUserResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> SsoUserResponse:
        obj = self.db.query(SsoUser).filter(
            SsoUser.auto_id == auto_id
        ).first()

        if not obj:
            raise NotFoundException("用户不存在")

        return SsoUserResponse.model_validate(obj)

    def update(self, auto_id: int, data: SsoUserUpdate) -> SsoUserResponse:
        obj = self.db.query(SsoUser).filter(
            SsoUser.auto_id == auto_id
        ).first()

        if not obj:
            raise NotFoundException("用户不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return SsoUserResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(SsoUser).filter(
            SsoUser.auto_id == auto_id
        ).first()

        if not obj:
            raise NotFoundException("用户不存在")

        self.db.delete(obj)
        self.db.commit()