<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-box">
        <div class="auth-header">
          <h1>创建账号</h1>
          <p>开始你的 AI 学习之旅</p>
        </div>

        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>邮箱</label>
            <input 
              v-model="form.email"
              type="email"
              placeholder="请输入邮箱"
              required
            />
          </div>

          <div class="form-group">
            <label>密码</label>
            <input 
              v-model="form.password"
              type="password"
              placeholder="至少 8 位字符"
              required
              minlength="8"
            />
          </div>

          <div class="form-group">
            <label>确认密码</label>
            <input 
              v-model="form.confirmPassword"
              type="password"
              placeholder="再次输入密码"
              required
            />
          </div>

          <div class="form-options">
            <label class="agreement">
              <input type="checkbox" v-model="form.agree" required />
              我已阅读并同意 <a href="#">用户协议</a> 和 <a href="#">隐私政策</a>
            </label>
          </div>

          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>

        <div class="divider">
          <span>或</span>
        </div>

        <div class="social-login">
          <button class="btn-social">
            <span class="icon">📧</span> Google 注册
          </button>
        </div>

        <div class="auth-footer">
          <p>已有账号？ <router-link to="/login">立即登录</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'

const router = useRouter()

const form = ref({
  email: '',
  password: '',
  confirmPassword: '',
  agree: false
})

const loading = ref(false)

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  
  try {
    const result = await register({
      username: form.value.email.split('@')[0],
      email: form.value.email,
      password: form.value.password,
      confirm_password: form.value.confirmPassword
    })
    
    alert('注册成功！请登录')
    router.push('/login')
  } catch (error) {
    alert(error.message || '注册失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  background: #f9fafb;
}

.auth-container {
  width: 100%;
  max-width: 420px;
}

.auth-box {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.auth-header p {
  color: #6b7280;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #4f46e5;
}

.form-options {
  margin-bottom: 24px;
}

.agreement {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
}

.agreement input {
  width: 16px;
  height: 16px;
}

.agreement a {
  color: #4f46e5;
  text-decoration: none;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #4338ca;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
  color: #9ca3af;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e5e7eb;
}

.divider span {
  padding: 0 16px;
  font-size: 14px;
}

.social-login {
  margin-bottom: 24px;
}

.btn-social {
  width: 100%;
  padding: 12px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-social:hover {
  background: #f9fafb;
}

.auth-footer {
  text-align: center;
  font-size: 14px;
  color: #6b7280;
}

.auth-footer a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}
</style>
