from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.student import StudentSimple


class CourseBase(BaseModel):
    """课程基础字段"""
    name: str = Field(..., max_length=100, description="课程名称")
    description: Optional[str] = Field(None, max_length=200, description="课程描述")


class CourseCreate(CourseBase):
    """创建课程时的请求体"""
    pass


class CourseUpdate(BaseModel):
    """更新课程时的请求体，所有字段可选"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=200)


class CourseResponse(CourseBase):
    """课程响应体，包含数据库生成的字段"""
    id: int
    student_ids: str = Field(default="", description="已选课学生ID，逗号分隔")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseSimple(BaseModel):
    """课程简要信息（用于嵌套在学生响应中）"""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CourseWithStudents(CourseResponse):
    """带学生详情的响应体"""
    students: List["StudentSimple"] = Field(default=[], description="已选课学生列表")

