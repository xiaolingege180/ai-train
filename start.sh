#!/bin/sh
set -e

echo "=================================="
echo "AI Training Platform - 启动脚本"
echo "=================================="

# 检查前端是否需要构建
if [ ! -d "frontend/dist" ] || [ ! -f "frontend/dist/index.html" ]; then
    echo "📦 前端 dist 目录不存在，开始自动构建..."
    
    cd frontend
    
    # 检查 node_modules 是否存在
    if [ ! -d "node_modules" ]; then
        echo "⬇️  安装 npm 依赖..."
        npm install
    fi
    
    echo "🔨 构建前端项目..."
    npm run build
    
    echo "✅ 前端构建完成"
    cd ..
else
    echo "✅ 前端 dist 目录已存在，跳过构建"
fi

# 启动 Docker 服务
echo "🚀 启动 Docker 服务..."
docker-compose up -d --build

echo ""
echo "=================================="
echo "服务启动完成！"
echo "=================================="
echo "访问地址: http://localhost"
echo "API 文档: http://localhost/docs"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
