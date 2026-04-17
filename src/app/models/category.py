from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Category(Base):
    """
    分类表模型
    只有单级分类，不涉及父子层级
    """
    __tablename__ = 'categories'

    # 主键，自增整数
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 分类名称，最长100字符，不允许为空，必须唯一
    name = Column(String(100), nullable=False, unique=True)