<template>
  <div class="home-container">
    <div class="search-bar" :class="{ collapsed: isCollapsed }">
      <div class="search-bar-inner">
        <el-button class="filter-btn" @click="showFilterDialog = true">
          <el-icon><Filter /></el-icon>
          <span>筛选</span>
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

    <div class="banner-section">
      <div class="banner-wrapper">
        <div class="banner-item" v-for="(item, index) in bannerItems" :key="index">
          <img :src="item.image" :alt="item.title" class="banner-image" />
          <div class="banner-overlay"></div>
          <div class="banner-content">
            <div class="banner-title">{{ item.title }}</div>
            <div class="banner-desc">{{ item.desc }}</div>
            <el-button class="banner-btn">立即查看</el-button>
          </div>
        </div>
      </div>
      <div class="banner-indicators">
        <span
          v-for="(_, index) in bannerItems"
          :key="index"
          class="indicator"
          :class="{ active: currentBanner === index }"
          @click="currentBanner = index"
        ></span>
      </div>
    </div>

    <div class="recommend-section">
      <div class="section-header">
        <h3>推荐成果</h3>
        <el-button class="refresh-btn" @click="refreshRecommend">
          <el-icon><Refresh /></el-icon>
          换一批
        </el-button>
      </div>
      <div class="recommend-grid">
        <div
          v-for="item in recommendList"
          :key="item.id"
          class="recommend-card"
          @click="goToDetail(item.id)"
        >
          <div class="recommend-icon" :style="{ background: getCategoryColor(item.category) }">
            <el-icon><Star /></el-icon>
          </div>
          <div class="recommend-content">
            <span class="recommend-title">{{ item.title }}</span>
            <span class="recommend-category">{{ item.category }}</span>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="showFilterDialog"
      title="筛选"
      width="700px"
      :close-on-click-modal="false"
      @close="resetFilterDialog"
    >
      <div class="filter-dialog-content">
        <div class="filter-tabs">
          <el-tag
            v-for="cat in filterCategories"
            :key="cat.value"
            :type="filterCategory === cat.value ? 'primary' : 'info'"
            class="filter-tab"
            @click="filterCategory = cat.value"
          >
            {{ cat.label }}
          </el-tag>
        </div>

        <div class="filter-count">共 {{ filterResults.length }} 个成果</div>

        <div class="filter-list">
          <div v-for="item in filterResults" :key="item.id" class="filter-item" @click="goToDetail(item.id)">
            <span class="filter-category" :style="{ background: getCategoryColor(item.category) }">
              {{ item.category }}
            </span>
            <span class="filter-title">{{ item.title }}</span>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="resetFilterDialog">重置</el-button>
        <el-button type="primary" @click="closeFilterDialog">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Filter, Search, Star, Refresh } from '@element-plus/icons-vue'

const router = useRouter()

const searchKeyword = ref('')
const showFilterDialog = ref(false)
const filterCategory = ref('全部')
const recommendList = ref([])
const currentBanner = ref(0)
const isCollapsed = ref(false)
let carouselTimer = null
let lastScrollTop = 0

const achievements = ref([
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
])

const bannerItems = [
  { image: '/占位图片.png', title: '成果云', desc: '记录你的每一份成就' },
  { image: '/占位图片.png', title: '学科竞赛', desc: '展示你的竞赛风采' },
  { image: '/占位图片.png', title: '学术论文', desc: '发表你的研究成果' }
]

const filterCategories = [
  { label: '全部', value: '全部' },
  { label: '学科竞赛类', value: '学科竞赛类' },
  { label: '学术论文类', value: '学术论文类' },
  { label: '知识产权类', value: '知识产权类' },
  { label: '科研项目类', value: '科研项目类' },
  { label: '荣誉表彰类', value: '荣誉表彰类' },
  { label: '技能证书类', value: '技能证书类' },
  { label: '社会实践类', value: '社会实践类' }
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

const filterResults = computed(() => {
  if (filterCategory.value === '全部') {
    return achievements.value
  }
  return achievements.value.filter(item => item.category === filterCategory.value)
})

const handleSearch = () => {
  const keyword = searchKeyword.value.trim()
  router.push(`/home/search?keyword=${encodeURIComponent(keyword || '')}`)
}

const goToDetail = (id) => {
  router.push(`/home/detail/${id}`)
}

const resetFilterDialog = () => {
  filterCategory.value = '全部'
}

const closeFilterDialog = () => {
  resetFilterDialog()
  showFilterDialog.value = false
}

const refreshRecommend = () => {
  const shuffled = [...achievements.value].sort(() => Math.random() - 0.5)
  recommendList.value = shuffled.slice(0, 4)
}

const handleScroll = () => {
  const scrollTop = window.scrollY
  if (scrollTop > 100 && scrollTop > lastScrollTop) {
    isCollapsed.value = true
  } else if (scrollTop < 50) {
    isCollapsed.value = false
  }
  lastScrollTop = scrollTop
}

const startCarousel = () => {
  carouselTimer = setInterval(() => {
    currentBanner.value = (currentBanner.value + 1) % bannerItems.length
  }, 5000)
}

const stopCarousel = () => {
  if (carouselTimer) {
    clearInterval(carouselTimer)
    carouselTimer = null
  }
}

onMounted(() => {
  refreshRecommend()
  startCarousel()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  stopCarousel()
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.home-container {
  min-height: 100%;
  background: transparent;
  padding-bottom: 40px;
}

.search-bar {
  background: #fff;
  border-bottom: 1px solid #e8ecf0;
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 16px 24px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.search-bar.collapsed {
  padding: 8px 24px;
  background: #fff;
}

.search-bar-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(22, 119, 255, 0.06);
  color: #1677ff;
  border: 1px solid rgba(22, 119, 255, 0.15);
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(22, 119, 255, 0.12);
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

.banner-section {
  position: relative;
  margin: 0 24px 20px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.banner-wrapper {
  display: flex;
  transition: transform 0.5s ease;
}

.banner-item {
  min-width: 100%;
  position: relative;
}

.banner-image {
  width: 100%;
  height: 320px;
  object-fit: cover;
}

.banner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(22, 119, 255, 0.1), rgba(22, 119, 255, 0.4));
}

.banner-content {
  position: absolute;
  bottom: 40px;
  left: 40px;
  color: #333;
}

.banner-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}

.banner-desc {
  font-size: 15px;
  color: #666;
  margin-bottom: 16px;
}

.banner-btn {
  background: linear-gradient(135deg, #1677ff, #4096ff);
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
}

.banner-indicators {
  position: absolute;
  bottom: 20px;
  right: 40px;
  display: flex;
  gap: 8px;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(22, 119, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s;
}

.indicator.active {
  width: 20px;
  border-radius: 4px;
  background: #1677ff;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.refresh-btn {
  color: #4095e5;
  font-size: 14px;
}

.recommend-section {
  padding: 0 24px;
}

.recommend-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.recommend-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  cursor: pointer;
}

.recommend-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.recommend-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.recommend-content {
  flex: 1;
}

.recommend-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  display: block;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.recommend-category {
  font-size: 12px;
  color: #86909c;
}

.filter-dialog-content {
  padding: 20px 0;
}

.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.filter-tab {
  cursor: pointer;
  padding: 6px 14px;
  border-radius: 20px;
  transition: all 0.3s;
}

.filter-count {
  font-size: 14px;
  color: #86909c;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e8ecf0;
}

.filter-list {
  max-height: 300px;
  overflow-y: auto;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
}

.filter-item:hover {
  background: rgba(22, 119, 255, 0.04);
}

.filter-category {
  padding: 3px 10px;
  color: #fff;
  font-size: 12px;
  border-radius: 4px;
}

.filter-title {
  font-size: 14px;
  color: #333;
  flex: 1;
}
</style>