from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
        *,
        db: Session = Depends(get_db),
        course_in: schemas.CourseCreate,
):
    """创建新课程"""
    existing = crud.get_course_by_name(db, name=course_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="课程名称已存在",
        )
    return crud.create_course(db, course=course_in)


@router.get("/", response_model=List[schemas.CourseResponse])
def read_courses(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
):
    """获取课程列表（支持分页和名称搜索）"""
    return crud.get_courses(db, skip=skip, limit=limit, name=name)


@router.get("/{course_id}", response_model=schemas.CourseWithStudents)
def read_course(
        course_id: int,
        db: Session = Depends(get_db),
):
    """根据 ID 获取单个课程（包含已选课学生详情）"""
    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )

    students = crud.get_students_by_course(db, course_id=course_id)
    course_dict = schemas.CourseResponse.model_validate(course).model_dump()
    course_dict["students"] = students
    return course_dict


@router.put("/{course_id}", response_model=schemas.CourseResponse)
def update_course(
        course_id: int,
        course_in: schemas.CourseUpdate,
        db: Session = Depends(get_db),
):
    """更新课程信息（支持部分更新）"""
    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )

    if course_in.name is not None:
        existing = crud.get_course_by_name(db, name=course_in.name)
        if existing and existing.id != course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="课程名称已被其他课程使用",
            )

    return crud.update_course(db, course_id=course_id, course_update=course_in)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
        course_id: int,
        db: Session = Depends(get_db),
):
    """删除课程"""
    course = crud.get_course(db, course_id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )

    crud.delete_course(db, course_id=course_id)
    return None