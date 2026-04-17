from sqlalchemy.orm import Session
from app.models.student import Knowledge
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate


def get_knowledge(db: Session, knowledge_id: int):
    """根据 ID 查询单条知识"""
    return db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()


def get_knowledge_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category_id: int = None
):
    """查询知识列表，支持分页和按分类筛选"""
    query = db.query(Knowledge)
    if category_id is not None:
        query = query.filter(Knowledge.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def create_knowledge(db: Session, knowledge: KnowledgeCreate):
    """创建新知识条目"""
    db_knowledge = Knowledge(
        title=knowledge.title,
        content=knowledge.content,
        category_id=knowledge.category_id,
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


def update_knowledge(db: Session, knowledge_id: int, knowledge: KnowledgeUpdate):
    """更新知识条目（只更新传入的字段）"""
    db_knowledge = get_knowledge(db, knowledge_id)
    if not db_knowledge:
        return None

    # model_dump(exclude_unset=True) 只包含客户端实际传入的字段
    update_data = knowledge.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_knowledge, field, value)

    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


def delete_knowledge(db: Session, knowledge_id: int):
    """删除知识条目"""
    db_knowledge = get_knowledge(db, knowledge_id)
    if db_knowledge:
        db.delete(db_knowledge)
        db.commit()
        return True
    return False