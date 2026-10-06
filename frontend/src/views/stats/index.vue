<template>
  <div class="stats-page">
    <!-- Animated Background -->
    <div class="bg-decor">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
      <div class="grid-overlay"></div>
    </div>

    <!-- Content -->
    <div class="content-wrap">
      <!-- Page Header -->
      <div class="page-header">
        <div class="page-title-row">
          <div class="page-icon-wrap">
            <div class="page-icon">
              <el-icon :size="22"><DataAnalysis /></el-icon>
            </div>
            <div class="icon-pulse"></div>
          </div>
          <div class="page-title-text">
            <h1 class="page-title">统计报表</h1>
            <p class="page-subtitle">数据洞察 · 趋势分析 · 多维可视化</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><Trophy /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedTotal }}</span>
              <span class="stat-label">成果总数</span>
            </div>
          </div>
          <div class="stat-card stat-card--green">
            <div class="stat-icon">
              <el-icon :size="18"><CircleCheck /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedApproved }}</span>
              <span class="stat-label">已通过</span>
            </div>
          </div>
          <div class="stat-card stat-card--orange">
            <div class="stat-icon">
              <el-icon :size="18"><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedPending }}</span>
              <span class="stat-label">待审核</span>
            </div>
          </div>
          <div class="stat-card stat-card--purple">
            <div class="stat-icon">
              <el-icon :size="18"><School /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedClasses }}</span>
              <span class="stat-label">参与班级</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Trend Chart Card (Full Width) -->
      <div class="glass-card chart-card trend-card">
        <div class="chart-glow"></div>
        <div class="chart-header">
          <div class="chart-title-wrap">
            <div class="chart-icon-wrap chart-icon--trend">
              <el-icon :size="18"><TrendCharts /></el-icon>
            </div>
            <div>
              <div class="chart-title">成果趋势分析</div>
              <div class="chart-subtitle">提交与通过数量随时间变化趋势</div>
            </div>
          </div>
          <div class="chart-tabs">
            <button
              v-for="opt in trendOptions"
              :key="opt.value"
              :class="['tab-btn', { active: trendPeriod === opt.value }]"
              @click="changeTrendPeriod(opt.value)"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>
        <div class="chart-body">
          <div v-if="trendLoading" class="chart-skeleton">
            <div class="skeleton-chart"></div>
          </div>
          <div v-show="!trendLoading" ref="trendChartRef" class="chart-canvas"></div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="charts-grid">
        <!-- Type Distribution -->
        <div class="glass-card chart-card pie-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <div class="chart-icon-wrap chart-icon--pie">
                <el-icon :size="18"><PieChart /></el-icon>
              </div>
              <div>
                <div class="chart-title">成果类型分布</div>
                <div class="chart-subtitle">按主类别统计成果占比</div>
              </div>
            </div>
          </div>
          <div class="chart-body">
            <div v-if="loading" class="chart-skeleton">
              <div class="skeleton-chart"></div>
            </div>
            <div v-show="!loading" ref="typeChartRef" class="chart-canvas"></div>
          </div>
        </div>

        <!-- Level Distribution -->
        <div class="glass-card chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <div class="chart-icon-wrap chart-icon--bar">
                <el-icon :size="18"><Histogram /></el-icon>
              </div>
              <div>
                <div class="chart-title">成果级别分布</div>
                <div class="chart-subtitle">按级别统计成果数量</div>
              </div>
            </div>
          </div>
          <div class="chart-body">
            <div v-if="loading" class="chart-skeleton">
              <div class="skeleton-chart"></div>
            </div>
            <div v-show="!loading" ref="levelChartRef" class="chart-canvas"></div>
          </div>
        </div>

        <!-- Status Distribution -->
        <div class="glass-card chart-card pie-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <div class="chart-icon-wrap chart-icon--ring">
                <el-icon :size="18"><DataLine /></el-icon>
              </div>
              <div>
                <div class="chart-title">审核状态分布</div>
                <div class="chart-subtitle">待审核 / 已通过 / 已驳回</div>
              </div>
            </div>
          </div>
          <div class="chart-body">
            <div v-if="loading" class="chart-skeleton">
              <div class="skeleton-chart"></div>
            </div>
            <div v-show="!loading" ref="statusChartRef" class="chart-canvas"></div>
          </div>
        </div>

        <!-- Class Ranking -->
        <div class="glass-card chart-card">
          <div class="chart-header">
            <div class="chart-title-wrap">
              <div class="chart-icon-wrap chart-icon--rank">
                <el-icon :size="18"><Rank /></el-icon>
              </div>
              <div>
                <div class="chart-title">班级成果排名</div>
                <div class="chart-subtitle">各班级成果数量对比</div>
              </div>
            </div>
          </div>
          <div class="chart-body">
            <div v-if="loading" class="chart-skeleton">
              <div class="skeleton-chart"></div>
            </div>
            <div v-show="!loading" ref="classRankChartRef" class="chart-canvas"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  DataAnalysis, Trophy, CircleCheck, Clock, School,
  TrendCharts, PieChart, Histogram, DataLine, Rank
} from '@element-plus/icons-vue'
import { statsApi } from '@/api'
import { getUserInfo } from '@/utils/auth'
import { getMainCategoryLabel, getLevelLabel } from '@/utils/constants'

const typeChartRef = ref(null)
const levelChartRef = ref(null)
const statusChartRef = ref(null)
const classRankChartRef = ref(null)
const trendChartRef = ref(null)

const loading = ref(false)
const trendLoading = ref(false)
const trendPeriod = ref('7d')

const trendOptions = [
  { label: '最近7天', value: '7d' },
  { label: '最近30天', value: '30d' },
  { label: '最近90天', value: '90d' }
]

// Animated counters
const animatedTotal = ref(0)
const animatedApproved = ref(0)
const animatedPending = ref(0)
const animatedClasses = ref(0)

const animateValue = (target, refObj) => {
  const duration = 700
  const start = refObj.value
  const startTime = performance.now()
  const animate = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easeProgress = 1 - Math.pow(1 - progress, 3)
    const value = Math.round(start + (target - start) * easeProgress)
    refObj.value = value
    if (progress < 1) requestAnimationFrame(animate)
  }
  requestAnimationFrame(animate)
}

// Chart instances registry for proper disposal
const chartInstances = new Map()

const getChart = (key, el) => {
  if (chartInstances.has(key)) {
    const instance = chartInstances.get(key)
    instance.resize()
    return instance
  }
  const instance = echarts.init(el)
  chartInstances.set(key, instance)
  instance.resize()
  return instance
}

// Color palette - gradient based
const palette = ['#667eea', '#764ba2', '#4facfe', '#43e97b', '#fa709a', '#fee140', '#f093fb', '#30cfd0']

const getTypeText = (type) => getMainCategoryLabel(type)
const getLevelText = (level) => getLevelLabel(level)
const getStatusText = (status) => {
  const map = { pending: '待审核', approved: '已通过', rejected: '已驳回' }
  return map[status] || status
}

const loadStatsData = async () => {
  loading.value = true
  try {
    const userInfo = getUserInfo()
    let data
    if (userInfo.role === 'admin') {
      data = await statsApi.schoolStats()
    } else {
      data = await statsApi.classStats()
    }

    // Compute summary stats
    const total = (data.status_distribution ? Object.values(data.status_distribution).reduce((a, b) => a + b, 0) : 0)
    const approved = data.status_distribution?.approved || 0
    const pending = data.status_distribution?.pending || 0
    const classes = data.class_ranking ? data.class_ranking.length : 0

    animateValue(total, animatedTotal)
    animateValue(approved, animatedApproved)
    animateValue(pending, animatedPending)
    animateValue(classes, animatedClasses)

    // IMPORTANT: set loading to false BEFORE init charts so containers are visible
    loading.value = false
    await nextTick()

    if (data.type_distribution) initTypeChart(data.type_distribution)
    if (data.level_distribution) initLevelChart(data.level_distribution)
    if (data.status_distribution) initStatusChart(data.status_distribution)
    if (data.class_ranking) initClassRankChart(data.class_ranking)
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
    loading.value = false
  }
}

const loadTrendData = async () => {
  trendLoading.value = true
  try {
    const params = { period: trendPeriod.value }
    const data = await statsApi.trendStats(params)
    // IMPORTANT: set trendLoading to false BEFORE init chart so container is visible
    trendLoading.value = false
    await nextTick()
    if (data.trend_data) {
      initTrendChart(data.trend_data)
    }
  } catch (error) {
    console.error('加载趋势数据失败:', error)
    ElMessage.error('加载趋势数据失败')
    trendLoading.value = false
  }
}

const changeTrendPeriod = (val) => {
  trendPeriod.value = val
  loadTrendData()
}

const initTypeChart = (data) => {
  nextTick(() => {
    if (!typeChartRef.value) return
    const chart = getChart('type', typeChartRef.value)
    const entries = Object.entries(data)
    chart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)',
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: 'rgba(102,126,234,0.2)',
        borderWidth: 1,
        textStyle: { color: '#2a2a3a', fontSize: 12 }
      },
      legend: {
        orient: 'horizontal',
        bottom: '2%',
        left: 'center',
        textStyle: { color: '#5a5a6a', fontSize: 12 },
        itemWidth: 10,
        itemHeight: 10,
        itemGap: 14,
        type: 'scroll'
      },
      color: palette,
      series: [{
        name: '成果类型',
        type: 'pie',
        radius: ['54%', '85%'],
        center: ['50%', '46%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: 'rgba(255,255,255,0.9)',
          borderWidth: 2
        },
        label: { show: false },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
            color: '#2a2a3a'
          },
          itemStyle: {
            shadowBlur: 16,
            shadowColor: 'rgba(102,126,234,0.3)'
          }
        },
        labelLine: { show: false },
        data: entries.map(([key, value]) => ({
          value,
          name: getTypeText(key)
        }))
      }]
    })
  })
}

const initLevelChart = (data) => {
  nextTick(() => {
    if (!levelChartRef.value) return
    const chart = getChart('level', levelChartRef.value)
    const entries = Object.entries(data)
    chart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: 'rgba(102,126,234,0.2)',
        borderWidth: 1,
        textStyle: { color: '#2a2a3a', fontSize: 12 }
      },
      grid: { left: '3%', right: '6%', bottom: '3%', top: '8%', containLabel: true },
      xAxis: {
        type: 'category',
        data: entries.map(([k]) => getLevelText(k)),
        axisLine: { lineStyle: { color: 'rgba(0,0,0,0.1)' } },
        axisLabel: { color: '#8c8c9a', fontSize: 12 },
        axisTick: { show: false }
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: 'rgba(0,0,0,0.04)', type: 'dashed' } },
        axisLabel: { color: '#8c8c9a', fontSize: 12 }
      },
      series: [{
        name: '成果数量',
        type: 'bar',
        barWidth: '11%',
        data: entries.map(([_, value], idx) => ({
          value,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: palette[idx % palette.length] },
              { offset: 1, color: palette[idx % palette.length] + '66' }
            ]),
            borderRadius: [8, 8, 0, 0]
          }
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 12,
            shadowColor: 'rgba(102,126,234,0.3)'
          }
        }
      }]
    })
  })
}

const initStatusChart = (data) => {
  nextTick(() => {
    if (!statusChartRef.value) return
    const chart = getChart('status', statusChartRef.value)
    const statusColors = {
      approved: '#43e97b',
      pending: '#e6a23c',
      rejected: '#ef4444'
    }
    const entries = Object.entries(data)
    chart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)',
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: 'rgba(102,126,234,0.2)',
        borderWidth: 1,
        textStyle: { color: '#2a2a3a', fontSize: 12 }
      },
      legend: {
        bottom: '2%',
        left: 'center',
        textStyle: { color: '#5a5a6a', fontSize: 12 },
        itemWidth: 10,
        itemHeight: 10,
        itemGap: 18
      },
      series: [{
        name: '审核状态',
        type: 'pie',
        radius: ['48%', '85%'],
        center: ['50%', '46%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: 'rgba(255,255,255,0.9)',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'center',
          formatter: '{c|总数}\n{b|' + entries.reduce((a, [_, v]) => a + v, 0) + '}',
          rich: {
            c: { fontSize: 12, color: '#8c8c9a', lineHeight: 24 },
            b: { fontSize: 26, fontWeight: 'bold', color: '#667eea' }
          }
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 16,
            shadowColor: 'rgba(102,126,234,0.3)'
          }
        },
        labelLine: { show: false },
        data: entries.map(([key, value]) => ({
          value,
          name: getStatusText(key),
          itemStyle: {
            color: statusColors[key] || palette[0]
          }
        }))
      }]
    })
  })
}

const initClassRankChart = (data) => {
  nextTick(() => {
    if (!classRankChartRef.value) return
    const chart = getChart('rank', classRankChartRef.value)
    chart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: 'rgba(102,126,234,0.2)',
        borderWidth: 1,
        textStyle: { color: '#2a2a3a', fontSize: 12 }
      },
      grid: { left: '3%', right: '8%', bottom: '3%', top: '8%', containLabel: true },
      xAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: 'rgba(0,0,0,0.04)', type: 'dashed' } },
        axisLabel: { color: '#8c8c9a', fontSize: 12 }
      },
      yAxis: {
        type: 'category',
        data: data.map(item => item.class_name),
        axisLine: { lineStyle: { color: 'rgba(0,0,0,0.1)' } },
        axisTick: { show: false },
        axisLabel: { color: '#5a5a6a', fontSize: 12 }
      },
      series: [{
        name: '成果数量',
        type: 'bar',
        barWidth: '55%',
        data: data.map((item, idx) => ({
          value: item.achievement_count,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: idx < 3 ? '#667eea' : '#a8b1e8' },
              { offset: 1, color: idx < 3 ? '#764ba2' : '#c5cbf0' }
            ]),
            borderRadius: [0, 8, 8, 0]
          },
          label: {
            show: true,
            position: 'right',
            color: idx < 3 ? '#667eea' : '#8c8c9a',
            fontWeight: idx < 3 ? 'bold' : 'normal',
            fontSize: 12
          }
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 12,
            shadowColor: 'rgba(102,126,234,0.3)'
          }
        }
      }]
    })
  })
}

const initTrendChart = (data) => {
  nextTick(() => {
    if (!trendChartRef.value) return
    const chart = getChart('trend', trendChartRef.value)
    chart.setOption({
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: 'rgba(102,126,234,0.2)',
        borderWidth: 1,
        textStyle: { color: '#2a2a3a', fontSize: 12 }
      },
      legend: {
        data: ['提交数量', '通过数量'],
        top: '2%',
        right: '3%',
        textStyle: { color: '#5a5a6a', fontSize: 12 },
        itemWidth: 14,
        itemHeight: 8,
        itemGap: 18
      },
      grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: data.map(item => item.date),
        axisLine: { lineStyle: { color: 'rgba(0,0,0,0.1)' } },
        axisTick: { show: false },
        axisLabel: { color: '#8c8c9a', fontSize: 11 }
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: 'rgba(0,0,0,0.04)', type: 'dashed' } },
        axisLabel: { color: '#8c8c9a', fontSize: 12 }
      },
      series: [
        {
          name: '提交数量',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 7,
          data: data.map(item => item.submitted_count),
          lineStyle: { width: 3, color: '#667eea' },
          itemStyle: {
            color: '#667eea',
            borderColor: '#fff',
            borderWidth: 2
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(102,126,234,0.35)' },
              { offset: 1, color: 'rgba(102,126,234,0.02)' }
            ])
          },
          emphasis: {
            focus: 'series'
          }
        },
        {
          name: '通过数量',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 7,
          data: data.map(item => item.approved_count),
          lineStyle: { width: 3, color: '#43e97b' },
          itemStyle: {
            color: '#43e97b',
            borderColor: '#fff',
            borderWidth: 2
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(67,233,123,0.35)' },
              { offset: 1, color: 'rgba(67,233,123,0.02)' }
            ])
          },
          emphasis: {
            focus: 'series'
          }
        }
      ]
    })
  })
}

const handleResize = () => {
  chartInstances.forEach((instance) => {
    if (instance && !instance.isDisposed()) {
      instance.resize()
    }
  })
}

onMounted(() => {
  loadStatsData()
  loadTrendData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chartInstances.forEach((instance) => {
    if (instance && !instance.isDisposed()) {
      instance.dispose()
    }
  })
  chartInstances.clear()
})
</script>

<style scoped>
/* ============ Page Container ============ */
.stats-page {
  min-height: 100%;
  position: relative;
}

.content-wrap {
  position: relative;
  z-index: 1;
  padding-bottom: 20px;
}

/* ============ Animated Background ============ */
.bg-decor {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.blob-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  top: -100px;
  right: -100px;
  animation: float 20s ease-in-out infinite;
}

.blob-2 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  bottom: -50px;
  left: 10%;
  animation: float 25s ease-in-out infinite reverse;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #fa709a, #fee140);
  top: 40%;
  right: 20%;
  animation: float 30s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(40px, -30px) scale(1.05); }
  66% { transform: translate(-30px, 20px) scale(0.95); }
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    linear-gradient(rgba(102, 126, 234, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(102, 126, 234, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* ============ Page Header ============ */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-icon-wrap {
  position: relative;
}

.page-icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: #fff;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  position: relative;
}

.page-icon::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 18px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  z-index: -1;
  opacity: 0.3;
  filter: blur(8px);
}

.icon-pulse {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #43e97b;
  box-shadow: 0 0 0 0 rgba(67, 233, 123, 0.7);
  animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-ring {
  0% { box-shadow: 0 0 0 0 rgba(67, 233, 123, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(67, 233, 123, 0); }
  100% { box-shadow: 0 0 0 0 rgba(67, 233, 123, 0); }
}

.page-title {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  background: linear-gradient(135deg, #1a1a2e 0%, #667eea 50%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.page-subtitle {
  margin: 6px 0 0;
  font-size: 13px;
  color: #8c8c9a;
  letter-spacing: 0.2px;
}

.page-stats {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 22px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(102, 126, 234, 0.12);
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card--blue .stat-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-card--green .stat-icon {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.stat-card--orange .stat-icon {
  background: linear-gradient(135deg, #fa709a, #fee140);
}

.stat-card--purple .stat-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #1a1a2e 0%, #667eea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-variant-numeric: tabular-nums;
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: #8c8c9a;
  margin-top: 2px;
}

/* ============ Glass Card ============ */
.glass-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
  transition: box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.glass-card:hover {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
  opacity: 0.6;
  z-index: 1;
}

/* ============ Chart Card ============ */
.chart-card {
  margin-bottom: 20px;
}

.chart-glow {
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.12) 0%, transparent 70%);
  pointer-events: none;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  position: relative;
  z-index: 1;
}

.chart-title-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chart-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chart-icon--trend {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.chart-icon--pie {
  background: linear-gradient(135deg, #fa709a, #fee140);
}

.chart-icon--bar {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.chart-icon--ring {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.chart-icon--rank {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
}

.chart-subtitle {
  font-size: 12px;
  color: #8c8c9a;
  margin-top: 2px;
}

.chart-tabs {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 10px;
}

.tab-btn {
  padding: 6px 14px;
  border: none;
  background: transparent;
  border-radius: 7px;
  color: #8c8c9a;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-btn:hover {
  color: #667eea;
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
}

.chart-body {
  padding: 16px 20px 20px;
  position: relative;
  z-index: 1;
}

.chart-canvas {
  width: 100%;
  height: 340px;
}

.trend-card .chart-canvas {
  height: 380px;
}

.pie-card .chart-canvas {
  height: 380px;
}

/* ============ Skeleton ============ */
.chart-skeleton {
  width: 100%;
  height: 340px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.trend-card .chart-skeleton {
  height: 380px;
}

.pie-card .chart-skeleton {
  height: 380px;
}

.skeleton-chart {
  width: 90%;
  height: 80%;
  border-radius: 12px;
  background: linear-gradient(90deg, #f0f0f5 25%, #e8e8f0 50%, #f0f0f5 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ============ Charts Grid ============ */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.charts-grid .chart-card {
  margin-bottom: 0;
}

/* ============ Responsive ============ */
@media (max-width: 1200px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-stats {
    width: 100%;
  }

  .stat-card {
    flex: 1;
    min-width: calc(50% - 6px);
  }

  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .chart-tabs {
    width: 100%;
    justify-content: space-between;
  }

  .tab-btn {
    flex: 1;
  }

  .chart-canvas,
  .trend-card .chart-canvas,
  .pie-card .chart-canvas {
    height: 280px;
  }
}
</style>
