# 从子模块导入 Schema 类，方便其他地方统一导入
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate, KnowledgeResponse