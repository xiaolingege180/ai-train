#!/bin/sh
set -e

echo "🛑 停止服务并清理..."

# 停止并删除容器
docker-compose down "$@"

# 删除前端构建产物
if [ -d "frontend/dist" ]; then
    echo "🗑️  删除 frontend/dist..."
    rm -rf frontend/dist
    echo "✅ 已清理"
else
    echo "ℹ️  frontend/dist 不存在，跳过"
fi

echo ""
echo "服务已停止，前端构建产物已清理"
echo "下次启动请运行: ./start.sh"
