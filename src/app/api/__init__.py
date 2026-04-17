# API 包初始化文件

"""
API 端点速查表
==============

分类管理 (Categories) - 前缀: /api/v1/categories
-----------------------------------------------
POST   /                     创建分类
GET    /                     获取分类列表（支持 skip, limit 分页）
GET    /{category_id}        根据 ID 获取单个分类
PUT    /{category_id}        更新分类名称
DELETE /{category_id}        删除分类

知识管理 (Knowledge) - 前缀: /api/v1/knowledge
----------------------------------------------
POST   /                     创建知识条目
GET    /                     获取知识列表（支持 skip, limit, category_id 筛选）
GET    /{knowledge_id}       根据 ID 获取单条知识
PUT    /{knowledge_id}       更新知识（支持部分更新）
DELETE /{knowledge_id}       删除知识


请求体示例
==========

创建分类 (POST /api/v1/categories)
{
    "name": "技术文档"
}

创建知识 (POST /api/v1/knowledge)
{
    "title": "FastAPI 入门",
    "content": "FastAPI 是一个现代 Web 框架...",
    "category_id": 1
}

更新知识 (PUT /api/v1/knowledge/1)
{
    "title": "新标题",
    "content": "新内容"
}
注意：更新接口所有字段都是可选的，只传需要更新的字段即可
"""