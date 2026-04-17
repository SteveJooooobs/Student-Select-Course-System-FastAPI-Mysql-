from typing import List
from sqlalchemy.orm import Session
from app.models.student_course import StudentCourse
from app.models.student import Student
from app.models.course import Course
from app.schemas.student_course import StudentCourseCreate
from app.crud.student import update_student_course_ids, get_student
from app.crud.course import update_course_student_ids, get_course


def get_student_courses(db: Session, student_id: int):
    """查询某个学生已选的所有课程（返回课程ID列表）"""
    records = db.query(StudentCourse).filter(StudentCourse.student_id == student_id).all()
    return [record.course_id for record in records]


def get_course_students(db: Session, course_id: int):
    """查询某门课程的所有已选学生（返回学生ID列表）"""
    records = db.query(StudentCourse).filter(StudentCourse.course_id == course_id).all()
    return [record.student_id for record in records]


def add_course_to_student(db: Session, relation: StudentCourseCreate):
    """学生选课"""
    # 检查是否已选过
    existing = db.query(StudentCourse).filter(
        StudentCourse.student_id == relation.student_id,
        StudentCourse.course_id == relation.course_id,
    ).first()

    if existing:
        return None  # 已选过

    # 创建选课记录
    db_relation = StudentCourse(
        student_id=relation.student_id,
        course_id=relation.course_id,
    )
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)

    # 更新学生表的 course_ids 冗余字段
    _sync_student_course_ids(db, relation.student_id)
    # 更新课程表的 student_ids 冗余字段
    _sync_course_student_ids(db, relation.course_id)

    return db_relation


def remove_course_from_student(db: Session, student_id: int, course_id: int):
    """学生退课"""
    relation = db.query(StudentCourse).filter(
        StudentCourse.student_id == student_id,
        StudentCourse.course_id == course_id,
    ).first()

    if relation:
        db.delete(relation)
        db.commit()

        # 同步冗余字段
        _sync_student_course_ids(db, student_id)
        _sync_course_student_ids(db, course_id)
        return True
    return False


def get_students_by_course(db: Session, course_id: int):
    """获取某课程的所有选课学生（返回完整学生对象列表）"""
    student_ids = get_course_students(db, course_id)
    if not student_ids:
        return []
    return db.query(Student).filter(Student.id.in_(student_ids)).all()


def get_courses_by_student(db: Session, student_id: int):
    """获取某学生的所有已选课程（返回完整课程对象列表）"""
    course_ids = get_student_courses(db, student_id)
    if not course_ids:
        return []
    return db.query(Course).filter(Course.id.in_(course_ids)).all()


# ========== 内部辅助函数：同步冗余字段 ==========

def _sync_student_course_ids(db: Session, student_id: int):
    """同步学生表的 course_ids 字段"""
    course_ids = get_student_courses(db, student_id)
    course_ids_str = ",".join(str(cid) for cid in course_ids)
    update_student_course_ids(db, student_id, course_ids_str)


def _sync_course_student_ids(db: Session, course_id: int):
    """同步课程表的 student_ids 字段"""
    student_ids = get_course_students(db, course_id)
    student_ids_str = ",".join(str(sid) for sid in student_ids)
    update_course_student_ids(db, course_id, student_ids_str)