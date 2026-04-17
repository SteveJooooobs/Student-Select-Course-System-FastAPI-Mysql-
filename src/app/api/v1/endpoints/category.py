from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
        *,
        db: Session = Depends(get_db),
        category_in: schemas.CategoryCreate,
):
    """创建新分类"""
    # 检查分类名是否已存在
    existing = crud.get_category_by_name(db, name=category_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="分类名称已存在",
        )
    return crud.create_category(db, category=category_in)


@router.get("/", response_model=List[schemas.CategoryResponse])
def read_categories(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    """获取分类列表（支持分页）"""
    return crud.get_categories(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def read_category(
        category_id: int,
        db: Session = Depends(get_db),
):
    """根据 ID 获取单个分类"""
    category = crud.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在",
        )
    return category


@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
        category_id: int,
        category_in: schemas.CategoryCreate,
        db: Session = Depends(get_db),
):
    """更新分类名称"""
    # 检查分类是否存在
    category = crud.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在",
        )

    # 检查新名称是否与其他分类冲突
    existing = crud.get_category_by_name(db, name=category_in.name)
    if existing and existing.id != category_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="分类名称已存在",
        )

    return crud.update_category(db, category_id=category_id, name=category_in.name)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
):
    """删除分类"""
    # 检查分类是否存在
    category = crud.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在",
        )

    crud.delete_category(db, category_id=category_id)
    return None