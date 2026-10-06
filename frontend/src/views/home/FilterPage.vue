<template>
  <div class="filter-overlay" @click.self="handleClose">
    <div class="filter-page">
      <div class="filter-header">
        <h2>筛选成果</h2>
        <el-button class="close-btn" @click="handleClose">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>

      <div class="filter-section">
        <div class="filter-label">分类</div>
        <div class="category-tags">
          <span
            v-for="cat in categories"
            :key="cat.value"
            class="category-tag"
            :class="{ active: selectedCategory === cat.value }"
            @click="selectedCategory = cat.value"
          >
            {{ cat.label }}
          </span>
        </div>
      </div>

      <div class="filter-results">
        <div class="results-header">
          <span>共 {{ filteredAchievements.length }} 个成果</span>
        </div>

        <div v-if="filteredAchievements.length > 0" class="results-grid">
          <div
            v-for="item in filteredAchievements"
            :key="item.id"
            class="result-card"
            @click="goToDetail(item.id)"
          >
            <div class="result-image-wrapper">
              <img src="/占位图片.png" :alt="item.title" class="result-image" />
              <div class="result-badge" v-if="item.status === 'approved'">已通过</div>
              <div class="result-badge pending" v-else-if="item.status === 'pending'">待审核</div>
            </div>
            <div class="result-info">
              <span class="result-title">{{ item.title }}</span>
              <span class="result-category">{{ getMainCategoryLabel(item.main_category) }}</span>
            </div>
          </div>
        </div>

        <div v-else class="no-data">
          <el-icon class="no-data-icon"><Document /></el-icon>
          <p>暂无数据</p>
        </div>
      </div>

      <div class="filter-footer">
        <el-button class="reset-btn" @click="selectedCategory = ''">重置</el-button>
        <el-button class="confirm-btn" @click="handleConfirm">确认</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Close, Document } from '@element-plus/icons-vue'
import { getMainCategoryLabel } from '@/utils/constants'

const router = useRouter()

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  achievements: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'select'])

const selectedCategory = ref('')

const filteredAchievements = computed(() => {
  if (!selectedCategory.value) {
    return props.achievements
  }
  return props.achievements.filter(item => item.main_category === selectedCategory.value)
})

const handleClose = () => {
  emit('close')
}

const handleConfirm = () => {
  emit('select', selectedCategory.value)
}

const goToDetail = (id) => {
  emit('close')
  router.push(`/home/detail/${id}`)
}
</script>

<style scoped>
.filter-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-page {
  width: 800px;
  max-height: 80vh;
  background: #1f1f1f;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.filter-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 20px;
}

.close-btn:hover {
  color: #fff;
}

.filter-section {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.filter-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 12px;
}

.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.category-tag {
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-tag:hover {
  background: rgba(255, 255, 255, 0.15);
}

.category-tag.active {
  background: #4095e5;
  color: #fff;
}

.filter-results {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

.results-header {
  margin-bottom: 16px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.result-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.result-card:hover {
  transform: translateY(-4px);
}

.result-image-wrapper {
  position: relative;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 10px;
}

.result-image {
  width: 100%;
  height: 140px;
  object-fit: cover;
}

.result-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  padding: 2px 6px;
  background: #67c23a;
  color: #fff;
  font-size: 11px;
  border-radius: 3px;
}

.result-badge.pending {
  background: #e6a23c;
}

.result-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-title {
  font-size: 13px;
  color: #fff;
  font-weight: 500;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-category {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: rgba(255, 255, 255, 0.3);
}

.no-data-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.no-data p {
  margin: 0;
  font-size: 14px;
}

.filter-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(0, 0, 0, 0.2);
}

.reset-btn {
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
  border: none;
  border-radius: 4px;
  font-size: 14px;
}

.reset-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}

.confirm-btn {
  padding: 8px 24px;
  background: #4095e5;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}
</style>