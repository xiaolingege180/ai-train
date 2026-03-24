<template>
  <div class="admin-dashboard">
    <el-container>
      <el-aside width="200px">
        <el-menu
          default-active="1"
          class="admin-menu"
          background-color="#304156"
          text-color="#fff"
          active-text-color="#409EFF"
        >
          <el-menu-item index="1">
            <el-icon><DataLine /></el-icon>
            <span>数据概览</span>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon><Reading /></el-icon>
            <span>课程管理</span>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="4">
            <el-icon><ChatDotRound /></el-icon>
            <span>社区管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main>
        <h1>管理员控制台</h1>
        <el-row :gutter="20" class="stat-cards">
          <el-col :span="6">
            <el-card>
              <div class="stat-item">
                <div class="stat-value">1,234</div>
                <div class="stat-label">总用户</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card>
              <div class="stat-item">
                <div class="stat-value">56</div>
                <div class="stat-label">课程数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card>
              <div class="stat-item">
                <div class="stat-value">8,901</div>
                <div class="stat-label">学习记录</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card>
              <div class="stat-item">
                <div class="stat-value">342</div>
                <div class="stat-label">帖子数</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { DataLine, Reading, User, ChatDotRound } from '@element-plus/icons-vue'
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
}

.admin-menu {
  height: 100vh;
}

.stat-cards {
  margin-top: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  margin-top: 10px;
  color: #666;
}

h1 {
  margin-bottom: 20px;
}
</style>
