"""
CRUD 函数速查表
===============

分类 (Category)
---------------
get_category(db, category_id)          → 根据 ID 查单个分类
get_category_by_name(db, name)         → 根据名称查分类（重名检查）
get_categories(db, skip, limit)        → 查分类列表（分页）
create_category(db, category)          → 创建分类
update_category(db, category_id, name) → 更新分类名称
delete_category(db, category_id)       → 删除分类，返回 True/False

知识 (Knowledge)
----------------
get_knowledge(db, knowledge_id)        → 根据 ID 查单条知识
get_knowledge_list(db, skip, limit, category_id) → 查知识列表（分页+筛选）
create_knowledge(db, knowledge)        → 创建知识
update_knowledge(db, knowledge_id, knowledge) → 更新知识（部分更新）
delete_knowledge(db, knowledge_id)     → 删除知识，返回 True/False
"""


# 从子模块导入 CRUD 函数，方便其他地方统一导入
from app.crud.category import (
    get_category,
    get_category_by_name,
    get_categories,
    create_category,
    update_category,
    delete_category,
)

from app.crud.knowledge import (
    get_knowledge,
    get_knowledge_list,
    create_knowledge,
    update_knowledge,
    delete_knowledge,
)