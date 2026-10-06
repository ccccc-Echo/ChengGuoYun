<template>
  <div class="teacher-page">
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
            <h1 class="page-title">教师管理</h1>
            <p class="page-subtitle">管理教师账号 · 审核注册 · 分配角色</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><User /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedTotal }}</span>
              <span class="stat-label">教师总数</span>
            </div>
          </div>
          <div class="stat-card stat-card--orange">
            <div class="stat-icon">
              <el-icon :size="18"><View /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedPending }}</span>
              <span class="stat-label">待审核</span>
            </div>
          </div>
          <div class="stat-card stat-card--green">
            <div class="stat-icon">
              <el-icon :size="18"><SwitchButton /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedApproved }}</span>
              <span class="stat-label">已通过</span>
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
                placeholder="教师姓名"
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
                v-model="filterForm.teacher_no"
                placeholder="工号"
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
              <el-input
                v-model="filterForm.department"
                placeholder="院系"
                clearable
                size="large"
                class="filter-input"
              >
                <template #prefix>
                  <el-icon><OfficeBuilding /></el-icon>
                </template>
              </el-input>
            </div>
            <div class="filter-item">
              <el-select
                v-model="filterForm.role"
                placeholder="角色"
                clearable
                size="large"
                class="filter-select"
              >
                <el-option v-for="role in roleOptions" :key="role.id" :label="role.name" :value="role.name" />
              </el-select>
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
              v-if="$hasPermission('teacher:add')"
              class="btn-create-effect"
              @click="handleAdd"
            >
              <el-icon><Plus /></el-icon>
              <span>添加教师</span>
              <div class="btn-shine"></div>
            </button>
          </div>
        </div>
      </div>

      <!-- Table Card -->
      <div class="glass-card table-card">
        <div class="table-header">
          <div class="tabs-wrap">
            <button
              :class="['tab-btn', { active: activeTab === 'pending' }]"
              @click="handleTabChange('pending')"
            >
              <el-icon :size="16"><View /></el-icon>
              <span>待审核</span>
              <span class="tab-count">{{ pendingCount }}</span>
            </button>
            <button
              :class="['tab-btn', { active: activeTab === 'approved' }]"
              @click="handleTabChange('approved')"
            >
              <el-icon :size="16"><SwitchButton /></el-icon>
              <span>已通过</span>
              <span class="tab-count">{{ approvedCount }}</span>
            </button>
          </div>
          <div class="header-actions">
            <span class="result-summary">
              共 <b>{{ pagination.total }}</b> 条结果
            </span>
          </div>
        </div>

        <!-- Skeleton Loading -->
        <div v-if="loading && teachers.length === 0" class="skeleton-wrap">
          <div v-for="n in 5" :key="n" class="skeleton-row">
            <div class="skeleton-item" style="width: 40px"></div>
            <div class="skeleton-item skeleton-avatar" style="width: 36px; height: 36px"></div>
            <div class="skeleton-item" style="width: 100px"></div>
            <div class="skeleton-item" style="width: 80px"></div>
            <div class="skeleton-item" style="width: 120px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 70px"></div>
            <div class="skeleton-item" style="width: 110px"></div>
            <div class="skeleton-item" style="width: 130px"></div>
            <div class="skeleton-item" style="width: 200px"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="teachers.length === 0" class="empty-state">
          <div class="empty-illustration">
            <div class="empty-circle">
              <el-icon :size="48" color="#c0c0d0"><UserFilled /></el-icon>
            </div>
            <div class="empty-orbit"></div>
          </div>
          <h3 class="empty-title">{{ activeTab === 'pending' ? '暂无待审核教师' : '暂无教师数据' }}</h3>
          <p class="empty-desc">{{ activeTab === 'pending' ? '等待新教师注册后进行审核' : '点击添加教师开始管理' }}</p>
          <button
            v-if="$hasPermission('teacher:add')"
            class="btn-create-effect btn-empty"
            @click="handleAdd"
          >
            <el-icon><Plus /></el-icon>
            <span>添加教师</span>
          </button>
        </div>

        <!-- Table -->
        <div v-else class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-name">教师信息</th>
                <th class="col-teacher-no">工号</th>
                <th class="col-department">院系</th>
                <th class="col-role">角色</th>
                <th class="col-phone">手机号</th>
                <th class="col-status">状态</th>
                <th class="col-time">创建时间</th>
                <th class="col-action">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, idx) in teachers"
                :key="row.id"
                class="table-row"
                :style="{ '--accent-color': getRoleColor(row.role), animationDelay: idx * 30 + 'ms' }"
              >
                <td class="col-index">
                  <span class="index-num">{{ String(idx + 1).padStart(2, '0') }}</span>
                </td>
                <td class="col-name">
                  <div class="teacher-cell">
                    <div class="teacher-avatar" :style="{ background: getRoleColor(row.role) }">
                      {{ (row.name || '?').charAt(0) }}
                    </div>
                    <span class="teacher-name">{{ row.name }}</span>
                  </div>
                </td>
                <td class="col-teacher-no">
                  <span class="code-text">{{ row.teacher_no }}</span>
                </td>
                <td class="col-department">
                  <span class="dept-text">{{ row.department || '-' }}</span>
                </td>
                <td class="col-role">
                  <span class="role-badge" :style="{ background: getRoleColor(row.role) }">
                    {{ row.role }}
                  </span>
                </td>
                <td class="col-phone">
                  <span class="phone-text">{{ row.phone || '-' }}</span>
                </td>
                <td class="col-status">
                  <span class="status-badge" :class="'status-' + row.status">
                    <span class="status-dot"></span>
                    {{ row.status === 'approved' ? '已通过' : '待审核' }}
                  </span>
                </td>
                <td class="col-time">
                  <span class="time-text">{{ row.created_at || '-' }}</span>
                </td>
                <td class="col-action">
                  <div class="action-group">
                    <button
                      class="action-btn action-btn--info"
                      @click="handleViewDetail(row)"
                    >
                      <el-icon><InfoFilled /></el-icon>
                      详情
                    </button>
                    <button
                      v-if="$hasPermission('teacher:edit') && row.status === 'approved'"
                      class="action-btn action-btn--primary"
                      @click="handleEdit(row)"
                    >
                      <el-icon><View /></el-icon>
                      编辑
                    </button>
                    <button
                      v-if="$hasPermission('teacher:audit') && row.status === 'pending'"
                      class="action-btn action-btn--accent"
                      @click="handleApprove(row)"
                    >
                      <el-icon><SwitchButton /></el-icon>
                      通过
                    </button>
                    <button
                      v-if="$hasPermission('teacher:delete')"
                      class="action-btn action-btn--warn"
                      @click="handleUnlock(row)"
                    >
                      <el-icon><Open /></el-icon>
                      解锁
                    </button>
                    <button
                      v-if="$hasPermission('teacher:delete')"
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
        <div class="table-footer" v-if="teachers.length > 0">
          <span class="total-text">
            共 <b>{{ pagination.total }}</b> 个教师，每页 <b>{{ pagination.page_size }}</b> 条
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
            <select v-model="pagination.page_size" class="page-size-select" @change="loadTeachers">
              <option :value="10">10 条/页</option>
              <option :value="20">20 条/页</option>
              <option :value="50">50 条/页</option>
              <option :value="100">100 条/页</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Add/Edit Dialog -->
      <el-dialog v-model="showAddDialog" width="540px" class="custom-dialog" align-center>
        <template #header>
          <div class="dialog-header">
            <div class="dialog-header-icon" :class="isEditing ? 'edit-icon' : 'add-icon'">
              <el-icon :size="20"><component :is="isEditing ? View : Plus" /></el-icon>
            </div>
            <div>
              <div class="dialog-title">{{ isEditing ? '编辑教师' : '添加教师' }}</div>
              <div class="dialog-subtitle">{{ isEditing ? '修改教师信息和角色配置' : '填写教师基本信息以创建账号' }}</div>
            </div>
          </div>
        </template>
        <el-form ref="addFormRef" :model="addForm" :rules="addRules" label-width="100px" class="dialog-form">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="addForm.name" placeholder="请输入姓名" size="large" />
          </el-form-item>
          <el-form-item label="工号" prop="teacher_no">
            <el-input v-model="addForm.teacher_no" :disabled="isEditing" placeholder="请输入工号" size="large" />
          </el-form-item>
          <el-form-item v-if="!isEditing" label="密码" prop="password">
            <el-input v-model="addForm.password" type="password" placeholder="请输入密码（至少6位）" size="large" show-password />
          </el-form-item>
          <el-form-item label="院系" prop="department">
            <el-input v-model="addForm.department" placeholder="请输入院系" size="large" />
          </el-form-item>
          <el-form-item label="职称">
            <el-input v-model="addForm.title" placeholder="请输入职称" size="large" />
          </el-form-item>
          <el-form-item label="角色" prop="role">
            <el-select v-model="addForm.role" placeholder="请选择角色" size="large" style="width: 100%;">
              <el-option v-for="role in roleOptions" :key="role.id" :label="role.name" :value="role.name" />
            </el-select>
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="addForm.phone" placeholder="请输入手机号" size="large" />
          </el-form-item>
        </el-form>
        <template #footer>
          <button class="btn-ghost-effect" @click="showAddDialog = false">取消</button>
          <button class="btn-create-effect" :disabled="saving" @click="handleSave">
            <span v-if="!saving">{{ isEditing ? '保存修改' : '确认添加' }}</span>
            <span v-else>保存中...</span>
          </button>
        </template>
      </el-dialog>

      <!-- Detail Dialog -->
      <el-dialog v-model="detailVisible" width="720px" class="custom-dialog detail-dialog" align-center>
        <template #header>
          <div class="dialog-header">
            <div class="dialog-header-icon detail-icon">
              <el-icon :size="20"><InfoFilled /></el-icon>
            </div>
            <div>
              <div class="dialog-title">教师详情</div>
              <div class="dialog-subtitle">{{ detail.name || '' }} · {{ detail.teacher_no || '' }}</div>
            </div>
          </div>
        </template>

        <div v-loading="detailLoading" class="detail-body">
          <!-- 基本信息 -->
          <div class="detail-section">
            <div class="section-title">
              <span class="section-bar"></span>
              基本信息
            </div>
            <div class="info-grid">
              <div class="info-cell">
                <span class="info-key">姓名</span>
                <span class="info-val">{{ detail.name || '-' }}</span>
              </div>
              <div class="info-cell">
                <span class="info-key">工号</span>
                <span class="info-val code">{{ detail.teacher_no || '-' }}</span>
              </div>
              <div class="info-cell">
                <span class="info-key">院系</span>
                <span class="info-val">{{ detail.department || '-' }}</span>
              </div>
              <div class="info-cell">
                <span class="info-key">职称</span>
                <span class="info-val">{{ detail.title || '-' }}</span>
              </div>
              <div class="info-cell">
                <span class="info-key">手机号</span>
                <span class="info-val">{{ detail.phone || '-' }}</span>
              </div>
              <div class="info-cell">
                <span class="info-key">邮箱</span>
                <span class="info-val">{{ detail.email || '-' }}</span>
              </div>
              <div class="info-cell">
                <span class="info-key">角色</span>
                <span class="info-val">
                  <span v-if="detail.role" class="role-badge" :style="{ background: getRoleColor(detail.role) }">
                    {{ detail.role }}
                  </span>
                  <span v-else>-</span>
                </span>
              </div>
              <div class="info-cell">
                <span class="info-key">状态</span>
                <span class="info-val">
                  <span v-if="detail.status" class="status-badge" :class="'status-' + detail.status">
                    <span class="status-dot"></span>
                    {{ detail.status === 'approved' ? '已通过' : '待审核' }}
                  </span>
                  <span v-else>-</span>
                </span>
              </div>
              <div class="info-cell">
                <span class="info-key">创建时间</span>
                <span class="info-val">{{ detail.created_at || '-' }}</span>
              </div>
            </div>
          </div>

          <!-- 加入的团队 -->
          <div class="detail-section">
            <div class="section-title">
              <span class="section-bar"></span>
              加入的团队
              <span class="section-count">{{ detail.teams?.length || 0 }}</span>
            </div>
            <div v-if="detail.teams && detail.teams.length > 0" class="mini-table-wrap">
              <table class="mini-table">
                <thead>
                  <tr>
                    <th>团队名称</th>
                    <th>类型</th>
                    <th>团队角色</th>
                    <th>加入时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="team in detail.teams" :key="team.id">
                    <td class="cell-strong">{{ team.name }}</td>
                    <td>{{ getTeamTypeLabel(team.type) }}</td>
                    <td>
                      <span class="member-tag" :class="team.member_role === 'leader' ? 'member-leader' : 'member-normal'">
                        {{ team.member_role === 'leader' ? '负责人' : '成员' }}
                      </span>
                    </td>
                    <td class="cell-time">{{ team.joined_at || team.created_at || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="empty-inline">该教师尚未加入任何团队</div>
          </div>

          <!-- 创建的课程 -->
          <div class="detail-section">
            <div class="section-title">
              <span class="section-bar"></span>
              创建的课程
              <span class="section-count">{{ detail.courses?.length || 0 }}</span>
            </div>
            <div v-if="detail.courses && detail.courses.length > 0" class="mini-table-wrap">
              <table class="mini-table">
                <thead>
                  <tr>
                    <th>课程名称</th>
                    <th>课程代码</th>
                    <th>学生人数</th>
                    <th>学期</th>
                    <th>创建时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="course in detail.courses" :key="course.id">
                    <td class="cell-strong">{{ course.name }}</td>
                    <td class="cell-code">{{ course.code }}</td>
                    <td>{{ course.student_count ?? 0 }}</td>
                    <td>{{ course.semester || '-' }}</td>
                    <td class="cell-time">{{ course.created_at || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="empty-inline">该教师尚未创建任何课程</div>
          </div>
        </div>

        <template #footer>
          <button class="btn-ghost-effect" @click="detailVisible = false">关闭</button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, UserFilled, Search, Refresh, User,
  OfficeBuilding, Delete, View, Document,
  ArrowLeft, ArrowRight, SwitchButton, InfoFilled, Open
} from '@element-plus/icons-vue'
import { teacherApi, permissionApi, authApi } from '@/api'
import { getUserInfo, setUserInfo } from '@/utils/auth'

const loading = ref(false)
const saving = ref(false)
const teachers = ref([])
const showAddDialog = ref(false)
const addFormRef = ref(null)
const isEditing = ref(false)
const editId = ref(null)
const activeTab = ref('pending')
const roleOptions = ref([])

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

// Role colors for avatar and accent bar
const roleColors = {
  '院系负责人': 'linear-gradient(135deg, #667eea, #764ba2)',
  '辅导员': 'linear-gradient(135deg, #fa709a, #fee140)',
  '教师': 'linear-gradient(135deg, #4facfe, #00f2fe)',
  '教务管理员': 'linear-gradient(135deg, #43e97b, #38f9d7)'
}

const getRoleColor = (role) => {
  return roleColors[role] || 'linear-gradient(135deg, #a8edea, #fed6e3)'
}

const filterForm = ref({
  name: '',
  teacher_no: '',
  department: '',
  role: ''
})

const pagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

const addForm = ref({
  name: '',
  teacher_no: '',
  password: '',
  department: '',
  title: '',
  role: '',
  phone: ''
})

// 教师详情
const detailVisible = ref(false)
const detailLoading = ref(false)
const detail = ref({})

const addRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  teacher_no: [
    { required: true, message: '请输入工号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不少于6位', trigger: 'blur' }
  ],
  department: [
    { required: true, message: '请输入院系', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

// Animated counters
const animatedTotal = ref(0)
const animatedPending = ref(0)
const animatedApproved = ref(0)

const pendingCount = computed(() => {
  if (activeTab.value === 'pending') return pagination.value.total
  return 0
})

const approvedCount = computed(() => {
  if (activeTab.value === 'approved') return pagination.value.total
  return 0
})

// 加载教师统计（总数/待审核/已通过），直接赋值驱动顶部三个统计卡（与团队管理页一致的做法）
const loadStatistics = async () => {
  try {
    const res = await teacherApi.statistics()
    const data = (res && res.total !== undefined) ? res : ((res && res.data) || {})
    animatedTotal.value = data.total || 0
    animatedPending.value = data.pending || 0
    animatedApproved.value = data.approved || 0
  } catch (error) {
    console.error('加载教师统计失败:', error)
    animatedTotal.value = pagination.value.total || 0
  }
}

const loadTeachers = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      status: activeTab.value,
      ...filterForm.value
    }

    const res = await teacherApi.list(params)
    teachers.value = res.teachers || []
    pagination.value.total = res.pagination?.total || 0
    loadStatistics()
  } catch (error) {
    console.error('加载教师列表失败:', error)
    ElMessage.error('加载教师列表失败')
  } finally {
    loading.value = false
  }
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  pagination.value.page = 1
  loadTeachers()
}

const handleSearch = () => {
  pagination.value.page = 1
  loadTeachers()
}

const resetFilter = () => {
  filterForm.value = {
    name: '',
    teacher_no: '',
    department: '',
    role: ''
  }
  pagination.value.page = 1
  loadTeachers()
}

const goPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  pagination.value.page = page
  loadTeachers()
}

const handleAdd = () => {
  isEditing.value = false
  editId.value = null
  addForm.value = { name: '', teacher_no: '', password: '', department: '', title: '', role: '', phone: '' }
  showAddDialog.value = true
}

const handleEdit = (row) => {
  isEditing.value = true
  editId.value = row.id
  addForm.value = {
    name: row.name,
    teacher_no: row.teacher_no,
    department: row.department,
    title: row.title || '',
    role: row.role,
    phone: row.phone || ''
  }
  showAddDialog.value = true
}

// 团队类型标签
const teamTypeMap = {
  department: '院系',
  subject_group: '科组',
  campus: '校区',
  grade: '年级',
  other: '其他'
}
const getTeamTypeLabel = (type) => teamTypeMap[type] || type || '-'

const handleViewDetail = async (row) => {
  detailVisible.value = true
  detailLoading.value = true
  detail.value = { name: row.name, teacher_no: row.teacher_no }
  try {
    const res = await teacherApi.get(row.id)
    detail.value = {
      ...(res.teacher || {}),
      teams: res.teams || [],
      courses: res.courses || []
    }
  } catch (error) {
    console.error('加载教师详情失败:', error)
    ElMessage.error('加载教师详情失败')
  } finally {
    detailLoading.value = false
  }
}

const handleApprove = (row) => {
  ElMessageBox.confirm(
    `确认通过「${row.name}」的注册申请吗？<br/><span style="color:#8c8c9a;font-size:12px;">通过后该教师将可正常登录系统。</span>`,
    '确认通过',
    {
      confirmButtonText: '确认通过',
      cancelButtonText: '取消',
      type: 'info',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      await teacherApi.approve(row.id)
      ElMessage.success('审核通过')
      loadTeachers()
    } catch (error) {
      console.error('审核失败:', error)
      ElMessage.error('审核失败')
    }
  })
}

const handleUnlock = (row) => {
  ElMessageBox.confirm(
    `确认解锁教师「${row.name}」的账号吗？<br/><span style="color:#8c8c9a;font-size:12px;">解锁后清除登录失败锁定，可正常登录。</span>`,
    '确认解锁',
    {
      confirmButtonText: '确认解锁',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      const res = await teacherApi.unlock(row.id)
      ElMessage.success(res?.data?.message || '账号已解锁')
      loadTeachers()
    } catch (error) {
      console.error('解锁失败:', error)
      ElMessage.error('解锁失败')
    }
  })
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确认删除教师「${row.name}」的账号吗？<br/><span style="color:#8c8c9a;font-size:12px;">此操作不可恢复。</span>`,
    '确认删除',
    {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      await teacherApi.delete(row.id)
      ElMessage.success('删除成功')
      loadTeachers()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  })
}

const handleSave = async () => {
  if (!addFormRef.value) return

  try {
    await addFormRef.value.validate()
    saving.value = true

    if (isEditing.value) {
      await teacherApi.update(editId.value, addForm.value)
      ElMessage.success('教师信息更新成功')

      const currentUser = getUserInfo()
      const editedTeacher = teachers.value.find(t => t.id === editId.value)
      if (editedTeacher && currentUser) {
        const currentUserId = Number(currentUser.id)
        const editedUserId = Number(editedTeacher.user_id)
        if (currentUserId === editedUserId) {
          await refreshUserInfo()
        }
      }
    } else {
      await teacherApi.create(addForm.value)
      ElMessage.success('教师添加成功')
    }

    showAddDialog.value = false
    addForm.value = { name: '', teacher_no: '', password: '', department: '', title: '', role: '', phone: '' }
    isEditing.value = false
    editId.value = null
    loadTeachers()
  } catch (error) {
    if (error !== false) {
      console.error('保存失败:', error)
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

const refreshUserInfo = async () => {
  try {
    const res = await authApi.getMe()
    if (res.user) {
      setUserInfo(res.user)
      window.dispatchEvent(new Event('userInfoUpdated'))
      ElMessage.success('身份信息已更新')
    }
  } catch (error) {
    console.error('刷新用户信息失败:', error)
  }
}

const loadRoles = async () => {
  try {
    const res = await permissionApi.getRoles()
    roleOptions.value = res.roles || []
  } catch (error) {
    console.error('加载角色列表失败:', error)
    roleOptions.value = []
  }
}

onMounted(() => {
  loadRoles()
  loadTeachers()
  loadStatistics()
})
</script>

<style scoped>
/* ============ Page Container ============ */
.teacher-page {
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

.stat-card--orange .stat-icon {
  background: linear-gradient(135deg, #fa709a, #fee140);
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
  min-width: 180px;
}

.filter-input,
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
  box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.4) inset;
  background: rgba(255, 255, 255, 0.8);
}

.filter-input :deep(.el-input__wrapper.is-focus),
.filter-select :deep(.el-select__wrapper.is-focused) {
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
/* Center: index, number, date, status columns */
.data-table thead th.col-index,
.data-table thead th.col-status,
.data-table thead th.col-time,
.data-table tbody td.col-index,
.data-table tbody td.col-status,
.data-table tbody td.col-time {
  text-align: center;
}

/* Left: name, info columns */
.data-table thead th.col-name,
.data-table thead th.col-teacher-no,
.data-table thead th.col-department,
.data-table thead th.col-title,
.data-table thead th.col-role,
.data-table thead th.col-phone,
.data-table tbody td.col-name,
.data-table tbody td.col-teacher-no,
.data-table tbody td.col-department,
.data-table tbody td.col-title,
.data-table tbody td.col-role,
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

.teacher-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.teacher-avatar {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.teacher-name {
  font-weight: 600;
  color: #1a1a2e;
  font-size: 14px;
}

.code-text {
  font-family: 'SF Mono', 'Monaco', monospace;
  font-size: 13px;
  color: #5a5a6a;
}

.dept-text {
  color: #5a5a6a;
}

.title-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  border-radius: 8px;
  font-size: 12px;
  color: #667eea;
  font-weight: 500;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 10px;
  font-size: 12px;
  color: #fff;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.phone-text {
  font-size: 13px;
  color: #8c8c9a;
  font-variant-numeric: tabular-nums;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 0 currentColor;
  animation: status-pulse 2s infinite;
}

@keyframes status-pulse {
  0% { box-shadow: 0 0 0 0 currentColor; }
  70% { box-shadow: 0 0 0 6px transparent; }
  100% { box-shadow: 0 0 0 0 transparent; }
}

.status-pending {
  background: linear-gradient(135deg, rgba(250, 173, 20, 0.12), rgba(250, 173, 20, 0.06));
  color: #e6a23c;
}

.status-approved {
  background: linear-gradient(135deg, rgba(67, 233, 123, 0.12), rgba(67, 233, 123, 0.06));
  color: #2ecc71;
}

.time-text {
  font-size: 13px;
  color: #8c8c9a;
  font-variant-numeric: tabular-nums;
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
  color: #667eea;
}

.action-btn--primary:hover {
  background: rgba(102, 126, 234, 0.08);
  transform: translateY(-1px);
}

.action-btn--accent {
  color: #e6a23c;
}

.action-btn--accent:hover {
  background: rgba(230, 162, 60, 0.08);
  transform: translateY(-1px);
}

.action-btn--danger {
  color: #ef4444;
}

.action-btn--danger:hover {
  background: rgba(239, 68, 68, 0.08);
  transform: translateY(-1px);
}

.action-btn--info {
  color: #4facfe;
}

.action-btn--info:hover {
  background: rgba(79, 172, 254, 0.1);
  transform: translateY(-1px);
}

/* ============ Detail Dialog ============ */
.detail-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.detail-body {
  padding: 4px 28px 8px;
  max-height: 60vh;
  overflow-y: auto;
}

.detail-section {
  padding: 18px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.detail-section:last-child {
  border-bottom: none;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 14px;
}

.section-bar {
  width: 4px;
  height: 16px;
  border-radius: 2px;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.section-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 20px;
  padding: 0 7px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.12));
  color: #667eea;
  font-size: 12px;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px 20px;
}

.info-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px 14px;
  background: linear-gradient(135deg, rgba(247, 248, 250, 0.9), rgba(243, 244, 248, 0.6));
  border: 1px solid rgba(0, 0, 0, 0.03);
  border-radius: 10px;
  transition: all 0.2s ease;
}

.info-cell:hover {
  border-color: rgba(102, 126, 234, 0.2);
  background: rgba(255, 255, 255, 0.9);
}

.info-key {
  font-size: 12px;
  color: #8c8c9a;
  font-weight: 500;
}

.info-val {
  font-size: 14px;
  color: #1a1a2e;
  font-weight: 500;
  display: flex;
  align-items: center;
  word-break: break-all;
}

.info-val.code {
  font-family: 'SF Mono', 'Monaco', monospace;
  font-size: 13px;
  color: #5a5a6a;
}

/* ============ Mini Table (in detail) ============ */
.mini-table-wrap {
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.6);
}

.mini-table {
  width: 100%;
  border-collapse: collapse;
}

.mini-table thead th {
  font-size: 12px;
  font-weight: 600;
  color: #8c8c9a;
  text-align: left;
  padding: 10px 14px;
  background: rgba(247, 248, 250, 0.9);
  white-space: nowrap;
  letter-spacing: 0.3px;
}

.mini-table tbody td {
  font-size: 13px;
  color: #2a2a3a;
  padding: 11px 14px;
  border-top: 1px solid rgba(0, 0, 0, 0.03);
  white-space: nowrap;
}

.mini-table tbody tr {
  transition: background 0.18s ease;
}

.mini-table tbody tr:hover {
  background: rgba(102, 126, 234, 0.04);
}

.cell-strong {
  font-weight: 600;
  color: #1a1a2e;
}

.cell-code {
  font-family: 'SF Mono', 'Monaco', monospace;
  font-size: 12px;
  color: #5a5a6a;
}

.cell-time {
  font-size: 12px;
  color: #8c8c9a;
  font-variant-numeric: tabular-nums;
}

.member-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.member-leader {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.12));
  color: #667eea;
}

.member-normal {
  background: rgba(140, 140, 154, 0.1);
  color: #8c8c9a;
}

.empty-inline {
  padding: 18px;
  text-align: center;
  font-size: 13px;
  color: #b0b0c0;
  background: rgba(247, 248, 250, 0.6);
  border: 1px dashed rgba(0, 0, 0, 0.08);
  border-radius: 12px;
}

/* ============ Detail Header Icon ============ */
.dialog-header-icon.detail-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
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
  .filter-input,
  .filter-select {
    width: 100%;
  }
}
</style>
