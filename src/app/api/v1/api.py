from fastapi import APIRouter
from app.api.v1.endpoints import student, course, student_course

router = APIRouter()

router.include_router(student.router, prefix="/students", tags=["学生管理"])
router.include_router(course.router, prefix="/courses", tags=["课程管理"])
router.include_router(student_course.router, prefix="/student-courses", tags=["选课管理"])