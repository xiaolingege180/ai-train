<template>
  <div class="course-card hover-card">
    <router-link :to="`/courses/${course.id}`">
      <div class="course-cover">
        <img
          :src="course.cover_image || defaultCover"
          :alt="course.title"
          loading="lazy"
          @error="$event.target.src = defaultCover"
        />
        <div v-if="course.is_free" class="badge-free">免费</div>
        <div class="play-overlay">
          <VideoPlay class="play-icon" />
        </div>
      </div>

      <div class="course-info">
        <h3 class="course-title">{{ course.title }}</h3>
        <p class="course-desc">{{ course.description }}</p>

        <div class="course-meta">
          <span class="meta-item">
            <User /> {{ formatNumber(course.student_count) }}
          </span>
          <span class="meta-item rating">
            <StarFilled class="star" /> {{ course.rating }}
          </span>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup>
import { User, StarFilled, VideoPlay } from '@element-plus/icons-vue'

const props = defineProps({
  course: {
    type: Object,
    required: true
  }
})

const defaultCover = '/default-course-cover.svg'

const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toString()
}
</script>

<style scoped>
.course-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.course-card a {
  text-decoration: none;
  color: inherit;
}

.course-cover {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
}

.course-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.course-card:hover .course-cover img {
  transform: scale(1.05);
}

.badge-free {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #10b981;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.play-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.course-card:hover .play-overlay {
  opacity: 1;
}

.play-icon {
  width: 48px;
  height: 48px;
  color: white;
}

.course-info {
  padding: 16px;
}

.course-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-desc {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #9ca3af;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-item svg {
  width: 16px;
  height: 16px;
}

.rating {
  color: #f59e0b;
}

.star {
  color: #f59e0b;
}
</style>
