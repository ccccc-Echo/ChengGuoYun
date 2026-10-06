<template>
  <DashboardScreen v-if="isAdmin" />
  <div v-else class="dashboard-container">
    <div class="welcome-section">
      <div class="welcome-text">
        <h1>{{ welcomeText }}</h1>
        <p>{{ currentDate }}</p>
      </div>
      <div class="welcome-avatar">
        <el-avatar :size="64" :style="{ background: avatarColor }">
          {{ userInfo.name?.charAt(0)?.toUpperCase() || 'U' }}
        </el-avatar>
      </div>
    </div>

    <el-row :gutter="20" class="stats-row">
      <el-col v-for="stat in statCards" :key="stat.key" :xs="12" :sm="12" :md="6" :lg="6">
        <div class="stat-card" :class="stat.theme">
          <div class="stat-icon">
            <el-icon :size="28">
              <component :is="stat.icon" />
            </el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
          <div class="stat-trend" v-if="stat.trend !== undefined">
            <span :class="stat.trend >= 0 ? 'trend-up' : 'trend-down'">
              {{ stat.trend >= 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}%
            </span>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :lg="16">
        <div class="chart-card main-chart">
          <div class="card-header">
            <div class="header-left">
              <span class="header-title">{{ trendChartTitle }}</span>
            </div>
          </div>
          <LineChart :chart-data="trendChartData" height="320px" />
        </div>
      </el-col>
      <el-col :xs="24" :lg="8">
        <div class="chart-card pie-chart">
          <div class="card-header">
            <div class="header-left">
              <span class="header-title">{{ distributionTitle }}</span>
            </div>
          </div>
          <PieChart :chart-data="pieChartData" height="280px" />
          <div class="distribution-legend">
            <div 
              v-for="(item, index) in categoryDistribution" 
              :key="item.name" 
              class="legend-item"
            >
              <span class="legend-dot" :style="{ background: chartColors[index % chartColors.length] }"></span>
              <span class="legend-label">{{ getMainCategoryLabel(item.name) }}</span>
              <span class="legend-value">{{ item.count }}项</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-title">级别分布</span>
            </div>
          </div>
          <BarChart :chart-data="levelChartData" height="280px" />
        </div>
      </el-col>
      <el-col :xs="24" :lg="12">
        <div class="chart-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-title">能力雷达</span>
            </div>
          </div>
          <RadarChart :chart-data="radarChartData" height="280px" />
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="tables-row">
      <el-col :xs="24" :lg="12">
        <div class="table-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-title">{{ recentTitle }}</span>
            </div>
            <div class="header-right">
              <el-button type="primary" link @click="goToAchievements">查看全部</el-button>
            </div>
          </div>
          <el-table :data="recentList" style="width: 100%" height="300" :empty-text="recentEmptyText">
            <el-table-column prop="title" label="成果名称" min-width="180" show-overflow-tooltip />
            <el-table-column prop="student_name" label="学生" width="100" v-if="isAdminOrTeacher" />
            <el-table-column prop="category" label="类型" width="120">
              <template #default="{ row }">
                {{ getMainCategoryLabel(row.category) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
      <el-col :xs="24" :lg="12">
        <div class="table-card">
          <div class="card-header">
            <div class="header-left">
              <span class="header-title">{{ quickActionsTitle }}</span>
            </div>
          </div>
          <div class="quick-actions">
            <el-button 
              v-for="action in quickActions" 
              :key="action.key"
              :type="action.type"
              :icon="action.icon"
              size="large"
              @click="handleAction(action)"
            >
              {{ action.label }}
            </el-button>
          </div>
          <div class="system-info">
            <div class="info-item">
              <span class="info-label">系统版本</span>
              <span class="info-value">v1.0.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">在线用户</span>
              <span class="info-value">{{ onlineUsers }} 人</span>
            </div>
            <div class="info-item">
              <span class="info-label">数据库状态</span>
              <span class="info-value status-ok">正常</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import {
  Document, Clock, Check, Trophy, User, School,
  DataAnalysis, Bell, Plus, Edit, Refresh, Grid
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import LineChart from '@/components/Charts/LineChart.vue'
import BarChart from '@/components/Charts/BarChart.vue'
import PieChart from '@/components/Charts/PieChart.vue'
import RadarChart from '@/components/Charts/RadarChart.vue'
import DashboardScreen from './DashboardScreen.vue'
import { statsApi, achievementsApi } from '@/api'
import { getUserInfo } from '@/utils/auth'
import { getMainCategoryLabel, getLevelLabel, levelMap } from '@/utils/constants'

const router = useRouter()
const userInfo = ref(getUserInfo() || {})
const userRole = userInfo.value.role || 'student'

const statsData = ref({
  total_achievements: 0,
  pending_achievements: 0,
  approved_achievements: 0,
  total_classes: 0,
  total_students: 0,
  category_distribution: [],
  trend_data: [],
  pending_list: [],
  recent_list: [],
  level_distribution: []
})

const trendPeriod = ref('month')
const onlineUsers = ref(1)

const chartColors = ['#4095e5', '#67c23a', '#e6a23c', '#f56c6c', '#909399', '#b37feb', '#48b8d0']

const isAdminOrTeacher = computed(() => userRole === 'admin' || userRole === 'teacher')
const isStudent = computed(() => userRole === 'student')
const isAdmin = computed(() => userRole === 'admin')

const welcomeText = computed(() => {
  const hour = new Date().getHours()
  const name = userInfo.value.name || '用户'
  if (hour < 6) return `凌晨好，${name}！`
  if (hour < 12) return `早上好，${name}！`
  if (hour < 14) return `中午好，${name}！`
  if (hour < 18) return `下午好，${name}！`
  return `晚上好，${name}！`
})

const currentDate = computed(() => {
  const now = new Date()
  const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
  return now.toLocaleDateString('zh-CN', options)
})

const avatarColor = computed(() => {
  const colors = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  ]
  const index = userInfo.value.id % colors.length
  return colors[index] || colors[0]
})

const statCards = computed(() => {
  if (userRole === 'admin') {
    return [
      { key: 'students', label: '学生总数', value: statsData.value.total_students, icon: markRaw(User), theme: 'blue' },
      { key: 'classes', label: '班级总数', value: statsData.value.total_classes, icon: markRaw(School), theme: 'green' },
      { key: 'pending', label: '待审核', value: statsData.value.pending_achievements, icon: markRaw(Clock), theme: 'orange' },
      { key: 'approved', label: '已通过', value: statsData.value.approved_achievements, icon: markRaw(Check), theme: 'purple' }
    ]
  } else if (userRole === 'teacher') {
    return [
      { key: 'total', label: '成果总数', value: statsData.value.total_achievements, icon: markRaw(DataAnalysis), theme: 'blue' },
      { key: 'pending', label: '待审核', value: statsData.value.pending_achievements, icon: markRaw(Clock), theme: 'orange' },
      { key: 'approved', label: '已通过', value: statsData.value.approved_achievements, icon: markRaw(Check), theme: 'green' },
      { key: 'classes', label: '管理班级', value: statsData.value.total_classes, icon: markRaw(School), theme: 'purple' }
    ]
  } else {
    return [
      { key: 'total', label: '我的成果', value: statsData.value.total_achievements, icon: markRaw(Document), theme: 'blue' },
      { key: 'pending', label: '待审核', value: statsData.value.pending_achievements, icon: markRaw(Clock), theme: 'orange' },
      { key: 'approved', label: '已通过', value: statsData.value.approved_achievements, icon: markRaw(Check), theme: 'green' },
      { key: 'award', label: '获奖数', value: statsData.value.award_count || 0, icon: markRaw(Trophy), theme: 'purple' }
    ]
  }
})

const categoryDistribution = computed(() => statsData.value.category_distribution || [])

const distributionTitle = computed(() => {
  if (isStudent.value) return '我的成果类型分布'
  return '成果类型分布'
})

const trendChartTitle = computed(() => {
  if (isStudent.value) return '我的成果提交趋势'
  return '成果提交趋势'
})

const recentTitle = computed(() => {
  if (isAdmin.value) return '待审核成果'
  if (userRole === 'teacher') return '最近成果'
  return '我的最近成果'
})

const recentEmptyText = computed(() => {
  if (isAdmin.value) return '暂无待审核成果'
  return '暂无成果记录'
})

const quickActionsTitle = computed(() => {
  if (isStudent.value) return '快捷操作'
  return '待办事项'
})

const recentList = computed(() => {
  if (isAdmin.value) {
    return statsData.value.pending_list || []
  }
  return statsData.value.recent_list || []
})

const trendChartData = computed(() => {
  const trendData = (statsData.value.trend_data || []).map(d => ({
    label: d.label || d.month || d.date || '',
    count: d.count || 0
  }))
  const filtered = filterTrendData(trendData, trendPeriod.value)
  
  return {
    legend: ['成果数量'],
    xAxis: filtered.map(d => d.label),
    series: [{
      name: '成果数量',
      type: 'line',
      smooth: true,
      data: filtered.map(d => d.count),
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64, 149, 229, 0.3)' },
          { offset: 1, color: 'rgba(64, 149, 229, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#4095e5',
        width: 3
      },
      itemStyle: {
        color: '#4095e5'
      }
    }]
  }
})

const pieChartData = computed(() => {
  const data = categoryDistribution.value.map((item, index) => ({
    value: item.count,
    name: getMainCategoryLabel(item.name),
    itemStyle: { color: chartColors[index % chartColors.length] }
  }))
  
  return {
    name: '成果类型',
    data: data
  }
})

const levelChartData = computed(() => {
  const levelDistribution = statsData.value.level_distribution || []
  const levelKeys = Object.keys(levelMap)
  const levelLabels = levelKeys.map(k => levelMap[k])
  const colors = ['#f56c6c', '#e6a23c', '#67c23a', '#4095e5']
  
  const data = levelKeys.map((key, index) => {
    const found = levelDistribution.find(l => l.level === key)
    return {
      value: found?.count || 0,
      itemStyle: { color: colors[index] }
    }
  })
  
  return {
    legend: ['级别分布'],
    xAxis: levelLabels,
    series: [{
      name: '级别分布',
      type: 'bar',
      data: data,
      barWidth: '50%',
      itemStyle: {
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }
})

const radarChartData = computed(() => {
  if (isStudent.value) {
    const studentIndicators = [
      { name: '学科竞赛', max: 100 },
      { name: '学术论文', max: 100 },
      { name: '知识产权', max: 100 },
      { name: '科研项目', max: 100 },
      { name: '荣誉表彰', max: 100 },
      { name: '技能证书', max: 100 }
    ]
    const studentValues = categoryDistribution.value.map(item => Math.min(item.count * 20, 100))
    while (studentValues.length < studentIndicators.length) {
      studentValues.push(0)
    }
    
    return {
      legend: ['我的能力'],
      indicator: studentIndicators,
      series: [{
        value: studentValues.slice(0, studentIndicators.length),
        name: '我的能力'
      }]
    }
  }
  
  const total = statsData.value.total_achievements || 1
  const values = categoryDistribution.value.map(item => Math.round((item.count / total) * 100))
  
  const indicators = categoryDistribution.value.length > 0
    ? categoryDistribution.value.map(item => ({
        name: getMainCategoryLabel(item.name),
        max: Math.max(...values, 100)
      }))
    : [
        { name: '学科竞赛', max: 100 },
        { name: '学术论文', max: 100 },
        { name: '知识产权', max: 100 },
        { name: '科研项目', max: 100 }
      ]
  
  const radarValues = categoryDistribution.value.length > 0
    ? values
    : [0, 0, 0, 0]
  
  return {
    legend: ['成果分布'],
    indicator: indicators,
    series: [{
      value: radarValues,
      name: '成果分布',
      areaStyle: { opacity: 0.3 }
    }]
  }
})

const quickActions = computed(() => {
  if (isStudent.value) {
    return [
      { key: 'submit', label: '提交成果', icon: markRaw(Plus), type: 'primary', action: 'submit' },
      { key: 'my', label: '我的成果', icon: markRaw(Document), type: 'success', action: 'my' },
      { key: 'courses', label: '我的课程', icon: markRaw(Grid), type: 'warning', action: 'courses' }
    ]
  } else if (isAdmin.value) {
    return [
      { key: 'audit', label: '审核成果', icon: markRaw(Check), type: 'primary', action: 'audit' },
      { key: 'teachers', label: '教师管理', icon: markRaw(User), type: 'success', action: 'teachers' },
      { key: 'students', label: '学生管理', icon: markRaw(School), type: 'warning', action: 'students' }
    ]
  } else {
    return [
      { key: 'audit', label: '审核成果', icon: markRaw(Check), type: 'primary', action: 'audit' },
      { key: 'classes', label: '我的班级', icon: markRaw(School), type: 'success', action: 'classes' },
      { key: 'students', label: '本班学生', icon: markRaw(User), type: 'warning', action: 'students' }
    ]
  }
})

const getStatusText = (status) => {
  const map = { pending: '待审核', approved: '已通过', rejected: '已驳回' }
  return map[status] || status
}

const getStatusType = (status) => {
  const map = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

const filterTrendData = (data, period) => {
  if (!data || data.length === 0) {
    const now = new Date()
    const result = []
    let count = 7
    if (period === 'month') count = 30
    if (period === 'year') count = 12
    
    for (let i = count - 1; i >= 0; i--) {
      const date = new Date(now)
      if (period === 'year') {
        date.setMonth(date.getMonth() - i)
        result.push({
          label: `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`,
          count: 0
        })
      } else {
        date.setDate(date.getDate() - i)
        result.push({
          label: period === 'year' ? date.toLocaleDateString('zh-CN', { month: 'short' }) : `${date.getMonth() + 1}/${date.getDate()}`,
          count: 0
        })
      }
    }
    return result
  }
  return data
}

const loadStats = async () => {
  try {
    const res = await statsApi.dashboard()
    if (res && typeof res === 'object') {
      statsData.value = { ...statsData.value, ...res }
    }
  } catch (error) {
    console.warn('加载统计数据失败，使用默认数据:', error?.message || error)
    statsData.value = {
      total_achievements: 0,
      pending_achievements: 0,
      approved_achievements: 0,
      rejected_achievements: 0,
      total_classes: 0,
      total_students: 0,
      award_count: 0,
      category_distribution: [],
      trend_data: [],
      pending_list: [],
      recent_list: [],
      level_distribution: []
    }
  }
}

const handleAction = (action) => {
  if (isStudent.value) {
    const studentRoutes = {
      submit: '/student/submit',
      my: '/student/achievement',
      courses: '/student/courses',
      audit: '/student/achievement',
      classes: '/student/courses'
    }
    const path = studentRoutes[action.action] || '/student/dashboard'
    router.push(path)
    return
  }

  const routes = {
    submit: '/dashboard/achievements/add',
    my: '/dashboard/achievements',
    knowledge: '/dashboard/settings',
    audit: '/dashboard/achievements',
    teachers: '/dashboard/teachers',
    students: '/dashboard/students',
    classes: '/dashboard/courses'
  }
  const path = routes[action.action] || '/dashboard/achievements'
  router.push(path)
}

const goToAchievements = () => {
  if (isStudent.value) {
    router.push('/student/achievement')
  } else {
    router.push('/dashboard/achievements')
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px;
  border-radius: 16px;
  margin-bottom: 20px;
  color: white;
}

.welcome-text h1 {
  font-size: 24px;
  margin: 0 0 8px 0;
}

.welcome-text p {
  margin: 0;
  opacity: 0.9;
}

.welcome-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.stat-card.blue::before { background: linear-gradient(90deg, #4095e5, #5ba8f5); }
.stat-card.green::before { background: linear-gradient(90deg, #67c23a, #85ce61); }
.stat-card.orange::before { background: linear-gradient(90deg, #e6a23c, #ebb563); }
.stat-card.purple::before { background: linear-gradient(90deg, #909399, #a6a9ad); }
.stat-card.red::before { background: linear-gradient(90deg, #f56c6c, #f78989); }

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-card.blue .stat-icon { background: linear-gradient(135deg, #4095e5, #5ba8f5); }
.stat-card.green .stat-icon { background: linear-gradient(135deg, #67c23a, #85ce61); }
.stat-card.orange .stat-icon { background: linear-gradient(135deg, #e6a23c, #ebb563); }
.stat-card.purple .stat-icon { background: linear-gradient(135deg, #909399, #a6a9ad); }
.stat-card.red .stat-icon { background: linear-gradient(135deg, #f56c6c, #f78989); }

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #222;
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: #86909c;
  margin-top: 6px;
}

.stat-trend {
  position: absolute;
  top: 16px;
  right: 16px;
}

.trend-up {
  color: #67c23a;
  font-size: 12px;
  font-weight: 500;
}

.trend-down {
  color: #f56c6c;
  font-size: 12px;
  font-weight: 500;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-card,
.table-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
  color: #222;
}

.distribution-legend {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f1f2;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

.legend-label {
  flex: 1;
  font-size: 13px;
  color: #666;
}

.legend-value {
  font-size: 13px;
  color: #222;
  font-weight: 500;
}

.tables-row {
  margin-bottom: 20px;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}

.quick-actions .el-button {
  flex: 1;
  min-width: 140px;
  height: 48px;
}

.system-info {
  background: #f7f8fa;
  border-radius: 8px;
  padding: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #86909c;
  font-size: 13px;
}

.info-value {
  color: #222;
  font-size: 13px;
  font-weight: 500;
}

.info-value.status-ok {
  color: #67c23a;
}

:deep(.el-table th) {
  background: #f7f8fa;
  color: #666;
  font-weight: 500;
  font-size: 13px;
}

:deep(.el-table td) {
  font-size: 13px;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 12px;
  }
  
  .welcome-section {
    padding: 20px;
  }
  
  .welcome-text h1 {
    font-size: 18px;
  }
  
  .stat-value {
    font-size: 24px;
  }
}
</style>
