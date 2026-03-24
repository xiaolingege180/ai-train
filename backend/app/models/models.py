from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    BANNED = "banned"

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CourseCategory(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    OFFICE = "office"
    CODE = "code"
    DATA = "data"

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    username = Column(String(100), nullable=True)
    avatar = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    
    # 用户画像
    occupation = Column(String(100), nullable=True)
    ai_level = Column(String(50), nullable=True)
    learning_goal = Column(Text, nullable=True)
    
    # 学习统计
    total_learning_time = Column(Integer, default=0)  # 分钟
    completed_courses = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联
    enrollments = relationship("Enrollment", back_populates="user")
    progress_records = relationship("Progress", back_populates="user")

# 课程模型
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    cover_image = Column(String(500), nullable=True)
    category = Column(Enum(CourseCategory), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER)
    
    # 统计
    student_count = Column(Integer, default=0)
    rating = Column(Float, default=5.0)
    rating_count = Column(Integer, default=0)
    
    # 价格
    price = Column(Float, default=0.0)
    is_free = Column(Boolean, default=True)
    
    # 状态
    is_published = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联
    chapters = relationship("Chapter", back_populates="course", order_by="Chapter.order")
    enrollments = relationship("Enrollment", back_populates="course")

# 章节模型
class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(200), nullable=False)
    order = Column(Integer, default=0)
    
    # 关联
    course = relationship("Course", back_populates="chapters")
    lessons = relationship("Lesson", back_populates="chapter", order_by="Lesson.order")

# 课时模型
class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    video_url = Column(String(500), nullable=True)
    duration = Column(Integer, default=0)  # 秒
    order = Column(Integer, default=0)
    
    # 关联
    chapter = relationship("Chapter", back_populates="lessons")
    progress_records = relationship("Progress", back_populates="lesson")

# 选课记录
class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

# 学习进度
class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    progress_time = Column(Integer, default=0)  # 已学习秒数
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联
    user = relationship("User", back_populates="progress_records")
    lesson = relationship("Lesson", back_populates="progress_records")
