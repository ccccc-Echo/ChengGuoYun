<template>
  <div class="students-page">
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
              <el-icon :size="22"><UserFilled /></el-icon>
            </div>
            <div class="icon-pulse"></div>
          </div>
          <div class="page-title-text">
            <h1 class="page-title">学生管理</h1>
            <p class="page-subtitle">管理学生档案 · 查看成果 · 班级分配</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><User /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedTotal }}</span>
              <span class="stat-label">学生总数</span>
            </div>
          </div>
          <div class="stat-card stat-card--green">
            <div class="stat-icon">
              <el-icon :size="18"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedAchievements }}</span>
              <span class="stat-label">成果总数</span>
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
                placeholder="学生姓名"
                clearable
                size="large"
                class="filter-input"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </div>
            <div class="filter-item">
              <el-input
                v-model="filterForm.student_no"
                placeholder="学号"
                clearable
                size="large"
                class="filter-input"
              >
                <template #prefix>
                  <el-icon><Document /></el-icon>
                </template>
              </el-input>
            </div>
            <div class="filter-item">
              <el-select
                v-model="filterForm.course_id"
                placeholder="选择课程"
                clearable
                size="large"
                class="filter-select"
              >
                <el-option v-for="course in courseOptions" :key="course.id" :label="course.name" :value="course.id" />
              </el-select>
            </div>
            <div class="filter-item">
              <el-input
                v-model="filterForm.major"
                placeholder="专业"
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
            <button
              v-if="$hasPermission('student:add')"
              class="btn-create-effect"
              @click="handleAdd"
            >
              <el-icon><Plus /></el-icon>
              <span>添加学生</span>
              <div class="btn-shine"></div>
            </button>
          </div>
        </div>
      </div>

      <!-- Table Card -->
      <div class="glass-card table-card">
        <div class="table-header">
          <div class="tabs-wrap" v-if="currentRole !== 'admin'">
            <button
              :class="['tab-btn', { active: activeTab === 'my_students' }]"
              @click="handleTabChange('my_students')"
            >
              <el-icon :size="16"><UserFilled /></el-icon>
              <span>本班学生</span>
              <span class="tab-count">{{ myStudentsCount }}</span>
            </button>
            <button
              :class="['tab-btn', { active: activeTab === 'other_students' }]"
              @click="handleTabChange('other_students')"
            >
              <el-icon :size="16"><User /></el-icon>
              <span>其他学生</span>
              <span class="tab-count">{{ otherStudentsCount }}</span>
            </button>
            <div class="tab-indicator" :style="tabIndicatorStyle"></div>
          </div>
          <div class="header-actions">
            <span class="result-summary">
              共 <b>{{ pagination.total }}</b> 条结果
            </span>
          </div>
        </div>

        <!-- Skeleton Loading -->
        <div v-if="loading && students.length === 0" class="skeleton-wrap">
          <div v-for="n in 5" :key="n" class="skeleton-row">
            <div class="skeleton-item" style="width: 40px"></div>
            <div class="skeleton-item skeleton-avatar" style="width: 36px; height: 36px"></div>
            <div class="skeleton-item" style="width: 100px"></div>
            <div class="skeleton-item" style="width: 120px"></div>
            <div class="skeleton-item" style="width: 80px"></div>
            <div class="skeleton-item" style="width: 140px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 70px"></div>
            <div class="skeleton-item" style="width: 80px"></div>
            <div class="skeleton-item" style="width: 200px"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="students.length === 0" class="empty-state">
          <div class="empty-illustration">
            <div class="empty-circle">
              <el-icon :size="48" color="#c0c0d0"><UserFilled /></el-icon>
            </div>
            <div class="empty-orbit"></div>
          </div>
          <h3 class="empty-title">{{ activeTab === 'my_students' ? '暂无本班学生' : '暂无学生数据' }}</h3>
          <p class="empty-desc">{{ activeTab === 'my_students' ? '点击添加学生，开始管理班级' : '使用筛选条件查找学生' }}</p>
          <button
            v-if="$hasPermission('student:add')"
            class="btn-create-effect btn-empty"
            @click="handleAdd"
          >
            <el-icon><Plus /></el-icon>
            <span>添加学生</span>
          </button>
        </div>

        <!-- Table -->
        <div v-else class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-name">学生信息</th>
                <th class="col-major">专业</th>
                <th class="col-phone">手机号</th>
                <th class="col-achievements">成果数</th>
                <th class="col-created">创建时间</th>
                <th class="col-action">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, idx) in students"
                :key="row.id"
                class="table-row"
                :style="{ animationDelay: idx * 30 + 'ms' }"
              >
                <td class="col-index">
                  <span class="index-num">{{ String(idx + 1).padStart(2, '0') }}</span>
                </td>
                <td class="col-name">
                  <div class="student-name-cell">
                    <div class="student-avatar" :style="{ background: getAvatarColor(row.name) }">
                      {{ (row.name || '?').charAt(0) }}
                    </div>
                    <div class="student-name-info">
                      <span class="student-name">{{ row.name }}</span>
                      <span class="student-sno">{{ row.student_no }}</span>
                    </div>
                  </div>
                </td>
                <td class="col-major">
                  <span class="major-text">{{ row.major || '-' }}</span>
                </td>
                <td class="col-phone">
                  <span class="phone-text">{{ row.phone || '-' }}</span>
                </td>
                <td class="col-achievements">
                  <span class="achievement-count" :class="{ 'has-achievement': row.achievement_count > 0 }">
                    {{ row.achievement_count || 0 }}
                  </span>
                </td>
                <td class="col-created">
                  <span class="time-text">{{ row.created_at || row.enrolled_at || '-' }}</span>
                </td>
                <td class="col-action">
                  <div class="action-group">
                    <button class="action-btn action-btn--primary" @click="handleEdit(row)">
                      <el-icon><View /></el-icon>
                      编辑
                    </button>
                    <button
                      v-if="$hasPermission('student:delete')"
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
        <div class="table-footer" v-if="students.length > 0">
          <span class="total-text">
            共 <b>{{ pagination.total }}</b> 个学生，每页 <b>{{ pagination.page_size }}</b> 条
          </span>
          <div class="pagination-wrap">
            <button
              class="page-btn"
              :disabled="pagination.page <= 1"
              @click="goPage(pagination.page - 1)"
            >
              <el-icon><ArrowLeft /></el-icon>
            </button>
            <button
              v-for="p in visiblePages"
              :key="p"
              :class="['page-btn', { active: p === '...' }]"
              :disabled="p === '...'"
              @click="p !== '...' && goPage(p)"
            >
              {{ p }}
            </button>
            <button
              class="page-btn"
              :disabled="pagination.page >= totalPages"
              @click="goPage(pagination.page + 1)"
            >
              <el-icon><ArrowRight /></el-icon>
            </button>
            <select v-model="pagination.page_size" class="page-size-select" @change="loadStudents">
              <option :value="10">10/页</option>
              <option :value="20">20/页</option>
              <option :value="50">50/页</option>
              <option :value="100">100/页</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Add/Edit Dialog -->
      <el-dialog
        v-model="showDialog"
        :title="isEditing ? '编辑学生' : '添加学生'"
        width="520px"
        class="custom-dialog"
        align-center
      >
        <template #header>
          <div class="dialog-header">
            <div class="dialog-header-icon" :class="isEditing ? 'edit-icon' : 'add-icon'">
              <el-icon :size="20"><component :is="isEditing ? View : Plus" /></el-icon>
            </div>
            <div>
              <div class="dialog-title">{{ isEditing ? '编辑学生信息' : '添加新学生' }}</div>
              <div class="dialog-subtitle">{{ isEditing ? '修改学生的基本信息' : '填写学生的基本信息以加入系统' }}</div>
            </div>
          </div>
        </template>
        <el-form ref="addFormRef" :model="addForm" :rules="addRules" label-width="80px" class="dialog-form">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="addForm.name" placeholder="请输入学生姓名" />
          </el-form-item>
          <el-form-item label="学号" prop="student_no">
            <el-input v-model="addForm.student_no" :disabled="isEditing" placeholder="请输入学号" />
          </el-form-item>
          <el-form-item label="院系" prop="department">
            <el-input v-model="addForm.department" placeholder="请输入院系" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="addForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          <div v-if="isEditing && $hasPermission('student:reset_pwd')" class="reset-password-section">
            <el-divider />
            <div class="reset-password-row">
              <div class="reset-password-info">
                <el-icon><SwitchButton /></el-icon>
                <span>重置密码</span>
              </div>
              <el-button type="warning" @click="handleResetPassword">
                <el-icon><Refresh /></el-icon>
                重置为 123456
              </el-button>
            </div>
          </div>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="closeDialog">取消</el-button>
            <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
          </div>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, UserFilled, Search, Refresh, User,
  OfficeBuilding, Delete, View, Document,
  ArrowLeft, ArrowRight, SwitchButton
} from '@element-plus/icons-vue'
import { studentsApi, coursesApi } from '@/api'
import { getUserInfo } from '@/utils/auth'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const saving = ref(false)
const students = ref([])
const courseOptions = ref([])
const showDialog = ref(false)
const addFormRef = ref(null)
const userInfo = ref(getUserInfo() || {})
const isEditing = ref(false)
const editId = ref(null)
const activeTab = ref(route.query.tab || 'my_students')

const currentRole = computed(() => {
  if (userInfo.value.role === 'teacher' && userInfo.value.teacher_role) {
    return userInfo.value.teacher_role
  }
  return userInfo.value.role
})

const canAddStudent = computed(() => {
  return ['admin', 'head', 'advisor'].includes(currentRole.value)
})

const filterForm = ref({
  name: '',
  student_no: '',
  course_id: '',
  major: ''
})

const pagination = ref({
  page: 1,
  page_size: 20,
  total: 0
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

const myStudentsCount = computed(() => {
  if (activeTab.value === 'my_students') return pagination.value.total
  return 0
})

const otherStudentsCount = computed(() => {
  if (activeTab.value === 'other_students') return pagination.value.total
  return 0
})

const tabIndicatorStyle = computed(() => {
  const index = activeTab.value === 'my_students' ? 0 : 1
  const width = currentRole.value === 'admin' ? 0 : 50
  const gap = 4
  const left = index * (width + gap)
  return {
    transform: `translateX(${left}px)`,
    width: `${width}px`
  }
})

const addForm = ref({
  name: '',
  student_no: '',
  department: '',
  phone: ''
})

const addRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  student_no: [
    { required: true, message: '请输入学号', trigger: 'blur' }
  ],
  department: [
    { required: true, message: '请输入院系', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1\d{10}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

// Animated counters
const animatedTotal = ref(0)
const animatedAchievements = ref(0)
const animateValue = (target, ref) => {
  const duration = 600
  const start = ref.value
  const startTime = performance.now()
  const animate = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easeProgress = 1 - Math.pow(1 - progress, 3)
    const value = Math.round(start + (target - start) * easeProgress)
    ref.value = value
    if (progress < 1) requestAnimationFrame(animate)
  }
  requestAnimationFrame(animate)
}

const totalAchievements = computed(() => {
  return students.value.reduce((sum, s) => sum + (s.achievement_count || 0), 0)
})

watch(() => pagination.value.total, (val) => {
  animateValue(val, animatedTotal)
})

watch(totalAchievements, (val) => {
  animateValue(val, animatedAchievements)
})

const avatarColors = [
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #f093fb, #f5576c)',
  'linear-gradient(135deg, #4facfe, #43e97b)',
  'linear-gradient(135deg, #fa709a, #fee140)',
  'linear-gradient(135deg, #a8edea, #fed6e3)',
  'linear-gradient(135deg, #ff9a9e, #fecfef)',
  'linear-gradient(135deg, #a1c4fd, #c2e9fb)'
]

const getAvatarColor = (name) => {
  if (!name) return avatarColors[0]
  const charCode = name.charCodeAt(0) || 0
  return avatarColors[charCode % avatarColors.length]
}

const loadStudents = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      ...filterForm.value
    }

    if (currentRole.value !== 'admin') {
      params.tab = activeTab.value
    }

    if (route.query.course_id) {
      params.course_id = route.query.course_id
    }

    const res = await studentsApi.list(params)
    students.value = res.students || []
    pagination.value.total = res.pagination?.total || 0
  } catch (error) {
    console.error('加载学生列表失败:', error)
    ElMessage.error('加载学生列表失败')
  } finally {
    loading.value = false
  }
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  router.push({ query: { ...route.query, tab } })
  pagination.value.page = 1
  loadStudents()
}

const loadCourses = async () => {
  try {
    const res = await coursesApi.list({ page_size: 1000 })
    courseOptions.value = res.courses || []
  } catch (error) {
    console.error('加载课程列表失败:', error)
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  loadStudents()
}

const resetFilter = () => {
  filterForm.value = {
    name: '',
    student_no: '',
    course_id: '',
    major: ''
  }
  pagination.value.page = 1
  loadStudents()
}

const goPage = (page) => {
  pagination.value.page = page
  loadStudents()
}

const handleAdd = () => {
  isEditing.value = false
  editId.value = null
  addForm.value = { name: '', student_no: '', department: '', phone: '' }
  showDialog.value = true
}

const handleEdit = (row) => {
  isEditing.value = true
  editId.value = row.id
  addForm.value = {
    name: row.name,
    student_no: row.student_no,
    department: row.department || '',
    phone: row.phone || ''
  }
  showDialog.value = true
}

const closeDialog = () => {
  showDialog.value = false
  addForm.value = { name: '', student_no: '', department: '', phone: '' }
  isEditing.value = false
  editId.value = null
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确认要删除学生「${row.name}」吗？<br/><span style="color:#8c8c9a;font-size:12px;">删除后，该学生将从本班级中移除。</span>`,
    '确认删除',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      await studentsApi.delete(row.id)
      ElMessage.success('学生已删除')
      loadStudents()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error(error.response?.data?.error || '删除失败')
    }
  })
}

const handleSave = async () => {
  if (!addFormRef.value) return

  try {
    await addFormRef.value.validate()
    saving.value = true

    if (isEditing.value) {
      await studentsApi.update(editId.value, addForm.value)
      ElMessage.success('学生信息修改成功')
    } else {
      await studentsApi.create(addForm.value)
      ElMessage.success('学生添加成功')
    }

    closeDialog()
    loadStudents()
  } catch (error) {
    if (error !== false) {
      console.error('保存失败:', error)
      ElMessage.error(error.response?.data?.error || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

const handleResetPassword = () => {
  ElMessageBox.confirm('确认将学生密码重置为 123456 吗？', '重置密码', {
    confirmButtonText: '确定重置',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await studentsApi.resetPassword(editId.value, { password: '123456' })
      ElMessage.success('密码重置成功')
    } catch (error) {
      console.error('重置密码失败:', error)
      ElMessage.error(error.response?.data?.error || '重置密码失败')
    }
  })
}

onMounted(() => {
  loadStudents()
  if (canAddStudent.value) {
    loadCourses()
  }

  if (route.query.course_id) {
    filterForm.value.course_id = route.query.course_id
  }
})
</script>

<style scoped>
/* ============ Page Container ============ */
.students-page {
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
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  top: -100px;
  right: -100px;
  animation: float 20s ease-in-out infinite;
}

.blob-2 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #667eea, #764ba2);
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
    linear-gradient(rgba(79, 172, 254, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(79, 172, 254, 0.03) 1px, transparent 1px);
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
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 16px;
  color: #fff;
  box-shadow: 0 8px 24px rgba(79, 172, 254, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  position: relative;
}

.page-icon::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 18px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
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

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.6; }
}

.page-title {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  background: linear-gradient(135deg, #1a1a2e 0%, #4facfe 50%, #00f2fe 100%);
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
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(79, 172, 254, 0.12);
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
  background: linear-gradient(135deg, #4facfe, #00f2fe);
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
  background: linear-gradient(135deg, #1a1a2e 0%, #4facfe 100%);
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
  box-shadow: 0 12px 40px rgba(79, 172, 254, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
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
  background: linear-gradient(90deg, transparent 0%, #4facfe 50%, transparent 100%);
  opacity: 0.6;
}

.filter-glow {
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(79, 172, 254, 0.12) 0%, transparent 70%);
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

.filter-select {
  width: 200px;
}

.filter-input :deep(.el-input__wrapper),
.filter-select :deep(.el-select__wrapper) {
  border-radius: 12px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.06) inset;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.6);
}

.filter-input :deep(.el-input__wrapper:hover),
.filter-select :deep(.el-select__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(79, 172, 254, 0.4) inset;
  background: rgba(255, 255, 255, 0.8);
}

.filter-input :deep(.el-input__wrapper.is-focus),
.filter-select :deep(.el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 2px rgba(79, 172, 254, 0.5) inset, 0 4px 12px rgba(79, 172, 254, 0.1);
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
  background: #4facfe;
  opacity: 0.1;
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.btn-ghost-effect:hover::after {
  width: 60px;
  height: 60px;
}

.btn-ghost-effect:hover {
  border-color: #4facfe;
  color: #4facfe;
  background: rgba(79, 172, 254, 0.04);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(79, 172, 254, 0.18);
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
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(79, 172, 254, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.btn-create-effect::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 14px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
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
  box-shadow: 0 8px 28px rgba(79, 172, 254, 0.5);
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
  background: linear-gradient(90deg, transparent 0%, #4facfe 50%, transparent 100%);
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
  z-index: 1;
}

.tab-btn:hover {
  color: #4facfe;
  background: rgba(79, 172, 254, 0.05);
}

.tab-btn.active {
  color: #4facfe;
  background: rgba(79, 172, 254, 0.08);
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: 10px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
}

.tab-indicator {
  position: absolute;
  bottom: -20px;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #4facfe, #00f2fe);
  border-radius: 3px;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
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
  color: #4facfe;
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
  background: linear-gradient(135deg, rgba(79, 172, 254, 0.08), rgba(0, 242, 254, 0.08));
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
  border: 2px dashed rgba(79, 172, 254, 0.15);
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
.data-table thead th.col-achievements,
.data-table thead th.col-created,
.data-table tbody td.col-index,
.data-table tbody td.col-achievements,
.data-table tbody td.col-created {
  text-align: center;
}

/* Left: name, info columns */
.data-table thead th.col-name,
.data-table thead th.col-class,
.data-table thead th.col-major,
.data-table thead th.col-phone,
.data-table tbody td.col-name,
.data-table tbody td.col-class,
.data-table tbody td.col-major,
.data-table tbody td.col-phone {
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

.student-name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.student-avatar {
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

.student-name-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.student-name {
  font-weight: 600;
  color: #1a1a2e;
}

.student-sno {
  font-size: 12px;
  color: #8c8c9a;
  font-family: 'SF Mono', 'Monaco', monospace;
}

.class-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: linear-gradient(135deg, rgba(79, 172, 254, 0.08), rgba(0, 242, 254, 0.08));
  border-radius: 8px;
  font-size: 12px;
  color: #4facfe;
  font-weight: 500;
}

.major-text {
  color: #5a5a6a;
}

.phone-text {
  font-family: 'SF Mono', 'Monaco', monospace;
  color: #5a5a6a;
  font-size: 13px;
}

.achievement-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 24px;
  padding: 0 8px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.04);
  font-size: 12px;
  font-weight: 600;
  color: #8c8c9a;
}

.achievement-count.has-achievement {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
  color: #fff;
}

.time-text {
  font-size: 13px;
  color: #8c8c9a;
}

/* ============ Action Buttons ============ */
.action-group {
  display: flex;
  gap: 4px;
  flex-wrap: nowrap;
  justify-content: flex-start;
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
  color: #4facfe;
}

.action-btn--primary:hover {
  background: rgba(79, 172, 254, 0.08);
  transform: translateY(-1px);
}

.action-btn--danger {
  color: #ef4444;
}

.action-btn--danger:hover {
  background: rgba(239, 68, 68, 0.08);
  transform: translateY(-1px);
}

.action-btn--accent {
  color: #43e97b;
}

.action-btn--accent:hover {
  background: rgba(67, 233, 123, 0.08);
  transform: translateY(-1px);
}

/* ============ Table Footer ============ */
.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 28px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.total-text {
  font-size: 13px;
  color: #8c8c9a;
}

.total-text b {
  color: #4facfe;
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
  border-color: #4facfe;
  color: #4facfe;
  background: rgba(79, 172, 254, 0.04);
}

.page-btn.active {
  border-color: transparent;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: #fff;
  box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
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
  border-color: #4facfe;
}

/* ============ Dialog ============ */
.custom-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.12);
}

.custom-dialog :deep(.el-dialog__header) {
  padding: 24px 28px 16px;
  margin-right: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.custom-dialog :deep(.el-dialog__body) {
  padding: 24px 28px;
}

.custom-dialog :deep(.el-dialog__footer) {
  padding: 16px 28px 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: 14px;
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
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.dialog-header-icon.edit-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
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
  box-shadow: 0 0 0 1px rgba(79, 172, 254, 0.3) inset;
}

.dialog-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(79, 172, 254, 0.4) inset;
  background: #fff;
}

.reset-password-section {
  margin-top: 8px;
}

.reset-password-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
}

.reset-password-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #5a5a6a;
  font-weight: 500;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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
  .filter-input,
  .filter-select {
    width: 100%;
  }
}
</style>
