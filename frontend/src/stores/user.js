import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getUserInfo } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)
  const loading = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const userId = computed(() => userInfo.value?.id)
  const username = computed(() => userInfo.value?.username || '用户')
  const avatar = computed(() => userInfo.value?.avatar || '/default-avatar.svg')

  // Actions
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const clearToken = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  const login = async (credentials) => {
    loading.value = true
    try {
      const res = await loginApi(credentials)
      setToken(res.access_token)
      await fetchUserInfo()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const fetchUserInfo = async () => {
    try {
      const res = await getUserInfo()
      userInfo.value = res
      return res
    } catch (error) {
      clearToken()
      throw error
    }
  }

  const setUserInfo = (info) => {
    userInfo.value = info
  }

  const logout = () => {
    clearToken()
  }

  // 初始化时如果有 token，获取用户信息
  if (token.value) {
    fetchUserInfo().catch(() => {
      // token 失效，自动清除
    })
  }

  return {
    token,
    userInfo,
    loading,
    isLoggedIn,
    userId,
    username,
    avatar,
    login,
    logout,
    fetchUserInfo,
    setUserInfo
  }
})
