from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.schemas import CourseResponse, CourseList, CourseDetailResponse
from app.models.models import Course, Chapter, Lesson, Enrollment
from app.services.auth_service import get_current_user_optional

router = APIRouter()

@router.get("", response_model=CourseList)
async def get_courses(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = "popularity",
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    """获取课程列表"""
    query = db.query(Course).filter(Course.is_published == True)
    
    # 分类筛选
    if category:
        query = query.filter(Course.category == category)
    
    # 难度筛选
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    
    # 搜索
    if search:
        query = query.filter(
            Course.title.ilike(f"%{search}%") | 
            Course.description.ilike(f"%{search}%")
        )
    
    # 排序
    if sort == "newest":
        query = query.order_by(Course.created_at.desc())
    elif sort == "rating":
        query = query.order_by(Course.rating.desc())
    else:  # popularity
        query = query.order_by(Course.student_count.desc())
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {"total": total, "items": items}

@router.get("/categories")
async def get_categories():
    """获取课程分类"""
    return [
        {"id": "text", "name": "文本生成", "icon": "📝"},
        {"id": "image", "name": "图像生成", "icon": "🎨"},
        {"id": "video", "name": "视频创作", "icon": "🎬"},
        {"id": "office", "name": "办公效率", "icon": "📊"},
        {"id": "code", "name": "代码辅助", "icon": "💻"},
        {"id": "data", "name": "数据分析", "icon": "📈"},
    ]

@router.get("/{course_id}", response_model=CourseDetailResponse)
async def get_course_detail(course_id: int, db: Session = Depends(get_db)):
    """获取课程详情"""
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.is_published == True
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    return course

@router.post("/{course_id}/enroll")
async def enroll_course(
    course_id: int,
    current_user = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """报名课程"""
    if not current_user:
        raise HTTPException(status_code=401, detail="请先登录")
    
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    # 检查是否已报名
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="已经报名该课程")
    
    # 创建报名记录
    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.add(enrollment)
    
    # 增加课程学生数
    course.student_count += 1
    
    db.commit()
    
    return {"message": "报名成功"}
