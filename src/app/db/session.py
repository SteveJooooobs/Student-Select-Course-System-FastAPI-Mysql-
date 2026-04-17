from sqlalchemy import create_engine  # 创建数据库引擎，负责连接池管理
from sqlalchemy.orm import sessionmaker  # 创建会话工厂，用于生成数据库会话
from src.app.core.config import settings

# ========== 创建数据库引擎 ==========
# create_engine 负责维护数据库连接池
engine = create_engine(
    settings.DATABASE_URL,
    echo = True,
    pool_pre_ping=True,
)

# ========== 创建会话工厂 ==========
# sessionmaker 是一个工厂函数，用来生成数据库会话对象
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ========== 依赖注入函数 ==========
def get_db():
    """
        FastAPI 依赖注入函数
        每个请求会调用这个函数，获取一个数据库会话
        请求结束后自动关闭会话，归还连接到连接池
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()