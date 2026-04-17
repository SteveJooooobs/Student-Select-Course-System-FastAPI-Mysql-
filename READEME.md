# FastAPI 知识库管理 Demo

## 🎯 项目目的
FastAPI + SQLAlchemy 练手项目，巩固后端工程化基础。

## ✅ 功能
- [x] 知识条目 CRUD（增删改查）
- [x] 单级分类筛选
- [x] Pydantic V2 数据校验
- [x] 环境变量管理（Pydantic Settings）
- [ ] Docker 部署（待补充）

## 🛠 技术栈
- FastAPI + SQLAlchemy + MySQL
- Pydantic V2 + Pydantic Settings
- Pytest + HTTPX

## 📦 快速开始

### 本地开发
```bash
# 1. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 .env（复制 .env.example 并修改数据库密码）
cp .env.example .env

# 4. 启动
uvicorn app.main:app --reload