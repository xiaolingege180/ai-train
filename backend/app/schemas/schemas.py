from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ========== 认证相关 Schema ==========

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

# ========== 用户相关 Schema ==========

class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    avatar: Optional[str] = None
    occupation: Optional[str] = None
    ai_level: Optional[str] = None
    learning_goal: Optional[str] = None

class UserResponse(UserBase):
    id: int
    avatar: Optional[str]
    status: str
    total_learning_time: int
    completed_courses: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== 课程相关 Schema ==========

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty: str
    price: float = 0.0
    is_free: bool = True

class CourseResponse(CourseBase):
    id: int
    cover_image: Optional[str]
    student_count: int
    rating: float
    rating_count: int
    is_published: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CourseList(BaseModel):
    total: int
    items: List[CourseResponse]

class LessonResponse(BaseModel):
    id: int
    title: str
    duration: int
    order: int
    
    class Config:
        from_attributes = True

class ChapterResponse(BaseModel):
    id: int
    title: str
    order: int
    lessons: List[LessonResponse] = []
    
    class Config:
        from_attributes = True

class CourseDetailResponse(CourseResponse):
    chapters: List[ChapterResponse]

# ========== 进度相关 Schema ==========

class ProgressCreate(BaseModel):
    course_id: int
    lesson_id: int
    progress_time: int
    is_completed: bool = False

class ProgressResponse(BaseModel):
    id: int
    course_id: int
    lesson_id: int
    progress_time: int
    is_completed: bool
    last_accessed: datetime
    
    class Config:
        from_attributes = True
