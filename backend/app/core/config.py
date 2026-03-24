try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings
from typing import List

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "AI Training Platform"
    DEBUG: bool = True
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./ai_training.db"  # 使用 SQLite 简化部署
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # 文件上传配置
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # AI API配置
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_API_BASE: str = "https://api.anthropic.com"
    
    MOONSHOT_API_KEY: str = ""
    MOONSHOT_API_BASE: str = "https://api.moonshot.cn/v1"
    
    DASHSCOPE_API_KEY: str = ""  # 通义千问
    DASHSCOPE_API_BASE: str = "https://dashscope.aliyuncs.com/api/v1"
    
    DOUBAO_API_KEY: str = ""  # 豆包
    DOUBAO_API_BASE: str = "https://ark.cn-beijing.volces.com/api/v3"
    
    class Config:
        env_file = ".env"

settings = Settings()
