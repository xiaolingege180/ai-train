#!/usr/bin/env python3
"""
课程数据导入工具
支持从 JSON 文件导入示例课程数据到数据库

用法:
    python import_courses.py                    # 使用内置示例数据
    python import_courses.py --file data.json   # 从 JSON 文件导入
    python import_courses.py --force            # 强制重新导入（先清空）
    python import_courses.py --dry-run          # 试运行，不写入数据库

JSON 文件格式:
[
    {
        "title": "课程标题",
        "description": "课程描述",
        "cover_image": "封面图片URL",
        "category": "text|image|video|office|code|data",
        "difficulty": "beginner|intermediate|advanced",
        "is_free": true,
        "price": 0.0,
        "is_published": true,
        "chapters": [
            {
                "title": "章节标题",
                "order": 1,
                "lessons": [
                    {"title": "课时标题", "duration": 300, "order": 1}
                ]
            }
        ]
    }
]
"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/app')

from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.models.models import Course, Chapter, Lesson, CourseCategory, DifficultyLevel

# 示例课程数据（内置）
SAMPLE_COURSES = [
    {
        "title": "ChatGPT 从入门到精通",
        "description": "系统学习 ChatGPT 的使用技巧，从基础对话到高级提示词工程，掌握 AI 对话的核心方法。",
        "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
        "category": "text",
        "difficulty": "beginner",
        "is_free": True,
        "price": 0.0,
        "is_published": True,
        "student_count": 12580,
        "rating": 4.8,
        "rating_count": 2341,
        "chapters": [
            {
                "title": "第一章：ChatGPT 基础入门",
                "order": 1,
                "lessons": [
                    {"title": "1.1 什么是 ChatGPT", "duration": 300, "order": 1},
                    {"title": "1.2 注册与界面介绍", "duration": 420, "order": 2},
                    {"title": "1.3 第一个对话", "duration": 360, "order": 3},
                ]
            },
            {
                "title": "第二章：提示词工程基础",
                "order": 2,
                "lessons": [
                    {"title": "2.1 提示词的核心要素", "duration": 480, "order": 1},
                    {"title": "2.2 角色设定技巧", "duration": 540, "order": 2},
                    {"title": "2.3 上下文管理", "duration": 600, "order": 3},
                ]
            },
            {
                "title": "第三章：实战应用场景",
                "order": 3,
                "lessons": [
                    {"title": "3.1 文案写作助手", "duration": 720, "order": 1},
                    {"title": "3.2 代码辅助编程", "duration": 780, "order": 2},
                    {"title": "3.3 数据分析解读", "duration": 660, "order": 3},
                ]
            }
        ]
    },
    {
        "title": "Midjourney 图像创作大师班",
        "description": "从零开始学习 AI 绘画，掌握 Midjourney 的提示词技巧，创作专业级别的视觉作品。",
        "cover_image": "https://images.unsplash.com/photo-1686191128892-3b37add4a934?w=800",
        "category": "image",
        "difficulty": "beginner",
        "is_free": False,
        "price": 99.0,
        "is_published": True,
        "student_count": 8932,
        "rating": 4.9,
        "rating_count": 1856,
        "chapters": [
            {
                "title": "第一章：Midjourney 入门",
                "order": 1,
                "lessons": [
                    {"title": "1.1 Discord 平台注册", "duration": 360, "order": 1},
                    {"title": "1.2 基础命令详解", "duration": 480, "order": 2},
                    {"title": "1.3 第一张 AI 绘画", "duration": 300, "order": 3},
                ]
            },
            {
                "title": "第二章：提示词语法详解",
                "order": 2,
                "lessons": [
                    {"title": "2.1 提示词结构解析", "duration": 600, "order": 1},
                    {"title": "2.2 风格与艺术家引用", "duration": 720, "order": 2},
                    {"title": "2.3 参数设置指南", "duration": 540, "order": 3},
                ]
            },
            {
                "title": "第三章：商业应用实战",
                "order": 3,
                "lessons": [
                    {"title": "3.1 电商产品图制作", "duration": 900, "order": 1},
                    {"title": "3.2 品牌视觉设计", "duration": 840, "order": 2},
                    {"title": "3.3 社交媒体配图", "duration": 660, "order": 3},
                ]
            }
        ]
    },
    {
        "title": "AI 视频创作：Runway 与剪映",
        "description": "学习使用 Runway Gen-2、剪映 AI 等工具进行视频创作，从脚本到成片的全流程。",
        "cover_image": "https://images.unsplash.com/photo-1536240478700-b869070f9279?w=800",
        "category": "video",
        "difficulty": "intermediate",
        "is_free": False,
        "price": 199.0,
        "is_published": True,
        "student_count": 5621,
        "rating": 4.7,
        "rating_count": 987,
        "chapters": [
            {
                "title": "第一章：AI 视频工具概览",
                "order": 1,
                "lessons": [
                    {"title": "1.1 Runway Gen-2 介绍", "duration": 420, "order": 1},
                    {"title": "1.2 剪映 AI 功能详解", "duration": 480, "order": 2},
                    {"title": "1.3 其他工具对比", "duration": 360, "order": 3},
                ]
            },
            {
                "title": "第二章：文生视频技术",
                "order": 2,
                "lessons": [
                    {"title": "2.1 提示词写法技巧", "duration": 600, "order": 1},
                    {"title": "2.2 镜头运动控制", "duration": 720, "order": 2},
                    {"title": "2.3 风格与氛围营造", "duration": 540, "order": 3},
                ]
            },
            {
                "title": "第三章：后期剪辑与发布",
                "order": 3,
                "lessons": [
                    {"title": "3.1 AI 配音与字幕", "duration": 480, "order": 1},
                    {"title": "3.2 剪辑节奏把控", "duration": 660, "order": 2},
                    {"title": "3.3 多平台发布策略", "duration": 420, "order": 3},
                ]
            }
        ]
    },
    {
        "title": "AI 办公效率提升指南",
        "description": "掌握 Office 365 Copilot、WPS AI 等工具，让 AI 帮你处理文档、表格和演示文稿。",
        "cover_image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800",
        "category": "office",
        "difficulty": "beginner",
        "is_free": True,
        "price": 0.0,
        "is_published": True,
        "student_count": 15890,
        "rating": 4.6,
        "rating_count": 3210,
        "chapters": [
            {
                "title": "第一章：Word 与 AI 写作",
                "order": 1,
                "lessons": [
                    {"title": "1.1 AI 辅助写作入门", "duration": 360, "order": 1},
                    {"title": "1.2 智能排版与格式", "duration": 300, "order": 2},
                    {"title": "1.3 文档自动校对", "duration": 240, "order": 3},
                ]
            },
            {
                "title": "第二章：Excel 数据分析",
                "order": 2,
                "lessons": [
                    {"title": "2.1 AI 生成公式", "duration": 480, "order": 1},
                    {"title": "2.2 智能图表制作", "duration": 540, "order": 2},
                    {"title": "2.3 数据洞察与报告", "duration": 600, "order": 3},
                ]
            },
            {
                "title": "第三章：PPT 智能设计",
                "order": 3,
                "lessons": [
                    {"title": "3.1 AI 生成大纲", "duration": 360, "order": 1},
                    {"title": "3.2 一键美化排版", "duration": 420, "order": 2},
                    {"title": "3.3 演讲者备注生成", "duration": 300, "order": 3},
                ]
            }
        ]
    },
    {
        "title": "AI 代码助手：Copilot 深度使用",
        "description": "GitHub Copilot 进阶教程，从代码补全到架构设计，全面提升开发效率。",
        "cover_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800",
        "category": "code",
        "difficulty": "intermediate",
        "is_free": False,
        "price": 149.0,
        "is_published": True,
        "student_count": 7234,
        "rating": 4.8,
        "rating_count": 1423,
        "chapters": [
            {
                "title": "第一章：Copilot 基础",
                "order": 1,
                "lessons": [
                    {"title": "1.1 安装与配置", "duration": 360, "order": 1},
                    {"title": "1.2 代码补全技巧", "duration": 480, "order": 2},
                    {"title": "1.3 注释驱动开发", "duration": 420, "order": 3},
                ]
            },
            {
                "title": "第二章：高级功能",
                "order": 2,
                "lessons": [
                    {"title": "2.1 多行代码生成", "duration": 540, "order": 1},
                    {"title": "2.2 测试代码生成", "duration": 600, "order": 2},
                    {"title": "2.3 代码解释与优化", "duration": 480, "order": 3},
                ]
            },
            {
                "title": "第三章：实战项目",
                "order": 3,
                "lessons": [
                    {"title": "3.1 Web 应用开发", "duration": 900, "order": 1},
                    {"title": "3.2 API 设计实现", "duration": 780, "order": 2},
                    {"title": "3.3 调试与重构", "duration": 660, "order": 3},
                ]
            }
        ]
    },
    {
        "title": "AI 数据分析：ChatGPT + Python",
        "description": "结合 ChatGPT 和 Python 进行数据分析，快速上手 pandas、matplotlib 等工具。",
        "cover_image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
        "category": "data",
        "difficulty": "advanced",
        "is_free": False,
        "price": 249.0,
        "is_published": True,
        "student_count": 4321,
        "rating": 4.9,
        "rating_count": 756,
        "chapters": [
            {
                "title": "第一章：环境搭建",
                "order": 1,
                "lessons": [
                    {"title": "1.1 Python 环境配置", "duration": 420, "order": 1},
                    {"title": "1.2 Jupyter Notebook 使用", "duration": 360, "order": 2},
                    {"title": "1.3 AI 辅助编程环境", "duration": 300, "order": 3},
                ]
            },
            {
                "title": "第二章：数据处理",
                "order": 2,
                "lessons": [
                    {"title": "2.1 Pandas 基础操作", "duration": 720, "order": 1},
                    {"title": "2.2 数据清洗技巧", "duration": 660, "order": 2},
                    {"title": "2.3 AI 生成处理代码", "duration": 540, "order": 3},
                ]
            },
            {
                "title": "第三章：可视化与报告",
                "order": 3,
                "lessons": [
                    {"title": "3.1 Matplotlib 基础", "duration": 600, "order": 1},
                    {"title": "3.2 高级图表制作", "duration": 720, "order": 2},
                    {"title": "3.3 自动化报告生成", "duration": 480, "order": 3},
                ]
            }
        ]
    }
]


def get_category(category_str: str) -> CourseCategory:
    """将字符串转换为 CourseCategory 枚举"""
    category_map = {
        "text": CourseCategory.TEXT,
        "image": CourseCategory.IMAGE,
        "video": CourseCategory.VIDEO,
        "office": CourseCategory.OFFICE,
        "code": CourseCategory.CODE,
        "data": CourseCategory.DATA,
    }
    return category_map.get(category_str.lower(), CourseCategory.TEXT)


def get_difficulty(difficulty_str: str) -> DifficultyLevel:
    """将字符串转换为 DifficultyLevel 枚举"""
    difficulty_map = {
        "beginner": DifficultyLevel.BEGINNER,
        "intermediate": DifficultyLevel.INTERMEDIATE,
        "advanced": DifficultyLevel.ADVANCED,
    }
    return difficulty_map.get(difficulty_str.lower(), DifficultyLevel.BEGINNER)


def import_courses(courses_data: list, force: bool = False, dry_run: bool = False) -> dict:
    """
    导入课程数据
    
    Args:
        courses_data: 课程数据列表
        force: 是否强制重新导入（清空现有数据）
        dry_run: 试运行模式，不写入数据库
    
    Returns:
        导入统计信息
    """
    db = SessionLocal()
    stats = {
        "courses_added": 0,
        "courses_skipped": 0,
        "chapters_added": 0,
        "lessons_added": 0,
        "errors": []
    }
    
    try:
        # 创建表
        if not dry_run:
            Base.metadata.create_all(bind=engine)
        
        # 检查现有数据
        existing_courses = {c.title: c for c in db.query(Course).all()}
        
        if force and not dry_run:
            print("⚠️  强制模式：清空现有课程数据...")
            db.query(Lesson).delete()
            db.query(Chapter).delete()
            db.query(Course).delete()
            db.commit()
            existing_courses = {}
            print("✅ 已清空现有数据")
        
        for course_data in courses_data:
            try:
                title = course_data["title"]
                
                # 检查是否已存在
                if title in existing_courses and not force:
                    print(f"⏭️  跳过已存在的课程: {title}")
                    stats["courses_skipped"] += 1
                    continue
                
                chapters_data = course_data.pop("chapters", [])
                
                # 转换枚举值
                course_data["category"] = get_category(course_data.get("category", "text"))
                course_data["difficulty"] = get_difficulty(course_data.get("difficulty", "beginner"))
                
                if dry_run:
                    print(f"[试运行] 将创建课程: {title}")
                    stats["courses_added"] += 1
                    for ch in chapters_data:
                        stats["chapters_added"] += 1
                        stats["lessons_added"] += len(ch.get("lessons", []))
                    continue
                
                # 创建课程
                course = Course(**course_data)
                db.add(course)
                db.flush()
                stats["courses_added"] += 1
                print(f"✅ 创建课程: {title} (ID: {course.id})")
                
                # 创建章节和课时
                for chapter_data in chapters_data:
                    lessons_data = chapter_data.pop("lessons", [])
                    chapter_data["course_id"] = course.id
                    
                    chapter = Chapter(**chapter_data)
                    db.add(chapter)
                    db.flush()
                    stats["chapters_added"] += 1
                    
                    for lesson_data in lessons_data:
                        lesson_data["chapter_id"] = chapter.id
                        lesson = Lesson(**lesson_data)
                        db.add(lesson)
                        stats["lessons_added"] += 1
                    
                    print(f"   📚 {chapter.title} ({len(lessons_data)} 课时)")
                
            except Exception as e:
                error_msg = f"导入课程 '{title}' 失败: {str(e)}"
                print(f"❌ {error_msg}")
                stats["errors"].append(error_msg)
        
        if not dry_run:
            db.commit()
        
        # 打印统计
        print("\n" + "=" * 50)
        print("📊 导入统计:")
        print(f"   课程: +{stats['courses_added']} 新增, {stats['courses_skipped']} 跳过")
        print(f"   章节: +{stats['chapters_added']} 新增")
        print(f"   课时: +{stats['lessons_added']} 新增")
        if stats["errors"]:
            print(f"   错误: {len(stats['errors'])} 个")
        print("=" * 50)
        
        if dry_run:
            print("\n⚠️  试运行模式：数据未实际写入数据库")
            print("   去掉 --dry-run 参数以实际导入")
        
        return stats
        
    except Exception as e:
        if not dry_run:
            db.rollback()
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


def export_sample_json(output_file: str = "sample_courses.json"):
    """导出示例数据到 JSON 文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_COURSES, f, ensure_ascii=False, indent=2)
    print(f"✅ 示例数据已导出到: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='AI培训平台课程数据导入工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用内置示例数据导入
  python import_courses.py

  # 从 JSON 文件导入
  python import_courses.py --file my_courses.json

  # 强制重新导入（先清空现有数据）
  python import_courses.py --force

  # 试运行，查看将要导入的数据
  python import_courses.py --dry-run

  # 导出示例数据到 JSON 文件
  python import_courses.py --export sample.json
        """
    )
    parser.add_argument('--file', '-f', type=str, help='从 JSON 文件导入课程数据')
    parser.add_argument('--force', action='store_true', help='强制重新导入（清空现有数据）')
    parser.add_argument('--dry-run', '-n', action='store_true', help='试运行模式，不写入数据库')
    parser.add_argument('--export', '-e', type=str, metavar='FILE', help='导出内置示例数据到 JSON 文件')
    
    args = parser.parse_args()
    
    print("🚀 AI培训平台 - 课程数据导入工具")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 导出示例数据
    if args.export:
        export_sample_json(args.export)
        return
    
    # 加载数据
    if args.file:
        if not Path(args.file).exists():
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        
        print(f"📂 从文件加载数据: {args.file}")
        with open(args.file, 'r', encoding='utf-8') as f:
            courses_data = json.load(f)
    else:
        print("📦 使用内置示例数据")
        courses_data = SAMPLE_COURSES
    
    print(f"📋 准备导入 {len(courses_data)} 门课程")
    print("-" * 50)
    
    # 执行导入
    try:
        import_courses(courses_data, force=args.force, dry_run=args.dry_run)
        print("\n✨ 导入完成!")
    except Exception as e:
        print(f"\n❌ 导入失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
