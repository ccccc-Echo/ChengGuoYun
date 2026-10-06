<template>
  <div class="classes-page">
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
              <el-icon :size="22"><OfficeBuilding /></el-icon>
            </div>
            <div class="icon-pulse"></div>
          </div>
          <div class="page-title-text">
            <h1 class="page-title">课程管理</h1>
            <p class="page-subtitle">管理课程档案 · 学生分配 · 成果查看</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><OfficeBuilding /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedTotal }}</span>
              <span class="stat-label">课程总数</span>
            </div>
          </div>
          <div class="stat-card stat-card--green">
            <div class="stat-icon">
              <el-icon :size="18"><User /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedStudents }}</span>
              <span class="stat-label">学生总数</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Filter Card -->
      <div class="glass-card filter-card">
        <div class="filter-glow"></div>
        <div class="filter-inner">
          <div class="filter-group">
            <div class="filter-item">
              <el-input
                v-model="filterForm.name"
                placeholder="课程名称"
                clearable
                size="large"
                class="filter-input"
              >
                <template #prefix>
                  <el-icon><OfficeBuilding /></el-icon>
                </template>
              </el-input>
            </div>
          </div>
          <div class="filter-divider"></div>
          <div class="filter-actions">
            <button class="btn-ghost-effect" @click="handleSearch">
              <el-icon><Search /></el-icon>
              <span>查询</span>
            </button>
            <button class="btn-ghost-effect" @click="resetFilter">
              <el-icon><Refresh /></el-icon>
              <span>重置</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Table Card -->
      <div class="glass-card table-card">
        <div class="table-header">
          <div class="tabs-wrap">
            <button
              :class="['tab-btn', { active: activeTab === 'all' }]"
              @click="handleTabChange('all')"
            >
              <el-icon :size="16"><OfficeBuilding /></el-icon>
              <span>全部课程</span>
              <span class="tab-count">{{ pagination.total }}</span>
            </button>
          </div>
          <div class="header-actions">
            <span class="result-summary">
              共 <b>{{ pagination.total }}</b> 条结果
            </span>
          </div>
        </div>

        <!-- Skeleton Loading -->
        <div v-if="loading && courses.length === 0" class="skeleton-wrap">
          <div v-for="n in 5" :key="n" class="skeleton-row">
            <div class="skeleton-item" style="width: 40px"></div>
            <div class="skeleton-item skeleton-avatar" style="width: 36px; height: 36px"></div>
            <div class="skeleton-item" style="width: 140px"></div>
            <div class="skeleton-item" style="width: 100px"></div>
            <div class="skeleton-item" style="width: 80px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 70px"></div>
            <div class="skeleton-item" style="width: 80px"></div>
            <div class="skeleton-item" style="width: 100px"></div>
            <div class="skeleton-item" style="width: 200px"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="courses.length === 0" class="empty-state">
          <div class="empty-illustration">
            <div class="empty-circle">
              <el-icon :size="48" color="#c0c0d0"><OfficeBuilding /></el-icon>
            </div>
            <div class="empty-orbit"></div>
          </div>
          <h3 class="empty-title">暂无课程数据</h3>
          <p class="empty-desc">暂无课程，教师可在「我的课程」中创建课程</p>
        </div>

        <!-- Table -->
        <div v-else class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-name">课程信息</th>
                <th class="col-code">编号</th>
                <th class="col-department">学期</th>
                <th class="col-count">学生人数</th>
                <th class="col-advisor">负责人</th>
                <th class="col-created">创建时间</th>
                <th class="col-action">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, idx) in courses"
                :key="row.id"
                class="table-row"
                :style="{ '--accent-color': getRowColor(row), animationDelay: idx * 30 + 'ms' }"
              >
                <td class="col-index">
                  <span class="index-num">{{ String(idx + 1).padStart(2, '0') }}</span>
                </td>
                <td class="col-name">
                  <div class="class-name-cell">
                    <div class="class-avatar" :style="{ background: getRowColor(row) }">
                      {{ (row.name || '?').charAt(0) }}
                    </div>
                    <div class="class-name-info">
                      <span class="class-name">
                        {{ row.name }}
                        <el-icon v-if="row.is_locked ?? 0" class="lock-icon" title="已锁定"><Lock /></el-icon>
                      </span>
                      <span class="class-sub">{{ row.semester || '未设置学期' }}</span>
                    </div>
                  </div>
                </td>
                <td class="col-code">
                  <span class="code-text">{{ row.id || row.code || '-' }}</span>
                </td>
                <td class="col-department">
                  <span class="dept-text">{{ row.semester || '-' }}</span>
                </td>
                <td class="col-count">
                  <span class="count-badge" :class="{ 'has-students': row.student_count > 0 }">
                    <el-icon class="count-icon"><User /></el-icon>
                    {{ row.student_count || 0 }}
                    <span class="count-max" v-if="row.max_students">/{{ row.max_students }}</span>
                  </span>
                </td>
                <td class="col-advisor">
                  <div class="advisor-cell" v-if="row.teacher_name">
                    <span class="advisor-avatar">{{ (row.teacher_name || '?').charAt(0) }}</span>
                    <span class="advisor-name">{{ row.teacher_name }}</span>
                  </div>
                  <span v-else class="no-data">-</span>
                </td>
                <td class="col-created">
                  <span class="time-text">{{ row.created_at || '-' }}</span>
                </td>
                <td class="col-action">
                  <div class="action-group">
                    <button class="action-btn action-btn--primary" @click="goToCourseDetail(row.id)">
                      <el-icon><View /></el-icon>
                      详情
                    </button>
                    <button
                      v-if="$hasPermission('course:lock')"
                      :class="['action-btn', (row.is_locked ?? 0) ? 'action-btn--warning' : 'action-btn--lock']"
                      @click="handleToggleLock(row)"
                    >
                      <el-icon><Lock v-if="!(row.is_locked ?? 0)" /><Unlock v-else /></el-icon>
                      {{ (row.is_locked ?? 0) ? '解锁' : '锁定' }}
                    </button>
                    <button
                      v-if="$hasPermission('course:delete')"
                      class="action-btn action-btn--danger"
                      @click="handleDelete(row)"
                    >
                      <el-icon><Delete /></el-icon>
                      删除
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Table Footer -->
        <div class="table-footer" v-if="courses.length > 0">
          <span class="total-text">
            共 <b>{{ pagination.total }}</b> 门课程，每页 <b>{{ pagination.page_size }}</b> 条
          </span>
          <div class="pagination-wrap">
            <button
              class="page-btn"
              :disabled="pagination.page <= 1"
              @click="goPage(pagination.page - 1)"
            >
              <el-icon><ArrowLeft /></el-icon>
            </button>
            <template v-for="p in visiblePages" :key="p">
              <button
                v-if="p !== '...'"
                :class="['page-btn', { active: p === pagination.page }]"
                @click="goPage(p)"
              >{{ p }}</button>
              <span v-else class="page-ellipsis">...</span>
            </template>
            <button
              class="page-btn"
              :disabled="pagination.page >= totalPages"
              @click="goPage(pagination.page + 1)"
            >
              <el-icon><ArrowRight /></el-icon>
            </button>
            <select v-model="pagination.page_size" class="page-size-select" @change="loadCourses">
              <option :value="10">10 条/页</option>
              <option :value="20">20 条/页</option>
              <option :value="50">50 条/页</option>
              <option :value="100">100 条/页</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Add/Edit Dialog (移除，课程由教师在“我的课程”创建) -->
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, User,
  OfficeBuilding, Delete, View,
  ArrowLeft, ArrowRight, Lock, Unlock
} from '@element-plus/icons-vue'
import { coursesApi } from '@/api'

const router = useRouter()
const loading = ref(false)
const courses = ref([])
const activeTab = ref('all')

const pagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

const filterForm = ref({
  name: ''
})

// Animated counters
const animatedTotal = ref(0)
const animatedStudents = ref(0)
const animateValue = (target, refObj) => {
  const duration = 600
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

const totalStudents = computed(() => {
  return courses.value.reduce((sum, c) => sum + (c.student_count || 0), 0)
})

watch(() => pagination.value.total, (val) => {
  animateValue(val, animatedTotal)
})

watch(totalStudents, (val) => {
  animateValue(val, animatedStudents)
})

const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.page_size))

const visiblePages = computed(() => {
  const pages = []
  const current = pagination.value.page
  const total = totalPages.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

// Color scheme for rows
const classColors = [
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #4facfe, #00f2fe)',
  'linear-gradient(135deg, #43e97b, #38f9d7)',
  'linear-gradient(135deg, #fa709a, #fee140)',
  'linear-gradient(135deg, #f093fb, #f5576c)',
  'linear-gradient(135deg, #a8edea, #fed6e3)'
]

const getRowColor = (row) => {
  const name = row.name || ''
  const charCode = name.charCodeAt(0) || 0
  return classColors[charCode % classColors.length]
}

const loadCourses = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      ...filterForm.value
    }

    const res = await coursesApi.list(params)
    courses.value = res.courses || []
    pagination.value.total = res.pagination?.total || 0
  } catch (error) {
    console.error('加载课程列表失败:', error)
    ElMessage.error('加载课程列表失败')
  } finally {
    loading.value = false
  }
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  pagination.value.page = 1
  loadCourses()
}

const handleSearch = () => {
  pagination.value.page = 1
  loadCourses()
}

const resetFilter = () => {
  filterForm.value = {
    name: ''
  }
  pagination.value.page = 1
  loadCourses()
}

const goPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  pagination.value.page = page
  loadCourses()
}

const handleDelete = (row) => {
  if (row.is_locked) {
    ElMessage.warning('课程已锁定，请先解锁再删除')
    return
  }
  ElMessageBox.confirm(
    `确认要删除该课程「${row.name}」吗？<br/><span style="color:#8c8c9a;font-size:12px;">此操作不可恢复。</span>`,
    '确认删除',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      await coursesApi.delete(row.id)
      ElMessage.success('课程已删除')
      loadCourses()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error(error.response?.data?.error || '删除失败')
    }
  })
}

const goToCourseDetail = (courseId) => {
  router.push(`/dashboard/courses/${courseId}`)
}

const handleToggleLock = async (row) => {
  const action = row.is_locked ? '解锁' : '锁定'
  const isLocked = !row.is_locked
  ElMessageBox.confirm(
    `确认要${action}「${row.name}」吗？`,
    `确认${action}`,
    {
      confirmButtonText: `确定${action}`,
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const res = await coursesApi.lock(row.id, { is_locked: isLocked })
      ElMessage.success(res?.message || `${action}成功`)
      loadCourses()
    } catch (error) {
      console.error(`${action}失败:`, error)
      ElMessage.error(error.response?.data?.error || `${action}失败`)
    }
  })
}

onMounted(() => {
  loadCourses()
})
</script>

<style scoped>
/* ============ Page Container ============ */
.classes-page {
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
  background: linear-gradient(135deg, #43e97b, #38f9d7);
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
  gap: 14px;
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
}

.glass-card:hover {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
}

/* ============ Filter Card ============ */
.filter-card {
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}

.filter-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
  opacity: 0.6;
}

.filter-glow {
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.12) 0%, transparent 70%);
  pointer-events: none;
}

.filter-inner {
  padding: 22px 28px;
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.filter-item {
  min-width: 200px;
}

.filter-input {
  width: 220px;
}

.filter-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.06) inset;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.6);
}

.filter-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.4) inset;
  background: rgba(255, 255, 255, 0.8);
}

.filter-input :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.5) inset, 0 4px 12px rgba(102, 126, 234, 0.1);
  background: #fff;
}

.filter-divider {
  width: 1px;
  height: 36px;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.08), transparent);
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}

.btn-ghost-effect {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.8);
  color: #5a5a6a;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-ghost-effect::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: #667eea;
  opacity: 0.1;
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.btn-ghost-effect:hover::after {
  width: 60px;
  height: 60px;
}

.btn-ghost-effect:hover {
  border-color: #667eea;
  color: #667eea;
  background: rgba(102, 126, 234, 0.04);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.18);
}

.btn-ghost-effect:active {
  transform: translateY(0);
}

.btn-create-effect {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.btn-create-effect::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 14px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  z-index: -1;
  opacity: 0;
  filter: blur(8px);
  transition: opacity 0.3s;
}

.btn-create-effect:hover::before {
  opacity: 0.5;
}

.btn-create-effect:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(102, 126, 234, 0.5);
}

.btn-create-effect:active {
  transform: translateY(0);
}

.btn-create-effect:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shine 3s infinite;
}

@keyframes shine {
  100% { left: 100%; }
}

.btn-empty {
  margin-top: 20px;
  padding: 12px 28px;
  font-size: 15px;
}

/* ============ Table Card ============ */
.table-card {
  overflow: visible;
  position: relative;
  padding: 0 28px;
}

.table-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
  opacity: 0.6;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.tabs-wrap {
  display: flex;
  gap: 4px;
  position: relative;
}

.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  background: transparent;
  border-radius: 10px;
  color: #8c8c9a;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.tab-btn:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.tab-btn.active {
  color: #667eea;
  background: rgba(102, 126, 234, 0.08);
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.result-summary {
  font-size: 13px;
  color: #8c8c9a;
}

.result-summary b {
  color: #667eea;
  font-weight: 600;
}

/* ============ Skeleton ============ */
.skeleton-wrap {
  padding: 12px 28px;
}

.skeleton-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #f5f5fa;
}

.skeleton-item {
  height: 16px;
  border-radius: 6px;
  background: linear-gradient(90deg, #f0f0f5 25%, #e8e8f0 50%, #f0f0f5 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-avatar {
  border-radius: 10px;
}

.skeleton-tag {
  height: 20px;
  border-radius: 10px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ============ Empty State ============ */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.empty-illustration {
  position: relative;
  width: 100px;
  height: 100px;
  margin-bottom: 24px;
}

.empty-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float-circle 3s ease-in-out infinite;
}

@keyframes float-circle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.empty-orbit {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border: 2px dashed rgba(102, 126, 234, 0.15);
  border-radius: 50%;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  to { transform: rotate(360deg); }
}

.empty-title {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: #2a2a3a;
}

.empty-desc {
  margin: 0 0 4px;
  font-size: 14px;
  color: #8c8c9a;
}

/* ============ Table ============ */
.table-scroll {
  overflow-x: auto;
}

.data-table {
  width: auto;
  border-collapse: separate;
  border-spacing: 0;
}

.data-table thead th {
  font-size: 12px;
  font-weight: 600;
  color: #8c8c9a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  white-space: nowrap;
  position: sticky;
  top: 0;
  background: transparent;
  vertical-align: middle;
}

.data-table tbody td {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.03);
  font-size: 14px;
  color: #2a2a3a;
  vertical-align: middle;
  white-space: nowrap;
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

/* ============ Column Alignment ============ */
/* Center: index, number, date columns */
.data-table thead th.col-index,
.data-table thead th.col-count,
.data-table thead th.col-created,
.data-table tbody td.col-index,
.data-table tbody td.col-count,
.data-table tbody td.col-created {
  text-align: center;
}

/* Left: name, info columns */
.data-table thead th.col-name,
.data-table thead th.col-code,
.data-table thead th.col-department,
.data-table thead th.col-grade,
.data-table thead th.col-advisor,
.data-table tbody td.col-name,
.data-table tbody td.col-code,
.data-table tbody td.col-department,
.data-table tbody td.col-grade,
.data-table tbody td.col-advisor {
  text-align: left;
}

/* Left: action column */
.data-table thead th.col-action,
.data-table tbody td.col-action {
  text-align: left;
}

.index-num {
  font-size: 13px;
  font-weight: 600;
  color: #c0c0d0;
  font-variant-numeric: tabular-nums;
}

.class-name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: flex-start;
}

.class-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 15px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.class-name-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  justify-content: center;
}

.class-name {
  font-weight: 600;
  color: #1a1a2e;
  white-space: nowrap;
  line-height: 1.4;
}

.class-sub {
  font-size: 12px;
  color: #8c8c9a;
  line-height: 1.3;
}

.code-text {
  font-family: 'SF Mono', 'Monaco', monospace;
  font-size: 13px;
  color: #5a5a6a;
  white-space: nowrap;
  line-height: 1.4;
}

.dept-text {
  color: #5a5a6a;
  white-space: nowrap;
  line-height: 1.4;
}

.grade-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  border-radius: 8px;
  font-size: 12px;
  color: #667eea;
  font-weight: 500;
  white-space: nowrap;
  vertical-align: middle;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.04);
  font-size: 12px;
  font-weight: 600;
  color: #8c8c9a;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  vertical-align: middle;
}

.count-badge.has-students {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
  color: #fff;
}

.count-icon {
  font-size: 12px;
}

.count-max {
  opacity: 0.7;
  font-weight: 400;
}

.advisor-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: flex-start;
}

.advisor-avatar {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5a5a6a;
  font-weight: 600;
  font-size: 13px;
  flex-shrink: 0;
}

.advisor-name {
  font-size: 14px;
  color: #2a2a3a;
  white-space: nowrap;
  line-height: 1.4;
}

.no-data {
  color: #c0c0d0;
  line-height: 1.4;
}

.time-text {
  font-size: 13px;
  color: #8c8c9a;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  line-height: 1.4;
}

/* ============ Action Buttons ============ */
.action-group {
  display: flex;
  gap: 4px;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #5a5a6a;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

.action-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.1;
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.action-btn:hover::after {
  width: 40px;
  height: 40px;
}

.action-btn:active {
  transform: translateY(0);
}

.action-btn--primary {
  color: #667eea;
}

.action-btn--primary:hover {
  background: rgba(102, 126, 234, 0.08);
  transform: translateY(-1px);
}

.action-btn--danger {
  color: #ef4444;
}

.action-btn--danger:hover {
  background: rgba(239, 68, 68, 0.08);
  transform: translateY(-1px);
}

.action-btn--lock {
  color: #f59e0b;
}

.action-btn--lock:hover {
  background: rgba(245, 158, 11, 0.08);
  transform: translateY(-1px);
}

.action-btn--warning {
  color: #10b981;
}

.action-btn--warning:hover {
  background: rgba(16, 185, 129, 0.08);
  transform: translateY(-1px);
}

.lock-icon {
  color: #f59e0b;
  font-size: 14px;
  margin-left: 4px;
  vertical-align: middle;
}

.form-tip {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
  font-size: 12px;
  color: #f59e0b;
}

.form-tip .el-icon {
  font-size: 14px;
}

/* ============ Table Footer ============ */
.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 28px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.total-text {
  font-size: 13px;
  color: #8c8c9a;
}

.total-text b {
  color: #667eea;
  font-weight: 600;
}

.pagination-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 34px;
  padding: 0 10px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.8);
  color: #5a5a6a;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-btn:hover:not(:disabled):not(.active) {
  border-color: #667eea;
  color: #667eea;
  background: rgba(102, 126, 234, 0.04);
}

.page-btn.active {
  border-color: transparent;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-ellipsis {
  padding: 0 4px;
  color: #b0b0c0;
}

.page-size-select {
  height: 34px;
  padding: 0 12px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.8);
  color: #5a5a6a;
  font-size: 13px;
  cursor: pointer;
  outline: none;
  transition: all 0.2s ease;
}

.page-size-select:hover {
  border-color: #667eea;
}

/* ============ Dialog ============ */
.custom-dialog :deep(.el-dialog) {
  border-radius: 20px !important;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(24px);
}

.custom-dialog :deep(.el-dialog__header) {
  padding: 0;
  margin: 0;
}

.custom-dialog :deep(.el-dialog__body) {
  padding: 24px 28px;
}

.custom-dialog :deep(.el-dialog__footer) {
  padding: 16px 28px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 24px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.dialog-header-icon {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.dialog-header-icon.add-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.dialog-header-icon.edit-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.dialog-title {
  font-size: 17px;
  font-weight: 600;
  color: #1a1a2e;
}

.dialog-subtitle {
  font-size: 12px;
  color: #8c8c9a;
  margin-top: 2px;
}

.dialog-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #5a5a6a;
}

.dialog-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.06) inset;
  transition: all 0.25s ease;
  background: rgba(255, 255, 255, 0.6);
}

.dialog-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3) inset;
}

.dialog-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.4) inset;
  background: #fff;
}

/* ============ Scrollbar ============ */
.table-scroll::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

.table-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.table-scroll::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.table-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.2);
}

/* ============ Responsive ============ */
@media (max-width: 1200px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .filter-actions {
    margin-left: 0;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .page-stats {
    flex-wrap: wrap;
  }

  .filter-group {
    flex-direction: column;
    width: 100%;
  }

  .filter-item,
  .filter-input {
    width: 100%;
  }
}
</style>
