<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <!-- Logo -->
        <router-link to="/" class="logo">
          <span class="logo-icon">🤖</span>
          <span class="logo-text">AI</span>
          <span class="logo-sub">培训平台</span>
        </router-link>

        <!-- 导航 -->
        <nav class="nav">
          <router-link to="/courses" class="nav-link">课程</router-link>
          <router-link to="/prompt-lab" class="nav-link">Prompt实验室</router-link>
          <router-link to="/community" class="nav-link">社区</router-link>
        </nav>

        <!-- 右侧操作区 -->
        <div class="actions">
          <!-- 搜索 -->
          <div class="search-box">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索课程..."
              @keyup.enter="handleSearch"
            />
            <button @click="handleSearch">
              <Search class="search-icon" />
            </button>
          </div>

          <!-- 用户状态 -->
          <template v-if="userStore.isLoggedIn">
            <el-dropdown @command="handleCommand" trigger="click">
              <div class="user-info">
                <img :src="userStore.avatar || '/default-avatar.svg'" :alt="userStore.username" class="avatar" @error="$event.target.src = '/default-avatar.svg'" />
                <span class="username">{{ displayUsername }}</span>
                <ArrowDown class="dropdown-arrow" />
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                  <el-dropdown-item command="courses">我的课程</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>

          <template v-else>
            <router-link to="/login" class="btn-login">登录</router-link>
            <router-link to="/register" class="btn-register">注册</router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Search, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const searchQuery = ref('')

// 处理用户名显示，确保最少显示2个字符
const displayUsername = computed(() => {
  const name = userStore.username || '用户'
  return name.length > 8 ? name.slice(0, 8) + '...' : name
})

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/courses',
      query: { search: searchQuery.value }
    })
  }
}

const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'courses':
      router.push('/profile?tab=courses')
      break
    case 'logout':
      userStore.logout()
      router.push('/')
      break
  }
}
</script>

<style scoped>
.header {
  background: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  font-size: 18px;
  font-weight: 600;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 22px;
}

.logo-text {
  color: #409eff;
}

.logo-sub {
  color: #303133;
}

/* 导航 */
.nav {
  display: flex;
  gap: 40px;
  margin: 0 40px;
}

.nav-link {
  color: #606266;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: #409eff;
}

.nav-link.router-link-active {
  color: #409eff;
  border-bottom-color: #409eff;
}

/* 右侧操作区 */
.actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 搜索框 - 企业级样式 */
.search-box {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.search-box:focus-within {
  border-color: #409eff;
  background: #ffffff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.1);
}

.search-box input {
  border: none;
  background: transparent;
  padding: 9px 12px;
  width: 180px;
  font-size: 14px;
  color: #303133;
  outline: none;
}

.search-box input::placeholder {
  color: #a8abb2;
}

.search-box button {
  background: transparent;
  color: #909399;
  border: none;
  padding: 9px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.search-box button:hover {
  background: #409eff;
  color: #ffffff;
}

.search-icon {
  width: 16px;
  height: 16px;
}

/* 按钮 */
.btn-login {
  color: #606266;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.btn-login:hover {
  color: #409eff;
  background: #f5f7fa;
}

.btn-register {
  background: #409eff;
  color: #ffffff;
  padding: 8px 20px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-register:hover {
  background: #66b1ff;
}

/* 用户信息 - 企业级样式 */
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.user-info:hover {
  background: #f5f7fa;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #e4e7ed;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-arrow {
  width: 14px;
  height: 14px;
  color: #909399;
  transition: transform 0.2s ease;
}

.user-info:hover .dropdown-arrow {
  transform: rotate(180deg);
}
</style>
