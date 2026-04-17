from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
        *,
        db: Session = Depends(get_db),
        student_in: schemas.StudentCreate,
):
    """创建新学生"""
    existing = crud.get_student_by_number(db, student_number=student_in.student_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="学号已存在",
        )
    return crud.create_student(db, student=student_in)


@router.get("/", response_model=List[schemas.StudentResponse])
def read_students(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
):
    """获取学生列表"""
    return crud.get_students(db, skip=skip, limit=limit, name=name)


@router.get("/{student_id}", response_model=schemas.StudentWithCourses)
def read_student(
        student_id: int,
        db: Session = Depends(get_db),
):
    """根据 ID 获取单个学生"""
    student = crud.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )

    courses = crud.get_courses_by_student(db, student_id=student_id)
    student_dict = schemas.StudentResponse.model_validate(student).model_dump()
    student_dict["courses"] = courses
    return student_dict


@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
        student_id: int,
        student_in: schemas.StudentUpdate,
        db: Session = Depends(get_db),
):
    """更新学生信息"""
    student = crud.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )

    if student_in.student_number is not None:
        existing = crud.get_student_by_number(db, student_number=student_in.student_number)
        if existing and existing.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学号已被其他学生使用",
            )

    return crud.update_student(db, student_id=student_id, student_update=student_in)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
        student_id: int,
        db: Session = Depends(get_db),
):
    """删除学生"""
    student = crud.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在",
        )

    crud.delete_student(db, student_id=student_id)
    return None