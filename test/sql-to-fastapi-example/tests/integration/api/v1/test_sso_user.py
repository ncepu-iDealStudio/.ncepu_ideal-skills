"""
用户账号信息（登录中心）接口集成测试（直连真实 MySQL）

路径：/api/v1/sso-user
说明：
- 主键字段：auto_id（类型 int）
- 本表无软删字段，DELETE 为硬删除；删除后详情应 404，库中记录应不存在。
- 状态字段走 PATCH /{pk}/status；通用 PUT 不得携带状态字段（期望 422）。

【覆盖策略】文件已存在则 skill 跳过（人手维护）。
"""

import uuid

import httpx
import pytest
from sqlalchemy import select

from core import database
from models.sso_user import SsoUser



def _new_user_id() -> str:
    """生成测试用唯一 user_id，避免多次运行冲突"""
    
    value = f"skill_user_id_" + uuid.uuid4().hex[:8]
    
    return value[:22]
    
    



def _new_account() -> str:
    """生成测试用唯一 account，避免多次运行冲突"""
    
    value = f"skill_account_" + uuid.uuid4().hex[:8]
    
    return value[:255]
    
    



async def _db_row(pk: int) -> SsoUser | None:
    async with database.AsyncSessionLocal() as s:
        return (
            await s.execute(
                select(SsoUser).where(SsoUser.auto_id == pk)
            )
        ).scalar_one_or_none()


@pytest.mark.asyncio
async def test_sso_user_crud_flow(app):
    """基础 CRUD 集成测试（真实 MySQL）"""
    transport = httpx.ASGITransport(app=app)
    headers = {"Authorization": "Bearer test-token"}
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            
            "user_id": _new_user_id(),
            
            "account": _new_account(),
            
            "password": "TestPass123!",
            
            "user_type": 1,
            
            "status": 1,
            
        }

        # 1) 创建
        resp = await client.post("/api/v1/sso-user", json=payload, headers=headers)
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["code"] == "SUCCESS"
        data = body["data"]
        pk = data["auto_id"]

        row = await _db_row(pk)
        assert row is not None, "创建后未在真实 sso_user 表中找到记录"
        

        # 2) 列表
        resp = await client.get(
            "/api/v1/sso-user",
            params={"page": 1, "page_size": 10},
            headers=headers,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["data"]["total"] >= 1

        # 3) 详情
        resp = await client.get(f"/api/v1/sso-user/{pk}", headers=headers)
        assert resp.status_code == 200, resp.text

        try:
            # 4) 更新（不含状态/标识位字段；唯一字段用随机值避免冲突）
            update_payload = {
                "password": "UpdatedPass456!",
                "user_type": 2,
            }
            resp = await client.put(
                f"/api/v1/sso-user/{pk}",
                json=update_payload,
                headers=headers,
            )
            assert resp.status_code == 200, resp.text

            # 4b) PUT 携带状态字段应被 Schema 拒绝
            resp = await client.put(
                f"/api/v1/sso-user/{pk}",
                json={"status": 0},
                headers=headers,
            )
            assert resp.status_code == 422, resp.text

            # 5) 专用改状态
            resp = await client.patch(
                f"/api/v1/sso-user/{pk}/status",
                json={"status": 0},
                headers=headers,
            )
            assert resp.status_code == 200, resp.text
            assert resp.json()["data"]["status"] == 0

            resp = await client.patch(
                f"/api/v1/sso-user/{pk}/status",
                json={"status": 1},
                headers=headers,
            )
            assert resp.status_code == 200, resp.text
        finally:
            # 无论后续断言是否失败，尽量硬删除测试数据，避免残留
            await client.delete(f"/api/v1/sso-user/{pk}", headers=headers)

        resp = await client.get(f"/api/v1/sso-user/{pk}", headers=headers)
        assert resp.status_code == 404, resp.text

        row = await _db_row(pk)
        assert row is None, "硬删除后记录应不在 sso_user 表中"
        


@pytest.mark.asyncio
@pytest.mark.skip(reason="占位：补齐商业逻辑接口测试后移除 skip")
async def test_sso_user_business_api_placeholder(app):
    """占位：商业逻辑接口集成测试"""
    transport = httpx.ASGITransport(app=app)
    headers = {"Authorization": "Bearer test-token"}
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        assert False, "请实现商业逻辑接口集成测试"