"""
用户账号信息（登录中心）数据访问层（Repository）

【AUTO-GENERATED】由 sql-to-fastapi-restfulapi-scaffold 生成，可被 skill 覆盖。
禁止在此文件编写业务规则。
Resource/API 层不要直接依赖本 Repository。

职责边界（强制）：
- 本层只做「单表、单条记录」的基础 CRUD，方法名固定为：
  create / get / update / delete
- 列表分页、过滤、状态变更、跨表流程等一律视为业务逻辑，写在 Service。
"""

from typing import Any, Dict, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.sso_user import SsoUser
from schemas.sso_user import SsoUserCreate, SsoUserUpdate
from utils.custom_exceptions import NotFoundException


class SsoUserRepository:
    """
    用户账号信息（登录中心）仓储：仅负责单表单条记录的 CRUD
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: SsoUserCreate) -> SsoUser:
        """插入一条记录并提交"""
        obj = SsoUser(**data.model_dump())
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def get(self, auto_id: int) -> SsoUser:
        """按主键获取一条（软删除视为不存在）"""
        
        obj = await self.db.scalar(
            select(SsoUser).where(
                SsoUser.auto_id == auto_id
            )
        )
        
        if not obj:
            raise NotFoundException("用户账号信息（登录中心）不存在")
        return obj

    async def update(
        self,
        auto_id: int,
        data: Union[SsoUserUpdate, Dict[str, Any]],
    ) -> SsoUser:
        """按主键更新一条记录（仅更新传入字段）"""
        if hasattr(data, "model_dump"):
            fields = data.model_dump(exclude_unset=True)
        else:
            fields = data
        obj = await self.get(auto_id)
        for key, value in fields.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, auto_id: int) -> None:
        """删除一条：有软删字段则软删，否则硬删"""
        obj = await self.get(auto_id)
        
        await self.db.delete(obj)
        await self.db.commit()
        