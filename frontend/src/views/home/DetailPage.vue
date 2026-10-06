<template>
  <div class="detail-container">
    <div class="detail-header">
      <el-button class="back-btn" @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        <span>返回</span>
      </el-button>
    </div>

    <div v-if="achievement" class="detail-content">
      <div class="detail-category">{{ achievement.category }}</div>
      <div class="detail-title">{{ achievement.title }}</div>
    </div>

    <div v-else class="empty-state">
      <p>未找到相关成果</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const achievement = ref(null)

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

const loadDetail = () => {
  const id = parseInt(route.params.id)
  achievement.value = achievements.find(item => item.id === id)
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  loadDetail()
})
</script>

<style scoped>
.detail-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #eaf4ff 0%, #f5f9ff 100%);
}

.detail-header {
  padding: 16px 24px;
  background: #fff;
  border-bottom: 1px solid #e8ecf0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
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

.detail-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 24px;
}

.detail-category {
  font-size: 16px;
  color: #1677ff;
  font-weight: 500;
  margin-bottom: 20px;
  padding: 8px 20px;
  background: rgba(22, 119, 255, 0.1);
  border-radius: 20px;
}

.detail-title {
  font-size: 28px;
  color: #333;
  font-weight: 600;
  text-align: center;
  line-height: 1.5;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
  color: #86909c;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
}
</style>
