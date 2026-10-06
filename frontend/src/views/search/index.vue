<template>
  <div class="search-page">
    <div class="search-header">
      <div class="search-header-inner">
        <el-button class="back-btn" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          <span>返回</span>
        </el-button>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索成果（如：数学建模、英语四级）"
          class="search-input"
          prefix-icon="Search"
          @keyup.enter="handleSearch"
        />
        <el-button class="search-btn" @click="handleSearch">搜索</el-button>
      </div>
    </div>

    <div class="search-content">
      <div v-if="searchKeyword.trim() && searchResults.length > 0" class="results-header">
        <span>搜索「{{ searchKeyword }}」共找到 {{ searchResults.length }} 个成果</span>
      </div>

      <div v-if="searchResults.length > 0" class="results-grid">
        <div
          v-for="item in searchResults"
          :key="item.id"
          class="result-card"
          @click="goToDetail(item.id)"
        >
          <div class="card-image-placeholder" :style="{ background: getCategoryColor(item.category) }">
            <el-icon class="placeholder-icon"><Star /></el-icon>
          </div>
          <div class="card-info">
            <span class="card-title">{{ item.title }}</span>
            <span class="card-category">{{ item.category }}</span>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <el-icon class="empty-icon"><Search /></el-icon>
        <p>{{ searchKeyword.trim() ? '未找到相关成果' : '请输入关键词进行搜索' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, Search, Star } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const searchKeyword = ref('')

const achievements = [
  { id: 19, title: '全国大学生数学建模竞赛省一等奖', category: '学科竞赛类' },
  { id: 20, title: '大学英语六级（CET-6）', category: '技能证书类' },
  { id: 21, title: '2023-2024学年三好学生', category: '荣誉表彰类' },
  { id: 22, title: '互联网+大学生创新创业大赛省级银奖', category: '学科竞赛类' },
  { id: 23, title: '智慧校园管理系统软件著作权', category: '知识产权类' },
  { id: 24, title: '优秀共青团员', category: '荣誉表彰类' },
  { id: 25, title: '基于深度学习的图像识别研究（省级期刊）', category: '学术论文类' },
  { id: 26, title: '全国计算机等级考试三级（数据库）', category: '技能证书类' },
  { id: 27, title: '国家级大创项目"智能垃圾分类系统"', category: '科研项目类' },
  { id: 28, title: '挑战杯课外学术科技作品竞赛省二等奖', category: '学科竞赛类' },
  { id: 29, title: '一种新型智能台灯实用新型专利', category: '知识产权类' },
  { id: 30, title: '国家奖学金', category: '荣誉表彰类' },
  { id: 31, title: 'ACM-ICPC国际大学生程序设计竞赛亚洲区域赛铜奖', category: '学科竞赛类' },
  { id: 32, title: 'EI会议论文：AI在医疗诊断中的应用', category: '学术论文类' },
  { id: 33, title: '高中信息技术教师资格证', category: '技能证书类' },
  { id: 34, title: '普通话水平测试二级甲等', category: '技能证书类' },
  { id: 35, title: '暑期"三下乡"社会实践优秀个人', category: '社会实践类' },
  { id: 36, title: '国家励志奖学金', category: '荣誉表彰类' }
]

const categoryColors = {
  '学科竞赛类': '#4095e5',
  '学术论文类': '#b37feb',
  '知识产权类': '#f56c6c',
  '科研项目类': '#48b8d0',
  '荣誉表彰类': '#e6a23c',
  '技能证书类': '#67c23a',
  '社会实践类': '#909399'
}

const getCategoryColor = (category) => {
  return categoryColors[category] || '#909399'
}

const searchResults = computed(() => {
  if (!searchKeyword.value.trim()) {
    return []
  }
  const keyword = searchKeyword.value.trim()
  return achievements.filter(item => item.title.includes(keyword))
})

const handleSearch = () => {
}

const goToDetail = (id) => {
  router.push(`/home/detail/${id}`)
}

const goBack = () => {
  router.push('/home/index')
}

onMounted(() => {
  const keyword = route.query.keyword || ''
  searchKeyword.value = keyword
})
</script>

<style scoped>
.search-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #eaf4ff 0%, #f5f9ff 100%);
}

.search-header {
  background: #fff;
  border-bottom: 1px solid #e8ecf0;
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.search-header-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  color: #666;
  font-size: 14px;
  transition: all 0.3s ease;
}

.back-btn:hover {
  color: #1677ff;
}

.search-input {
  flex: 1;
  max-width: 600px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 8px;
  border-color: #e8ecf0;
}

.search-input :deep(.el-input__inner) {
  color: #333;
  font-size: 14px;
}

.search-btn {
  padding: 8px 24px;
  background: linear-gradient(135deg, #1677ff, #4096ff);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.search-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.results-header {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e8ecf0;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.result-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  cursor: pointer;
}

.result-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.card-image-placeholder {
  width: 100%;
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 48px;
  color: rgba(255, 255, 255, 0.6);
}

.card-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
}

.card-title {
  font-size: 14px;
  color: #333;
  font-weight: 500;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-category {
  font-size: 12px;
  color: #86909c;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
  color: #86909c;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  color: #c0c4cc;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
}
</style>
