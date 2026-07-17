"""
教研室与研究所部门信息业务服务（Service）

【HAND-WRITTEN】业务逻辑写在本文件；skill 仅在文件不存在时生成一次，之后不再覆盖。

约定：
- API/Resource 层统一只依赖本 Service，不直接调用 Repository。
- Repository 仅提供单条 CRUD：create / get / update / delete。
- 列表分页、过滤、状态变更、跨表流程等均视为业务逻辑，写在本层。
"""

from typing import Any, Dict, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.sys_department import SysDepartment
from repository.sys_department_repository import SysDepartmentRepository
from schemas.sys_department import (
    SysDepartmentCreate,
    SysDepartmentUpdate,
    SysDepartmentResponse,
    
)


class SysDepartmentService:
    """
    教研室与研究所部门信息业务服务

    - 单条 CRUD：委托 Repository.create / get / update / delete
    - 列表及其他业务：在本类实现
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SysDepartmentRepository(db)

    # -------------------- 单条 CRUD（委托 Repository）--------------------

    async def create(self, data: SysDepartmentCreate) -> SysDepartmentResponse:
        """创建教研室与研究所部门信息"""
        obj = await self.repo.create(data)
        return SysDepartmentResponse.model_validate(obj)

    async def get_detail(self, department_id: int) -> SysDepartmentResponse:
        """详情（单条）"""
        obj = await self.repo.get(department_id)
        return SysDepartmentResponse.model_validate(obj)

    async def update(
        self,
        department_id: int,
        data: SysDepartmentUpdate,
    ) -> SysDepartmentResponse:
        """更新（不含状态/标识位字段；状态请用 update_status）"""
        obj = await self.repo.update(department_id, data)
        return SysDepartmentResponse.model_validate(obj)

    async def delete(self, department_id: int) -> None:
        """删除"""
        await self.repo.delete(department_id)

    # -------------------- 业务逻辑：列表 --------------------

    async def get_list(
        self,
        page: int = 1,
        size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """分页列表（业务逻辑：分页 / 过滤 / 排除软删除）"""
        
        conditions = [SysDepartment.is_delete == False]  # noqa: E712
        
        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(SysDepartment, field):
                    conditions.append(getattr(SysDepartment, field) == value)

        stmt = select(SysDepartment).order_by(SysDepartment.department_id.asc())
        count_stmt = select(func.count()).select_from(SysDepartment)
        for cond in conditions:
            stmt = stmt.where(cond)
            count_stmt = count_stmt.where(cond)

        total = await self.db.scalar(count_stmt) or 0
        offset = (page - 1) * size
        rows = (await self.db.execute(stmt.offset(offset).limit(size))).scalars().all()
        return {
            "items": [SysDepartmentResponse.model_validate(item) for item in rows],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size else 0,
        }

    

    # ---------- 在下方添加商业逻辑方法 ----------
    # 示例：
    # async def transfer_department(
    #     self,
    #     department_id: int,
    #     new_department_id: int,
    # ) -> SysDepartmentResponse:
    #     obj = await self.repo.get(department_id)
    #     # ... 业务规则 / 跨表操作 ...
    #     return SysDepartmentResponse.model_validate(obj)