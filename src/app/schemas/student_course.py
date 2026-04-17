from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StudentCourseBase(BaseModel):
    """选课关系基础字段"""
    student_id: int
    course_id: int


class StudentCourseCreate(StudentCourseBase):
    """创建选课关系时的请求体"""
    pass


class StudentCourseResponse(StudentCourseBase):
    """选课关系响应体"""
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)