<template>
  <div class="exercise-page">
    <div class="container">
      <div class="page-header">
        <h1>✏️ 练习中心</h1>
        <p>通过实战练习巩固所学知识</p>
      </div>

      <div class="exercise-content">
        <!-- 左侧：练习列表 -->
        <div class="exercise-list">
          <div class="filter-bar">
            <select v-model="filterType">
              <option value="">全部类型</option>
              <option value="prompt">提示词练习</option>
              <option value="quiz">知识测验</option>
              <option value="practical">实战任务</option>
            </select>
            <select v-model="filterDifficulty">
              <option value="">全部难度</option>
              <option value="easy">简单</option>
              <option value="medium">中等</option>
              <option value="hard">困难</option>
            </select>
          </div>

          <div class="exercises">
            <div 
              v-for="exercise in filteredExercises" 
              :key="exercise.id"
              class="exercise-card"
              @click="selectExercise(exercise)">
              <div class="exercise-header">
                <span class="type-tag" :class="exercise.type">{{ getTypeLabel(exercise.type) }}</span>
                <span class="difficulty" :class="exercise.difficulty">{{ getDifficultyLabel(exercise.difficulty) }}</span>
              </div>
              
              <h3>{{ exercise.title }}</h3>
              <p>{{ exercise.description }}</p>
              
              <div class="exercise-meta">
                <span>⏱ {{ exercise.duration }} 分钟</span>
                <span>👥 {{ exercise.completedCount }} 人完成</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：当前练习 -->
        <div class="current-exercise" v-if="currentExercise">
          <div class="exercise-detail">
            <h2>{{ currentExercise.title }}</h2>
            <div class="exercise-info">
              <span class="type-tag" :class="currentExercise.type">{{ getTypeLabel(currentExercise.type) }}</span>
              <span class="difficulty" :class="currentExercise.difficulty">{{ getDifficultyLabel(currentExercise.difficulty) }}</span>
            </div>

            <div class="task-description">
              <h3>任务描述</h3>
              <p>{{ currentExercise.task }}</p>
            </div>

            <div class="answer-area">
              <h3>你的答案</h3>
              <textarea 
                v-model="answer" >
                rows="8">
                placeholder="请输入你的答案...">
              ></textarea>
            </div>

            <div class="action-buttons">
              <button class="btn-secondary" @click="saveDraft">保存草稿</button>
              <button class="btn-primary" @click="submitAnswer" :disabled="submitting">
                {{ submitting ? '提交中...' : '提交答案' }}
              </button>
            </div>

            <!-- 评分结果 -->
            <div class="result-panel" v-if="result">
              <div class="score">
                <span class="score-number">{{ result.score }}</span>
                <span class="score-total">/ 10</span>
              </div>
              
              <div class="feedback">
                <h4>AI 评价</h4>
                <p>{{ result.feedback }}</p>
              </div>
              
              <div class="suggestions" v-if="result.suggestions.length">
                <h4>改进建议</h4>
                <ul>
                  <li v-for="(suggestion, index) in result.suggestions" :key="index">{{ suggestion }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="empty-state" v-else>
          <p>选择左侧练习开始答题</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const filterType = ref('')
const filterDifficulty = ref('')
const currentExercise = ref(null)
const answer = ref('')
const submitting = ref(false)
const result = ref(null)

const exercises = ref([
  {
    id: 1,
    title: '优化客服回复',
    description: '学习如何编写高效的客服场景提示词',
    type: 'prompt',
    difficulty: 'easy',
    duration: 15,
    completedCount: 1256,
    task: '请补全以下 Prompt，使其能生成一份专业的客服回复：\n\n"你是一位专业的客服代表，需要回复一位客户关于[问题]的咨询。请用礼貌、专业的语气..."'
  },
  {
    id: 2,
    title: '文案改写大师',
    description: '掌握文案改写的核心技巧',
    type: 'prompt',
    difficulty: 'medium',
    duration: 20,
    completedCount: 892,
    task: '请编写一个 Prompt，将以下口语化的文案改写成专业的商务文案。要求保持原意，提升专业度。'
  },
  {
    id: 3,
    title: 'AI 工具知识测验',
    description: '测试你对主流 AI 工具的了解程度',
    type: 'quiz',
    difficulty: 'easy',
    duration: 10,
    completedCount: 2341,
    task: '请回答：ChatGPT 和 GPT-4 的主要区别是什么？列举至少 3 点。'
  },
  {
    id: 4,
    title: 'Midjourney 提示词编写',
    description: '学习图像生成提示词的编写技巧',
    type: 'practical',
    difficulty: 'hard',
    duration: 30,
    completedCount: 567,
    task: '请编写一个完整的 Midjourney 提示词，生成一张"未来城市日落"的场景图。要求包含：风格、光线、色彩、构图等要素。'
  }
])

const filteredExercises = computed(() => {
  return exercises.value.filter(e => {
    if (filterType.value && e.type !== filterType.value) return false
    if (filterDifficulty.value && e.difficulty !== filterDifficulty.value) return false
    return true
  })
})

const getTypeLabel = (type) => {
  const map = { prompt: '提示词', quiz: '测验', practical: '实战' }
  return map[type] || type
}

const getDifficultyLabel = (difficulty) => {
  const map = { easy: '简单', medium: '中等', hard: '困难' }
  return map[difficulty] || difficulty
}

const selectExercise = (exercise) => {
  currentExercise.value = exercise
  answer.value = ''
  result.value = null
}

const saveDraft = () => {
  localStorage.setItem(`exercise_draft_${currentExercise.value.id}`, answer.value)
  alert('草稿已保存')
}

const submitAnswer = async () => {
  if (!answer.value.trim()) {
    alert('请输入答案')
    return
  }
  
  submitting.value = true
  
  // 模拟 AI 评分
  setTimeout(() => {
    result.value = {
      score: Math.floor(Math.random() * 3) + 7, // 7-10 分
      feedback: '整体表现不错！你的答案涵盖了主要要点，结构清晰。建议在具体案例描述上可以更加详细一些。',
      suggestions: [
        '增加具体的场景描述',
        '可以尝试使用更专业的术语',
        '建议补充实际应用案例'
      ]
    }
    submitting.value = false
  }, 1500)
}
</script>

<style scoped>
.exercise-page {
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

.exercise-content {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 24px;
}

.exercise-list {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.filter-bar select {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  font-size: 14px;
}

.exercises {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.exercise-card {
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.exercise-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.1);
}

.exercise-header {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.type-tag {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.type-tag.prompt {
  background: #e0e7ff;
  color: #4f46e5;
}

.type-tag.quiz {
  background: #fef3c7;
  color: #d97706;
}

.type-tag.practical {
  background: #d1fae5;
  color: #059669;
}

.difficulty {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
}

.difficulty.easy {
  background: #d1fae5;
  color: #059669;
}

.difficulty.medium {
  background: #fef3c7;
  color: #d97706;
}

.difficulty.hard {
  background: #fee2e2;
  color: #dc2626;
}

.exercise-card h3 {
  font-size: 16px;
  margin-bottom: 8px;
}

.exercise-card p {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 12px;
}

.exercise-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #9ca3af;
}

.current-exercise {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.exercise-detail h2 {
  font-size: 24px;
  margin-bottom: 12px;
}

.exercise-info {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.task-description {
  margin-bottom: 24px;
}

.task-description h3 {
  font-size: 16px;
  margin-bottom: 12px;
}

.task-description p {
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.answer-area h3 {
  font-size: 16px;
  margin-bottom: 12px;
}

.answer-area textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin: 24px 0;
}

.btn-primary {
  padding: 12px 24px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 12px 24px;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}

.result-panel {
  margin-top: 32px;
  padding: 24px;
  background: #f9fafb;
  border-radius: 12px;
}

.score {
  text-align: center;
  margin-bottom: 20px;
}

.score-number {
  font-size: 48px;
  font-weight: 700;
  color: #4f46e5;
}

.score-total {
  font-size: 24px;
  color: #9ca3af;
}

.feedback h4,
.suggestions h4 {
  font-size: 16px;
  margin-bottom: 12px;
}

.feedback p {
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 20px;
}

.suggestions ul {
  padding-left: 20px;
}

.suggestions li {
  color: #6b7280;
  margin: 8px 0;
}

.empty-state {
  background: white;
  border-radius: 12px;
  padding: 60px;
  text-align: center;
  color: #9ca3af;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .exercise-content {
    grid-template-columns: 1fr;
  }
}
</style>
