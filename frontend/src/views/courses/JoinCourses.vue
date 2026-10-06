<template>
  <div class="join-courses-page">
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
              <el-icon :size="22"><Promotion /></el-icon>
            </div>
            <div class="icon-pulse"></div>
          </div>
          <div class="page-title-text">
            <h1 class="page-title">加入课程</h1>
            <p class="page-subtitle">邀请码加课 · 扫码加课 · 微课程选择</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><Reading /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedJoined }}</span>
              <span class="stat-label">已加入课程</span>
            </div>
          </div>
          <div class="stat-card stat-card--green">
            <div class="stat-icon">
              <el-icon :size="18"><Star /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedStarred }}</span>
              <span class="stat-label">置顶课程</span>
            </div>
          </div>
          <div class="stat-card stat-card--purple">
            <div class="stat-icon">
              <el-icon :size="18"><Collection /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedMicro }}</span>
              <span class="stat-label">可选微课程</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Title + Action -->
      <div class="section-bar">
        <div class="section-title-wrap">
          <div class="section-dot"></div>
          <h3 class="section-title">已加入课程</h3>
          <span class="section-count">{{ filteredCourses.length }}</span>
        </div>
        <div class="section-actions">
          <div class="search-box">
            <el-icon class="search-icon"><Search /></el-icon>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索课程名称、教师..."
              class="search-input"
            />
            <button v-if="searchKeyword" class="clear-btn" @click="searchKeyword = ''">
              <el-icon><Close /></el-icon>
            </button>
          </div>
          <button class="add-btn" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            <span>添加课程</span>
            <div class="btn-shine"></div>
          </button>
        </div>
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
          class="course-card"
          :class="{ 'course-card--starred': course.is_starred }"
          :style="{ animationDelay: `${idx * 60}ms` }"
        >
          <div class="card-glow"></div>
          <div class="card-accent"></div>

          <!-- Star Badge -->
          <div v-if="course.is_starred" class="star-badge">
            <el-icon><StarFilled /></el-icon>
          </div>

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
                  <el-icon><User /></el-icon>
                </div>
                <div class="info-text">
                  <span class="info-label">任课教师</span>
                  <span class="info-value">{{ course.teacher_name || '-' }}</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon info-icon--green">
                  <el-icon><UserFilled /></el-icon>
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

            <div v-if="course.description" class="card-description">
              <el-icon><Document /></el-icon>
              <span>{{ course.description }}</span>
            </div>
          </div>

          <!-- Card Footer -->
          <div class="card-footer">
            <button class="action-btn action-btn--star" @click.stop="handleStar(course.id)">
              <el-icon>
                <StarFilled v-if="course.is_starred" />
                <Star v-else />
              </el-icon>
              <span>{{ course.is_starred ? '取消置顶' : '置顶' }}</span>
            </button>
            <button class="action-btn action-btn--leave" @click.stop="handleLeave(course.id)">
              <el-icon><SwitchButton /></el-icon>
              <span>退课</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-orbit">
          <div class="empty-circle">
            <el-icon :size="48"><Reading /></el-icon>
          </div>
          <div class="orbit-dot orbit-dot--1"></div>
          <div class="orbit-dot orbit-dot--2"></div>
          <div class="orbit-dot orbit-dot--3"></div>
        </div>
        <h3 class="empty-title">{{ searchKeyword ? '未找到匹配的课程' : '暂无已加入课程' }}</h3>
        <p class="empty-desc">
          {{ searchKeyword ? '试试调整搜索关键词' : '通过邀请码、扫码或选择微课程加入课程' }}
        </p>
        <button v-if="!searchKeyword" class="add-btn add-btn--center" @click="showAddDialog = true">
          <el-icon><Plus /></el-icon>
          <span>添加课程</span>
          <div class="btn-shine"></div>
        </button>
      </div>
    </div>

    <!-- Add Course Dialog -->
    <el-dialog
      v-model="showAddDialog"
      width="560px"
      :close-on-click-modal="false"
      class="add-dialog"
      :show-close="false"
    >
      <template #header>
        <div class="dialog-header">
          <div class="dialog-icon-wrap">
            <el-icon :size="20"><Plus /></el-icon>
          </div>
          <div>
            <h3 class="dialog-title">添加课程</h3>
            <p class="dialog-subtitle">选择方式加入课程</p>
          </div>
          <button class="dialog-close" @click="showAddDialog = false">
            <el-icon><Close /></el-icon>
          </button>
        </div>
      </template>

      <!-- Custom Tabs -->
      <div class="custom-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          :class="['tab-item', { active: addCourseTab === tab.value }]"
          @click="addCourseTab = tab.value"
        >
          <el-icon><component :is="tab.icon" /></el-icon>
          <span>{{ tab.label }}</span>
        </button>
        <div
          class="tab-indicator"
          :style="indicatorStyle"
        ></div>
      </div>

      <div class="tab-content">
        <!-- Invite Code -->
        <div v-show="addCourseTab === 'invite'" class="invite-pane">
          <div class="invite-icon-wrap">
            <el-icon :size="32"><Key /></el-icon>
          </div>
          <h4 class="pane-title">邀请码加课</h4>
          <p class="pane-desc">请输入教师提供的6位邀请码</p>
          <div class="code-input-group">
            <input
              v-for="(_, i) in 6"
              :key="i"
              :ref="el => codeInputs[i] = el"
              v-model="codeDigits[i]"
              type="text"
              maxlength="1"
              class="code-input"
              @input="handleCodeInput($event, i)"
              @keydown.delete="handleCodeDelete($event, i)"
              @paste="handleCodePaste($event, i)"
            />
          </div>
          <button
            class="submit-btn"
            :disabled="codeDigits.join('').length !== 6 || joining"
            @click="joinByInviteCode"
          >
            <el-icon v-if="joining" class="is-loading"><Loading /></el-icon>
            <el-icon v-else><Check /></el-icon>
            <span>{{ joining ? '加入中...' : '加入课程' }}</span>
          </button>
        </div>

        <!-- Scan QR -->
        <div v-show="addCourseTab === 'scan'" class="scan-pane">
          <div class="qr-frame">
            <div class="qr-corner qr-corner--tl"></div>
            <div class="qr-corner qr-corner--tr"></div>
            <div class="qr-corner qr-corner--bl"></div>
            <div class="qr-corner qr-corner--br"></div>
            <div class="qr-inner">
              <el-icon :size="56"><Iphone /></el-icon>
              <p>扫码识别课程邀请码</p>
            </div>
            <div class="scan-line"></div>
          </div>
          <p class="scan-tip">请使用手机扫描教师展示的二维码加入课程</p>
        </div>

        <!-- Micro Courses -->
        <div v-show="addCourseTab === 'micro'" class="micro-pane">
          <div v-if="microCourses.length > 0" class="micro-list">
            <div
              v-for="course in microCourses"
              :key="course.id"
              class="micro-item"
            >
              <div class="micro-icon-wrap">
                <el-icon><Collection /></el-icon>
              </div>
              <div class="micro-info">
                <span class="micro-name">{{ course.name }}</span>
                <span class="micro-desc">{{ course.description || '暂无描述' }}</span>
              </div>
              <button
                class="micro-join-btn"
                :disabled="joining"
                @click="joinByCourseId(course.id)"
              >
                <el-icon><Plus /></el-icon>
                <span>加入</span>
              </button>
            </div>
          </div>
          <div v-else class="micro-empty">
            <div class="empty-circle-small">
              <el-icon :size="32"><Collection /></el-icon>
            </div>
            <p>暂无可选微课程</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Star, StarFilled, FolderOpened, Document, Promotion,
  Reading, User, UserFilled, Search, Close, Collection, Key,
  Iphone, Check, SwitchButton, Loading
} from '@element-plus/icons-vue'

const showAddDialog = ref(false)
const addCourseTab = ref('invite')
const inviteCode = ref('')
const joining = ref(false)
const loading = ref(true)
const myCourses = ref([])
const microCourses = ref([])
const searchKeyword = ref('')

// Code digit inputs
const codeDigits = ref(['', '', '', '', '', ''])
const codeInputs = ref([])

const tabs = [
  { label: '邀请码', value: 'invite', icon: Key },
  { label: '扫码', value: 'scan', icon: Iphone },
  { label: '微课程', value: 'micro', icon: Collection }
]

const indicatorStyle = computed(() => {
  const idx = tabs.findIndex(t => t.value === addCourseTab.value)
  return { transform: `translateX(${idx * 100}%)` }
})

// Computed
const filteredCourses = computed(() => {
  if (!searchKeyword.value) return myCourses.value
  const kw = searchKeyword.value.toLowerCase()
  return myCourses.value.filter(c =>
    (c.name && c.name.toLowerCase().includes(kw)) ||
    (c.teacher_name && c.teacher_name.toLowerCase().includes(kw)) ||
    (c.code && c.code.toLowerCase().includes(kw))
  )
})

// Animated counters
const animatedJoined = ref(0)
const animatedStarred = ref(0)
const animatedMicro = ref(0)

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
  animateValue(myCourses.value.length, animatedJoined)
  animateValue(myCourses.value.filter(c => c.is_starred).length, animatedStarred)
  animateValue(microCourses.value.length, animatedMicro)
}

// Code input handlers
const handleCodeInput = (e, i) => {
  const val = e.target.value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase()
  codeDigits.value[i] = val
  if (val && i < 5) {
    nextTick(() => codeInputs.value[i + 1]?.focus())
  }
  inviteCode.value = codeDigits.value.join('')
}

const handleCodeDelete = (e, i) => {
  if (!codeDigits.value[i] && i > 0) {
    e.preventDefault()
    nextTick(() => codeInputs.value[i - 1]?.focus())
  }
}

const handleCodePaste = (e, i) => {
  e.preventDefault()
  const pasted = e.clipboardData.getData('text').replace(/[^a-zA-Z0-9]/g, '').toUpperCase().slice(0, 6)
  if (pasted) {
    for (let j = 0; j < 6; j++) {
      codeDigits.value[j] = pasted[j] || ''
    }
    inviteCode.value = codeDigits.value.join('')
    const lastIdx = Math.min(pasted.length, 5)
    nextTick(() => codeInputs.value[lastIdx]?.focus())
  }
}

const resetCodeInputs = () => {
  codeDigits.value = ['', '', '', '', '', '']
  inviteCode.value = ''
}

watch(showAddDialog, (val) => {
  if (val) resetCodeInputs()
})

const loadMyCourses = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/courses/my', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const data = await response.json()
    if (response.ok) {
      myCourses.value = data.courses || []
      updateStats()
    } else {
      ElMessage.error(data.error || '加载已加入课程失败')
    }
  } catch (error) {
    console.error('加载已加入课程失败:', error)
    ElMessage.error('加载已加入课程失败')
  } finally {
    loading.value = false
  }
}

const loadMicroCourses = async () => {
  try {
    const response = await fetch('/api/courses/available?type=micro', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const data = await response.json()
    if (response.ok) {
      microCourses.value = data.courses || []
      updateStats()
    } else {
      ElMessage.error(data.error || '加载微课程列表失败')
    }
  } catch (error) {
    console.error('加载微课程列表失败:', error)
    ElMessage.error('加载微课程列表失败')
  }
}

const joinByInviteCode = async () => {
  if (inviteCode.value.length !== 6) {
    ElMessage.warning('邀请码必须是6位')
    return
  }
  joining.value = true
  try {
    const response = await fetch('/api/courses/join', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ invite_code: inviteCode.value })
    })
    const data = await response.json()
    if (response.ok) {
      ElMessage.success(data.message || '加入课程成功')
      showAddDialog.value = false
      loadMyCourses()
    } else {
      ElMessage.error(data.error || '加入课程失败')
    }
  } catch (error) {
    console.error('加入课程失败:', error)
    ElMessage.error('加入课程失败')
  } finally {
    joining.value = false
  }
}

const joinByCourseId = async (courseId) => {
  joining.value = true
  try {
    const response = await fetch('/api/courses/join', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ course_id: courseId })
    })
    const data = await response.json()
    if (response.ok) {
      ElMessage.success(data.message || '加入课程成功')
      showAddDialog.value = false
      loadMyCourses()
      loadMicroCourses()
    } else {
      ElMessage.error(data.error || '加入课程失败')
    }
  } catch (error) {
    console.error('加入课程失败:', error)
    ElMessage.error('加入课程失败')
  } finally {
    joining.value = false
  }
}

const handleStar = async (courseId) => {
  try {
    const response = await fetch('/api/courses/star', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ course_id: courseId })
    })
    const data = await response.json()
    if (response.ok) {
      ElMessage.success(data.message)
      loadMyCourses()
    } else {
      ElMessage.error(data.error || '操作失败')
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

const handleLeave = async (courseId) => {
  try {
    await ElMessageBox.confirm('确定要退出该课程吗？退课后将无法查看课程内容。', '退课确认', {
      confirmButtonText: '确认退课',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    })
  } catch {
    return
  }

  try {
    const response = await fetch('/api/courses/leave', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ course_id: courseId })
    })
    const data = await response.json()
    if (response.ok) {
      ElMessage.success(data.message || '退课成功')
      loadMyCourses()
      loadMicroCourses()
    } else {
      ElMessage.error(data.error || '退课失败')
    }
  } catch (error) {
    console.error('退课失败:', error)
    ElMessage.error('退课失败')
  }
}

onMounted(() => {
  loadMyCourses()
  loadMicroCourses()
})
</script>

<style scoped>
/* ============ Page Container ============ */
.join-courses-page {
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
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-icon-wrap { position: relative; }

.page-icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: #fff;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
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
.stat-card--green .stat-icon { background: linear-gradient(135deg, #f5af19, #f12711); }
.stat-card--purple .stat-icon { background: linear-gradient(135deg, #43e97b, #38f9d7); }

.stat-content { display: flex; flex-direction: column; }

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

/* ============ Section Bar ============ */
.section-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.section-title-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
}

.section-title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #1a1a2e;
}

.section-count {
  padding: 2px 10px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.08));
  color: #667eea;
  font-size: 12px;
  font-weight: 600;
  border-radius: 20px;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  width: 280px;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: #8c8c9a;
  font-size: 16px;
  z-index: 1;
}

.search-input {
  width: 100%;
  height: 42px;
  padding: 0 36px 0 40px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  font-size: 13px;
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
  right: 10px;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  color: #8c8c9a;
  cursor: pointer;
}

.clear-btn:hover { background: rgba(0, 0, 0, 0.1); }

.add-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 22px;
  height: 42px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(102, 126, 234, 0.4);
}

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

.add-btn--center { margin-top: 8px; }

/* ============ Cards Grid ============ */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
}

.course-card {
  position: relative;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 22px;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
  animation: card-enter 0.5s cubic-bezier(0.4, 0, 0.2, 1) backwards;
}

.course-card--starred {
  border-color: rgba(245, 175, 25, 0.4);
  box-shadow: 0 8px 32px rgba(245, 175, 25, 0.12);
}

@keyframes card-enter {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.course-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.15);
}

.card-glow {
  position: absolute;
  top: -50%;
  right: -30%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.35s;
}

.course-card:hover .card-glow { opacity: 1; }

.card-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, transparent 100%);
  opacity: 0.7;
}

.star-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f5af19, #f12711);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(245, 175, 25, 0.4);
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
  padding-right: 36px;
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

.card-title-area { flex: 1; min-width: 0; }

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
  margin-bottom: 12px;
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

.info-text { display: flex; flex-direction: column; min-width: 0; }

.info-label { font-size: 11px; color: #8c8c9a; }

.info-value {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
  font-variant-numeric: tabular-nums;
}

.info-divider { color: #c0c0d0; margin: 0 2px; font-weight: 400; }
.info-max { color: #8c8c9a; font-weight: 400; font-size: 12px; }

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
  gap: 10px;
  padding-top: 14px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.action-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.6);
  color: #5a5a6a;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-btn:hover { transform: translateY(-1px); }

.action-btn--star:hover {
  border-color: rgba(245, 175, 25, 0.4);
  color: #f5af19;
  background: rgba(245, 175, 25, 0.05);
}

.action-btn--leave:hover {
  border-color: rgba(239, 68, 68, 0.4);
  color: #ef4444;
  background: rgba(239, 68, 68, 0.05);
}

/* ============ Skeleton ============ */
.skeleton-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  padding: 22px;
  height: 260px;
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

.orbit-dot--1 { top: 0; left: 50%; background: #667eea; animation: orbit-1 4s linear infinite; }
.orbit-dot--2 { bottom: 10px; left: 10px; background: #43e97b; animation: orbit-2 5s linear infinite; }
.orbit-dot--3 { bottom: 10px; right: 10px; background: #fa709a; animation: orbit-3 6s linear infinite; }

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
.add-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
}

.add-dialog :deep(.el-dialog__header) { margin: 0; padding: 0; }
.add-dialog :deep(.el-dialog__body) { padding: 0 28px 24px; }
.add-dialog :deep(.el-dialog__footer) { padding: 0; }

.dialog-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 22px 28px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.05));
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  position: relative;
  margin-bottom: 20px;
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

.dialog-title { margin: 0; font-size: 17px; font-weight: 600; color: #1a1a2e; }
.dialog-subtitle { margin: 2px 0 0; font-size: 12px; color: #8c8c9a; }

.dialog-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(0,0,0,0.04);
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

/* Custom Tabs */
.custom-tabs {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  background: rgba(0, 0, 0, 0.03);
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 24px;
}

.tab-item {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 12px;
  border: none;
  background: transparent;
  border-radius: 9px;
  color: #8c8c9a;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.25s;
}

.tab-item.active { color: #fff; }

.tab-indicator {
  position: absolute;
  z-index: 0;
  top: 4px;
  left: 4px;
  width: calc((100% - 8px) / 3);
  height: calc(100% - 8px);
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 9px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
}

/* Tab Content */
.tab-content { min-height: 280px; }

/* Invite Pane */
.invite-pane {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 0;
}

.invite-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.08));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  margin-bottom: 14px;
}

.pane-title { margin: 0 0 6px; font-size: 16px; font-weight: 600; color: #1a1a2e; }
.pane-desc { margin: 0 0 22px; font-size: 13px; color: #8c8c9a; }

.code-input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.code-input {
  width: 48px;
  height: 56px;
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  outline: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'SF Mono', 'Consolas', monospace;
}

.code-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.12);
  transform: translateY(-2px);
}

.submit-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 46px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s;
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

/* Scan Pane */
.scan-pane {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 0;
}

.qr-frame {
  position: relative;
  width: 200px;
  height: 200px;
  margin-bottom: 20px;
}

.qr-corner {
  position: absolute;
  width: 24px;
  height: 24px;
  border: 3px solid #667eea;
}

.qr-corner--tl { top: 0; left: 0; border-right: none; border-bottom: none; border-radius: 8px 0 0 0; }
.qr-corner--tr { top: 0; right: 0; border-left: none; border-bottom: none; border-radius: 0 8px 0 0; }
.qr-corner--bl { bottom: 0; left: 0; border-right: none; border-top: none; border-radius: 0 0 0 8px; }
.qr-corner--br { bottom: 0; right: 0; border-left: none; border-top: none; border-radius: 0 0 8px 0; }

.qr-inner {
  position: absolute;
  inset: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.04), rgba(118, 75, 162, 0.04));
  border-radius: 12px;
}

.qr-inner p { margin: 0; font-size: 12px; color: #8c8c9a; }

.scan-line {
  position: absolute;
  left: 20px;
  right: 20px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #667eea, transparent);
  box-shadow: 0 0 8px rgba(102, 126, 234, 0.5);
  animation: scan 2.5s ease-in-out infinite;
}

@keyframes scan {
  0%, 100% { top: 24px; }
  50% { top: calc(100% - 26px); }
}

.scan-tip { margin: 0; font-size: 13px; color: #8c8c9a; }

/* Micro Pane */
.micro-pane { padding: 4px 0; }

.micro-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 320px;
  overflow-y: auto;
  padding-right: 4px;
}

.micro-list::-webkit-scrollbar { width: 6px; }
.micro-list::-webkit-scrollbar-thumb { background: rgba(102, 126, 234, 0.2); border-radius: 3px; }

.micro-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 12px;
  transition: all 0.25s;
}

.micro-item:hover {
  background: rgba(102, 126, 234, 0.04);
  border-color: rgba(102, 126, 234, 0.2);
  transform: translateX(4px);
}

.micro-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #43e97b, #38f9d7);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.micro-info { flex: 1; min-width: 0; }

.micro-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
  display: block;
  margin-bottom: 2px;
}

.micro-desc {
  font-size: 12px;
  color: #8c8c9a;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.micro-join-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s;
  flex-shrink: 0;
}

.micro-join-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.micro-join-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.micro-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
  color: #8c8c9a;
}

.empty-circle-small {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  border: 2px dashed rgba(102, 126, 234, 0.3);
  margin-bottom: 12px;
}

.micro-empty p { margin: 0; font-size: 13px; }

/* ============ Responsive ============ */
@media (max-width: 768px) {
  .content-wrap { padding: 16px; }

  .page-header { flex-direction: column; align-items: flex-start; }

  .page-stats { width: 100%; }

  .stat-card { flex: 1; min-width: calc(33.33% - 8px); padding: 12px; }

  .section-bar { flex-direction: column; align-items: stretch; }

  .section-actions { flex-direction: column; }

  .search-box { width: 100%; }

  .cards-grid { grid-template-columns: 1fr; }

  .info-grid { grid-template-columns: 1fr; }

  .code-input { width: 42px; height: 50px; font-size: 18px; }
}
</style>
