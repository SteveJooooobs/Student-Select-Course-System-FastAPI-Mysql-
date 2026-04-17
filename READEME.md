```markdown
# 学生选课系统 API

基于 FastAPI + SQLAlchemy + Pydantic V2 的学生选课管理系统，支持学生、课程的增删改查以及选课/退课功能。

## 技术栈

- Python 3.11
- FastAPI 0.115+
- SQLAlchemy 2.0+
- Pydantic V2
- MySQL
- PyMySQL

## 功能特性

- 学生管理：学号、姓名，支持分页和姓名搜索
- 课程管理：名称、描述，支持分页和名称搜索
- 选课管理：学生选课/退课，查询学生的课程、课程的学生
- 冗余字段优化：学生表存储已选课程ID，提升查询性能
- 自动生成 Swagger API 文档

## 项目结构
```
```markdown
src/app/
├── main.py                 # 应用入口
├── core/
│   ├── __init__.py
│   └── config.py           # 配置管理（Pydantic Settings）
├── db/
│   ├── __init__.py
│   ├── base.py             # ORM 基类
│   └── session.py          # 数据库连接和会话
├── models/
│   ├── __init__.py
│   ├── student.py          # 学生表模型
│   ├── course.py           # 课程表模型
│   └── student_course.py   # 中间表模型
├── schemas/
│   ├── __init__.py
│   ├── student.py          # 学生 Pydantic 模型
│   ├── course.py           # 课程 Pydantic 模型
│   └── student_course.py   # 选课 Pydantic 模型
├── crud/
│   ├── __init__.py
│   ├── student.py          # 学生 CRUD
│   ├── course.py           # 课程 CRUD
│   └── student_course.py   # 选课 CRUD
└── api/
    └── v1/
        ├── api.py          # 路由汇总
        └── endpoints/
            ├── student.py      # 学生接口
            ├── course.py       # 课程接口
            └── student_course.py # 选课接口
```
```

## 快速开始

### 1. 克隆项目

```bash
git clone <仓库地址>
cd course_select_api
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### 3. 安装依赖

```bash
pip install -e .
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env`，修改数据库配置：

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的密码
MYSQL_DATABASE=course_select
```

### 5. 创建数据库

```sql
CREATE DATABASE course_select CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. 启动服务

```bash
uvicorn app.main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看 Swagger 文档。

## API 接口

### 学生管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/students` | 创建学生 |
| GET | `/api/v1/students` | 学生列表（分页、姓名搜索） |
| GET | `/api/v1/students/{id}` | 单个学生（含已选课程） |
| PUT | `/api/v1/students/{id}` | 更新学生 |
| DELETE | `/api/v1/students/{id}` | 删除学生 |

### 课程管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/courses` | 创建课程 |
| GET | `/api/v1/courses` | 课程列表（分页、名称搜索） |
| GET | `/api/v1/courses/{id}` | 单个课程（含选课学生） |
| PUT | `/api/v1/courses/{id}` | 更新课程 |
| DELETE | `/api/v1/courses/{id}` | 删除课程 |

### 选课管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/student-courses` | 学生选课 |
| DELETE | `/api/v1/student-courses` | 学生退课 |
| GET | `/api/v1/student-courses/students/{id}/courses` | 学生的所有课程 |
| GET | `/api/v1/student-courses/courses/{id}/students` | 课程的所有学生 |

## 数据库设计

### 表关系

```
Student (学生)  ←──→  StudentCourse (中间表)  ←──→  Course (课程)
    1                          N:M                           1
```

### 冗余字段

- `Student.course_ids`：逗号分隔的课程ID，用于快速展示已选课程
- `Course.student_ids`：逗号分隔的学生ID，用于快速展示选课学生

选课/退课时自动同步更新。

## 测试示例

```bash
# 创建学生
curl -X POST http://127.0.0.1:8000/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{"student_number": "20240001", "name": "张三"}'

# 创建课程
curl -X POST http://127.0.0.1:8000/api/v1/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Python 程序设计", "description": "从入门到实践"}'

# 选课
curl -X POST http://127.0.0.1:8000/api/v1/student-courses \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "course_id": 1}'

# 查询学生的课程
curl http://127.0.0.1:8000/api/v1/student-courses/students/1/courses
```

## 常见问题

### Q: 启动报错 `Unknown database`
A: 需要在 MySQL 中先创建数据库。

### Q: `/docs` 打不开，报 `class-not-fully-defined`
A: 循环导入问题，确保 `schemas/__init__.py` 中有 `model_rebuild()` 调用。

### Q: 类型警告 `student_id` 类型不匹配
A: 数据库主键用 `id`，业务学号用 `student_number`。

## 许可证

MIT
```

