# AI工具培训平台 - 项目完整交付包

## 📦 交付内容清单

### 1. 需求文档
- `docs/PRD.md` - 产品需求规格说明书 (完整版)

### 2. 设计文档
- `docs/Prototype.md` - 原型图设计文档 (含8个核心页面)

### 3. 测试文档
- `docs/TestCases.md` - 测试用例文档 (功能/接口/性能/安全)

### 4. 前端代码 (Vue 3)
- `frontend/` - Vue 3 + Element Plus 项目
  - 完整路由配置
  - Pinia 状态管理
  - Axios API 封装
  - 核心页面组件

### 5. 后端代码 (Python FastAPI)
- `backend/` - FastAPI + SQLAlchemy 项目
  - RESTful API 接口
  - 数据库模型
  - 认证授权
  - 业务逻辑服务

### 6. 部署配置
- `docker-compose.yml` - 一键部署配置
- `README.md` - 部署说明

---

## 🚀 快速启动

### 环境要求
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### 1. 启动后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 配置数据库
export DATABASE_URL="postgresql://user:password@localhost:5432/ai_training"
export SECRET_KEY="your-secret-key"

# 初始化数据库
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端
```bash
cd frontend
npm install
npm run dev
```

### 3. 访问应用
- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

---

## 📁 项目结构

```
ai-training-platform/
├── docs/                     # 文档目录
│   ├── PRD.md               # 需求文档
│   ├── Prototype.md         # 原型设计
│   └── TestCases.md         # 测试用例
│
├── frontend/                # Vue 前端
│   ├── src/
│   │   ├── api/            # API 封装
│   │   ├── components/     # 组件
│   │   ├── router/         # 路由
│   │   ├── stores/         # Pinia 状态
│   │   ├── views/          # 页面
│   │   └── App.vue         # 根组件
│   └── package.json
│
├── backend/                 # Python 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic 模型
│   │   └── services/       # 业务逻辑
│   └── requirements.txt
│
└── docker-compose.yml       # 部署配置
```

---

## 🔧 核心功能

### 用户系统
- 邮箱/手机号注册登录
- JWT Token 认证
- 用户画像与学习路径推荐

### 课程系统
- 课程分类与搜索
- 视频播放与进度追踪
- 章节学习与笔记

### 练习系统
- Prompt 练习器
- AI 自动评分
- 错题回顾

### 社区系统
- 帖子发布与互动
- 作品展示
- 学习小组

---

## 📝 API 接口列表

### 认证接口
- `POST /api/v1/auth/register` - 注册
- `POST /api/v1/auth/login` - 登录
- `GET /api/v1/users/me` - 获取当前用户

### 课程接口
- `GET /api/v1/courses` - 课程列表
- `GET /api/v1/courses/{id}` - 课程详情
- `POST /api/v1/courses/{id}/enroll` - 报名课程

### 学习接口
- `POST /api/v1/progress` - 更新进度
- `GET /api/v1/progress/{course_id}` - 获取进度

---

## 🧪 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

---

## 🐳 Docker 部署

```bash
# 一键启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 📮 联系方式

如需技术支持或定制开发，请联系：
- 邮箱: 280573224@qq.com

---

**版本**: v1.0  
**创建日期**: 2026-03-15  
**作者**: ai-train
