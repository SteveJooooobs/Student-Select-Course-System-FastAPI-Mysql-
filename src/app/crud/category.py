from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate

def get_category(db: Session, category_id: int):
    """根据 ID 查询单个分类"""
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    """根据名称查询分类（用于检查是否重名）"""
    return db.query(Category).filter(Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """查询分类列表，支持分页"""
    return db.query(Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: CategoryCreate):
    """创建新分类"""
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)  # 刷新以获取数据库生成的 id
    return db_category

def update_category(db: Session, category_id: int, name: str):
    """更新分类名称"""
    db_category = get_category(db, category_id)
    if db_category:
        db_category.name = name
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    """删除分类"""
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False