from fastapi import APIRouter
from app.api.v1.endpoints import category, knowledge

router = APIRouter()

# 注册分类路由，前缀为 /categories
router.include_router(
    category.router,
    prefix="/categories",
    tags=["分类管理"]
)

# 注册知识路由，前缀为 /knowledge
router.include_router(
    knowledge.router,
    prefix="/knowledge",
    tags=["知识管理"]
)