<template>
  <div class="community">
    <div class="container">
      <div class="page-header">
        <h1>💬 学习社区</h1>
        <p>交流心得，分享经验，共同进步</p>
      </div>

      <div class="community-layout">
        <!-- 左侧：帖子列表 -->
        <div class="main-content">
          <!-- 发布框 -->
          <div class="post-box">
            <input 
              v-model="newPost.title"
              placeholder="分享你的学习心得..."
              class="post-title-input"
            />
            <textarea 
              v-model="newPost.content"
              placeholder="详细描述你的问题或经验..."
              rows="3"
            ></textarea>
            
            <div class="post-actions">
              <select v-model="newPost.category">
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
              <button class="btn-primary" @click="publishPost">发布</button>
            </div>
          </div>

          <!-- 帖子列表 -->
          <div class="post-list">
            <div v-for="post in posts" :key="post.id" class="post-card">
              <div class="post-header">
                <img :src="post.author.avatar || defaultAvatar" class="avatar" @error="$event.target.src = defaultAvatar" />
                <div class="post-meta">
                  <span class="username">{{ post.author.username }}</span>
                  <span class="time">{{ post.created_at }}</span>
                  <span class="category-tag">{{ post.category }}</span>
                </div>
              </div>
              
              <h3 class="post-title">{{ post.title }}</h3>
              <p class="post-content">{{ post.content }}</p>
              
              <div class="post-stats">
                <span @click="likePost(post)">👍 {{ post.likes }}</span>
                <span>💬 {{ post.comments }}</span>
                <span>👁 {{ post.views }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：侧边栏 -->
        <div class="sidebar">
          <!-- 热门话题 -->
          <div class="widget">
            <h3>🔥 热门话题</h3>
            <ul>
              <li v-for="topic in hotTopics" :key="topic.id">
                <span class="rank">{{ topic.rank }}</span>
                <span class="name">{{ topic.name }}</span>
              </li>
            </ul>
          </div>

          <!-- 社区公告 -->
          <div class="widget">
            <h3>📢 社区公告</h3>
            <ul class="notice-list">
              <li v-for="notice in notices" :key="notice.id">{{ notice.title }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const defaultAvatar = '/default-avatar.svg'

const newPost = ref({
  title: '',
  content: '',
  category: 'share'
})

const categories = [
  { id: 'share', name: '经验分享' },
  { id: 'question', name: '提问求助' },
  { id: 'discussion', name: '讨论交流' },
  { id: 'showcase', name: '作品展示' }
]

const posts = ref([
  {
    id: 1,
    title: '分享一个超实用的 ChatGPT 提示词模板',
    content: '最近在做内容运营，整理了一套小红书文案生成提示词，效果特别好。分享给大家...',
    author: { username: '张三', avatar: '' },
    category: '经验分享',
    created_at: '2小时前',
    likes: 156,
    comments: 23,
    views: 1200
  },
  {
    id: 2,
    title: 'Midjourney 生成的人物总是不够真实，求指导',
    content: '我尝试用 Midjourney 生成逼真的人物照片，但总觉得有点假，有什么技巧吗？',
    author: { username: '李四', avatar: '' },
    category: '提问求助',
    created_at: '5小时前',
    likes: 45,
    comments: 18,
    views: 560
  },
  {
    id: 3,
    title: '用 AI 工具一周完成了一个月的工作量',
    content: '分享一下我是如何用 ChatGPT + Copilot 提升工作效率的真实案例...',
    author: { username: '王五', avatar: '' },
    category: '经验分享',
    created_at: '1天前',
    likes: 289,
    comments: 45,
    views: 2300
  }
])

const hotTopics = [
  { id: 1, rank: 1, name: 'ChatGPT 提示词技巧' },
  { id: 2, rank: 2, name: 'Midjourney 最新功能' },
  { id: 3, rank: 3, name: 'AI 辅助编程' },
  { id: 4, rank: 4, name: 'AI 绘画创作' },
  { id: 5, rank: 5, name: '办公效率提升' }
]

const notices = [
  { id: 1, title: '🎉 社区上线一周年活动开始啦！' },
  { id: 2, title: '📚 新增《AI 视频创作》课程' },
  { id: 3, title: '🔧 系统维护通知：本周日凌晨 2-4 点' }
]

const publishPost = () => {
  if (!newPost.value.title || !newPost.value.content) {
    alert('请填写标题和内容')
    return
  }
  
  const cat = categories.find(c => c.id === newPost.value.category)
  
  posts.value.unshift({
    id: Date.now(),
    title: newPost.value.title,
    content: newPost.value.content,
    author: { username: '我', avatar: '' },
    category: cat ? cat.name : '分享',
    created_at: '刚刚',
    likes: 0,
    comments: 0,
    views: 0
  })
  
  newPost.value = { title: '', content: '', category: 'share' }
  alert('发布成功！')
}

const likePost = (post) => {
  post.likes++
}
</script>

<style scoped>
.community {
  padding: 40px 0;
  min-height: calc(100vh - 200px);
  background: #f9fafb;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 32px;
  margin-bottom: 12px;
}

.page-header p {
  color: #6b7280;
}

.community-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.post-box {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.post-title-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  margin-bottom: 12px;
}

.post-box textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
  margin-bottom: 12px;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-actions select {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
}

.btn-primary {
  background: #4f46e5;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.post-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.username {
  font-weight: 600;
  color: #111827;
}

.time {
  font-size: 12px;
  color: #9ca3af;
}

.category-tag {
  font-size: 12px;
  color: #4f46e5;
  background: #e0e7ff;
  padding: 2px 8px;
  border-radius: 4px;
  width: fit-content;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  cursor: pointer;
}

.post-title:hover {
  color: #4f46e5;
}

.post-content {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 16px;
}

.post-stats {
  display: flex;
  gap: 24px;
  color: #9ca3af;
  font-size: 14px;
}

.post-stats span {
  cursor: pointer;
  transition: color 0.2s;
}

.post-stats span:hover {
  color: #4f46e5;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.widget {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.widget h3 {
  font-size: 16px;
  margin-bottom: 16px;
}

.widget ul {
  list-style: none;
  padding: 0;
}

.widget li {
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  align-items: center;
  gap: 12px;
}

.widget li:last-child {
  border-bottom: none;
}

.rank {
  width: 24px;
  height: 24px;
  background: #f3f4f6;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.rank:first-child {
  background: #fef3c7;
  color: #d97706;
}

.notice-list li {
  color: #6b7280;
  font-size: 14px;
}

@media (max-width: 768px) {
  .community-layout {
    grid-template-columns: 1fr;
  }
}
</style>
