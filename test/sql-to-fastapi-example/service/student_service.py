"""
学生基本信息业务服务（Service）

【HAND-WRITTEN】业务逻辑写在本文件；skill 仅在文件不存在时生成一次，之后不再覆盖。

约定：
- API/Resource 层统一只依赖本 Service，不直接调用 Repository。
- Repository 仅提供单条 CRUD：create / get / update / delete。
- 列表分页、过滤、状态变更、跨表流程等均视为业务逻辑，写在本层。
"""

from typing import Any, Dict, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.student import Student
from repository.student_repository import StudentRepository
from schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    
)


class StudentService:
    """
    学生基本信息业务服务

    - 单条 CRUD：委托 Repository.create / get / update / delete
    - 列表及其他业务：在本类实现
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = StudentRepository(db)

    # -------------------- 单条 CRUD（委托 Repository）--------------------

    async def create(self, data: StudentCreate) -> StudentResponse:
        """创建学生基本信息"""
        obj = await self.repo.create(data)
        return StudentResponse.model_validate(obj)

    async def get_detail(self, auto_id: int) -> StudentResponse:
        """详情（单条）"""
        obj = await self.repo.get(auto_id)
        return StudentResponse.model_validate(obj)

    async def update(
        self,
        auto_id: int,
        data: StudentUpdate,
    ) -> StudentResponse:
        """更新（不含状态/标识位字段；状态请用 update_status）"""
        obj = await self.repo.update(auto_id, data)
        return StudentResponse.model_validate(obj)

    async def delete(self, auto_id: int) -> None:
        """删除"""
        await self.repo.delete(auto_id)

    # -------------------- 业务逻辑：列表 --------------------

    async def get_list(
        self,
        page: int = 1,
        size: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """分页列表（业务逻辑：分页 / 过滤 / 排除软删除）"""
        
        conditions = [Student.is_delete == False]  # noqa: E712
        
        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(Student, field):
                    conditions.append(getattr(Student, field) == value)

        stmt = select(Student).order_by(Student.auto_id.asc())
        count_stmt = select(func.count()).select_from(Student)
        for cond in conditions:
            stmt = stmt.where(cond)
            count_stmt = count_stmt.where(cond)

        total = await self.db.scalar(count_stmt) or 0
        offset = (page - 1) * size
        rows = (await self.db.execute(stmt.offset(offset).limit(size))).scalars().all()
        return {
            "items": [StudentResponse.model_validate(item) for item in rows],
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size if size else 0,
        }

    

    # ---------- 在下方添加商业逻辑方法 ----------
    # 示例：
    # async def transfer_department(
    #     self,
    #     auto_id: int,
    #     new_department_id: int,
    # ) -> StudentResponse:
    #     obj = await self.repo.get(auto_id)
    #     # ... 业务规则 / 跨表操作 ...
    #     return StudentResponse.model_validate(obj)