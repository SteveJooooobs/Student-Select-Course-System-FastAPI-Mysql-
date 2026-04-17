from typing import Optional
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


def get_student(db: Session, student_id: int):
    """根据数据库主键 ID 查询学生"""
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_number(db: Session, student_number: str):
    """根据学号查询学生"""
    return db.query(Student).filter(Student.student_number == student_number).first()


def get_students(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
):
    """查询学生列表，支持分页和姓名模糊搜索"""
    query = db.query(Student)
    if name:
        query = query.filter(Student.name.contains(name))
    return query.offset(skip).limit(limit).all()


def create_student(db: Session, student: StudentCreate):
    """创建新学生"""
    db_student = Student(
        student_number=student.student_number,
        name=student.name,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student_update: StudentUpdate):
    """更新学生信息"""
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    update_data = student_update.model_dump(exclude_unset=True)

    # 如果更新了学号，字段名是 student_number
    if "student_number" in update_data:
        db_student.student_number = update_data["student_number"]
    if "name" in update_data:
        db_student.name = update_data["name"]

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    """删除学生"""
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False


def update_student_course_ids(db: Session, student_id: int, course_ids: str):
    """更新学生的 course_ids 冗余字段"""
    db_student = get_student(db, student_id)
    if db_student:
        db_student.course_ids = course_ids
        db.commit()
        db.refresh(db_student)
    return db_student