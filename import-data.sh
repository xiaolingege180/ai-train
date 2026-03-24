#!/bin/bash
# 课程数据导入脚本
# 使用方法: ./import-data.sh [选项]

set -e

cd "$(dirname "$0")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 AI培训平台 - 课程数据导入工具${NC}"
echo "=========================================="

# 检查是否在 Docker 环境中运行
if [ -f /.dockerenv ]; then
    # 在容器内直接运行
    echo "📦 在 Docker 容器内运行..."
    cd /app
    python app/scripts/import_courses.py "$@"
else
    # 在宿主机，通过 docker-compose 运行
    echo "🐳 通过 Docker 运行导入脚本..."
    
    # 检查 docker-compose 是否运行
    if ! docker-compose ps | grep -q "ai-training-backend"; then
        echo -e "${RED}❌ 错误: 后端服务未运行${NC}"
        echo "请先启动服务: docker-compose up -d"
        exit 1
    fi
    
    # 运行导入脚本
    docker-compose exec backend python app/scripts/import_courses.py "$@"
fi

echo ""
echo -e "${GREEN}✅ 导入脚本执行完成${NC}"
