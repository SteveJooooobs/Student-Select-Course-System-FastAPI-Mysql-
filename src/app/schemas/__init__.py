from app.schemas.student import (
    StudentBase,
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentSimple,
    StudentWithCourses,
)
from app.schemas.course import (
    CourseBase,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseSimple,
    CourseWithStudents,
)
from app.schemas.student_course import (
    StudentCourseBase,
    StudentCourseCreate,
    StudentCourseResponse,
)

# 在所有类导入完成后，重建有循环引用的模型
StudentWithCourses.model_rebuild()
CourseWithStudents.model_rebuild()