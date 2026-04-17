"""
CRUD 函数速查表

学生管理
get_student(db, student_id)                       → 根据主键 ID 查学生
get_student_by_number(db, student_number)         → 根据学号查学生
get_students(db, skip, limit, name)               → 查学生列表
create_student(db, student)                       → 创建学生
update_student(db, student_id, student_update)    → 更新学生
delete_student(db, student_id)                    → 删除学生

课程管理
get_course(db, course_id)                         → 根据主键 ID 查课程
get_course_by_name(db, name)                      → 根据名称查课程
get_courses(db, skip, limit, name)                → 查课程列表
create_course(db, course)                         → 创建课程
update_course(db, course_id, course_update)       → 更新课程
delete_course(db, course_id)                      → 删除课程

选课管理
add_course_to_student(db, relation)               → 学生选课
remove_course_from_student(db, student_id, course_id) → 学生退课
get_students_by_course(db, course_id)             → 获取课程的所有学生对象
get_courses_by_student(db, student_id)            → 获取学生的所有课程对象
"""

from app.crud.student import (
    get_student,
    get_student_by_number,
    get_students,
    create_student,
    update_student,
    delete_student,
)

from app.crud.course import (
    get_course,
    get_course_by_name,
    get_courses,
    create_course,
    update_course,
    delete_course,
)

from app.crud.student_course import (
    add_course_to_student,
    remove_course_from_student,
    get_students_by_course,
    get_courses_by_student,
)