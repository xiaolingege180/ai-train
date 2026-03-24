from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.services.auth_service import get_current_user_optional

router = APIRouter()

class PostCreate(BaseModel):
    title: str
    content: str
    category: str

@router.get("/posts")
async def get_posts(
    category: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """获取帖子列表"""
    # 示例数据
    return {
        "total": 100,
        "items": [
            {
                "id": 1,
                "title": "分享一个超实用的 ChatGPT 提示词模板",
                "content": "最近在做内容运营，整理了一套小红书文案生成提示词...",
                "author": {"id": 1, "username": "张三", "avatar": ""},
                "category": "分享",
                "likes": 156,
                "comments": 23,
                "created_at": "2026-03-15T10:00:00"
            }
        ]
    }

@router.post("/posts")
async def create_post(
    post: PostCreate,
    current_user = Depends(get_current_user_optional)
):
    """发布帖子"""
    if not current_user:
        raise HTTPException(status_code=401, detail="请先登录")
    
    return {"id": 1, "title": post.title, "message": "发布成功"}

@router.get("/posts/{post_id}")
async def get_post_detail(post_id: int):
    """获取帖子详情"""
    return {
        "id": post_id,
        "title": "分享一个超实用的 ChatGPT 提示词模板",
        "content": "详细内容...",
        "author": {"id": 1, "username": "张三", "avatar": ""},
        "comments": []
    }

@router.post("/posts/{post_id}/like")
async def like_post(
    post_id: int,
    current_user = Depends(get_current_user_optional)
):
    """点赞帖子"""
    if not current_user:
        raise HTTPException(status_code=401, detail="请先登录")
    
    return {"message": "点赞成功", "post_id": post_id}
