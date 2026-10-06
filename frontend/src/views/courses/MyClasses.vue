<template>
  <div class="my-classes-page">
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
              <el-icon :size="22"><School /></el-icon>
            </div>
            <div class="icon-pulse"></div>
          </div>
          <div class="page-title-text">
            <h1 class="page-title">我的课程</h1>
            <p class="page-subtitle">管理教学课程 · 查看学生 · 分享邀请码</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><School /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedClasses }}</span>
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
          <div class="stat-card stat-card--purple">
            <div class="stat-icon">
              <el-icon :size="18"><Calendar /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedSemesters }}</span>
              <span class="stat-label">覆盖学期</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Bar -->
      <div class="action-bar">
        <div class="search-box">
          <el-icon class="search-icon"><Search /></el-icon>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索班级名称、代码或学期..."
            class="search-input"
          />
          <button v-if="searchKeyword" class="clear-btn" @click="searchKeyword = ''">
            <el-icon><Close /></el-icon>
          </button>
        </div>
        <button
          v-if="$hasPermission('course:create')"
          class="create-btn"
          @click="showCreateDialog = true"
        >
          <el-icon><Plus /></el-icon>
          <span>创建课程</span>
          <div class="btn-shine"></div>
        </button>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="loading" class="cards-grid">
        <div v-for="i in 6" :key="i" class="skeleton-card">
          <div class="skeleton-header"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line short"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-footer"></div>
        </div>
      </div>

      <!-- Cards Grid -->
      <div v-else-if="filteredCourses.length > 0" class="cards-grid">
        <div
          v-for="(course, idx) in filteredCourses"
          :key="course.id"
          class="class-card"
          :style="{ animationDelay: `${idx * 60}ms` }"
          @click="goToDetail(course.id)"
        >
          <div class="card-glow"></div>
          <div class="card-accent"></div>

          <!-- Card Header -->
          <div class="card-header">
            <div class="card-icon-wrap">
              <el-icon :size="20"><Reading /></el-icon>
            </div>
            <div class="card-title-area">
              <h3 class="card-title">{{ course.name }}</h3>
              <span class="card-code">{{ course.code || '无代码' }}</span>
            </div>
            <span v-if="course.type === 'micro'" class="micro-tag">微课程</span>
          </div>

          <!-- Card Body -->
          <div class="card-body">
            <div class="info-grid">
              <div class="info-item">
                <div class="info-icon info-icon--blue">
                  <el-icon><Calendar /></el-icon>
                </div>
                <div class="info-text">
                  <span class="info-label">学期</span>
                  <span class="info-value">{{ course.semester || '-' }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon info-icon--green">
                  <el-icon><User /></el-icon>
                </div>
                <div class="info-text">
                  <span class="info-label">人数</span>
                  <span class="info-value">
                    {{ course.student_count || 0 }}
                    <span class="info-divider">/</span>
                    <span class="info-max">{{ course.max_students || 50 }}</span>
                  </span>
                </div>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="progress-area">
              <div class="progress-track">
                <div
                  class="progress-fill"
                  :style="{ width: getProgressWidth(course) + '%' }"
                ></div>
              </div>
              <span class="progress-text">{{ getProgressWidth(course) }}% 满员</span>
            </div>

            <div v-if="course.description" class="card-description">
              <el-icon><Document /></el-icon>
              <span>{{ course.description }}</span>
            </div>
          </div>

          <!-- Card Footer -->
          <div class="card-footer">
            <span class="footer-text">点击查看详情</span>
            <el-icon class="footer-arrow"><ArrowRight /></el-icon>
          </div>

          <!-- QR Action -->
          <div class="card-qr-action" @click.stop>
            <button class="qr-btn" @click="handleGenerateQR(course)">
              <el-icon><Grid /></el-icon>
              <span>生成二维码</span>
            </button>
            <button class="qr-btn qr-btn--invite" @click="handleGenerateInvite(course)">
              <el-icon><Key /></el-icon>
              <span>生成邀请码</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-orbit">
          <div class="empty-circle">
            <el-icon :size="48"><School /></el-icon>
          </div>
          <div class="orbit-dot orbit-dot--1"></div>
          <div class="orbit-dot orbit-dot--2"></div>
          <div class="orbit-dot orbit-dot--3"></div>
        </div>
        <h3 class="empty-title">{{ searchKeyword ? '未找到匹配的班级' : '暂无创建的班级' }}</h3>
        <p class="empty-desc">
          {{ searchKeyword ? '试试调整搜索关键词' : '创建您的第一个教学班级，开始管理学生和成果' }}
        </p>
        <button
          v-if="$hasPermission('course:create') && !searchKeyword"
          class="create-btn create-btn--center"
          @click="showCreateDialog = true"
        >
          <el-icon><Plus /></el-icon>
          <span>创建课程</span>
          <div class="btn-shine"></div>
        </button>
      </div>
    </div>

    <!-- Create Dialog -->
    <el-dialog
      v-model="showCreateDialog"
      width="520px"
      :close-on-click-modal="false"
      class="create-dialog"
      :show-close="false"
    >
      <template #header>
        <div class="dialog-header">
          <div class="dialog-icon-wrap">
            <el-icon :size="20"><Plus /></el-icon>
          </div>
          <div>
            <h3 class="dialog-title">创建课程</h3>
            <p class="dialog-subtitle">填写课程基本信息</p>
          </div>
          <button class="dialog-close" @click="showCreateDialog = false">
            <el-icon><Close /></el-icon>
          </button>
        </div>
      </template>

      <el-form :model="createForm" :rules="createRules" ref="createFormRef" label-position="top" class="create-form">
        <el-form-item label="班级名称" prop="name">
          <el-input v-model="createForm.name" placeholder="请输入班级名称" prefix-icon="Reading" />
        </el-form-item>
        <el-form-item label="学期" prop="semester">
          <el-input v-model="createForm.semester" placeholder="如：2024-2025学年第一学期" prefix-icon="Calendar" />
        </el-form-item>
        <el-form-item label="班级描述">
          <el-input
            v-model="createForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入班级描述（选填）"
          />
        </el-form-item>
        <el-form-item label="最大人数">
          <el-input-number v-model="createForm.max_students" :min="1" :max="500" placeholder="最大班级人数" class="full-width" />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="showCreateDialog = false">取消</button>
          <button class="confirm-btn" @click="handleCreate">
            <el-icon><Check /></el-icon>
            <span>创建班级</span>
          </button>
        </div>
      </template>
    </el-dialog>

    <!-- QR Code Dialog -->
    <el-dialog
      v-model="qrVisible"
      width="400px"
      :close-on-click-modal="true"
      class="qr-dialog"
      align-center
    >
      <template #header>
        <div class="dialog-header">
          <div class="dialog-icon-wrap">
            <el-icon :size="20"><Grid /></el-icon>
          </div>
          <div>
            <h3 class="dialog-title">班级二维码</h3>
            <p class="dialog-subtitle">请学生扫描二维码加入课程</p>
          </div>
        </div>
      </template>
      <div class="qr-wrapper">
        <div v-if="qrLoading" class="qr-loading">
          <el-icon class="is-loading" :size="32"><Loading /></el-icon>
          <p>正在生成二维码...</p>
        </div>
        <div v-else-if="qrCodeDataUrl" class="qr-image-wrap">
          <img :src="qrCodeDataUrl" alt="课程二维码" class="qr-image" />
          <p class="qr-course-name">{{ currentCourse?.name }}</p>
          <p class="qr-code-text">邀请码：{{ currentCourse?.invite_code || '-' }}</p>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="qrVisible = false">关闭</button>
          <button v-if="qrCodeDataUrl" class="confirm-btn" @click="downloadQR">
            <el-icon><Download /></el-icon>
            <span>下载二维码</span>
          </button>
        </div>
      </template>
    </el-dialog>

    <!-- Invite Code Dialog -->
    <el-dialog
      v-model="inviteVisible"
      width="400px"
      :close-on-click-modal="true"
      class="qr-dialog"
      align-center
    >
      <template #header>
        <div class="dialog-header">
          <div class="dialog-icon-wrap">
            <el-icon :size="20"><Key /></el-icon>
          </div>
          <div>
            <h3 class="dialog-title">课程邀请码</h3>
            <p class="dialog-subtitle">学生加入课程输入此邀请码</p>
          </div>
        </div>
      </template>
      <div class="qr-wrapper">
        <div v-if="inviteLoading" class="qr-loading">
          <el-icon class="is-loading" :size="32"><Loading /></el-icon>
          <p>正在生成邀请码...</p>
        </div>
        <div v-else class="invite-box">
          <span class="invite-code-text">{{ inviteCode || '--' }}</span>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="inviteVisible = false">关闭</button>
          <button class="confirm-btn" @click="copyInviteCode">
            <el-icon><CopyDocument /></el-icon>
            <span>复制邀请码</span>
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import QRCode from 'qrcode'
import {
  Plus, FolderOpened, School, User, Calendar, Search, Close,
  Reading, Document, ArrowRight, Check, Grid, Loading, Download,
  Key, CopyDocument
} from '@element-plus/icons-vue'

const router = useRouter()
const courses = ref([])
const loading = ref(true)
const searchKeyword = ref('')
const showCreateDialog = ref(false)
const createFormRef = ref(null)
const createForm = ref({
  name: '',
  semester: '',
  description: '',
  max_students: 50
})

const createRules = {
  name: [{ required: true, message: '请输入班级名称', trigger: 'blur' }],
  semester: [{ required: true, message: '请输入学期', trigger: 'blur' }]
}

// QR Code
const qrVisible = ref(false)
const qrLoading = ref(false)
const qrCodeDataUrl = ref('')
const currentCourse = ref(null)

// Invite Code
const inviteVisible = ref(false)
const inviteLoading = ref(false)
const inviteCode = ref('')

// Computed
const filteredCourses = computed(() => {
  if (!searchKeyword.value) return courses.value
  const kw = searchKeyword.value.toLowerCase()
  return courses.value.filter(c =>
    (c.name && c.name.toLowerCase().includes(kw)) ||
    (c.code && c.code.toLowerCase().includes(kw)) ||
    (c.semester && c.semester.toLowerCase().includes(kw))
  )
})

// Animated counters
const animatedClasses = ref(0)
const animatedStudents = ref(0)
const animatedSemesters = ref(0)

const animateValue = (target, refObj) => {
  const duration = 800
  const start = refObj.value
  const startTime = performance.now()
  const animate = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easeProgress = 1 - Math.pow(1 - progress, 3)
    refObj.value = Math.round(start + (target - start) * easeProgress)
    if (progress < 1) requestAnimationFrame(animate)
  }
  requestAnimationFrame(animate)
}

const updateStats = () => {
  const total = courses.value.length
  const students = courses.value.reduce((sum, c) => sum + (c.student_count || 0), 0)
  const semesters = new Set(courses.value.map(c => c.semester).filter(Boolean)).size
  animateValue(total, animatedClasses)
  animateValue(students, animatedStudents)
  animateValue(semesters, animatedSemesters)
}

const getProgressWidth = (course) => {
  const max = course.max_students || 50
  const current = course.student_count || 0
  return Math.min(Math.round((current / max) * 100), 100)
}

const fetchCourses = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/courses/my', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    const data = await res.json()
    if (data.courses) {
      courses.value = data.courses
      updateStats()
    }
  } catch (error) {
    console.error('获取课程列表失败:', error)
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
}

const goToDetail = (courseId) => {
  router.push(`/dashboard/courses/${courseId}`)
}

const handleGenerateQR = async (course) => {
  currentCourse.value = course
  qrVisible.value = true
  qrLoading.value = true
  qrCodeDataUrl.value = ''
  try {
    const res = await fetch(`/api/courses/${course.id}/qrcode`, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    const data = await res.json()
    if (res.ok) {
      qrCodeDataUrl.value = await QRCode.toDataURL(data.join_url, {
        width: 240,
        margin: 2,
        color: { dark: '#1a1a2e', light: '#ffffff' }
      })
      currentCourse.value = { ...course, invite_code: data.invite_code }
    } else {
      ElMessage.error(data.error || '生成二维码失败')
      qrVisible.value = false
    }
  } catch (error) {
    console.error('生成二维码失败:', error)
    ElMessage.error('生成二维码失败')
    qrVisible.value = false
  } finally {
    qrLoading.value = false
  }
}

const downloadQR = () => {
  if (!qrCodeDataUrl.value) return
  const link = document.createElement('a')
  link.download = `班级二维码_${currentCourse.value?.name || ''}.png`
  link.href = qrCodeDataUrl.value
  link.click()
}

const handleGenerateInvite = async (course) => {
  inviteVisible.value = true
  inviteCode.value = ''
  if (course?.invite_code) {
    inviteCode.value = course.invite_code
    return
  }
  inviteLoading.value = true
  try {
    const res = await fetch(`/api/courses/${course.id}/invite`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    const data = await res.json()
    if (res.ok && data.invite_code) {
      inviteCode.value = data.invite_code
      course.invite_code = data.invite_code
    } else {
      ElMessage.error(data.error || '生成邀请码失败')
    }
  } catch (error) {
    console.error('生成邀请码失败:', error)
    ElMessage.error('生成邀请码失败')
  } finally {
    inviteLoading.value = false
  }
}

const copyInviteCode = async () => {
  if (!inviteCode.value) return
  try {
    await navigator.clipboard.writeText(inviteCode.value)
    ElMessage.success('邀请码已复制')
  } catch (error) {
    ElMessage.error('复制失败，请手动复制')
  }
}

const handleCreate = async () => {
  if (!createFormRef.value) return
  await createFormRef.value.validate(async (valid) => {
    if (!valid) return
    try {
      const res = await fetch('/api/courses/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(createForm.value)
      })
      const data = await res.json()
      if (res.ok) {
        ElMessage.success('课程创建成功')
        showCreateDialog.value = false
        createForm.value = { name: '', semester: '', description: '', max_students: 50 }
        await fetchCourses()
      } else {
        ElMessage.error(data.error || '创建课程失败')
      }
    } catch (error) {
      console.error('创建课程失败:', error)
      ElMessage.error('创建课程失败')
    }
  })
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
/* ============ Page Container ============ */
.my-classes-page {
  min-height: 100%;
  position: relative;
}

.content-wrap {
  position: relative;
  z-index: 1;
  padding: 24px;
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
}

.stat-card--blue .stat-icon { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-card--green .stat-icon { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.stat-card--purple .stat-icon { background: linear-gradient(135deg, #f093fb, #f5576c); }

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

/* ============ Action Bar ============ */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  max-width: 420px;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  color: #8c8c9a;
  font-size: 16px;
  z-index: 1;
}

.search-input {
  width: 100%;
  height: 46px;
  padding: 0 40px 0 44px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  font-size: 14px;
  color: #2a2a3a;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-input::placeholder { color: #b0b0c0; }

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

.clear-btn {
  position: absolute;
  right: 12px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  color: #8c8c9a;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover { background: rgba(0, 0, 0, 0.1); color: #5a5a6a; }

.create-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 24px;
  height: 46px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.3);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(102, 126, 234, 0.4);
}

.create-btn:active { transform: translateY(0); }

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shine 3s ease-in-out infinite;
}

@keyframes shine {
  0%, 100% { left: -100%; }
  50% { left: 200%; }
}

.create-btn--center { margin-top: 8px; }

/* ============ Cards Grid ============ */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
}

.class-card {
  position: relative;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 22px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
  animation: card-enter 0.5s cubic-bezier(0.4, 0, 0.2, 1) backwards;
}

@keyframes card-enter {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.class-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.3);
}

.card-glow {
  position: absolute;
  top: -50%;
  right: -30%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
  pointer-events: none;
  transition: opacity 0.35s;
  opacity: 0;
}

.class-card:hover .card-glow { opacity: 1; }

.card-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, transparent 100%);
  opacity: 0.7;
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.card-icon-wrap {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.card-title-area {
  flex: 1;
  min-width: 0;
}

.card-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-code {
  font-size: 12px;
  color: #8c8c9a;
  font-family: 'SF Mono', 'Consolas', monospace;
  letter-spacing: 0.5px;
}

.micro-tag {
  flex-shrink: 0;
  padding: 3px 10px;
  background: linear-gradient(135deg, #fa709a, #fee140);
  color: #fff;
  font-size: 11px;
  font-weight: 500;
  border-radius: 20px;
}

/* Card Body */
.card-body { margin-bottom: 16px; }

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 14px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 10px;
}

.info-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.info-icon--blue { background: linear-gradient(135deg, #667eea, #764ba2); }
.info-icon--green { background: linear-gradient(135deg, #43e97b, #38f9d7); }

.info-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.info-label {
  font-size: 11px;
  color: #8c8c9a;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
  font-variant-numeric: tabular-nums;
}

.info-divider { color: #c0c0d0; margin: 0 2px; font-weight: 400; }
.info-max { color: #8c8c9a; font-weight: 400; font-size: 12px; }

/* Progress */
.progress-area {
  margin-bottom: 12px;
}

.progress-track {
  height: 6px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-text {
  font-size: 11px;
  color: #8c8c9a;
  margin-top: 6px;
  display: block;
}

.card-description {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
  color: #5a5a6a;
  line-height: 1.5;
  padding: 10px 12px;
  background: rgba(102, 126, 234, 0.04);
  border-radius: 10px;
  max-height: 60px;
  overflow: hidden;
}

.card-description .el-icon {
  color: #667eea;
  flex-shrink: 0;
  margin-top: 2px;
}

/* Card Footer */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.footer-text {
  font-size: 12px;
  color: #667eea;
  font-weight: 500;
}

.footer-arrow {
  color: #667eea;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.class-card:hover .footer-arrow { transform: translateX(4px); }

/* ============ Skeleton ============ */
.skeleton-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  padding: 22px;
  height: 280px;
}

.skeleton-header,
.skeleton-line,
.skeleton-footer {
  background: linear-gradient(90deg, #f0f0f5 25%, #e8e8f0 50%, #f0f0f5 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

.skeleton-header { width: 60%; height: 20px; margin-bottom: 20px; }
.skeleton-line { width: 100%; height: 14px; margin-bottom: 12px; }
.skeleton-line.short { width: 40%; }
.skeleton-footer { width: 30%; height: 14px; margin-top: 20px; }

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ============ Empty State ============ */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 24px;
}

.empty-orbit {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
}

.empty-circle {
  width: 100px;
  height: 100px;
  margin: 10px auto;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  border: 2px dashed rgba(102, 126, 234, 0.3);
  animation: float-circle 4s ease-in-out infinite;
}

@keyframes float-circle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.orbit-dot {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.orbit-dot--1 {
  top: 0;
  left: 50%;
  background: #667eea;
  animation: orbit-1 4s linear infinite;
}

.orbit-dot--2 {
  bottom: 10px;
  left: 10px;
  background: #43e97b;
  animation: orbit-2 5s linear infinite;
}

.orbit-dot--3 {
  bottom: 10px;
  right: 10px;
  background: #fa709a;
  animation: orbit-3 6s linear infinite;
}

@keyframes orbit-1 {
  from { transform: rotate(0deg) translateY(-60px) rotate(0deg); }
  to { transform: rotate(360deg) translateY(-60px) rotate(-360deg); }
}

@keyframes orbit-2 {
  from { transform: rotate(120deg) translateY(-60px) rotate(-120deg); }
  to { transform: rotate(480deg) translateY(-60px) rotate(-480deg); }
}

@keyframes orbit-3 {
  from { transform: rotate(240deg) translateY(-60px) rotate(-240deg); }
  to { transform: rotate(600deg) translateY(-60px) rotate(-600deg); }
}

.empty-title {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
  color: #2a2a3a;
}

.empty-desc {
  margin: 0 0 24px;
  font-size: 13px;
  color: #8c8c9a;
}

/* ============ Dialog ============ */
.create-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
}

.create-dialog :deep(.el-dialog__header) {
  margin: 0;
  padding: 0;
}

.create-dialog :deep(.el-dialog__body) {
  padding: 24px 28px 8px;
}

.create-dialog :deep(.el-dialog__footer) {
  padding: 8px 28px 24px;
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 22px 28px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.05));
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  position: relative;
}

.dialog-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.dialog-title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #1a1a2e;
}

.dialog-subtitle {
  margin: 2px 0 0;
  font-size: 12px;
  color: #8c8c9a;
}

.dialog-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 50%;
  color: #5a5a6a;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.dialog-close:hover {
  background: rgba(0, 0, 0, 0.08);
  transform: rotate(90deg);
}

.create-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 500;
  color: #2a2a3a;
  padding-bottom: 6px;
}

.create-form :deep(.el-input__wrapper),
.create-form :deep(.el-textarea__inner),
.create-form :deep(.el-input-number) {
  border-radius: 10px;
}

.full-width { width: 100%; }

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 0 22px;
  height: 40px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background: transparent;
  color: #5a5a6a;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.25s;
}

.cancel-btn:hover {
  background: rgba(0, 0, 0, 0.04);
  border-color: rgba(0, 0, 0, 0.15);
}

.confirm-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0 22px;
  height: 40px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.confirm-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4);
}

/* ============ QR Action Button ============ */
.card-qr-action {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.qr-btn--invite {
  border-color: rgba(56, 189, 248, 0.3);
  background: rgba(56, 189, 248, 0.06);
  color: #0ea5e9;
}

.qr-btn--invite:hover {
  background: linear-gradient(135deg, #38bdf8, #0ea5e9);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
}

/* ============ Invite Box ============ */
.invite-box {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 20px;
  background: rgba(102, 126, 234, 0.06);
  border: 1px dashed rgba(102, 126, 234, 0.4);
  border-radius: 14px;
}

.invite-code-text {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 34px;
  font-weight: 700;
  letter-spacing: 6px;
  color: #1a1a2e;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.qr-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 16px;
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 10px;
  background: rgba(102, 126, 234, 0.06);
  color: #667eea;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s;
}

.qr-btn:hover {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* ============ QR Dialog ============ */
.qr-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
}

.qr-dialog :deep(.el-dialog__header) {
  margin: 0;
  padding: 0;
}

.qr-dialog :deep(.el-dialog__body) {
  padding: 24px 28px 8px;
}

.qr-dialog :deep(.el-dialog__footer) {
  padding: 8px 28px 24px;
}

.qr-wrapper {
  text-align: center;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-loading {
  text-align: center;
  color: #8c8c9a;
}

.qr-loading p {
  margin-top: 12px;
  font-size: 14px;
}

.qr-loading .is-loading {
  animation: rotate 1.2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.qr-image-wrap {
  text-align: center;
}

.qr-image {
  width: 240px;
  height: 240px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.qr-course-name {
  margin: 16px 0 4px;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
}

.qr-code-text {
  margin: 0;
  font-size: 13px;
  color: #8c8c9a;
  font-family: 'SF Mono', 'Consolas', monospace;
  letter-spacing: 0.5px;
}

/* ============ Responsive ============ */
@media (max-width: 768px) {
  .content-wrap { padding: 16px; }

  .page-header { flex-direction: column; align-items: flex-start; }

  .page-stats { width: 100%; }

  .stat-card { flex: 1; min-width: calc(33.33% - 8px); padding: 12px; }

  .action-bar { flex-direction: column; align-items: stretch; }

  .search-box { max-width: none; }

  .cards-grid { grid-template-columns: 1fr; }

  .info-grid { grid-template-columns: 1fr; }
}
</style>
