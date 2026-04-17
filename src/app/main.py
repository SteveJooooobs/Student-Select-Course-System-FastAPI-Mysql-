# FastAPI 应用入口
from fastapi import FastAPI

# 导入数据库引擎和基类
from app.db.session import engine
from app.db.base import Base

# 导入所有模型（必须导入，否则 Base 不知道有哪些表需要创建）
from app.models import Category, Knowledge

# 导入 API 路由
from app.api.v1.api import router as api_v1_router

# 创建 FastAPI 应用实例
app = FastAPI(
    title="学生选课系统 API",
    description="FastAPI + SQLAlchemy 学生选课系统作业项目",
    version="0.1.0"
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 注册 API 路由，所有接口统一加 /api/v1 前缀
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def root():
    """测试服务是否正常运行"""
    return {"message": "选课系统 API 服务运行中", "status": "ok"}


@app.get("/health")
def health_check():
    """健康检查端点"""
    return {"status": "healthy"}