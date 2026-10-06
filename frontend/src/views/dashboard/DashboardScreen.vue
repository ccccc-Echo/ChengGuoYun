<template>
  <div class="screen-wrap">
    <div class="screen-bg-grid"></div>

    <!-- 顶部标题栏 -->
    <div class="screen-header">
      <div class="header-deco deco-left"></div>
      <div class="header-title">
        <span class="title-main">成果云数据中心</span>
        <span class="title-sub">ACHIEVEMENT DATA CENTER</span>
      </div>
      <div class="header-actions">
        <el-button class="action-btn" :icon="Refresh" circle title="刷新" @click="refreshData" :loading="loading" />
      </div>
      <div class="header-deco deco-right"></div>
    </div>

    <!-- 顶部数据卡片 -->
    <div class="stat-cards">
      <div v-for="card in statCards" :key="card.key" class="stat-card" :class="card.gradient">
        <div class="card-icon">
          <el-icon :size="30"><component :is="card.icon" /></el-icon>
        </div>
        <div class="card-body">
          <div class="card-num">
            <AnimatedNumber :to="card.value" />
          </div>
          <div class="card-label">{{ card.label }}</div>
        </div>
        <div class="card-glow"></div>
      </div>
    </div>

    <!-- 中部图表区 -->
    <div class="chart-row">
      <div class="chart-card">
        <div class="chart-title">成果分类分布</div>
        <div class="chart-body"><PieChart v-if="hasCharts" :chart-data="categoryOption" height="260px" /></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">成果级别分布</div>
        <div class="chart-body"><BarChart v-if="hasCharts" :chart-data="levelOption" height="260px" /></div>
      </div>
    </div>
    <div class="chart-row">
      <div class="chart-card">
        <div class="chart-title">成果提交趋势（近12月）</div>
        <div class="chart-body"><LineChart v-if="hasCharts" :chart-data="trendOption" height="260px" /></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">各院系成果对比</div>
        <div class="chart-body"><BarChart v-if="hasCharts" :chart-data="deptOption" height="260px" /></div>
      </div>
    </div>

    <!-- 底部数据区 -->
    <div class="bottom-row">
      <div class="approval-card">
        <div class="chart-title">成果审核通过率</div>
        <div class="approval-inner">
          <div class="approval-rate">
            <AnimatedNumber class="rate-num" :to="approvalRate" :decimal="1" />
            <span class="rate-suffix">%</span>
          </div>
          <el-progress :percentage="approvalRate" :stroke-width="12" :show-text="false" color="#4d8bfe" class="progress-bar" />
          <div class="progress-labels">
            <span>已通过</span>
            <span>{{ approvedCount }} 项</span>
          </div>
        </div>
      </div>
      <div class="news-card">
        <div class="chart-title">实时动态</div>
        <div class="news-scroll" ref="newsRef">
          <div class="news-track" :style="{ transform: `translateY(-${newsOffset}px)` }">
            <div v-for="(item, idx) in newsLoopList" :key="idx" class="news-item">
              <span class="news-time">{{ item.created_at }}</span>
              <span class="news-text">{{ item.action_detail || item.action_type }}</span>
              <span class="news-user">{{ item.username }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { User, UserFilled, School, Refresh, DataAnalysis } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import LineChart from '@/components/Charts/LineChart.vue'
import BarChart from '@/components/Charts/BarChart.vue'
import PieChart from '@/components/Charts/PieChart.vue'
import { statsApi } from '@/api'
import { getMainCategoryLabel, getLevelLabel } from '@/utils/constants'

// 数字滚动组件（内联实现）
const AnimatedNumber = {
  name: 'AnimatedNumber',
  props: {
    to: { type: Number, default: 0 },
    decimal: { type: Number, default: 0 }
  },
  setup(props) {
    const display = ref(0)
    let raf = null
    const run = () => {
      if (raf) cancelAnimationFrame(raf)
      const start = performance.now()
      const from = 0
      const duration = 900
      const step = (t) => {
        const p = Math.min((t - start) / duration, 1)
        const eased = 1 - Math.pow(1 - p, 3)
        display.value = from + (props.to - from) * eased
        if (p < 1) raf = requestAnimationFrame(step)
        else display.value = props.to
      }
      raf = requestAnimationFrame(step)
    }
    watch(() => props.to, run)
    onMounted(run)
    onUnmounted(() => raf && cancelAnimationFrame(raf))
    return () => display.value.toFixed(props.decimal)
  }
}

const loading = ref(false)

const data = ref({
  overview: { total_achievements: 0, total_students: 0, total_teachers: 0, total_courses: 0 },
  category: [],
  level: [],
  trend: [],
  department: [],
  approval_rate: 0,
  recent: []
})

const chartColors = ['#4d8bfe', '#7c5cff', '#24d3d9', '#22c88a', '#f9a826', '#f76b8e', '#9b8cff', '#3fc1ff']

//
// 图表 options（复用自定义组件协议）
//
const hasCharts = ref(false)

const categoryOption = computed(() => ({
  name: '成果类型',
  data: data.value.category.map((item, i) => ({
    value: item.count,
    name: getMainCategoryLabel(item.name),
    itemStyle: {
      color: chartColors[i % chartColors.length],
      borderColor: '#fff',
      borderWidth: 2,
      shadowBlur: 8,
      shadowColor: 'rgba(77,139,254,0.25)'
    }
  }))
}))

const levelOption = computed(() => {
  const order = ['Xiao Ji', 'Sheng Ji', 'Guo Jia Ji', 'Guo Ji Ji']
  const labels = order.map(k => getLevelLabel(k))
  const values = order.map(k => {
    const f = data.value.level.find(l => l.level === k)
    return { value: f?.count || 0, itemStyle: { color: chartColors[order.indexOf(k)] } }
  })
  return {
    legend: ['级别分布'],
    xAxis: labels,
    series: [{ name: '级别分布', type: 'bar', data: values, barWidth: '45%', itemStyle: { borderRadius: [6, 6, 0, 0] } }]
  }
})

const trendOption = computed(() => ({
  legend: ['成果数量'],
  xAxis: data.value.trend.map(t => t.month),
  series: [{
    name: '成果数量',
    type: 'line',
    smooth: true,
    data: data.value.trend.map(t => t.count),
    areaStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(77,139,254,0.35)' },
        { offset: 1, color: 'rgba(77,139,254,0.03)' }
      ])
    },
    lineStyle: { color: '#4d8bfe', width: 3 },
    itemStyle: { color: '#4d8bfe' }
  }]
}))

const deptOption = computed(() => {
  const colors = data.value.department.map((_, i) => chartColors[i % chartColors.length])
  return {
    legend: ['成果数量'],
    xAxis: data.value.department.map(d => d.department),
    series: [{
      name: '成果数量',
      type: 'bar',
      data: data.value.department.map((d, i) => ({
        value: d.count,
        itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: colors[i] },
          { offset: 1, color: colors[i] + '55' }
        ]), borderRadius: [6, 6, 0, 0] }
      })),
      barWidth: '50%'
    }]
  }
})

//
// 顶部卡片
//
const statCards = computed(() => [
  { key: 'ach', label: '成果总数', value: data.value.overview.total_achievements, icon: DataAnalysis, gradient: 'g-blue' },
  { key: 'stu', label: '学生总数', value: data.value.overview.total_students, icon: User, gradient: 'g-purple' },
  { key: 'tea', label: '教师总数', value: data.value.overview.total_teachers, icon: UserFilled, gradient: 'g-cyan' },
  { key: 'cou', label: '班级/课程总数', value: data.value.overview.total_courses, icon: School, gradient: 'g-green' }
])

const approvalRate = computed(() => Number(data.value.approval_rate) || 0)
const approvedCount = computed(() => {
  const a = data.value.category.reduce((s, c) => s + c.count, 0)
  return a
})

// 实时动态滚动
const newsOffset = ref(0)
let newsTimer = null
const newsRef = ref(null)
const newsLoopList = computed(() => {
  const list = data.value.recent || []
  return list.length ? [...list, ...list] : []
})
const ITEM_HEIGHT = 38
const startNewsScroll = () => {
  stopNewsScroll()
  const list = data.value.recent || []
  if (list.length <= 5) return
  const total = list.length * ITEM_HEIGHT
  newsTimer = setInterval(() => {
    newsOffset.value += ITEM_HEIGHT
    if (newsOffset.value >= total) newsOffset.value = 0
  }, 1200)
}
const stopNewsScroll = () => {
  if (newsTimer) { clearInterval(newsTimer); newsTimer = null }
}

// 数据加载
const loadData = async () => {
  loading.value = true
  hasCharts.value = false
  try {
    const res = await statsApi.screenStats()
    if (res && typeof res === 'object') {
      data.value = {
        overview: res.overview || data.value.overview,
        category: res.category || [],
        level: res.level || [],
        trend: res.trend || [],
        department: res.department || [],
        approval_rate: res.approval_rate || 0,
        recent: res.recent || []
      }
    }
    hasCharts.value = true
    startNewsScroll()
  } catch (error) {
    hasCharts.value = true
    console.warn('加载大屏数据失败:', error?.message || error)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  loadData()
}

onMounted(() => {
  loadData()
})
onUnmounted(() => {
  stopNewsScroll()
})
</script>

<style scoped>
.screen-wrap {
  position: relative;
  padding: 24px 28px 28px;
  min-height: 100vh;
  background: linear-gradient(160deg, #f0f5ff 0%, #f7f9ff 40%, #eef3fe 100%);
  overflow: hidden;
  transition: all 0.3s ease;
}

.screen-wrap.is-fullscreen {
  padding: 24px 28px 28px;
}

.screen-bg-grid {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image:
    linear-gradient(rgba(77,139,254,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(77,139,254,0.05) 1px, transparent 1px);
  background-size: 42px 42px;
  pointer-events: none;
  z-index: 0;
}

.screen-wrap > * {
  position: relative;
  z-index: 1;
}

/* 顶部标题栏 */
.screen-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
  padding: 0 4px;
}

.header-deco {
  width: 130px;
  height: 2px;
  background: linear-gradient(90deg, #4d8bfe, transparent);
  box-shadow: 0 0 12px rgba(77,139,254,0.6);
}
.header-deco.deco-right {
  background: linear-gradient(270deg, #4d8bfe, transparent);
}

.header-title {
  text-align: center;
  display: flex;
  flex-direction: column;
}
.title-main {
  font-size: 30px;
  font-weight: 700;
  background: linear-gradient(135deg, #2b5fe0, #7c5cff, #24a3d9);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: 3px;
}
.title-sub {
  font-size: 10px;
  color: #8a94b3;
  letter-spacing: 5px;
  margin-top: 4px;
}

.header-actions {
  display: flex;
  gap: 10px;
  position: absolute;
  right: 28px;
  top: 24px;
  z-index: 5;
}
.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid rgba(77,139,254,0.25);
  background: rgba(255,255,255,0.7);
  color: #4d8bfe;
  backdrop-filter: blur(6px);
  transition: all 0.25s ease;
}
.action-btn:hover {
  background: #4d8bfe;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(77,139,254,0.35);
}

/* 顶部数据卡片 */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 20px;
}
.stat-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 22px 24px;
  border-radius: 16px;
  overflow: hidden;
  color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  animation: cardIn 0.6s ease both;
}
.stat-card:nth-child(2) { animation-delay: 0.08s; }
.stat-card:nth-child(3) { animation-delay: 0.16s; }
.stat-card:nth-child(4) { animation-delay: 0.24s; }
.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 30px rgba(30, 60, 140, 0.20);
}

.g-blue { background: linear-gradient(135deg, #4d8bfe 0%, #2b5fe0 100%); }
.g-purple { background: linear-gradient(135deg, #7c5cff 0%, #5a3de0 100%); }
.g-cyan { background: linear-gradient(135deg, #24d3d9 0%, #1aa8e2 100%); }
.g-green { background: linear-gradient(135deg, #22c88a 0%, #16a56f 100%); }

.card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 14px;
  background: rgba(255,255,255,0.18);
  backdrop-filter: blur(4px);
  flex-shrink: 0;
}
.card-body { display: flex; flex-direction: column; }
.card-num {
  font-size: 34px;
  font-weight: 800;
  line-height: 1.1;
  text-shadow: 0 2px 10px rgba(255,255,255,0.25);
}
.card-label {
  font-size: 13px;
  opacity: 0.9;
  margin-top: 6px;
  letter-spacing: 1px;
}
.card-glow {
  position: absolute;
  right: -30px;
  top: -30px;
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.25), transparent 70%);
  pointer-events: none;
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 图表区 */
.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}
.chart-card, .approval-card, .news-card {
  position: relative;
  background: rgba(255,255,255,0.82);
  border: 1px solid rgba(77,139,254,0.14);
  border-radius: 16px;
  padding: 18px 20px;
  backdrop-filter: blur(8px);
  box-shadow: 0 6px 20px rgba(40, 80, 160, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  animation: cardIn 0.6s ease both;
}
.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(40, 80, 160, 0.12);
}

.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: #2b3550;
  margin-bottom: 12px;
  padding-left: 10px;
  border-left: 3px solid #4d8bfe;
}

/* 底部 */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 18px;
}
.approval-inner {
  padding: 8px 4px;
}
.approval-rate {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 16px;
}
.rate-num {
  font-size: 52px;
  font-weight: 800;
  background: linear-gradient(135deg, #2b5fe0, #7c5cff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.rate-suffix { font-size: 20px; color: #2b3550; font-weight: 600; }
.progress-bar { margin-bottom: 10px; }
.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #8a94b3;
}

/* 实时动态 */
.news-card {
  min-height: 180px;
}
.news-scroll {
  height: 160px;
  overflow: hidden;
  margin-top: 6px;
}
.news-track { transition: transform 1s ease; }
.news-item {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 38px;
  padding: 0 6px;
  border-bottom: 1px dashed rgba(77,139,254,0.15);
  font-size: 13px;
  color: #2b3550;
}
.news-time {
  flex-shrink: 0;
  font-size: 12px;
  color: #8a94b3;
  font-family: Consolas, monospace;
}
.news-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.news-user {
  flex-shrink: 0;
  padding: 2px 10px;
  border-radius: 10px;
  background: rgba(77,139,254,0.1);
  color: #4d8bfe;
  font-size: 12px;
}

@media (max-width: 900px) {
  .stat-cards, .chart-row, .bottom-row { grid-template-columns: 1fr; }
  .stat-cards { grid-template-columns: repeat(2, 1fr); }
}
</style>