import api from './index'

export const getCourses = (params) => {
  return api.get('/courses', { params })
}

export const getCourseById = (id) => {
  return api.get(`/courses/${id}`)
}

export const getCourseLessons = (courseId) => {
  return api.get(`/courses/${courseId}/lessons`)
}

export const getLessonById = (courseId, lessonId) => {
  return api.get(`/courses/${courseId}/lessons/${lessonId}`)
}

export const getCategories = () => {
  return api.get('/courses/categories')
}

export const enrollCourse = (courseId) => {
  return api.post(`/courses/${courseId}/enroll`)
}

export const updateProgress = (courseId, lessonId, data) => {
  return api.post('/progress', {
    course_id: courseId,
    lesson_id: lessonId,
    ...data
  })
}

export const getMyCourses = () => {
  return api.get('/users/me/courses')
}
