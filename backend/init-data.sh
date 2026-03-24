#!/bin/bash
# 等待数据库就绪
echo "⏳ 等待数据库就绪..."
until pg_isready -h postgres -p 5432 -U postgres; do
  echo "数据库未就绪，等待 2 秒..."
  sleep 2
done
echo "✅ 数据库已就绪"

# 运行数据初始化
echo "🚀 开始初始化示例课程数据..."
cd /app
python app/scripts/init_courses.py

echo "✨ 初始化脚本执行完成"
