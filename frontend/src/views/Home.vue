<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1>
            <span class="gradient-text">掌握 AI 工具</span>，<br />
            提升 10 倍工作效率
          </h1>
          <p class="hero-desc">
            系统学习 ChatGPT、Midjourney 等主流 AI 工具<br />
            从零基础到熟练应用，让 AI 成为你的得力助手
          </p>
          <div class="hero-actions">
            <router-link to="/courses" class="btn-primary">
              开始学习
              <ArrowRight class="icon" />
            </router-link>
            <router-link to="/prompt-lab" class="btn-secondary">
              试用 Prompt 实验室
            </router-link>
          </div>
        </div>
        <div class="hero-image">
          <div class="floating-cards">
            <div class="card card-1">📝 文案生成</div>
            <div class="card card-2">🎨 图像设计</div>
            <div class="card card-3">💻 代码辅助</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">精品课程</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">10万+</div>
            <div class="stat-label">学员</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">98%</div>
            <div class="stat-label">好评率</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Courses Section -->
    <section class="courses">
      <div class="container">
        <div class="section-header">
          <h2>📚 热门课程</h2>
          <p>精选最实用的 AI 工具课程，助你快速上手</p>
        </div>

        <div class="course-grid">
          <CourseCard
            v-for="course in featuredCourses"
            :key="course.id"
            :course="course"
          />
        </div>

        <div class="section-footer">
          <router-link to="/courses" class="link-arrow">
            查看全部课程
            <ArrowRight />
          </router-link>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="container">
        <div class="cta-content">
          <h2>准备好开始学习了吗？</h2>
          <p>加入我们的学习社区，与 10 万+ 学员一起成长</p>
          <router-link to="/register" class="btn-primary">
            立即注册
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue'
import CourseCard from '@/components/course/CourseCard.vue'
import { getCourses } from '@/api/courses'

const featuredCourses = ref([])

onMounted(async () => {
  try {
    const res = await getCourses({ page_size: 4 })
    featuredCourses.value = res.items
  } catch (error) {
    // 使用示例数据
    featuredCourses.value = [
      {
        id: 1,
        title: 'ChatGPT 从入门到精通',
        description: '系统学习提示词工程，掌握高效使用 ChatGPT 的方法',
        cover_image: '',
        category: 'text',
        student_count: 12500,
        rating: 4.9,
        is_free: true
      },
      {
        id: 2,
        title: 'Midjourney 图像生成完全指南',
        description: '从零开始学习 AI 绘画，创作专业级视觉作品',
        cover_image: '',
        category: 'image',
        student_count: 8300,
        rating: 4.8,
        is_free: false
      },
      {
        id: 3,
        title: 'AI 办公效率提升课',
        description: '用 AI 工具提升 PPT、Excel、文档处理效率',
        cover_image: '',
        category: 'office',
        student_count: 15600,
        rating: 4.7,
        is_free: true
      },
      {
        id: 4,
        title: 'AI 编程助手实战',
        description: '掌握 GitHub Copilot 和通义灵码的使用技巧',
        cover_image: '',
        category: 'code',
        student_count: 6200,
        rating: 4.9,
        is_free: true
      }
    ]
  }
})
</script>

<style scoped>
.hero {
  padding: 80px 0;
  background: linear-gradient(135deg, #f5f7ff 0%, #ffffff 100%);
}

.hero .container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.hero h1 {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 24px;
  color: #111827;
}

.gradient-text {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 18px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.icon {
  width: 20px;
  height: 20px;
  margin-left: 8px;
}

.floating-cards {
  position: relative;
  height: 400px;
}

.card {
  position: absolute;
  background: white;
  padding: 20px 28px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  font-size: 18px;
}

.card-1 {
  top: 20%;
  left: 10%;
  animation: float 3s ease-in-out infinite;
}

.card-2 {
  top: 45%;
  right: 10%;
  animation: float 3s ease-in-out infinite 0.5s;
}

.card-3 {
  bottom: 20%;
  left: 25%;
  animation: float 3s ease-in-out infinite 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.stats {
  background: #1f2937;
  padding: 64px 0;
  color: white;
}

.stats .container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  text-align: center;
}

.stat-number {
  font-size: 48px;
  font-weight: 700;
  background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 16px;
  color: #9ca3af;
  margin-top: 8px;
}

.courses {
  padding: 80px 0;
}

.courses .container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-header h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 12px;
}

.section-header p {
  color: #6b7280;
  font-size: 18px;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 48px;
}

.section-footer {
  text-align: center;
}

.link-arrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #4f46e5;
  font-weight: 600;
  text-decoration: none;
}

.cta {
  padding: 80px 0;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: white;
}

.cta .container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  text-align: center;
}

.cta h2 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
}

.cta p {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 32px;
}

.cta .btn-primary {
  background: white;
  color: #4f46e5;
  padding: 16px 32px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}

@media (max-width: 1024px) {
  .hero .container {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero h1 {
    font-size: 36px;
  }

  .hero-actions {
    justify-content: center;
  }

  .floating-cards {
    display: none;
  }

  .course-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .course-grid {
    grid-template-columns: 1fr;
  }
}
</style>
