
```markdown
# FastAPI 数据流向图

## 请求阶段（创建学生）


 客户端 JSON
     ↓
 路由层：接收 POST 请求
     ↓
 Schema层：FastAPI 自动将 JSON 转为 StudentCreate 对象
     ↓
 CRUD层：从 StudentCreate 取值，创建 Student (ORM) 对象
     ↓
 Model层：SQLAlchemy 将 ORM 对象转为 SQL 语句
     ↓
 数据库：执行 INSERT，存储数据

```

```markdown
## 响应阶段

数据库：返回刚插入的记录
    ↓
Model层：SQLAlchemy 封装为 Student (ORM) 对象
    ↓
CRUD层：返回 ORM 对象给路由层
    ↓
Schema层：FastAPI 自动将 ORM 对象转为 StudentResponse
    ↓
客户端：收到 JSON 响应
```

```markdown
- ## 类型转换点

请求进入：JSON -> StudentCreate (FastAPI 自动)
业务处理：StudentCreate -> Student (手动)
数据库操作：Student -> SQL (SQLAlchemy 自动)
响应返回：Student -> StudentResponse (FastAPI 自动)
最终输出：StudentResponse -> JSON (FastAPI 自动)
```

```markdown
## 各模块做什么

api/endpoints/：接收 HTTP 请求，返回响应
schemas/：定义请求和响应的数据格式
crud/：执行数据库增删改查
models/：定义数据库表结构
db/session.py：管理数据库连接
```
