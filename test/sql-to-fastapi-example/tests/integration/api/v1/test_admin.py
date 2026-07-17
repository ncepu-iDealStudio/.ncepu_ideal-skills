"""
管理员接口集成测试（直连真实 MySQL）

路径：/api/v1/admin
说明：
- 主键字段：auto_id（类型 int）
- DELETE 为软删除（is_delete=True/1），记录仍留在表中，详情应 404。

【覆盖策略】文件已存在则 skill 跳过（人手维护）。
"""

import uuid

import httpx
import pytest
from sqlalchemy import select

from core import database
from models.admin import Admin



async def _db_row(pk: int) -> Admin | None:
    async with database.AsyncSessionLocal() as s:
        return (
            await s.execute(
                select(Admin).where(Admin.auto_id == pk)
            )
        ).scalar_one_or_none()


@pytest.mark.asyncio
async def test_admin_crud_flow(app):
    """基础 CRUD 集成测试（真实 MySQL）"""
    transport = httpx.ASGITransport(app=app)
    headers = {"Authorization": "Bearer test-token"}
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            
            "admin_id": 1,
            
            "user_id": ("t_" + uuid.uuid4().hex)[:22],
            
            "department_id": 1,
            
            "name": "测试姓名",
            
            "email": f"u_{uuid.uuid4().hex[:8]}@example.com",
            
            "phone": "13800138000",
            
            "office_address": ("t_" + uuid.uuid4().hex)[:255],
            
        }

        # 1) 创建
        resp = await client.post("/api/v1/admin", json=payload, headers=headers)
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["code"] == "SUCCESS"
        data = body["data"]
        pk = data["auto_id"]

        row = await _db_row(pk)
        assert row is not None, "创建后未在真实 admin 表中找到记录"
        
        assert row.is_delete in (False, 0)
        

        # 2) 列表
        resp = await client.get(
            "/api/v1/admin",
            params={"page": 1, "page_size": 10},
            headers=headers,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["data"]["total"] >= 1

        # 3) 详情
        resp = await client.get(f"/api/v1/admin/{pk}", headers=headers)
        assert resp.status_code == 200, resp.text

        # 4) 更新（不含状态/标识位字段）
        update_payload = {
            
            "user_id": "Skill更新",
            
            "name": "Skill更新",
            
        }
        resp = await client.put(
            f"/api/v1/admin/{pk}",
            json=update_payload,
            headers=headers,
        )
        assert resp.status_code == 200, resp.text

        

        # 删除
        resp = await client.delete(f"/api/v1/admin/{pk}", headers=headers)
        assert resp.status_code == 200, resp.text

        resp = await client.get(f"/api/v1/admin/{pk}", headers=headers)
        assert resp.status_code == 404, resp.text

        row = await _db_row(pk)
        
        assert row is not None, "软删除后记录应仍留在 admin 表中"
        assert row.is_delete in (True, 1)
        


@pytest.mark.asyncio
@pytest.mark.skip(reason="占位：补齐商业逻辑接口测试后移除 skip")
async def test_admin_business_api_placeholder(app):
    """占位：商业逻辑接口集成测试"""
    transport = httpx.ASGITransport(app=app)
    headers = {"Authorization": "Bearer test-token"}
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        assert False, "请实现商业逻辑接口集成测试"