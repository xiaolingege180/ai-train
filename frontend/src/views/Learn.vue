<template>
  <div class="learn-page">
    <div class="learn-layout">
      <!-- 左侧：视频播放器 -->
      <div class="video-section">
        <div class="video-player">
          <div class="video-placeholder">
            <VideoPlay class="play-icon" />
            <p>点击播放视频</p>
          </div>
        </div>

        <div class="video-info">
          <h1>{{ currentLesson.title }}</h1>
          <p>{{ course.title }}</p>
        </div>

        <div class="lesson-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.key"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key">
            {{ tab.label }}
          </button>
        </div>

        <div class="lesson-content">
          <div v-if="activeTab === 'content'" class="tab-panel">
            <h3>本节知识点</h3>
            <ul>
              <li v-for="point in currentLesson.points" :key="point">{{ point }}</li>
            </ul>
          </div>

          <div v-if="activeTab === 'notes'" class="tab-panel">
            <textarea 
              v-model="notes"
              placeholder="记录学习笔记..."
              rows="8"
            ></textarea>
            <button class="btn-save" @click="saveNotes">保存笔记</button>
          </div>

          <div v-if="activeTab === 'qa'" class="tab-panel">
            <div class="qa-list">
              <div v-for="qa in qas" :key="qa.id" class="qa-item">
                <div class="question">
                  <span class="q-mark">Q</span>
                  <p>{{ qa.question }}</p>
                </div>
                <div class="answer">
                  <span class="a-mark">A</span>
                  <p>{{ qa.answer }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：课程目录 -->
      <div class="sidebar">
        <div class="course-progress">
          <div class="progress-header">
            <h3>课程进度</h3>
            <span>{{ overallProgress }}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: overallProgress + '%' }"></div>
          </div>
        </div>

        <div class="chapter-list">
          <div v-for="chapter in chapters" :key="chapter.id" class="chapter">
            <div class="chapter-title" @click="chapter.expanded = !chapter.expanded">
              <span class="toggle">{{ chapter.expanded ? '▼' : '▶' }}</span>
              {{ chapter.title }}
            </div>
            
            <div v-show="chapter.expanded" class="lesson-list">
              <div 
                v-for="lesson in chapter.lessons"
                :key="lesson.id"
                :class="['lesson-item', { active: lesson.id === currentLesson.id, completed: lesson.completed }]"
                @click="selectLesson(lesson)"
              >
                <span class="lesson-status">
                  <Check v-if="lesson.completed" class="icon-check" />
                  <VideoPlay v-else class="icon-play" />
                </span>
                <span class="lesson-title">{{ lesson.title }}</span>
                <span class="lesson-duration">{{ lesson.duration }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { VideoPlay, Check } from '@element-plus/icons-vue'

const route = useRoute()
const courseId = route.params.id

const tabs = [
  { key: 'content', label: '课程内容' },
  { key: 'notes', label: '我的笔记' },
  { key: 'qa', label: '常见问题' }
]

const activeTab = ref('content')
const notes = ref('')

const course = ref({
  id: courseId,
  title: 'ChatGPT 从入门到精通'
})

const currentLesson = ref({
  id: 1,
  title: '什么是 ChatGPT',
  points: [
    '了解 ChatGPT 的基本概念和发展历史',
    '理解大语言模型的工作原理',
    '认识 ChatGPT 的应用场景'
  ]
})

const chapters = ref([
  {
    id: 1,
    title: '第一章：ChatGPT 基础',
    expanded: true,
    lessons: [
      { id: 1, title: '什么是 ChatGPT', duration: '10:00', completed: true },
      { id: 2, title: '如何访问和使用', duration: '08:00', completed: true },
      { id: 3, title: '基础对话技巧', duration: '12:00', completed: false }
    ]
  },
  {
    id: 2,
    title: '第二章：提示词工程入门',
    expanded: false,
    lessons: [
      { id: 4, title: '提示词的基本结构', duration: '15:00', completed: false },
      { id: 5, title: '角色设定技巧', duration: '10:00', completed: false },
      { id: 6, title: '上下文管理', duration: '09:00', completed: false }
    ]
  }
])

const qas = ref([
  { id: 1, question: 'ChatGPT 免费版和付费版有什么区别？', answer: '免费版有使用次数限制，付费版(GPT-4)响应更快、能力更强，且可以使用插件功能。' },
  { id: 2, question: '如何写出好的提示词？', answer: '好的提示词应该包含：明确的角色设定、具体的任务描述、清晰的输出格式要求和必要的上下文信息。' }
])

const overallProgress = computed(() => {
  let total = 0
  let completed = 0
  chapters.value.forEach(ch => {
    ch.lessons.forEach(l => {
      total++
      if (l.completed) completed++
    })
  })
  return total > 0 ? Math.round((completed / total) * 100) : 0
})

const selectLesson = (lesson) => {
  currentLesson.value = {
    ...lesson,
    points: ['知识点 1', '知识点 2', '知识点 3']
  }
}

const saveNotes = () => {
  alert('笔记已保存')
}
</script>

<style scoped>
.learn-page {
  height: calc(100vh - 80px);
  overflow: hidden;
}

.learn-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  height: 100%;
}

.video-section {
  overflow-y: auto;
}

.video-player {
  aspect-ratio: 16/9;
  background: #111827;
  position: relative;
}

.video-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
}

.play-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
}

.video-info {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.video-info h1 {
  font-size: 20px;
  margin-bottom: 8px;
}

.video-info p {
  color: #6b7280;
  font-size: 14px;
}

.lesson-tabs {
  display: flex;
  gap: 32px;
  padding: 0 24px;
  border-bottom: 1px solid #e5e7eb;
}

.lesson-tabs button {
  background: none;
  border: none;
  padding: 16px 0;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.lesson-tabs button.active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
}

.lesson-content {
  padding: 24px;
}

.tab-panel h3 {
  font-size: 16px;
  margin-bottom: 16px;
}

.tab-panel ul {
  padding-left: 24px;
}

.tab-panel li {
  margin: 8px 0;
  color: #374151;
}

.tab-panel textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 16px;
}

.btn-save {
  padding: 10px 20px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.qa-item {
  margin-bottom: 24px;
}

.question,
.answer {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}

.q-mark,
.a-mark {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.q-mark {
  background: #4f46e5;
  color: white;
}

.a-mark {
  background: #10b981;
  color: white;
}

.question p {
  font-weight: 500;
}

.answer p {
  color: #6b7280;
}

.sidebar {
  background: #f9fafb;
  border-left: 1px solid #e5e7eb;
  overflow-y: auto;
}

.course-progress {
  padding: 20px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.progress-header h3 {
  font-size: 14px;
}

.progress-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4f46e5;
  border-radius: 3px;
  transition: width 0.3s;
}

.chapter {
  border-bottom: 1px solid #e5e7eb;
}

.chapter-title {
  padding: 16px 20px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.chapter-title:hover {
  background: #f3f4f6;
}

.toggle {
  color: #9ca3af;
  font-size: 12px;
}

.lesson-item {
  padding: 12px 20px 12px 48px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
}

.lesson-item:hover {
  background: #f3f4f6;
}

.lesson-item.active {
  background: #e0e7ff;
  color: #4f46e5;
}

.lesson-item.completed {
  color: #374151;
}

.lesson-status {
  display: flex;
  align-items: center;
}

.icon-check {
  width: 18px;
  height: 18px;
  color: #10b981;
}

.icon-play {
  width: 18px;
  height: 18px;
}

.lesson-title {
  flex: 1;
}

.lesson-duration {
  font-size: 12px;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .learn-layout {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    display: none;
  }
}
</style>
