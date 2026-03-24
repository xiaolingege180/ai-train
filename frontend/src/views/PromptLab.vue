<template>
  <div class="prompt-lab">
    <div class="container">
      <div class="page-header">
        <h1>🧪 Prompt 实验室</h1>
        <p>输入提示词，即时预览 AI 输出效果，学习和优化你的 Prompt 技巧</p>
      </div>

      <!-- 模型选择 -->
      <div class="model-selector">
        <label>选择 AI 模型：</label>
        <div class="model-options">
          <button 
            v-for="m in availableModels" 
            :key="m.id"
            :class="['model-btn', { active: selectedModel === m.id, disabled: !m.available }]"
            @click="m.available && (selectedModel = m.id)"
            :disabled="!m.available"
          >
            <span class="model-name">{{ m.name }}</span>
            <span class="model-provider">{{ getProviderLabel(m.provider) }}</span>
            <span v-if="!m.available" class="model-unavailable">未配置</span>
          </button>
        </div>
      </div>

      <div class="lab-interface">
        <!-- 左侧：输入区 -->
        <div class="input-section">
          <div class="section-header">
            <h3>📝 提示词输入</h3>
            <div class="templates">
              <select v-model="selectedTemplate" @change="applyTemplate">
                <option value="">📋 选择模板</option>
                <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.category }} - {{ t.name }}</option>
              </select>
            </div>
          </div>
          
          <div class="input-area">
            <textarea 
              v-model="prompt"
              placeholder="请输入你的提示词...&#10;例如：帮我写一封感谢客户的邮件，表达对他们长期支持的感激之情"
              rows="14"
              @keydown.ctrl.enter="runPrompt"
              :disabled="streaming"
            ></textarea>
            <div class="input-hint">
              💡 按 Ctrl + Enter 快速运行
              <span v-if="selectedModel" class="selected-model">
                · {{ getModelName(selectedModel) }}
              </span>
            </div>
          </div>
          
          <div class="input-actions">
            <button class="btn-secondary" @click="clear" :disabled="streaming">
              <span class="icon">🗑️</span> 清空
            </button>
            <button 
              class="btn-primary" 
              @click="streaming ? stopStream() : runPrompt()" 
              :disabled="!prompt.trim() || loadingModels"
            >
              <span class="icon">{{ streaming ? '⏹️' : '▶️' }}</span>
              {{ streaming ? '停止' : (loading ? '生成中...' : '运行') }}
            </button>
          </div>
        </div>

        <!-- 右侧：输出区 -->
        <div class="output-section">
          <div class="section-header">
            <h3>🤖 AI 输出</h3>
            <div class="output-actions" v-if="output">
              <span v-if="!streaming" class="meta-info">{{ selectedModel }} · {{ output.length }} 字符</span>
              <span v-else class="streaming-indicator">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
                生成中
              </span>
              <button class="btn-copy" @click="copyOutput" :disabled="streaming">
                <span class="icon">📋</span> 复制
              </button>
            </div>
          </div>
          
          <div class="output-content" v-if="output">
            <div class="output-text" v-html="formattedOutput"></div>
          </div>
          
          <div class="output-placeholder" v-else>
            <div class="placeholder-icon">🤖</div>
            <p>在左侧输入提示词，点击"运行"查看 AI 输出</p>
            <div class="quick-tips">
              <h4>💡 提示技巧：</h4>
              <ul>
                <li>明确说明你想要什么</li>
                <li>提供足够的上下文信息</li>
                <li>指定输出格式（列表、表格等）</li>
                <li>使用角色设定获得更专业的回复</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 历史记录 -->
      <div class="history-section" v-if="history.length > 0">
        <div class="history-header">
          <h3>📜 历史记录</h3>
          <button class="btn-clear" @click="clearHistory">清空历史</button>
        </div>
        <div class="history-list">
          <div 
            v-for="(item, index) in history" 
            :key="index"
            class="history-item"
            @click="loadHistory(item)"
          >
            <div class="history-content">
              <div class="history-prompt">{{ item.prompt.substring(0, 60) }}...</div>
              <div class="history-meta">
                <span class="model-tag">{{ item.model }}</span>
                <span class="time">{{ formatTime(item.time) }}</span>
              </div>
            </div>
            <button class="btn-delete" @click.stop="deleteHistory(index)">×</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '@/api'

// 状态
const prompt = ref('')
const output = ref('')
const loading = ref(false)
const streaming = ref(false)
const selectedModel = ref('')
const models = ref([])
const loadingModels = ref(false)
const selectedTemplate = ref('')
const history = ref([])
const abortController = ref(null)

// 模板列表
const templates = [
  { id: 'rewrite', name: '文案改写', category: '写作', prompt: '请改写以下文案，使其更专业、更有吸引力：\n\n[在此输入文案]' },
  { id: 'email', name: '邮件生成', category: '办公', prompt: '请帮我写一封正式的商务邮件。\n主题：[主题]\n收件人：[姓名]\n目的：[说明目的]' },
  { id: 'summary', name: '内容摘要', category: '效率', prompt: '请总结以下内容的要点：\n\n[在此输入内容]' },
  { id: 'brainstorm', name: '头脑风暴', category: '创意', prompt: '请围绕"[主题]"进行头脑风暴，给出 10 个创意点子。' },
  { id: 'code-review', name: '代码审查', category: '编程', prompt: '请审查以下代码，指出潜在问题并提供改进建议：\n\n```\n[在此粘贴代码]\n```' },
  { id: 'explain', name: '概念解释', category: '学习', prompt: '请用简单易懂的语言解释"[概念]"，适合初学者理解。' },
  { id: 'sql', name: 'SQL生成', category: '编程', prompt: '请根据以下需求生成SQL查询语句：\n需求：[描述查询需求]' }
]

// 计算可用模型
const availableModels = computed(() => {
  return models.value.filter(m => m.available)
})

// 计算格式化输出
const formattedOutput = computed(() => {
  if (!output.value) return ''
  return output.value
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="code-block"><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/## (.*)/g, '<h3>$1</h3>')
    .replace(/### (.*)/g, '<h4>$1</h4>')
    .replace(/\n/g, '<br>')
})

// 获取提供商标签
const getProviderLabel = (provider) => {
  const labels = {
    'openai': 'OpenAI',
    'anthropic': 'Anthropic',
    'moonshot': 'Moonshot',
    'dashscope': '阿里云',
    'doubao': '字节跳动'
  }
  return labels[provider] || provider
}

// 获取模型名称
const getModelName = (modelId) => {
  const model = models.value.find(m => m.id === modelId)
  return model ? model.name : modelId
}

// 加载模型列表
const loadModels = async () => {
  loadingModels.value = true
  try {
    const res = await api.get('/ai-lab/models')
    models.value = res
    // 自动选择第一个可用模型
    const firstAvailable = res.find(m => m.available)
    if (firstAvailable && !selectedModel.value) {
      selectedModel.value = firstAvailable.id
    }
  } catch (error) {
    console.error('加载模型列表失败', error)
  } finally {
    loadingModels.value = false
  }
}

// 应用模板
const applyTemplate = () => {
  const t = templates.find(t => t.id === selectedTemplate.value)
  if (t) {
    prompt.value = t.prompt
  }
}

// 运行Prompt（流式）
const runPrompt = async () => {
  if (!prompt.value.trim() || loading.value || streaming.value) return
  if (!selectedModel.value) {
    alert('请先选择一个AI模型')
    return
  }
  
  loading.value = true
  streaming.value = true
  output.value = ''
  
  // 创建 AbortController 用于取消请求
  abortController.value = new AbortController()
  
  try {
    const response = await fetch('/api/v1/ai-lab/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
      },
      body: JSON.stringify({
        prompt: prompt.value,
        model: selectedModel.value,
        temperature: 0.7,
        max_tokens: 2000,
        stream: true
      }),
      signal: abortController.value.signal
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '请求失败')
    }
    
    // 读取流式响应
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data === '[DONE]') {
            streaming.value = false
            break
          }
          try {
            const json = JSON.parse(data)
            if (json.content) {
              output.value += json.content
            }
            if (json.error) {
              output.value += `\n\n❌ 错误：${json.error}`
              streaming.value = false
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    }
    
    // 添加到历史
    if (output.value && !output.value.includes('❌')) {
      history.value.unshift({
        prompt: prompt.value,
        output: output.value,
        model: selectedModel.value,
        time: new Date()
      })
      
      // 限制历史记录数量
      if (history.value.length > 20) {
        history.value = history.value.slice(0, 20)
      }
      
      // 保存到本地存储
      saveHistory()
    }
    
  } catch (error) {
    if (error.name === 'AbortError') {
      output.value += '\n\n[已停止生成]'
    } else {
      output.value = `❌ 请求失败：${error.message || '请稍后重试'}`
    }
  } finally {
    loading.value = false
    streaming.value = false
    abortController.value = null
  }
}

// 停止生成
const stopStream = () => {
  if (abortController.value) {
    abortController.value.abort()
  }
}

// 清空
const clear = () => {
  prompt.value = ''
  output.value = ''
  selectedTemplate.value = ''
}

// 复制输出
const copyOutput = () => {
  navigator.clipboard.writeText(output.value)
  alert('已复制到剪贴板')
}

// 加载历史
const loadHistory = (item) => {
  prompt.value = item.prompt
  output.value = item.output
  selectedModel.value = item.model
}

// 删除单条历史
const deleteHistory = (index) => {
  history.value.splice(index, 1)
  saveHistory()
}

// 清空历史
const clearHistory = () => {
  if (confirm('确定要清空所有历史记录吗？')) {
    history.value = []
    localStorage.removeItem('prompt_lab_history')
  }
}

// 保存历史到本地存储
const saveHistory = () => {
  localStorage.setItem('prompt_lab_history', JSON.stringify(history.value))
}

// 加载本地存储的历史
const loadLocalHistory = () => {
  const saved = localStorage.getItem('prompt_lab_history')
  if (saved) {
    try {
      history.value = JSON.parse(saved)
    } catch (e) {
      console.error('加载历史失败', e)
    }
  }
}

// 格式化时间
const formatTime = (date) => {
  const d = new Date(date)
  return d.toLocaleString('zh-CN', { 
    month: 'short', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 初始化
onMounted(() => {
  loadModels()
  loadLocalHistory()
})

// 清理
onUnmounted(() => {
  if (abortController.value) {
    abortController.value.abort()
  }
})
</script>

<style scoped>
.prompt-lab {
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
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}

.page-header p {
  color: #6b7280;
}

/* 模型选择 */
.model-selector {
  background: white;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.model-selector label {
  font-weight: 600;
  margin-bottom: 12px;
  display: block;
}

.model-options {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.model-btn {
  flex: 1;
  min-width: 150px;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  position: relative;
}

.model-btn:hover:not(:disabled) {
  border-color: #4f46e5;
}

.model-btn.active {
  border-color: #4f46e5;
  background: #eef2ff;
}

.model-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f9fafb;
}

.model-name {
  display: block;
  font-weight: 600;
  font-size: 16px;
  margin-bottom: 4px;
}

.model-provider {
  display: block;
  font-size: 12px;
  color: #6b7280;
}

.model-unavailable {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 10px;
  background: #e5e7eb;
  color: #6b7280;
  padding: 2px 6px;
  border-radius: 4px;
}

/* 实验室界面 */
.lab-interface {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 40px;
}

.input-section,
.output-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
}

.templates select {
  padding: 8px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  font-size: 14px;
}

/* 输入区域 */
.input-area {
  position: relative;
}

textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.2s;
}

textarea:focus {
  outline: none;
  border-color: #4f46e5;
}

textarea:disabled {
  background: #f9fafb;
  cursor: not-allowed;
}

.input-hint {
  position: absolute;
  bottom: 8px;
  right: 12px;
  font-size: 12px;
  color: #9ca3af;
}

.selected-model {
  color: #4f46e5;
  font-weight: 500;
}

.input-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  justify-content: flex-end;
}

.btn-primary {
  background: #4f46e5;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #4338ca;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 输出区域 */
.output-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.meta-info {
  font-size: 12px;
  color: #9ca3af;
}

.streaming-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #4f46e5;
}

.dot {
  width: 6px;
  height: 6px;
  background: #4f46e5;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.btn-copy {
  background: #e0e7ff;
  color: #4f46e5;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: background 0.2s;
}

.btn-copy:hover:not(:disabled) {
  background: #c7d2fe;
}

.btn-copy:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.output-content {
  min-height: 350px;
  max-height: 500px;
  overflow-y: auto;
}

.output-text {
  line-height: 1.8;
  color: #374151;
}

.output-text :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
}

.output-text :deep(code) {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  color: #4f46e5;
}

.output-text :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.output-text :deep(h3) {
  font-size: 18px;
  margin: 16px 0 8px;
  color: #111827;
}

.output-text :deep(h4) {
  font-size: 16px;
  margin: 12px 0 6px;
  color: #1f2937;
}

.output-text :deep(strong) {
  color: #111827;
}

.output-placeholder {
  min-height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  text-align: center;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.quick-tips {
  margin-top: 32px;
  text-align: left;
  background: #f9fafb;
  padding: 16px 20px;
  border-radius: 8px;
}

.quick-tips h4 {
  margin-bottom: 12px;
  color: #374151;
}

.quick-tips ul {
  list-style: none;
  padding: 0;
}

.quick-tips li {
  padding: 6px 0;
  padding-left: 20px;
  position: relative;
  font-size: 14px;
}

.quick-tips li::before {
  content: "•";
  position: absolute;
  left: 6px;
  color: #4f46e5;
}

/* 历史记录 */
.history-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.history-header h3 {
  font-size: 18px;
}

.btn-clear {
  background: none;
  border: none;
  color: #ef4444;
  font-size: 13px;
  cursor: pointer;
  padding: 4px 8px;
}

.btn-clear:hover {
  text-decoration: underline;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.history-item:hover {
  background: #f3f4f6;
}

.history-content {
  flex: 1;
  min-width: 0;
}

.history-prompt {
  font-size: 14px;
  color: #374151;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #9ca3af;
}

.model-tag {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}

.btn-delete {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 20px;
  cursor: pointer;
  padding: 0 8px;
  line-height: 1;
}

.btn-delete:hover {
  color: #ef4444;
}

@media (max-width: 768px) {
  .lab-interface {
    grid-template-columns: 1fr;
  }
  
  .model-options {
    flex-direction: column;
  }
  
  .model-btn {
    width: 100%;
  }
}
</style>
