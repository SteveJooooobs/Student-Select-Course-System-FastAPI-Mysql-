from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int):
    """根据 ID 查询单个课程"""
    return db.query(Course).filter(Course.id == course_id).first()


def get_course_by_name(db: Session, name: str):
    """根据名称查询课程（用于检查课程名是否重复）"""
    return db.query(Course).filter(Course.name == name).first()


def get_courses(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
):
    """查询课程列表，支持分页和名称模糊搜索"""
    query = db.query(Course)
    if name:
        query = query.filter(Course.name.contains(name))
    return query.offset(skip).limit(limit).all()


def create_course(db: Session, course: CourseCreate):
    """创建新课程"""
    db_course = Course(
        name=course.name,
        description=course.description,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course_update: CourseUpdate):
    """更新课程信息（只更新传入的字段）"""
    db_course = get_course(db, course_id)
    if not db_course:
        return None

    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)

    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    """删除课程"""
    db_course = get_course(db, course_id)
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False


def update_course_student_ids(db: Session, course_id: int, student_ids: str):
    """更新课程的 student_ids 冗余字段（选课/退课时调用）"""
    db_course = get_course(db, course_id)
    if db_course:
        db_course.student_ids = student_ids
        db.commit()
        db.refresh(db_course)
    return db_course