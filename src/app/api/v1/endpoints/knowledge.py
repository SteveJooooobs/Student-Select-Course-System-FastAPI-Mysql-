from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.KnowledgeResponse, status_code=status.HTTP_201_CREATED)
def create_knowledge(
        *,
        db: Session = Depends(get_db),
        knowledge_in: schemas.KnowledgeCreate,
):
    """创建新知识条目"""
    # 检查分类是否存在
    category = crud.get_category(db, category_id=knowledge_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="指定的分类不存在",
        )
    return crud.create_knowledge(db, knowledge=knowledge_in)


@router.get("/", response_model=List[schemas.KnowledgeResponse])
def read_knowledge_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
):
    """获取知识列表（支持分页和按分类筛选）"""
    return crud.get_knowledge_list(db, skip=skip, limit=limit, category_id=category_id)


@router.get("/{knowledge_id}", response_model=schemas.KnowledgeResponse)
def read_knowledge(
        knowledge_id: int,
        db: Session = Depends(get_db),
):
    """根据 ID 获取单条知识"""
    knowledge = crud.get_knowledge(db, knowledge_id=knowledge_id)
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识条目不存在",
        )
    return knowledge


@router.put("/{knowledge_id}", response_model=schemas.KnowledgeResponse)
def update_knowledge(
        knowledge_id: int,
        knowledge_in: schemas.KnowledgeUpdate,
        db: Session = Depends(get_db),
):
    """更新知识条目（支持部分更新）"""
    # 检查知识是否存在
    knowledge = crud.get_knowledge(db, knowledge_id=knowledge_id)
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识条目不存在",
        )

    # 如果要更新分类，检查新分类是否存在
    if knowledge_in.category_id is not None:
        category = crud.get_category(db, category_id=knowledge_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="指定的分类不存在",
            )

    return crud.update_knowledge(db, knowledge_id=knowledge_id, knowledge=knowledge_in)


@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(
        knowledge_id: int,
        db: Session = Depends(get_db),
):
    """删除知识条目"""
    # 检查知识是否存在
    knowledge = crud.get_knowledge(db, knowledge_id=knowledge_id)
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识条目不存在",
        )

    crud.delete_knowledge(db, knowledge_id=knowledge_id)
    return None