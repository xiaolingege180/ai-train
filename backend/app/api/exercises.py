from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.auth_service import get_current_user_optional

router = APIRouter()

@router.get("")
async def get_exercises(
    course_id: int = None,
    db: Session = Depends(get_db)
):
    """获取练习题列表"""
    # 示例数据
    return [
        {
            "id": 1,
            "type": "prompt",
            "title": "优化客服回复",
            "difficulty": 3,
            "task": "请补全以下 Prompt，使其能生成一份专业的客服回复..."
        }
    ]

@router.post("/{exercise_id}/submit")
async def submit_exercise(
    exercise_id: int,
    answer: str,
    current_user = Depends(get_current_user_optional)
):
    """提交练习答案"""
    # AI 评分逻辑
    return {
        "score": 8.5,
        "feedback": "回答结构完整，可以继续优化...",
        "suggestions": ["增加具体场景描述", "明确输出格式要求"]
    }
