"""
学院信息业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.sys_college_info import SysCollegeInfo
from schemas.sys_college_info import SysCollegeInfoCreate, SysCollegeInfoUpdate, SysCollegeInfoResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class SysCollegeInfoService:
    """
    学院信息服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SysCollegeInfoCreate) -> SysCollegeInfoResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = SysCollegeInfo(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return SysCollegeInfoResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(SysCollegeInfo).filter(SysCollegeInfo.is_delete == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [SysCollegeInfoResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> SysCollegeInfoResponse:
        obj = self.db.query(SysCollegeInfo).filter(
            SysCollegeInfo.auto_id == auto_id,
            SysCollegeInfo.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学院不存在")

        return SysCollegeInfoResponse.model_validate(obj)

    def update(self, auto_id: int, data: SysCollegeInfoUpdate) -> SysCollegeInfoResponse:
        obj = self.db.query(SysCollegeInfo).filter(
            SysCollegeInfo.auto_id == auto_id,
            SysCollegeInfo.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学院不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return SysCollegeInfoResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(SysCollegeInfo).filter(
            SysCollegeInfo.auto_id == auto_id,
            SysCollegeInfo.is_delete == False
        ).first()

        if not obj:
            raise NotFoundException("学院不存在")

        setattr(obj, "is_delete", True)
        self.db.commit()