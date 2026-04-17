from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func

from app.db.base import Base

class Knowledge(Base):
    """
    知识条目表模型
    每条知识必须属于一个分类
    """
    __tablename__ = 'knowledge'

    # 主键，自增整数
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 标题，最长200字符，不允许为空
    title = Column(String(200), nullable=False)
    # 内容，使用 Text 类型存储长文本，不允许为空
    content = Column(Text, nullable=False)
    # 外键，关联到 categories 表的 id 字段
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    # 创建时间，使用数据库服务器的当前时间作为默认值
    created_at = Column(DateTime, server_default=func.now())
    # 更新时间，使用数据库服务器的当前时间，且每次更新记录时自动更新
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())