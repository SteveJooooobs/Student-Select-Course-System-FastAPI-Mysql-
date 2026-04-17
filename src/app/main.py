from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models import Student, Course, StudentCourse
from app.api.v1.api import router as api_v1_router

app = FastAPI(
    title="学生选课系统 API",
    description="FastAPI + SQLAlchemy 学生选课增删改查练手项目",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "学生选课系统 API 服务运行中", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}