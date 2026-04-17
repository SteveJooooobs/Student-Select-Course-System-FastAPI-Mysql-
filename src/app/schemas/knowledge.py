from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class KnowledgeBase(BaseModel):
    """知识条目的基础字段"""
    title: str
    content: str
    category_id: int

class KnowledgeCreate(KnowledgeBase):
    """创建知识条目时的请求体"""
    pass

class KnowledgeUpdate(BaseModel):
    """更新知识条目时的请求体，所有字段都是可选的"""
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

class KnowledgeResponse(KnowledgeBase):
    """知识条目的响应体，包含数据库生成的字段"""
    id: int
    created_at: datetime
    updated_at: datetime

    # Pydantic V2 配置：允许从 ORM 对象自动转换
    model_config = ConfigDict(from_attributes=True)