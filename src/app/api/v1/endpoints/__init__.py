# 端点包初始化文件
"""
API 端点速查表

学生管理 - /api/v1/students
POST   /                      创建学生
GET    /                      获取学生列表（支持分页、姓名搜索）
GET    /{id}                  获取单个学生（含已选课程详情）
PUT    /{id}                  更新学生信息
DELETE /{id}                  删除学生

课程管理 - /api/v1/courses
POST   /                      创建课程
GET    /                      获取课程列表（支持分页、名称搜索）
GET    /{id}                  获取单个课程（含选课学生详情）
PUT    /{id}                  更新课程信息
DELETE /{id}                  删除课程

选课管理 - /api/v1/student-courses
POST   /                      学生选课
DELETE /                      学生退课（通过 query 参数传 student_id 和 course_id）
GET    /students/{id}/courses 获取某学生的所有课程
GET    /courses/{id}/students 获取某课程的所有学生
"""