from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.StudentCourseResponse, status_code=status.HTTP_201_CREATED)
def add_course(
        *,
        db: Session = Depends(get_db),
        relation_in: schemas.StudentCourseCreate,
):
    """学生选课"""
    student = crud.get_student(db, student_id=relation_in.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )

    course = crud.get_course(db, course_id=relation_in.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )

    result = crud.add_course_to_student(db, relation=relation_in)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该学生已选此课程",
        )
    return result


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def remove_course(
        *,
        db: Session = Depends(get_db),
        student_id: int,
        course_id: int,
):
    """学生退课"""
    student = crud.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )

    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )

    result = crud.remove_course_from_student(db, student_id=student_id, course_id=course_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="选课记录不存在",
        )
    return None


@router.get("/students/{student_id}/courses", response_model=List[schemas.CourseResponse])
def read_student_courses(
        student_id: int,
        db: Session = Depends(get_db),
):
    """获取某学生的所有已选课程"""
    student = crud.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )
    return crud.get_courses_by_student(db, student_id=student_id)


@router.get("/courses/{course_id}/students", response_model=List[schemas.StudentResponse])
def read_course_students(
        course_id: int,
        db: Session = Depends(get_db),
):
    """获取某课程的所有选课学生"""
    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )
    return crud.get_students_by_course(db, course_id=course_id)