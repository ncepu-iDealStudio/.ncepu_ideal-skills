"""
用户账号信息数据模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from datetime import datetime
from sqlalchemy import Column, String, BigInteger, Integer, Boolean, DateTime
from models import Base


class SsoUser(Base):
    """
    用户账号信息
    """
    __tablename__ = "sso_user"

    auto_id = Column("autoID", BigInteger, primary_key=True, nullable=False)
    user_id = Column("userID", String(22), nullable=True, comment="用户ID")
    account = Column("account", String(255), nullable=True, comment="登录账号-默认为手机号")
    password = Column("password", String(255), nullable=True, comment="密码")
    user_type = Column("userType", Integer, nullable=True, comment="账号类型：1--学生；2--老师；3--管理人员")
    status = Column("status", Integer, nullable=True, comment="账号的状态：1--可用；0--锁定")
    add_time = Column("addTime", DateTime, default=datetime.now, nullable=True, comment="记录添加时间")

    @property
    def masked_password(self) -> str:
        return "******"

    @property
    def masked_phone(self) -> str:
        if self.account and len(self.account) >= 11:
            return f"{self.account[:3]}****{self.account[-4:]}"
        return "****"