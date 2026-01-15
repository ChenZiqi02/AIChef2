from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from core.config import ROOT_DIR

# 数据库文件路径
DB_PATH = os.path.join(ROOT_DIR, "data", "users.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 创建引擎
# check_same_thread=False 是 SQLite 必须的，允许多线程访问
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建 SessionLocal 类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类，供模型继承
Base = declarative_base()

# 依赖项 (Dependency) - 用于 FastAPI 注入数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
