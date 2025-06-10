from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    __tablename__ = "Users"  # 資料表名稱

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
