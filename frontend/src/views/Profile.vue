<template>
  <div class="profile">
    <div class="container">
      <div class="profile-header">
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" class="avatar" @error="$event.target.src = defaultAvatar" />
          <div class="user-meta">
            <h1>{{ user.username || user.email }}</h1>
            <p>{{ user.email }}</p>
            <div class="user-tags">
              <span class="tag">{{ user.occupation || '学习者' }}</span>
              <span class="tag level">{{ user.ai_level || '入门' }}</span>
            </div>
          </div>
        </div>

        <div class="user-stats">
          <div class="stat-item">
            <div class="stat-value">{{ stats.learningTime }}</div>
            <div class="stat-label">学习时长(小时)</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.completedCourses }}</div>
            <div class="stat-label">完成课程</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.certificates }}</div>
            <div class="stat-label">获得证书</div>
          </div>
        </div>
      </div>

      <div class="profile-content">
        <!-- 左侧导航 -->
        <div class="profile-nav">
          <button 
            v-for="item in navItems" 
            :key="item.key"
            :class="{ active: activeTab === item.key }"
            @click="activeTab = item.key">
            {{ item.label }}
          </button>
        </div>

        <!-- 右侧内容 -->
        <div class="profile-panel">
          <!-- 我的课程 -->
          <div v-if="activeTab === 'courses'" class="tab-content">
            <h2>我的课程</h2>
            <div v-if="myCourses.length === 0" class="empty-state">
              <p>还没有报名任何课程</p>
              <router-link to="/courses" class="btn-primary">去选课</router-link>
            </div>
            
            <div v-else class="course-list">
              <div v-for="course in myCourses" :key="course.id" class="course-item">
                <img :src="course.cover || defaultCover" class="course-thumb" @error="$event.target.src = defaultCover" />
                <div class="course-info">
                  <h3>{{ course.title }}</h3>
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: course.progress + '%' }"></div>
                  </div>
                  <p class="progress-text">已学习 {{ course.progress }}%</p>
                </div>
                
                <router-link :to="`/learn/${course.id}`" class="btn-continue">继续学习</router-link>
              </div>
            </div>
          </div>

          <!-- 账号设置 -->
          <div v-if="activeTab === 'settings'" class="tab-content">
            <h2>账号设置</h2>
            
            <form @submit.prevent="saveSettings">
              <div class="form-group">
                <label>昵称</label>
                <input v-model="settings.username" />
              </div>

              <div class="form-group">
                <label>职业</label>
                <select v-model="settings.occupation">
                  <option value="">请选择</option>
                  <option value="学生">学生</option>
                  <option value="产品经理">产品经理</option>
                  <option value="设计师">设计师</option>
                  <option value="程序员">程序员</option>
                  <option value="运营">运营</option>
                  <option value="其他">其他</option>
                </select>
              </div>

              <div class="form-group">
                <label>AI 水平</label>
                <select v-model="settings.ai_level">
                  <option value="入门">入门</option>
                  <option value="进阶">进阶</option>
                  <option value="高级">高级</option>
                </select>
              </div>

              <div class="form-group">
                <label>学习目标</label>
                <textarea v-model="settings.learning_goal" rows="3"></textarea>
              </div>

              <button type="submit" class="btn-primary">保存修改</button>
            </form>
          </div>

          <!-- 我的证书 -->
          <div v-if="activeTab === 'certificates'" class="tab-content">
            <h2>我的证书</h2>
            <div class="certificate-grid">
              <div v-for="cert in certificates" :key="cert.id" class="certificate-card">
                <div class="cert-icon">🏆</div>
                <h3>{{ cert.title }}</h3>
                <p>获得时间：{{ cert.date }}</p>
                <button class="btn-download">下载证书</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const defaultAvatar = '/default-avatar.svg'
const defaultCover = '/default-course-cover.svg'

const user = ref(userStore.userInfo || {
  email: 'user@example.com',
  username: '学习者',
  occupation: '',
  ai_level: '入门'
})

const stats = ref({
  learningTime: 12.5,
  completedCourses: 3,
  certificates: 2
})

const activeTab = ref('courses')

const navItems = [
  { key: 'courses', label: '我的课程' },
  { key: 'certificates', label: '我的证书' },
  { key: 'settings', label: '账号设置' }
]

const myCourses = ref([
  { id: 1, title: 'ChatGPT 从入门到精通', cover: '', progress: 65 },
  { id: 2, title: 'AI 办公效率提升课', cover: '', progress: 30 },
  { id: 3, title: 'Midjourney 图像生成', cover: '', progress: 100 }
])

const settings = reactive({
  username: user.value.username,
  occupation: user.value.occupation,
  ai_level: user.value.ai_level,
  learning_goal: ''
})

const certificates = ref([
  { id: 1, title: 'ChatGPT 基础认证', date: '2026-03-01' },
  { id: 2, title: 'AI 办公效率认证', date: '2026-02-15' }
])

const saveSettings = () => {
  userStore.setUserInfo({ ...user.value, ...settings })
  alert('设置已保存')
}
</script>

<style scoped>
.profile {
  padding: 40px 0;
  min-height: calc(100vh - 200px);
  background: #f9fafb;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.profile-header {
  background: white;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.user-meta h1 {
  font-size: 24px;
  margin-bottom: 4px;
}

.user-meta p {
  color: #6b7280;
  margin-bottom: 12px;
}

.user-tags {
  display: flex;
  gap: 8px;
}

.tag {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.tag.level {
  background: #fef3c7;
  color: #d97706;
}

.user-stats {
  display: flex;
  gap: 48px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #4f46e5;
}

.stat-label {
  color: #6b7280;
  font-size: 14px;
  margin-top: 4px;
}

.profile-content {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 24px;
}

.profile-nav {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.profile-nav button {
  width: 100%;
  padding: 12px 16px;
  text-align: left;
  background: none;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.profile-nav button:hover,
.profile-nav button.active {
  background: #e0e7ff;
  color: #4f46e5;
}

.profile-panel {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tab-content h2 {
  font-size: 20px;
  margin-bottom: 24px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: #6b7280;
}

.empty-state p {
  margin-bottom: 16px;
}

.course-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.course-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.course-thumb {
  width: 120px;
  height: 72px;
  border-radius: 8px;
  object-fit: cover;
}

.course-info {
  flex: 1;
}

.course-info h3 {
  font-size: 16px;
  margin-bottom: 8px;
}

.progress-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4f46e5;
  border-radius: 4px;
  transition: width 0.3s;
}

.progress-text {
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.btn-continue {
  padding: 10px 20px;
  background: #4f46e5;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
}

.btn-primary {
  padding: 12px 24px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}

.certificate-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.certificate-card {
  text-align: center;
  padding: 32px;
  background: #f9fafb;
  border-radius: 12px;
  border: 2px solid #e0e7ff;
}

.cert-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.certificate-card h3 {
  font-size: 16px;
  margin-bottom: 8px;
}

.certificate-card p {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 16px;
}

.btn-download {
  padding: 8px 16px;
  background: white;
  border: 1px solid #4f46e5;
  color: #4f46e5;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-content {
    grid-template-columns: 1fr;
  }
  
  .certificate-grid {
    grid-template-columns: 1fr;
  }
}
</style>
