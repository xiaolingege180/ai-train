<template>
  <div class="courses-page">
    <div class="container">
      <div class="page-header">
        <h1>📚 全部课程</h1>
        <p>系统学习 AI 工具，提升工作效率</p>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <div class="search-box">
          <input v-model="searchQuery" placeholder="搜索课程..." @keyup.enter="handleSearch" />
          <button @click="handleSearch">搜索</button>
        </div>
        <div class="filters">
          <select v-model="selectedCategory" @change="handleFilter">
            <option value="">全部分类</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
          <select v-model="selectedDifficulty" @change="handleFilter">
            <option value="">全部难度</option>
            <option value="beginner">入门</option>
            <option value="intermediate">进阶</option>
            <option value="advanced">高级</option>
          </select>
          <select v-model="selectedSort" @change="handleFilter">
            <option value="popularity">最受欢迎</option>
            <option value="newest">最新发布</option>
            <option value="rating">评分最高</option>
          </select>
        </div>
      </div>

      <!-- 课程列表 -->
      <div class="course-grid">
        <CourseCard v-for="course in courses" :key="course.id" :course="course" />
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <button :disabled="page <= 1" @click="page--">上一页</button>
        <span>第 {{ page }} 页</span>
        <button @click="page++">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import CourseCard from '@/components/course/CourseCard.vue'
import { getCourses, getCategories } from '@/api/courses'

const courses = ref([])
const categories = ref([])
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedDifficulty = ref('')
const selectedSort = ref('popularity')
const page = ref(1)

const loadCourses = async () => {
  try {
    const res = await getCourses({
      category: selectedCategory.value,
      difficulty: selectedDifficulty.value,
      search: searchQuery.value,
      sort: selectedSort.value,
      page: page.value
    })
    courses.value = res.items
  } catch (error) {
    // 示例数据
    courses.value = [
      { id: 1, title: 'ChatGPT 从入门到精通', description: '系统学习提示词工程', cover_image: '', category: 'text', difficulty: 'beginner', student_count: 12500, rating: 4.9, is_free: true },
      { id: 2, title: 'Midjourney 图像生成完全指南', description: '从零开始学习 AI 绘画', cover_image: '', category: 'image', difficulty: 'intermediate', student_count: 8300, rating: 4.8, is_free: false },
      { id: 3, title: 'AI 办公效率提升课', description: '用 AI 工具提升 PPT、Excel、文档处理效率', cover_image: '', category: 'office', difficulty: 'beginner', student_count: 15600, rating: 4.7, is_free: true },
      { id: 4, title: 'AI 编程助手实战', description: '掌握 GitHub Copilot 和通义灵码的使用技巧', cover_image: '', category: 'code', difficulty: 'intermediate', student_count: 6200, rating: 4.9, is_free: true }
    ]
  }
}

const loadCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res
  } catch (error) {
    categories.value = [
      { id: 'text', name: '文本生成' },
      { id: 'image', name: '图像生成' },
      { id: 'video', name: '视频创作' },
      { id: 'office', name: '办公效率' },
      { id: 'code', name: '代码辅助' },
      { id: 'data', name: '数据分析' }
    ]
  }
}

const handleSearch = () => {
  page.value = 1
  loadCourses()
}

const handleFilter = () => {
  page.value = 1
  loadCourses()
}

watch(page, loadCourses)

onMounted(() => {
  loadCourses()
  loadCategories()
})
</script>

<style scoped>
.courses-page {
  padding: 40px 0;
  min-height: calc(100vh - 200px);
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

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.search-box {
  display: flex;
  gap: 8px;
}

.search-box input {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  width: 280px;
}

.search-box button {
  padding: 10px 20px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.filters {
  display: flex;
  gap: 12px;
}

.filters select {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.pagination button {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .course-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .course-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box input {
    width: 100%;
  }
  
  .filters {
    flex-wrap: wrap;
  }
}
</style>
