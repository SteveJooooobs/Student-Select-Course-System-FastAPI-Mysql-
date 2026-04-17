from pydantic import BaseModel, ConfigDict



class CategoryBase(BaseModel):
    """分类的基础字段"""
    name: str

class CategoryCreate(CategoryBase):
    """创建分类时的请求体，字段与 Base 相同"""
    pass

class CategoryResponse(CategoryBase):
    """分类的响应体，包含数据库生成的 id"""
    id: int

    # Pydantic V2 配置：允许从 ORM 对象自动转换
    model_config = ConfigDict(from_attributes=True)