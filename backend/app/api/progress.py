from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.schemas.schemas import ProgressCreate, ProgressResponse
from app.services.auth_service import get_current_user
from app.models.models import Progress

router = APIRouter()

@router.post("", response_model=ProgressResponse)
async def update_progress(
    data: ProgressCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新学习进度"""
    # 查找或创建进度记录
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.course_id == data.course_id,
        Progress.lesson_id == data.lesson_id
    ).first()
    
    if progress:
        progress.progress_time = data.progress_time
        progress.is_completed = data.is_completed
        if data.is_completed and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
        progress.last_accessed = datetime.utcnow()
    else:
        progress = Progress(
            user_id=current_user.id,
            course_id=data.course_id,
            lesson_id=data.lesson_id,
            progress_time=data.progress_time,
            is_completed=data.is_completed,
            completed_at=datetime.utcnow() if data.is_completed else None
        )
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    
    return progress

@router.get("/{course_id}")
async def get_course_progress(
    course_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取课程学习进度"""
    progress_list = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.course_id == course_id
    ).all()
    
    return progress_list
