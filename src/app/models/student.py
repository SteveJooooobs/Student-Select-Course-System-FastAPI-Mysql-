from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(11), nullable=False, unique=True, comment="学号，11位字符串")
    name = Column(String(100), nullable=False, comment="学生姓名")
    course_ids = Column(Text, default="", comment="冗余字段：逗号分隔的已选课程ID")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 多对多关系
    courses = relationship(
        "Course",
        secondary="student_courses",
        back_populates="students"
    )