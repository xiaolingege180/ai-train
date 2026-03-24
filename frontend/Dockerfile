FROM node:20-alpine

WORKDIR /app

# 配置 npm 国内镜像
RUN npm config set registry https://registry.npmmirror.com

# 安装依赖
COPY package*.json ./
RUN npm install

# 复制源码
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]
