from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 存储用户偏好，例如: {"allergies": ["花生"], "dislikes": ["香菜"], "cuisine_style": "川菜"}
    # SQLite 本身没有 JSON 类型，SQLAlchemy 会自动处理文本和 JSON 的转换 (部分支持)
    # 对于简单的 SQLite，有时作为一个 Text 存储更保险，但 SQLAlchemy 的 JSON 类型通常能很好工作。
    preferences = Column(JSON, default={})

    favorites = relationship("UserFavorite", back_populates="user")

class UserFavorite(Base):
    __tablename__ = "user_favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(String, index=True) # 对应 ChromaDB 中的 ID
    recipe_name = Column(String)           # 冗余存储，方便展示
    saved_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
