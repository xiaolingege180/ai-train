from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, users, courses, progress, exercises, community, ai_lab

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时清理资源

app = FastAPI(
    title="AI Training Platform API",
    description="AI工具培训平台后端API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["课程"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["学习进度"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["练习"])
app.include_router(community.router, prefix="/api/v1/community", tags=["社区"])
app.include_router(ai_lab.router, prefix="/api/v1/ai-lab", tags=["AI实验室"])

@app.get("/")
async def root():
    return {
        "message": "AI Training Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
