from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, comment="课程名称")
    description = Column(String(200), default="", comment="课程描述，最长200字符")
    student_ids = Column(Text, default="", comment="冗余字段：逗号分隔的已选课学生ID")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 多对多关系
    students = relationship(
        "Student",
        secondary="student_courses",
        back_populates="courses"
    )