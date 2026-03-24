from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import UserResponse, UserUpdate, ProgressCreate, ProgressResponse
from app.services.auth_service import get_current_user
from app.models.models import Progress, Enrollment

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me/courses")
async def get_my_courses(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取我的课程"""
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).all()
    
    return enrollments
