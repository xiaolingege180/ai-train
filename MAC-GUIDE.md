# AI工具培训平台 - Mac 运行指南

## 🖥️ Mac 环境准备

### 1. 安装 Homebrew（如未安装）
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 安装 Python 3.10+
```bash
brew install python@3.10
# 或者使用最新版
brew install python3
```

### 3. 安装 Node.js 18+
```bash
brew install node@18
# 或者使用 nvm 管理
brew install nvm
nvm install 18
nvm use 18
```

---

## 🚀 Mac 启动步骤

### 第一步：解压项目
```bash
tar -xzf ai-training-platform-v1.0.tar.gz
cd ai-training-platform
```

### 第二步：启动后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境（Mac/Linux 命令）
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**后端运行后：**
- API 地址: http://localhost:8000
- API 文档: http://localhost:8000/docs

---

### 第三步：启动前端（新开终端窗口）

```bash
cd ai-training-platform/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**前端运行后：**
- 访问地址: http://localhost:3000

---

## ⚠️ Mac 可能需要修改的地方

### 1. 端口占用检查
如果端口被占用，Mac 可以修改端口：

**后端端口修改：**
```bash
# 使用 8001 端口代替
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**前端端口修改：**
```bash
# 在 frontend/package.json 中修改 scripts
"dev": "vite --port 3001"
```

### 2. Python 版本问题
如果 Mac 默认 Python 版本较低：
```bash
# 检查版本
python3 --version

# 如果低于 3.10，使用 Homebrew 安装新版本
brew install python@3.10
brew link python@3.10 --force
```

### 3. 权限问题
Mac 可能会遇到权限问题：
```bash
# 如果遇到权限错误，尝试使用 sudo（不推荐用于开发）
# 或者修改文件夹权限
chmod -R 755 ai-training-platform/
```

### 4. SQLite 数据库（项目默认使用）
项目使用 SQLite 数据库，**无需额外安装**。
数据文件会保存在 `backend/` 目录下。

---

## 🐳 Mac Docker 部署（可选）

如果安装了 Docker Desktop for Mac：

```bash
# 一键启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

---

## 📋 常用命令速查

| 操作 | 命令 |
|-----|------|
| 启动后端 | `cd backend && source venv/bin/activate && uvicorn app.main:app --reload` |
| 启动前端 | `cd frontend && npm run dev` |
| 安装后端依赖 | `pip install -r requirements.txt` |
| 安装前端依赖 | `npm install` |
| 检查端口 | `lsof -i :8000` 或 `lsof -i :3000` |
| 杀死进程 | `kill -9 <PID>` |

---

## 🔍 故障排查

### 问题1：`pip install` 很慢
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题2：`npm install` 很慢
```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install
```

### 问题3：后端启动失败
```bash
# 检查 Python 版本
python3 --version  # 需要 3.10+

# 检查依赖
pip list | grep fastapi
```

### 问题4：前端启动失败
```bash
# 清除缓存重新安装
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## ✅ 启动成功标志

打开浏览器访问：
- 前端: http://localhost:3000 → 看到登录页面
- 后端: http://localhost:8000/docs → 看到 Swagger API 文档

---

**版本**: v1.0-Mac  
**更新日期**: 2026-03-15
