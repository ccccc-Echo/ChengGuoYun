<template>
  <div class="achievements-page">
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
              <el-icon :size="22"><Document /></el-icon>
            </div>
            <div class="icon-pulse"></div>
          </div>
          <div class="page-title-text">
            <h1 class="page-title">{{ isStudent ? '个人成果' : '成果管理' }}</h1>
            <p class="page-subtitle">{{ isStudent ? '我的成果档案 · 录入 · 查看审核状态' : '审核学生成果 · 管理成果档案' }}</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedTotal }}</span>
              <span class="stat-label">成果总数</span>
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
                v-model="filterForm.title"
                placeholder="成果标题"
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
                v-model="filterForm.main_category"
                placeholder="一级分类"
                clearable
                size="large"
                class="filter-select"
                @change="handleMainCategoryChange"
              >
                <el-option v-for="item in mainCategories" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </div>
            <div class="filter-item">
              <el-select
                v-model="filterForm.sub_category"
                placeholder="二级细分"
                clearable
                size="large"
                class="filter-select"
                :disabled="!filterForm.main_category"
              >
                <el-option v-for="item in subCategories" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </div>
            <div class="filter-item">
              <el-select
                v-model="filterForm.status"
                placeholder="审核状态"
                clearable
                size="large"
                class="filter-select"
              >
                <el-option label="待审核" value="pending" />
                <el-option label="已通过" value="approved" />
                <el-option label="已驳回" value="rejected" />
              </el-select>
            </div>
            <div class="filter-item">
              <el-input
                v-model="filterForm.student_name"
                placeholder="学号/姓名"
                clearable
                size="large"
                class="filter-input"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
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
              v-if="isStudent"
              class="btn-create-effect"
              @click="handleAddAchievement"
            >
              <el-icon><Plus /></el-icon>
              <span>录入成果</span>
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
              :class="['tab-btn', { active: activeTab === 'all' }]"
              @click="handleTabChange('all')"
            >
              <el-icon :size="16"><Document /></el-icon>
              <span>全部成果</span>
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
        <div v-if="loading && achievements.length === 0" class="skeleton-wrap">
          <div v-for="n in 5" :key="n" class="skeleton-row">
            <div class="skeleton-item" style="width: 40px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 60px"></div>
            <div class="skeleton-item" style="width: 180px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 70px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 70px"></div>
            <div class="skeleton-item" style="width: 90px"></div>
            <div class="skeleton-item" style="width: 110px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 60px"></div>
            <div class="skeleton-item" style="width: 100px"></div>
            <div class="skeleton-item" style="width: 200px"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="achievements.length === 0" class="empty-state">
          <div class="empty-illustration">
            <div class="empty-circle">
              <el-icon :size="48" color="#c0c0d0"><Document /></el-icon>
            </div>
            <div class="empty-orbit"></div>
          </div>
          <h3 class="empty-title">暂无成果数据</h3>
          <p class="empty-desc">{{ isStudent ? '点击录入成果，开始建立你的成果档案' : '使用筛选条件查找成果' }}</p>
          <button
            v-if="isStudent"
            class="btn-create-effect btn-empty"
            @click="handleAddAchievement"
          >
            <el-icon><Plus /></el-icon>
            <span>录入成果</span>
          </button>
        </div>

        <!-- Table -->
        <div v-else class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-title">成果标题</th>
                <th class="col-category">分类</th>
                <th class="col-level">级别</th>
                <th class="col-student">学生</th>
                <th class="col-auditor">审核人</th>
                <th class="col-status">状态</th>
                <th class="col-time">提交时间</th>
                <th class="col-action">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, idx) in achievements"
                :key="row.id"
                class="table-row"
                :style="{ '--accent-color': getStatusColor(row.status), animationDelay: idx * 30 + 'ms' }"
              >
                <td class="col-index">
                  <span class="index-num">{{ String(idx + 1).padStart(2, '0') }}</span>
                </td>
                <td class="col-title">
                  <div class="title-cell">
                    <span class="title-text">{{ row.title }}</span>
                    <span class="title-sub">{{ getSubCategoryLabel(row.sub_category) || getMainCategoryLabel(row.main_category) }}</span>
                  </div>
                </td>
                <td class="col-category">
                  <span class="category-tag">{{ getMainCategoryLabel(row.main_category) }}</span>
                </td>
                <td class="col-level">
                  <span class="level-tag" :class="'level-' + getLevelClass(row.level)">
                    {{ getLevelLabel(row.level) || '-' }}
                  </span>
                </td>
                <td class="col-student">
                  <div class="student-cell">
                    <span class="student-avatar" :style="{ background: getAvatarColor(row.student_name) }">
                      {{ (row.student_name || '?').charAt(0) }}
                    </span>
                    <span class="student-name">{{ row.student_name }}</span>
                  </div>
                </td>
                <td class="col-auditor">
                  <span class="auditor-text">{{ row.auditor_name || '-' }}</span>
                </td>
                <td class="col-status">
                  <span class="status-badge" :class="'status-' + row.status">
                    <span class="status-dot"></span>
                    {{ statusText[row.status] }}
                  </span>
                </td>
                <td class="col-time">
                  <span class="time-text">{{ row.submitted_at || '-' }}</span>
                </td>
                <td class="col-action">
                  <div class="action-group">
                    <button
                      v-if="isStudent || $hasPermission('achievement:view')"
                      class="action-btn action-btn--primary"
                      @click="handleView(row)"
                    >
                      <el-icon><View /></el-icon>
                      详情
                    </button>
                    <button
                      v-if="$hasPermission('achievement:audit') && row.status === 'pending'"
                      class="action-btn action-btn--accent"
                      @click="handleAudit(row)"
                    >
                      <el-icon><SwitchButton /></el-icon>
                      审核
                    </button>
                    <button
                      v-if="isStudent && row.status === 'pending'"
                      class="action-btn action-btn--primary"
                      @click="handleEdit(row)"
                    >
                      <el-icon><View /></el-icon>
                      编辑
                    </button>
                    <button
                      v-if="canDeleteOrReject(row)"
                      class="action-btn action-btn--danger"
                      @click="handleDeleteOrReject(row)"
                    >
                      <el-icon><Delete /></el-icon>
                      {{ getDeleteButtonText(row) }}
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Table Footer -->
          <div class="table-footer" v-if="achievements.length > 0">
            <span class="total-text">
              共 <b>{{ pagination.total }}</b> 条成果，每页 <b>{{ pagination.page_size }}</b> 条
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
              <select v-model="pagination.page_size" class="page-size-select" @change="loadAchievements">
                <option :value="10">10 条/页</option>
                <option :value="20">20 条/页</option>
                <option :value="50">50 条/页</option>
                <option :value="100">100 条/页</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Detail Dialog -->
      <el-dialog v-model="showDetailDialog" width="640px" class="custom-dialog" align-center>
        <template #header>
          <div class="dialog-header">
            <div class="dialog-header-icon detail-icon">
              <el-icon :size="20"><View /></el-icon>
            </div>
            <div>
              <div class="dialog-title">成果详情</div>
              <div class="dialog-subtitle">查看成果完整信息</div>
            </div>
          </div>
        </template>
        <div class="detail-content">
          <div class="detail-title-row">
            <h3 class="detail-title">{{ detailData.title }}</h3>
            <span class="status-badge" :class="'status-' + detailData.status">
              <span class="status-dot"></span>
              {{ statusText[detailData.status] }}
            </span>
          </div>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="di-label">一级分类</span>
              <span class="di-value">{{ getMainCategoryLabel(detailData.main_category) }}</span>
            </div>
            <div class="detail-item">
              <span class="di-label">二级细分</span>
              <span class="di-value">{{ getSubCategoryLabel(detailData.sub_category) || '-' }}</span>
            </div>
            <div class="detail-item">
              <span class="di-label">级别</span>
              <span class="di-value">{{ getLevelLabel(detailData.level) || '-' }}</span>
            </div>
            <div class="detail-item">
              <span class="di-label">学生姓名</span>
              <span class="di-value">{{ detailData.student_name }}</span>
            </div>
            <div class="detail-item">
              <span class="di-label">班级</span>
              <span class="di-value">{{ detailData.class_name || '-' }}</span>
            </div>
            <div class="detail-item">
              <span class="di-label">审核人</span>
              <span class="di-value">{{ detailData.auditor_name || '无' }}</span>
            </div>
            <div class="detail-item" v-if="detailData.status === 'approved' || detailData.status === 'rejected'">
              <span class="di-label">审核时间</span>
              <span class="di-value">{{ detailData.reviewed_at || '无' }}</span>
            </div>
            <div class="detail-item">
              <span class="di-label">提交时间</span>
              <span class="di-value">{{ detailData.submitted_at }}</span>
            </div>
          </div>
          <div class="detail-section">
            <div class="ds-label">成果描述</div>
            <div class="ds-content">{{ detailData.description || '暂无描述' }}</div>
          </div>
          <div class="detail-section">
            <div class="ds-label">证明材料</div>
            <div v-if="detailData.attachments && detailData.attachments.length > 0" class="proof-files">
              <div v-for="file in detailData.attachments" :key="file.id" class="proof-card">
                <template v-if="isImageFile(file)">
                  <el-image
                    :src="getFileUrl(file.file_path)"
                    :preview-src-list="previewImageList"
                    :initial-index="previewImageIndex(file)"
                    fit="contain"
                    class="proof-image"
                    preview-teleported
                    hide-on-click-modal
                  >
                    <template #error>
                      <div class="image-error">
                        <el-icon :size="28"><Picture /></el-icon>
                        <span>图片加载失败</span>
                        <el-button type="primary" link @click="downloadFile(file)">点击下载</el-button>
                      </div>
                    </template>
                  </el-image>
                </template>
                <template v-else>
                  <div class="file-icon-wrap">
                    <el-icon :size="36" class="file-icon"><Document /></el-icon>
                  </div>
                </template>
                <div class="proof-actions">
                  <span class="file-name" :title="file.file_name">{{ file.file_name }}</span>
                  <span class="file-size">{{ formatFileSize(file.file_size) }}</span>
                  <el-button type="primary" size="small" circle @click="downloadFile(file)">
                    <el-icon><Download /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>
            <div v-else class="ds-content no-proof">暂无证明材料</div>
          </div>
          <div class="detail-section" v-if="detailData.review_comment">
            <div class="ds-label">审核意见</div>
            <div class="ds-content">{{ detailData.review_comment }}</div>
          </div>
        </div>
        <template #footer>
          <button class="btn-create-effect" @click="showDetailDialog = false">关闭</button>
        </template>
      </el-dialog>

      <!-- Audit Dialog -->
      <el-dialog v-model="showAuditDialog" width="560px" class="custom-dialog" align-center>
        <template #header>
          <div class="dialog-header">
            <div class="dialog-header-icon audit-icon">
              <el-icon :size="20"><SwitchButton /></el-icon>
            </div>
            <div>
              <div class="dialog-title">审核成果</div>
              <div class="dialog-subtitle">审核并给出意见</div>
            </div>
          </div>
        </template>
        <el-form ref="auditFormRef" :model="auditForm" label-width="100px" class="dialog-form">
          <el-form-item v-if="isAdmin" label="审核人" required>
            <el-select v-model="auditForm.auditor_id" placeholder="请选择审核教师" filterable size="large" style="width: 100%;">
              <el-option
                v-for="teacher in teacherList"
                :key="teacher.id"
                :label="`${teacher.name}（${teacher.teacher_no}）`"
                :value="teacher.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="审核结果" required>
            <div class="audit-result-group">
              <label
                :class="['audit-result-opt', { approved: auditForm.result === 'approved' }]"
                @click="auditForm.result = 'approved'"
              >
                <input v-model="auditForm.result" type="radio" value="approved" />
                <el-icon :size="18"><SwitchButton /></el-icon>
                <span>通过</span>
              </label>
              <label
                :class="['audit-result-opt', { rejected: auditForm.result === 'rejected' }]"
                @click="auditForm.result = 'rejected'"
              >
                <input v-model="auditForm.result" type="radio" value="rejected" />
                <el-icon :size="18"><Delete /></el-icon>
                <span>驳回</span>
              </label>
            </div>
          </el-form-item>
          <el-form-item label="审核意见" v-if="auditForm.result">
            <el-input
              v-model="auditForm.comment"
              type="textarea"
              :rows="4"
              :placeholder="auditForm.result === 'rejected' ? '请输入驳回理由（必填）' : '请输入审核意见（可选）'"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <button class="btn-ghost-effect" @click="showAuditDialog = false">取消</button>
          <button class="btn-create-effect" :disabled="auditing" @click="handleAuditSubmit">
            <span v-if="!auditing">确认审核</span>
            <span v-else>审核中...</span>
          </button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Document, Search, Refresh, View,
  Delete, SwitchButton, ArrowLeft, ArrowRight, Picture, Download
} from '@element-plus/icons-vue'
import { achievementsApi } from '@/api'
import { getUserInfo } from '@/utils/auth'
import { getMainCategoryLabel, getSubCategoryLabel, getLevelLabel } from '@/utils/constants'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const auditing = ref(false)
const achievements = ref([])
const showDetailDialog = ref(false)
const showAuditDialog = ref(false)
const auditFormRef = ref(null)
const userInfo = ref(getUserInfo() || {})
const detailData = ref({})
const activeTab = ref('all')
const auditForm = ref({
  result: '',
  comment: '',
  auditor_id: null
})
const auditId = ref(null)
const teacherList = ref([])

const mainCategories = [
  { label: '学科竞赛类', value: '学科竞赛类' },
  { label: '学术论文类', value: '学术论文类' },
  { label: '知识产权类', value: '知识产权类' },
  { label: '科研项目类', value: '科研项目类' },
  { label: '荣誉表彰类', value: '荣誉表彰类' },
  { label: '技能证书类', value: '技能证书类' },
  { label: '社会实践类', value: '社会实践类' }
]

const categorySubCategories = {
  '学科竞赛类': [
    { label: 'ACM', value: 'ACM' },
    { label: '数学建模', value: '数学建模' },
    { label: '互联网+', value: '互联网+' },
    { label: '挑战杯', value: '挑战杯' },
    { label: '电子设计', value: '电子设计' },
    { label: '智能车', value: '智能车' },
    { label: '其他', value: '其他' }
  ],
  '学术论文类': [
    { label: 'SCI', value: 'SCI' },
    { label: 'EI', value: 'EI' },
    { label: '核心期刊', value: '核心期刊' },
    { label: '普通期刊', value: '普通期刊' },
    { label: '会议论文', value: '会议论文' }
  ],
  '知识产权类': [
    { label: '发明专利', value: '发明专利' },
    { label: '实用新型', value: '实用新型' },
    { label: '外观设计', value: '外观设计' },
    { label: '软件著作权', value: '软件著作权' }
  ],
  '科研项目类': [
    { label: '国家级大创', value: '国家级大创' },
    { label: '省级大创', value: '省级大创' },
    { label: '校级大创', value: '校级大创' },
    { label: '参与教师科研', value: '参与教师科研' }
  ],
  '荣誉表彰类': [
    { label: '国家奖学金', value: '国家奖学金' },
    { label: '励志奖学金', value: '励志奖学金' },
    { label: '三好学生', value: '三好学生' },
    { label: '优秀干部', value: '优秀干部' },
    { label: '优秀团员', value: '优秀团员' }
  ],
  '技能证书类': [
    { label: '英语四六级', value: '英语四六级' },
    { label: '计算机等级', value: '计算机等级' },
    { label: '教师资格证', value: '教师资格证' },
    { label: '普通话', value: '普通话' },
    { label: '职业资格证', value: '职业资格证' }
  ],
  '社会实践类': [
    { label: '志愿服务', value: '志愿服务' },
    { label: '社会实践', value: '社会实践' },
    { label: '社团活动', value: '社团活动' }
  ]
}

const subCategories = computed(() => {
  return categorySubCategories[filterForm.value.main_category] || []
})

const currentRole = computed(() => {
  if (userInfo.value.role === 'teacher' && userInfo.value.teacher_role) {
    return userInfo.value.teacher_role
  }
  return userInfo.value.role
})

const isStudent = computed(() => currentRole.value === 'student')

const isTeacher = computed(() => {
  return ['head', 'advisor', 'faculty', 'teaching_admin'].includes(currentRole.value)
})

const isAdmin = computed(() => currentRole.value === 'admin')

const canAudit = computed(() => {
  return ['admin', 'head', 'advisor', 'faculty', 'teaching_admin'].includes(currentRole.value)
})

const canDeleteOrReject = (row) => {
  if (isAdmin.value) return true
  if (isStudent.value) return true
  if (isTeacher.value) {
    return row.status === 'approved'
  }
  return false
}

const getDeleteButtonText = (row) => {
  if (isTeacher.value && row.status === 'approved') {
    return '驳回'
  }
  return '删除'
}

const statusText = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已驳回'
}

const statusType = {
  pending: 'warning',
  approved: 'success',
  rejected: 'danger'
}

const levelType = {
  '国家级': 'danger',
  '省级': 'warning',
  '校级': '',
  '院级': 'info'
}

// Status colors for table accent bar
const getStatusColor = (status) => {
  const colors = {
    pending: 'linear-gradient(135deg, #fa709a, #fee140)',
    approved: 'linear-gradient(135deg, #43e97b, #38f9d7)',
    rejected: 'linear-gradient(135deg, #f093fb, #f5576c)'
  }
  return colors[status] || colors.pending
}

const getLevelClass = (level) => {
  const map = { '国家级': 'national', '省级': 'province', '校级': 'school', '院级': 'college' }
  return map[level] || 'other'
}

const avatarColors = [
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #f093fb, #f5576c)',
  'linear-gradient(135deg, #4facfe, #00f2fe)',
  'linear-gradient(135deg, #43e97b, #38f9d7)',
  'linear-gradient(135deg, #fa709a, #fee140)'
]

const getAvatarColor = (name) => {
  if (!name) return avatarColors[0]
  const charCode = name.charCodeAt(0) || 0
  return avatarColors[charCode % avatarColors.length]
}

const filterForm = ref({
  title: '',
  main_category: '',
  sub_category: '',
  status: '',
  student_name: ''
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

// Animated counters
const animatedTotal = ref(0)
const animatedPending = ref(0)
const animatedApproved = ref(0)
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

// Statistics computed from current page data
const pendingCount = computed(() => {
  return achievements.value.filter(a => a.status === 'pending').length
})

const approvedCount = computed(() => {
  return achievements.value.filter(a => a.status === 'approved').length
})

watch(() => pagination.value.total, (val) => {
  animateValue(val, animatedTotal)
})

watch(pendingCount, (val) => {
  animateValue(val, animatedPending)
})

watch(approvedCount, (val) => {
  animateValue(val, animatedApproved)
})

const handleMainCategoryChange = () => {
  filterForm.value.sub_category = ''
}

const loadAchievements = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      ...filterForm.value
    }

    if (route.query.student_id) {
      params.student_id = route.query.student_id
    }
    if (route.query.course_id) {
      params.course_id = route.query.course_id
    }

    const res = await achievementsApi.list(params)
    achievements.value = res.achievements || []
    pagination.value.total = res.pagination?.total || 0
  } catch (error) {
    console.error('加载成果列表失败:', error)
    ElMessage.error('加载成果列表失败')
  } finally {
    loading.value = false
  }
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  pagination.value.page = 1
  loadAchievements()
}

const handleSearch = () => {
  pagination.value.page = 1
  loadAchievements()
}

const resetFilter = () => {
  filterForm.value = {
    title: '',
    main_category: '',
    sub_category: '',
    status: '',
    student_name: ''
  }
  pagination.value.page = 1
  loadAchievements()
}

const goPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  pagination.value.page = page
  loadAchievements()
}

const handleView = async (row) => {
  try {
    const res = await achievementsApi.get(row.id)
    detailData.value = res.achievement || row
  } catch (error) {
    console.error('获取成果详情失败:', error)
    detailData.value = row
  }
  showDetailDialog.value = true
}

const handleAudit = async (row) => {
  auditId.value = row.id
  auditForm.value = {
    result: '',
    comment: '',
    auditor_id: null
  }

  if (isAdmin.value) {
    try {
      const res = await achievementsApi.getTeachers()
      teacherList.value = res.teachers || []
    } catch (error) {
      console.error('加载教师列表失败:', error)
      ElMessage.error('加载教师列表失败')
    }
  }

  showAuditDialog.value = true
}

const handleAuditSubmit = async () => {
  if (!auditForm.value.result) {
    ElMessage.warning('请选择审核结果')
    return
  }

  if (isAdmin.value && !auditForm.value.auditor_id) {
    ElMessage.warning('请选择审核人')
    return
  }

  if (auditForm.value.result === 'rejected' && !auditForm.value.comment) {
    ElMessage.warning('驳回时请填写审核意见')
    return
  }

  try {
    auditing.value = true
    const auditData = {
      status: auditForm.value.result,
      review_comment: auditForm.value.comment
    }
    if (isAdmin.value) {
      auditData.auditor_id = auditForm.value.auditor_id
    }
    await achievementsApi.audit(auditId.value, auditData)
    ElMessage.success('审核成功')
    showAuditDialog.value = false
    loadAchievements()
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  } finally {
    auditing.value = false
  }
}

const handleAddAchievement = () => {
  router.push('/dashboard/achievements/add')
}

const handleEdit = (row) => {
  router.push({
    path: '/dashboard/achievements/add',
    query: { id: row.id }
  })
}

const handleDeleteOrReject = (row) => {
  if (isTeacher.value && row.status === 'approved') {
    ElMessageBox.confirm(
      '确认驳回此成果吗？<br/><span style="color:#8c8c9a;font-size:12px;">驳回后，该成果状态将变更为"已驳回"，学生可重新修改后再次提交。</span>',
      '确认驳回',
      {
        confirmButtonText: '确认驳回',
        cancelButtonText: '取消',
        type: 'warning',
        dangerouslyUseHTMLString: true
      }
    ).then(async () => {
      try {
        await achievementsApi.audit(row.id, {
          status: 'rejected',
          review_comment: '教师驳回已通过成果'
        })
        ElMessage.success('驳回成功')
        loadAchievements()
      } catch (error) {
        console.error('驳回失败:', error)
        ElMessage.error('驳回失败')
      }
    })
    return
  }

  ElMessageBox.confirm(
    `确认删除成果「${row.title}」吗？<br/><span style="color:#8c8c9a;font-size:12px;">此操作不可恢复${isStudent.value && row.status === 'approved' ? '，已审核通过的成果删除后无法恢复' : ''}。</span>`,
    '确认删除',
    {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      await achievementsApi.delete(row.id)
      ElMessage.success('删除成功')
      loadAchievements()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  })
}

onMounted(() => {
  loadAchievements()
})

const getFileUrl = (filePath) => {
  if (!filePath) return '#'
  if (filePath.startsWith('http')) return filePath
  return `${import.meta.env.VITE_API_BASE_URL || ''}${filePath}`
}

const formatFileSize = (bytes) => {
  if (!bytes) return ''
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

const isImageFile = (file) => {
  if (!file) return false
  if (file.file_type && file.file_type.startsWith('image/')) return true
  const ext = file.file_name ? file.file_name.split('.').pop().toLowerCase() : ''
  return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'].includes(ext)
}

// 当前成果的所有图片 URL（用于 el-image 预览列表）
const previewImageList = computed(() => {
  const list = detailData.value.attachments || []
  return list.filter(isImageFile).map(f => getFileUrl(f.file_path))
})

// 点击某张图片时，预览从该图片开始
const previewImageIndex = (file) => {
  const url = getFileUrl(file.file_path)
  return Math.max(0, previewImageList.value.indexOf(url))
}

const getFileName = (filePath) => {
  if (!filePath) return '下载文件'
  const decoded = decodeURIComponent(filePath)
  return decoded.split('/').pop() || '下载文件'
}

const downloadFile = async (file) => {
  const url = getFileUrl(file.file_path)
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error('下载失败')
    const blob = await response.blob()
    const blobUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = file.file_name || getFileName(file.file_path)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(blobUrl)
    ElMessage.success('下载成功')
  } catch {
    const link = document.createElement('a')
    link.href = url
    link.download = file.file_name || getFileName(file.file_path)
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.info('浏览器即将开始下载...')
  }
}
</script>

<style scoped>
/* ============ Page Container ============ */
.achievements-page {
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
  background: linear-gradient(135deg, #fa709a, #fee140);
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
  padding: 20px 0;
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
/* Center: index, level, student, auditor, status, time columns */
.data-table thead th.col-index,
.data-table thead th.col-level,
.data-table thead th.col-student,
.data-table thead th.col-auditor,
.data-table thead th.col-status,
.data-table thead th.col-time,
.data-table tbody td.col-index,
.data-table tbody td.col-level,
.data-table tbody td.col-student,
.data-table tbody td.col-auditor,
.data-table tbody td.col-status,
.data-table tbody td.col-time {
  text-align: center;
}

/* Left: title, category, class columns */
.data-table thead th.col-title,
.data-table thead th.col-category,
.data-table thead th.col-class,
.data-table tbody td.col-title,
.data-table tbody td.col-category,
.data-table tbody td.col-class {
  text-align: left;
}

/* Left: action column */
.data-table thead th.col-action,
.data-table tbody td.col-action {
  text-align: left;
}

.data-table tbody td.col-action {
  overflow: visible;
  white-space: nowrap;
}

.index-num {
  font-size: 13px;
  font-weight: 600;
  color: #c0c0d0;
  font-variant-numeric: tabular-nums;
}

.title-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
  justify-content: center;
}

.title-text {
  font-weight: 600;
  color: #1a1a2e;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.title-sub {
  font-size: 12px;
  color: #8c8c9a;
  line-height: 1.3;
}

.category-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  border-radius: 8px;
  font-size: 12px;
  color: #667eea;
  font-weight: 500;
  white-space: nowrap;
  max-width: none;
  vertical-align: middle;
}

.level-tag {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  max-width: none;
  vertical-align: middle;
}

.level-national {
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.12), rgba(245, 108, 108, 0.06));
  color: #f56c6c;
}

.level-province {
  background: linear-gradient(135deg, rgba(250, 173, 20, 0.12), rgba(250, 173, 20, 0.06));
  color: #e6a23c;
}

.level-school {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(102, 126, 234, 0.06));
  color: #667eea;
}

.level-college {
  background: linear-gradient(135deg, rgba(144, 147, 153, 0.12), rgba(144, 147, 153, 0.06));
  color: #909399;
}

.level-other {
  background: rgba(0, 0, 0, 0.04);
  color: #8c8c9a;
}

.student-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}

.student-avatar {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.student-name {
  font-size: 14px;
  color: #2a2a3a;
  white-space: nowrap;
  line-height: 1.4;
}

.class-text {
  color: #5a5a6a;
  font-size: 13px;
  white-space: nowrap;
  line-height: 1.4;
}

.auditor-text {
  color: #5a5a6a;
  font-size: 13px;
  white-space: nowrap;
  line-height: 1.4;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  vertical-align: middle;
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

.status-rejected {
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.12), rgba(245, 108, 108, 0.06));
  color: #f56c6c;
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

/* ============ Table Footer ============ */
.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0 12px;
  width: 1180px;
  border-top: 1px solid rgba(0,0,0,0.04);
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

.dialog-header-icon.detail-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.dialog-header-icon.audit-icon {
  background: linear-gradient(135deg, #fa709a, #fee140);
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
  box-shadow: 0 0 0 1px rgba(0,0,0,0.06) inset;
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

/* ============ Detail Content ============ */
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.detail-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
  flex: 1;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px 16px;
  background: rgba(102, 126, 234, 0.03);
  border-radius: 10px;
}

.di-label {
  font-size: 12px;
  color: #8c8c9a;
  font-weight: 500;
}

.di-value {
  font-size: 14px;
  color: #1a1a2e;
  font-weight: 500;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ds-label {
  font-size: 12px;
  color: #8c8c9a;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ds-content {
  padding: 12px 16px;
  background: rgba(102, 126, 234, 0.03);
  border-radius: 10px;
  font-size: 14px;
  color: #2a2a3a;
  line-height: 1.6;
}

.no-proof {
  color: #c0c0d0;
  font-style: italic;
}

.proof-files {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.proof-card {
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.proof-card:hover {
  border-color: rgba(64, 149, 229, 0.35);
  box-shadow: 0 4px 16px rgba(64, 149, 229, 0.12);
  transform: translateY(-2px);
}

.proof-image {
  width: 100%;
  height: 160px;
  display: block;
  background: #f5f7fa;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.proof-image:hover {
  opacity: 0.85;
}

.proof-image :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.file-icon-wrap {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.06));
}

.file-icon {
  color: #667eea;
}

.proof-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  background: #fafbfc;
}

.file-name {
  flex: 1;
  font-size: 12px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 11px;
  color: #909399;
  flex-shrink: 0;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 160px;
  color: #909399;
  font-size: 12px;
  background: #f5f7fa;
}

/* ============ Audit Result Group ============ */
.audit-result-group {
  display: flex;
  gap: 12px;
}

.audit-result-opt {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  background: #fff;
  color: #5a5a6a;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  flex: 1;
  justify-content: center;
}

.audit-result-opt input {
  display: none;
}

.audit-result-opt:hover {
  border-color: #667eea;
}

.audit-result-opt.approved {
  border-color: #43e97b;
  background: linear-gradient(135deg, rgba(67, 233, 123, 0.08), rgba(56, 249, 215, 0.04));
  color: #2ecc71;
}

.audit-result-opt.rejected {
  border-color: #f56c6c;
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.08), rgba(245, 108, 108, 0.04));
  color: #f56c6c;
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

  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
