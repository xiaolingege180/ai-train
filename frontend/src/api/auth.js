import api from './index'

export const login = (credentials) => {
  // 使用 form-data 格式
  const formData = new URLSearchParams()
  formData.append('username', credentials.username)
  formData.append('password', credentials.password)
  
  return api.post('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
}

export const register = (data) => {
  return api.post('/auth/register', data)
}

export const getUserInfo = () => {
  return api.get('/users/me')
}

export const updateUserInfo = (data) => {
  return api.patch('/users/me', data)
}

export const uploadAvatar = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/users/me/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
