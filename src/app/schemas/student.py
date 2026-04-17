from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.schemas.course import CourseSimple


class StudentBase(BaseModel):
    student_number: str = Field(..., max_length=11, description="学号")
    name: str = Field(..., max_length=100, description="学生姓名")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    student_number: Optional[str] = Field(None, max_length=11)
    name: Optional[str] = Field(None, max_length=100)


class StudentResponse(StudentBase):
    id: int
    course_ids: str = Field(default="", description="已选课程ID，逗号分隔")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentSimple(BaseModel):
    id: int
    student_number: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class StudentWithCourses(StudentResponse):
    courses: List["CourseSimple"] = Field(default=[], description="已选课程列表")

