<template>
  <div class="course-detail">
    <div class="container" v-if="course">
      <!-- 课程头部 -->
      <div class="course-header">
        <div class="course-cover">
          <img :src="course.cover_image || defaultCover" :alt="course.title" @error="$event.target.src = defaultCover" />
        </div>
        <div class="course-info">
          <div class="category-tag">{{ getCategoryName(course.category) }}</div>
          <h1>{{ course.title }}</h1>
          <p class="description">{{ course.description }}</p>
          
          <div class="meta">
            <span>⭐ {{ course.rating }} ({{ course.rating_count }} 评价)</span>
            <span>👥 {{ formatNumber(course.student_count) }} 人学习</span>
            <span v-if="course.is_free" class="free-tag">免费</span>
            <span v-else class="price">¥{{ course.price }}</span>
          </div>
          
          <button class="enroll-btn" @click="enroll">立即学习</button>
        </div>
      </div>

      <!-- 课程内容 -->
      <div class="course-content">
        <div class="content-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.key"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- 课程目录 -->
        <div v-if="activeTab === 'catalog'" class="tab-panel">
          <div v-for="chapter in chapters" :key="chapter.id" class="chapter">
            <h3>{{ chapter.title }}</h3>
            <div class="lessons">
              <div 
                v-for="lesson in chapter.lessons" 
                :key="lesson.id"
                class="lesson"
                @click="goToLesson(lesson.id)"
              >
                <span class="lesson-number">{{ lesson.order }}</span>
                <span class="lesson-title">{{ lesson.title }}</span>
                <span class="lesson-duration">{{ formatDuration(lesson.duration) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 课程介绍 -->
        <div v-if="activeTab === 'intro'" class="tab-panel">
          <div class="intro-content">
            <h3>课程简介</h3>
            <p>{{ course.description }}</p>
            
            <h3>你将学到</h3>
            <ul>
              <li>掌握 AI 工具的核心使用方法</li>
              <li>学会编写高效的提示词</li>
              <li>提升工作效率 10 倍以上</li>
              <li>获得实际项目经验</li>
            </ul>
          </div>
        </div>

        <!-- 评价 -->
        <div v-if="activeTab === 'reviews'" class="tab-panel">
          <div class="reviews-list">
            <div v-for="review in reviews" :key="review.id" class="review-item">
              <div class="review-header">
                <img :src="review.avatar || defaultAvatar" class="avatar" @error="$event.target.src = defaultAvatar" />
                <div class="review-meta">
                  <div class="username">{{ review.username }}</div>
                  <div class="rating">{{ '⭐'.repeat(review.rating) }}</div>
                </div>
              </div>
              <p class="review-content">{{ review.content }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const courseId = route.params.id

const course = ref(null)
const chapters = ref([])
const reviews = ref([])
const activeTab = ref('catalog')

const tabs = [
  { key: 'catalog', label: '课程目录' },
  { key: 'intro', label: '课程介绍' },
  { key: 'reviews', label: '学员评价' }
]

const defaultCover = '/default-course-cover.svg'
const defaultAvatar = '/default-avatar.svg'

const categoryMap = {
  text: '文本生成',
  image: '图像生成',
  video: '视频创作',
  office: '办公效率',
  code: '代码辅助',
  data: '数据分析'
}

const getCategoryName = (id) => categoryMap[id] || id

const formatNumber = (num) => {
  if (num >= 10000) return (num / 10000).toFixed(1) + '万'
  return num
}

const formatDuration = (seconds) => {
  const mins = Math.floor(seconds / 60)
  return `${mins} 分钟`
}

const enroll = () => {
  router.push(`/learn/${courseId}`)
}

const goToLesson = (lessonId) => {
  router.push(`/learn/${courseId}/lesson/${lessonId}`)
}

onMounted(() => {
  // 示例数据
  course.value = {
    id: courseId,
    title: 'ChatGPT 从入门到精通',
    description: '系统学习提示词工程，掌握高效使用 ChatGPT 的方法。本课程将从基础概念讲起，逐步深入到高级技巧，帮助你成为提示词专家。',
    cover_image: '',
    category: 'text',
    difficulty: 'beginner',
    price: 0,
    is_free: true,
    rating: 4.9,
    rating_count: 1200,
    student_count: 12500
  }
  
  chapters.value = [
    {
      id: 1,
      title: '第一章：ChatGPT 基础',
      lessons: [
        { id: 1, title: '什么是 ChatGPT', duration: 600, order: 1 },
        { id: 2, title: '如何访问和使用', duration: 480, order: 2 },
        { id: 3, title: '基础对话技巧', duration: 720, order: 3 }
      ]
    },
    {
      id: 2,
      title: '第二章：提示词工程入门',
      lessons: [
        { id: 4, title: '提示词的基本结构', duration: 900, order: 1 },
        { id: 5, title: '角色设定技巧', duration: 600, order: 2 },
        { id: 6, title: '上下文管理', duration: 540, order: 3 }
      ]
    }
  ]
  
  reviews.value = [
    { id: 1, username: '张三', avatar: '', rating: 5, content: '非常棒的课程，学到了很多实用的技巧！' },
    { id: 2, username: '李四', avatar: '', rating: 5, content: '老师讲解很清晰，案例也很实用。' },
    { id: 3, username: '王五', avatar: '', rating: 4, content: '内容很丰富，希望能有更多实战案例。' }
  ]
})
</script>

<style scoped>
.course-detail {
  padding: 40px 0;
  min-height: calc(100vh - 200px);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.course-header {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.course-cover img {
  width: 100%;
  border-radius: 12px;
  aspect-ratio: 16/9;
  object-fit: cover;
}

.course-info {
  display: flex;
  flex-direction: column;
}

.category-tag {
  display: inline-block;
  background: #e0e7ff;
  color: #4f46e5;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  width: fit-content;
  margin-bottom: 16px;
}

.course-info h1 {
  font-size: 28px;
  margin-bottom: 16px;
  line-height: 1.3;
}

.description {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 24px;
}

.meta {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.meta span {
  color: #374151;
}

.free-tag {
  background: #10b981;
  color: white !important;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.price {
  color: #ef4444 !important;
  font-weight: 600;
  font-size: 24px;
}

.enroll-btn {
  background: #4f46e5;
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: auto;
  width: fit-content;
}

.enroll-btn:hover {
  background: #4338ca;
}

.course-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.content-tabs {
  display: flex;
  gap: 32px;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.content-tabs button {
  background: none;
  border: none;
  padding: 12px 0;
  font-size: 16px;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.content-tabs button.active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
}

.chapter {
  margin-bottom: 24px;
}

.chapter h3 {
  font-size: 18px;
  margin-bottom: 12px;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.lessons {
  padding-left: 16px;
}

.lesson {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.lesson:hover {
  background: #f3f4f6;
}

.lesson-number {
  width: 28px;
  height: 28px;
  background: #e0e7ff;
  color: #4f46e5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.lesson-title {
  flex: 1;
}

.lesson-duration {
  color: #9ca3af;
  font-size: 14px;
}

.intro-content h3 {
  font-size: 20px;
  margin: 24px 0 12px;
}

.intro-content p {
  color: #6b7280;
  line-height: 1.8;
}

.intro-content ul {
  padding-left: 24px;
}

.intro-content li {
  color: #6b7280;
  margin: 8px 0;
}

.review-item {
  padding: 20px 0;
  border-bottom: 1px solid #e5e7eb;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.username {
  font-weight: 600;
}

.rating {
  color: #f59e0b;
}

.review-content {
  color: #6b7280;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .course-header {
    grid-template-columns: 1fr;
  }
}
</style>
