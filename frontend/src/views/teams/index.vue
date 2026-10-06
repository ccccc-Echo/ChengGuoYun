<template>
  <div class="teams-page">
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
            <h1 class="page-title">团队管理</h1>
            <p class="page-subtitle">管理院系 · 科组 · 校区，支持邀请与协作</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--purple">
            <div class="stat-icon">
              <el-icon :size="18"><OfficeBuilding /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedTotal }}</span>
              <span class="stat-label">团队总数</span>
            </div>
          </div>
          <div class="stat-card stat-card--teal">
            <div class="stat-icon">
              <el-icon :size="18"><User /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedMembers }}</span>
              <span class="stat-label">成员总数</span>
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
                placeholder="团队名称"
                clearable
                size="large"
                class="filter-input"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
            <div class="filter-item">
              <el-input
                v-model="filterForm.creator"
                placeholder="负责人姓名"
                clearable
                size="large"
                class="filter-input"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
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
              v-if="$hasPermission('team:create')"
              class="btn-create-effect"
              @click="showCreateDialog = true"
            >
              <el-icon><Plus /></el-icon>
              <span>创建团队</span>
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
              v-for="tab in tabs"
              :key="tab.key"
              :class="['tab-btn', { active: activeTab === tab.key }]"
              @click="handleTabChange(tab.key)"
            >
              <el-icon :size="16"><component :is="tab.icon" /></el-icon>
              <span>{{ tab.label }}</span>
              <span v-if="tab.count > 0" class="tab-count">{{ tab.count }}</span>
            </button>
            <div class="tab-indicator" :style="tabIndicatorStyle"></div>
          </div>
          <div class="header-actions">
            <span class="result-summary">
              <b>{{ pagination.total }}</b> 条结果
            </span>
          </div>
        </div>

        <!-- Skeleton Loading -->
        <div v-if="loading && teams.length === 0" class="skeleton-wrap">
          <div v-for="n in 5" :key="n" class="skeleton-row">
            <div class="skeleton-item" style="width: 48px"></div>
            <div class="skeleton-item skeleton-avatar" style="width: 32px; height: 32px"></div>
            <div class="skeleton-item" style="width: 120px"></div>
            <div class="skeleton-item skeleton-tag" style="width: 60px"></div>
            <div class="skeleton-item" style="width: 80px"></div>
            <div class="skeleton-item" style="width: 50px"></div>
            <div class="skeleton-item" style="width: 140px"></div>
            <div class="skeleton-item" style="width: 180px"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="teams.length === 0" class="empty-state">
          <div class="empty-illustration">
            <div class="empty-circle">
              <el-icon :size="48" color="#c0c0d0"><UserFilled /></el-icon>
            </div>
            <div class="empty-orbit"></div>
          </div>
          <h3 class="empty-title">{{ emptyText }}</h3>
          <p class="empty-desc">{{ emptyDesc }}</p>
          <button
            v-if="$hasPermission('team:create')"
            class="btn-create-effect btn-empty"
            @click="showCreateDialog = true"
          >
            <el-icon><Plus /></el-icon>
            <span>立即创建</span>
          </button>
        </div>

        <!-- Table -->
        <div v-else class="table-scroll">
          <table class="team-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-name">团队名称</th>
                <th class="col-type">类型</th>
                <th class="col-creator">创建人</th>
                <th class="col-members">成员</th>
                <th class="col-created">创建时间</th>
                <th class="col-action">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, idx) in teams"
                :key="row.id"
                class="table-row"
                :style="{ '--accent-color': getTypeColorSafe(row.type), animationDelay: idx * 30 + 'ms' }"
              >
                <td class="col-index">
                  <span class="index-num">{{ String(idx + 1).padStart(2, '0') }}</span>
                </td>
                <td class="col-name">
                  <div class="team-name-cell">
                    <div class="team-avatar" :style="{ background: getTypeColorSafe(row.type) }">
                      {{ (row.name || '?').charAt(0) }}
                    </div>
                    <div class="team-name-info">
                      <span class="team-name">{{ row.name }}</span>
                      <span class="team-sub">{{ getTypeTextSafe(row.type) }}</span>
                    </div>
                  </div>
                </td>
                <td class="col-type">
                  <span class="type-tag" :style="getTypeTagStyle(row.type)">
                    {{ getTypeTextSafe(row.type) }}
                  </span>
                </td>
                <td class="col-creator">
                  <div class="creator-cell">
                    <span class="creator-avatar">{{ (row.creator_name || '?').charAt(0) }}</span>
                    <span class="creator-name">{{ row.creator_name }}</span>
                  </div>
                </td>
                <td class="col-members">
                  <span class="member-count">
                    <el-icon class="member-icon"><User /></el-icon>
                    {{ row.member_count }}
                  </span>
                </td>
                <td class="col-created">
                  <span class="time-text">{{ row.created_at }}</span>
                </td>
                <td class="col-action">
                  <div class="action-group">
                    <template v-if="activeTab === 'my_created'">
                      <button class="action-btn action-btn--primary" @click="handleShowInvite(row)">
                        <el-icon><UserFilled /></el-icon>
                        邀请
                      </button>
                      <button
                        v-if="$hasPermission('team:remove_member')"
                        class="action-btn action-btn--primary"
                        @click="handleManageMembers(row)"
                      >
                        <el-icon><User /></el-icon>
                        成员
                      </button>
                      <button
                        v-if="$hasPermission('team:delete')"
                        class="action-btn action-btn--danger"
                        @click="handleDeleteTeam(row)"
                      >
                        <el-icon><Delete /></el-icon>
                        删除
                      </button>
                    </template>
                    <template v-else-if="activeTab === 'available'">
                      <button class="action-btn action-btn--primary" @click="handleShowDetail(row)">
                        <el-icon><View /></el-icon>
                        详情
                      </button>
                      <button class="action-btn action-btn--accent" @click="handleJoinTeam(row)">
                        <el-icon><Plus /></el-icon>
                        加入
                      </button>
                    </template>
                    <template v-else>
                      <button class="action-btn action-btn--primary" @click="handleShowDetail(row)">
                        <el-icon><View /></el-icon>
                        详情
                      </button>
                      <button class="action-btn action-btn--danger" @click="handleLeaveTeam(row)">
                        <el-icon><SwitchButton /></el-icon>
                        退出
                      </button>
                    </template>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Table Footer -->
        <div class="table-footer" v-if="teams.length > 0">
          <span class="total-text">
            共 <b>{{ pagination.total }}</b> 个团队，每页 <b>{{ pagination.page_size }}</b> 条
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
            <select v-model="pagination.page_size" class="page-size-select" @change="loadTeams">
              <option :value="10">10 条/页</option>
              <option :value="20">20 条/页</option>
              <option :value="50">50 条/页</option>
              <option :value="100">100 条/页</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Dialog -->
    <el-dialog v-model="showCreateDialog" width="560px" class="custom-dialog" align-center>
      <template #header>
        <div class="dialog-header">
          <div class="dialog-header-icon">
            <el-icon :size="20"><Plus /></el-icon>
          </div>
          <div>
            <div class="dialog-title">创建团队</div>
            <div class="dialog-subtitle">填写团队信息，邀请成员协作</div>
          </div>
        </div>
      </template>
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="100px" class="dialog-form">
        <el-form-item label="团队名称" prop="name">
          <el-input v-model="createForm.name" placeholder="请输入团队名称" size="large" />
        </el-form-item>
        <el-form-item label="团队类型" prop="type">
          <div class="type-selector">
            <div
              v-for="t in typeOptions"
              :key="t.value"
              :class="['type-opt', { selected: createForm.type === t.value }]"
              :style="getTypeOptionStyle(createForm.type, t.value)"
              @click="handleTypeSelect(t.value)"
            >
              <span class="type-dot" :style="{ background: getTypeColorSafe(t.value) }"></span>
              {{ t.label }}
            </div>
          </div>
        </el-form-item>
        <el-form-item v-if="userInfo.role === 'admin'" label="创建者" prop="creator_id">
          <el-select v-model="createForm.creator_id" placeholder="请选择创建者" size="large" style="width: 100%;">
            <el-option
              v-for="teacher in teacherOptions"
              :key="teacher.id"
              :label="`${teacher.name} (${teacher.teacher_no})`"
              :value="teacher.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="加入方式">
          <div class="join-method-group">
            <label v-for="m in joinMethods" :key="m.value" :class="['join-method-opt', { checked: createForm.join_method === m.value }]">
              <input v-model="createForm.join_method" type="radio" :value="m.value" />
              <el-icon :size="16"><component :is="m.icon" /></el-icon>
              <span>{{ m.label }}</span>
            </label>
          </div>
        </el-form-item>
        <el-form-item label="团队简介">
          <el-input v-model="createForm.description" type="textarea" :rows="3" placeholder="简单介绍一下这个团队..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="btn-ghost-effect" @click="showCreateDialog = false">取消</button>
        <button class="btn-create-effect" :disabled="saving" @click="handleCreateTeam">
          <span v-if="!saving">确认创建</span>
          <span v-else>创建中...</span>
        </button>
      </template>
    </el-dialog>

    <!-- Invite Dialog -->
    <el-dialog v-model="showInviteDialog" width="460px" class="custom-dialog invite-dialog" align-center>
      <template #header>
        <div class="dialog-header">
          <div class="dialog-header-icon invite-icon">
            <el-icon :size="20"><UserFilled /></el-icon>
          </div>
          <div>
            <div class="dialog-title">邀请成员</div>
            <div class="dialog-subtitle">分享邀请码或扫码加入</div>
          </div>
        </div>
      </template>
      <div class="invite-tabs">
        <button
          :class="['invite-tab', { active: inviteTabActive === 'code' }]"
          @click="inviteTabActive = 'code'"
        >
          <el-icon :size="15"><Document /></el-icon>
          <span>邀请码</span>
        </button>
        <button
          :class="['invite-tab', { active: inviteTabActive === 'qr' }]"
          @click="inviteTabActive = 'qr'"
        >
          <el-icon :size="15"><View /></el-icon>
          <span>二维码</span>
        </button>
      </div>
      <div v-if="inviteTabActive === 'code'" class="invite-box">
        <div class="invite-code-box">
          <span class="invite-label">邀请码</span>
          <div class="invite-code-text">{{ currentTeam?.invite_code }}</div>
          <button class="btn-copy" @click="copyInviteCode">
            <el-icon><Document /></el-icon>
            复制邀请码
          </button>
        </div>
      </div>
      <div v-else class="invite-box invite-box--qr">
        <div class="qr-scan">
          <div v-if="teamQRLoading" class="qr-loading-wrap">
            <el-icon class="is-loading" :size="28"><Loading /></el-icon>
            <span>正在生成二维码...</span>
          </div>
          <img
            v-else-if="teamQRCodeUrl"
            :src="teamQRCodeUrl"
            alt="团队二维码"
            class="team-qr-image"
          />
          <span class="qr-hint">扫码即可加入该团队</span>
        </div>
      </div>
      <template #footer>
        <button class="btn-create-effect" @click="showInviteDialog = false">完成</button>
      </template>
    </el-dialog>

    <!-- Join Dialog -->
    <el-dialog v-model="showJoinDialog" width="440px" class="custom-dialog" align-center>
      <template #header>
        <div class="dialog-header">
          <div class="dialog-header-icon join-icon">
            <el-icon :size="20"><Plus /></el-icon>
          </div>
          <div>
            <div class="dialog-title">加入团队</div>
            <div class="dialog-subtitle">输入邀请码加入团队</div>
          </div>
        </div>
      </template>
      <div class="join-box">
        <div class="join-card">
          <div class="jc-icon" :style="{ background: getTypeColorSafe(joiningTeam?.type) }">
            {{ (joiningTeam?.name || '?').charAt(0) }}
          </div>
          <div class="jc-info">
            <div class="jc-name">{{ joiningTeam?.name }}</div>
            <div class="jc-meta">{{ getTypeTextSafe(joiningTeam?.type) }} · {{ joiningTeam?.creator_name }}</div>
          </div>
        </div>
        <div class="join-code-input">
          <el-input v-model="joinForm.invite_code" placeholder="请输入 6 位邀请码" size="large" maxlength="10" class="invite-input" />
        </div>
      </div>
      <template #footer>
        <button class="btn-ghost-effect" @click="showJoinDialog = false">取消</button>
        <button class="btn-create-effect" @click="handleConfirmJoin">确认加入</button>
      </template>
    </el-dialog>

    <!-- Detail Dialog -->
    <el-dialog v-model="showDetailDialog" width="600px" class="custom-dialog" align-center>
      <template #header>
        <div class="dialog-header">
          <div class="dialog-header-icon detail-icon">
            <el-icon :size="20"><View /></el-icon>
          </div>
          <div>
            <div class="dialog-title">团队详情</div>
            <div class="dialog-subtitle">查看团队完整信息</div>
          </div>
        </div>
      </template>
      <div class="detail-hero" :style="{ background: 'linear-gradient(135deg, ' + getTypeColorSafe(currentTeam?.type) + '22 0%, ' + getTypeColorSafe(currentTeam?.type) + '08 100%)' }">
        <div class="dh-avatar" :style="{ background: getTypeColorSafe(currentTeam?.type) }">
          {{ (currentTeam?.name || '?').charAt(0) }}
        </div>
        <div class="dh-info">
          <div class="dh-name">{{ currentTeam?.name }}</div>
          <div class="dh-meta">
            <span class="dh-type">{{ getTypeTextSafe(currentTeam?.type) }}</span>
            <span>·</span>
            <span>{{ currentTeam?.member_count }} 位成员</span>
          </div>
        </div>
      </div>
      <div class="detail-grid">
        <div class="detail-item">
          <span class="di-label">创建人</span>
          <span class="di-value">{{ currentTeam?.creator_name }}</span>
        </div>
        <div class="detail-item">
          <span class="di-label">创建时间</span>
          <span class="di-value">{{ currentTeam?.created_at }}</span>
        </div>
        <div v-if="currentTeam?.joined_at" class="detail-item highlight">
          <span class="di-label">加入时间</span>
          <span class="di-value">{{ currentTeam?.joined_at }}</span>
        </div>
        <div class="detail-item">
          <span class="di-label">成员数量</span>
          <span class="di-value">{{ currentTeam?.member_count }} 人</span>
        </div>
      </div>
      <template #footer>
        <button class="btn-create-effect" @click="showDetailDialog = false">关闭</button>
      </template>
    </el-dialog>

    <!-- Members Dialog -->
    <el-dialog v-model="showMembersDialog" width="680px" class="custom-dialog" align-center>
      <template #header>
        <div class="dialog-header">
          <div class="dialog-header-icon members-icon">
            <el-icon :size="20"><User /></el-icon>
          </div>
          <div>
            <div class="dialog-title">成员管理</div>
            <div class="dialog-subtitle">{{ currentTeam?.name }} · 共 {{ members.length }} 位成员</div>
          </div>
        </div>
      </template>
      <div class="members-list">
        <div v-for="member in members" :key="member.id" class="member-item">
          <div class="member-avatar">{{ (member.teacher_name || '?').charAt(0) }}</div>
          <div class="member-info">
            <div class="member-name-row">
              <span class="member-name">{{ member.teacher_name }}</span>
              <span :class="['member-role', member.role === 'leader' ? 'role-leader' : 'role-member']">
                {{ member.role === 'leader' ? '负责人' : '成员' }}
              </span>
            </div>
            <div class="member-meta">
              <span>{{ member.teacher_no }}</span>
              <span class="dot">·</span>
              <span>{{ member.joined_at }}</span>
            </div>
          </div>
          <button
            v-if="member.role !== 'leader' && $hasPermission('team:remove_member')"
            class="action-btn action-btn--danger btn-remove-member"
            @click="handleRemoveMember(member)"
          >
            <el-icon><Delete /></el-icon>
            移除
          </button>
        </div>
        <div v-if="members.length === 0" class="empty-members">暂无成员</div>
      </div>
      <template #footer>
        <button class="btn-create-effect" @click="showMembersDialog = false">完成</button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import QRCode from 'qrcode'
import {
  Plus, Document, UserFilled, Search, Refresh, User,
  OfficeBuilding, Delete, View, SwitchButton,
  ArrowLeft, ArrowRight, Setting, Loading
} from '@element-plus/icons-vue'
import { teamApi, authApi } from '@/api'
import { getUserInfo } from '@/utils/auth'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const saving = ref(false)
const teams = ref([])
const members = ref([])
const teacherOptions = ref([])

const showCreateDialog = ref(false)
const showInviteDialog = ref(false)
const showJoinDialog = ref(false)
const showDetailDialog = ref(false)
const showMembersDialog = ref(false)

const currentTeam = ref(null)
const joiningTeam = ref(null)

// Invite dialog tabs (邀请码 / 二维码)
const inviteTabActive = ref('code')
const teamQRCodeUrl = ref('')
const teamQRLoading = ref(false)

const userInfo = ref(getUserInfo() || {})

const activeTab = ref(route.query.tab || 'my_created')

const typeOptions = [
  { value: 'department', label: '院系' },
  { value: 'subject_group', label: '科组' },
  { value: 'campus', label: '校区' },
  { value: 'grade', label: '年级' },
  { value: 'other', label: '其他' }
]

const typeText = {}
typeOptions.forEach(t => { typeText[t.value] = t.label })

const typeColors = {
  department: '#667eea',
  subject_group: '#f093fb',
  campus: '#4facfe',
  grade: '#43e97b',
  other: '#fa709a'
}

// 安全的获取类型颜色函数
const getTypeColor = (type) => {
  if (!type || typeof type !== 'string') return '#667eea'
  return typeColors[type] || '#667eea'
}

// 验证团队类型是否有效
const isValidTeamType = (type) => {
  if (!type || typeof type !== 'string') return false
  return typeOptions.some(opt => opt.value === type)
}

// 确保团队类型值有效
const ensureValidTeamType = (type) => {
  if (isValidTeamType(type)) {
    return type
  }
  console.warn(`无效的团队类型: ${type}，使用默认值 'department'`)
  return 'department'
}

const getTypeTagStyle = (type) => {
  try {
    const color = getTypeColorSafe(type)
    return {
      background: color + '14',
      color: color,
      borderColor: color + '40'
    }
  } catch (error) {
    console.error('团队类型标签样式计算错误:', error)
    return {
      background: '#667eea14',
      color: '#667eea',
      borderColor: '#667eea40'
    }
  }
}

// 安全的获取类型颜色函数
const getTypeColorSafe = (type) => {
  if (!type || typeof type !== 'string') return '#667eea'
  return typeColors[type] || '#667eea'
}

// 安全的获取类型文本函数
const getTypeTextSafe = (type) => {
  if (!type || typeof type !== 'string') return type || '未知'
  const typeOption = typeOptions.find(opt => opt.value === type)
  return typeOption ? typeOption.label : type
}

// 获取类型选项样式
const getTypeOptionStyle = (currentType, optionType) => {
  try {
    const isSelected = currentType === optionType
    if (!isSelected) return {}

    const color = getTypeColorSafe(optionType)

    // 修复bug：选中状态下，字体颜色应该变白（已经在CSS中的.selected类处理）
    // 这里只处理背景和边框样式，字体颜色由CSS类控制
    const styles = {
      background: color + '18',  // 透明背景色
      borderColor: color         // 边框颜色
      // 不再设置color属性，避免与CSS冲突
    }
    return styles
  } catch (error) {
    console.error('团队类型样式计算错误:', error)
    return {}
  }
}

// 处理类型选择
const handleTypeSelect = (typeValue) => {
  console.log('handleTypeSelect triggered:', typeValue)
  const validType = ensureValidTeamType(typeValue)
  createForm.type = validType
  console.log('Type updated to:', createForm.type)
}

const pagination = ref({ page: 1, page_size: 20, total: 0 })

const tabs = computed(() => {
  const list = [
    { key: 'my_created', label: '我创建的', icon: Plus, count: activeTab.value === 'my_created' ? pagination.value.total : 0 },
    { key: 'available', label: '可加入的', icon: UserFilled, count: activeTab.value === 'available' ? pagination.value.total : 0 }
  ]
  // 管理员不参与“我加入的”团队管理，仅保留“我创建的”和“可加入的”
  if (userInfo.value.role !== 'admin') {
    list.push({ key: 'joined', label: '我加入的', icon: User, count: activeTab.value === 'joined' ? pagination.value.total : 0 })
  }
  return list
})

const totalMembers = computed(() => {
  return teams.value.reduce((sum, t) => sum + (t.member_count || 0), 0)
})

// Animated counters
const animatedTotal = ref(0)
const animatedMembers = ref(0)
const animateValue = (target, duration = 600) => {
  const start = target === animatedTotal.value || animatedMembers.value ? 0 : 0
  const startTime = performance.now()
  const animate = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easeProgress = 1 - Math.pow(1 - progress, 3)
    const value = Math.round(start + (target - start) * easeProgress)
    return value
  }
  // Simple approach: just set the value after mount
  return target
}
watch(() => pagination.value.total, (val) => {
  animatedTotal.value = val
})
watch(totalMembers, (val) => {
  animatedMembers.value = val
})

const tabIndicatorStyle = computed(() => {
  const idx = tabs.value.findIndex(t => t.key === activeTab.value)
  return {
    transform: `translateX(${idx * 140}px)`
  }
})

const emptyText = computed(() => {
  if (activeTab.value === 'my_created') return '你还没有创建任何团队'
  if (activeTab.value === 'available') return '暂无可加入的团队'
  return '你还没有加入任何团队'
})

const emptyDesc = computed(() => {
  if (activeTab.value === 'my_created') return '创建一个团队来管理成员和协作'
  if (activeTab.value === 'available') return '当前没有其他团队可加入'
  return '使用邀请码加入感兴趣的团队'
})

const joinMethods = [
  { value: 'code', label: '邀请码', icon: Document },
  { value: 'qr', label: '扫码', icon: Document },
  { value: 'both', label: '两者皆可', icon: Setting }
]

const createFormRef = ref(null)
const createForm = reactive({
  name: '',
  type: ensureValidTeamType('department'),
  description: '',
  creator_id: '',
  join_method: 'code'
})

const createRules = {
  name: [{ required: true, message: '请输入团队名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择团队类型', trigger: 'change' }]
}

const filterForm = ref({ name: '', creator: '' })
const joinForm = reactive({ invite_code: '' })

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

const goPage = (page) => {
  if (page < 1 || page > totalPages.value) return
  pagination.value.page = page
  loadTeams()
}

const loadTeacherOptions = async () => {
  try {
    const res = await authApi.getTeachers()
    teacherOptions.value = res.teachers || []
  } catch (error) {
    console.error('加载教师列表失败:', error)
  }
}

const loadTeams = async () => {
  loading.value = true
  try {
    const res = await teamApi.list({
      tab: activeTab.value,
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      name: filterForm.value.name,
      creator: filterForm.value.creator
    })
    teams.value = res.teams || []
    pagination.value.total = res.pagination?.total || 0
  } catch (error) {
    console.error('加载团队列表失败:', error)
    ElMessage.error('加载团队列表失败')
  } finally {
    loading.value = false
  }
}

const handleTabChange = (tab) => {
  activeTab.value = tab
  router.push({ query: { ...route.query, tab } })
  pagination.value.page = 1
  loadTeams()
}

const handleSearch = () => {
  pagination.value.page = 1
  loadTeams()
}

const resetFilter = () => {
  filterForm.value = { name: '', creator: '' }
  pagination.value.page = 1
  loadTeams()
}

const handleCreateTeam = async () => {
  if (!createFormRef.value) return
  try {
    await createFormRef.value.validate()
    saving.value = true
    await teamApi.create(createForm)
    ElMessage.success('团队创建成功')
    showCreateDialog.value = false
    createForm.name = ''
    createForm.type = ensureValidTeamType('department')
    createForm.description = ''
    createForm.creator_id = ''
    createForm.join_method = 'code'
    loadTeams()
  } catch (error) {
    if (error !== false) {
      console.error('创建团队失败:', error)
      ElMessage.error(error.response?.data?.error || '创建团队失败')
    }
  } finally {
    saving.value = false
  }
}

const handleDeleteTeam = (team) => {
  ElMessageBox.confirm('确认删除该团队吗？此操作不可恢复。', '删除确认', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'error'
  }).then(async () => {
    try {
      await teamApi.delete(team.id)
      ElMessage.success('团队删除成功')
      loadTeams()
    } catch (error) {
      console.error('删除团队失败:', error)
      ElMessage.error(error.response?.data?.error || '删除团队失败')
    }
  })
}

const handleShowInvite = (team) => {
  currentTeam.value = team
  inviteTabActive.value = 'code'
  teamQRCodeUrl.value = ''
  showInviteDialog.value = true
  if (team?.invite_code) {
    generateTeamQR(team)
  }
}

const generateTeamQR = async (team) => {
  if (!team?.invite_code) return
  teamQRLoading.value = true
  try {
    const joinUrl = `${window.location.origin}/team/join?code=${team.invite_code}`
    teamQRCodeUrl.value = await QRCode.toDataURL(joinUrl, {
      width: 220,
      margin: 2,
      color: { dark: '#1a1a2e', light: '#ffffff' }
    })
  } catch (error) {
    console.error('生成团队二维码失败:', error)
    ElMessage.error('生成二维码失败')
  } finally {
    teamQRLoading.value = false
  }
}

const handleShowDetail = (team) => {
  currentTeam.value = team
  showDetailDialog.value = true
}

const handleJoinTeam = (team) => {
  joiningTeam.value = team
  joinForm.invite_code = ''
  showJoinDialog.value = true
}

const handleConfirmJoin = async () => {
  if (!joinForm.invite_code) {
    ElMessage.error('邀请码不能为空')
    return
  }
  try {
    await teamApi.join({ invite_code: joinForm.invite_code })
    ElMessage.success('加入团队成功')
    showJoinDialog.value = false
    joiningTeam.value = null
    loadTeams()
  } catch (error) {
    console.error('加入团队失败:', error)
    ElMessage.error(error.response?.data?.error || '加入团队失败')
  }
}

const handleLeaveTeam = (team) => {
  ElMessageBox.confirm('确认退出该团队吗？', '退出确认', {
    confirmButtonText: '确定退出',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await teamApi.leave(team.id)
      ElMessage.success('已退出团队')
      loadTeams()
    } catch (error) {
      console.error('退出团队失败:', error)
      ElMessage.error(error.response?.data?.error || '退出团队失败')
    }
  })
}

const handleManageMembers = async (team) => {
  currentTeam.value = team
  try {
    const res = await teamApi.getMembers(team.id)
    members.value = res.members || []
    showMembersDialog.value = true
  } catch (error) {
    console.error('获取团队成员失败:', error)
    ElMessage.error('获取团队成员失败')
  }
}

const handleRemoveMember = (member) => {
  ElMessageBox.confirm('确认移除该成员吗？', '移除确认', {
    confirmButtonText: '确定移除',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await teamApi.removeMember(currentTeam.value.id, member.teacher_id)
      ElMessage.success('成员移除成功')
      members.value = members.value.filter(m => m.id !== member.id)
    } catch (error) {
      console.error('移除成员失败:', error)
      ElMessage.error(error.response?.data?.error || '移除成员失败')
    }
  })
}

const copyInviteCode = async () => {
  if (!currentTeam.value?.invite_code) return
  try {
    await navigator.clipboard.writeText(currentTeam.value.invite_code)
    ElMessage.success('邀请码已复制')
  } catch {
    ElMessage.error('复制失败，请手动复制')
  }
}

// 监听弹窗显示状态，重置表单
watch(showCreateDialog, (newVal, oldVal) => {
  if (newVal !== oldVal && !newVal) {
    // 弹窗关闭时重置类型到默认值
    createForm.type = ensureValidTeamType('department')
  }
})

onMounted(() => {
  loadTeams()
  animatedTotal.value = pagination.value.total
  animatedMembers.value = totalMembers.value
  if (userInfo.value.role === 'admin') {
    loadTeacherOptions()
  }
})
</script>

<style scoped>
/* ============ Page Container ============ */
.teams-page {
  position: relative;
  min-height: 100%;
  overflow: hidden;
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
  background: linear-gradient(135deg, #f093fb, #f5576c);
  bottom: -50px;
  left: 10%;
  animation: float 25s ease-in-out infinite reverse;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #4facfe, #43e97b);
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
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.icon-pulse {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #43e97b;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.6; }
}

.page-title {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  background: linear-gradient(135deg, #1a1a2e 0%, #667eea 100%);
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
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 14px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-card--purple .stat-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-card--teal .stat-icon {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  font-variant-numeric: tabular-nums;
}

.stat-label {
  font-size: 12px;
  color: #8c8c9a;
}

/* ============ Glass Card ============ */
.glass-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
}

/* ============ Filter Card ============ */
.filter-card {
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
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
}

.filter-item {
  min-width: 220px;
}

.filter-input {
  width: 240px;
}

.filter-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.06) inset;
  transition: all 0.25s ease;
  background: rgba(255, 255, 255, 0.6);
}

.filter-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px rgba(102, 126, 234, 0.3) inset;
}

.filter-input :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.4) inset;
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
  transition: all 0.2s ease;
}

.btn-ghost-effect:hover {
  border-color: #667eea;
  color: #667eea;
  background: rgba(102, 126, 234, 0.04);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
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
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4);
  transition: all 0.25s ease;
  overflow: hidden;
}

.btn-create-effect:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5);
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
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
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
  padding: 0 28px;
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

.tab-indicator {
  position: absolute;
  bottom: -20px;
  left: 0;
  height: 3px;
  width: calc(33.333% - 4px);
  margin-left: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
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

.team-table {
  width: auto;
  border-collapse: separate;
  border-spacing: 0;
}

.team-table thead th {
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

.team-table tbody td {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.03);
  font-size: 14px;
  color: #2a2a3a;
  vertical-align: middle;
  white-space: nowrap;
}

.team-table tbody tr:last-child td {
  border-bottom: none;
}

/* ============ Column Alignment ============ */
/* Center: index, number, date columns */
.team-table thead th.col-index,
.team-table thead th.col-members,
.team-table thead th.col-created,
.team-table tbody td.col-index,
.team-table tbody td.col-members,
.team-table tbody td.col-created {
  text-align: center;
}

/* Left: name, info columns */
.team-table thead th.col-name,
.team-table thead th.col-type,
.team-table thead th.col-creator,
.team-table tbody td.col-name,
.team-table tbody td.col-type,
.team-table tbody td.col-creator {
  text-align: left;
}

/* Left: action column */
.team-table thead th.col-action,
.team-table tbody td.col-action {
  text-align: left;
}

.index-num {
  font-size: 13px;
  font-weight: 600;
  color: #c0c0d0;
  font-variant-numeric: tabular-nums;
}

.team-name-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.team-avatar {
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

.team-name-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.team-name {
  font-weight: 600;
  color: #1a1a2e;
  font-size: 14px;
}

.team-sub {
  font-size: 12px;
  color: #b0b0c0;
}

.type-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid;
}

.creator-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.creator-avatar {
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

.creator-name {
  font-size: 14px;
  color: #2a2a3a;
}

.member-count {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
  color: #2a2a3a;
  font-variant-numeric: tabular-nums;
}

.member-icon {
  color: #8c8c9a;
  font-size: 14px;
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
  background: transparent;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.18s ease;
  white-space: nowrap;
}

.action-btn--primary {
  color: #667eea;
}

.action-btn--primary:hover {
  background: rgba(102, 126, 234, 0.08);
}

.action-btn--accent {
  color: #43e97b;
}

.action-btn--accent:hover {
  background: rgba(67, 233, 123, 0.08);
}

.action-btn--danger {
  color: #ef4444;
}

.action-btn--danger:hover {
  background: rgba(239, 68, 68, 0.08);
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
  color: #1a1a2e;
  font-weight: 600;
}

.pagination-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-btn {
  min-width: 34px;
  height: 34px;
  padding: 0 10px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  color: #5a5a6a;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled):not(.active) {
  border-color: #667eea;
  color: #667eea;
  background: rgba(102, 126, 234, 0.04);
}

.page-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: transparent;
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
}

.page-size-select:hover {
  border-color: #667eea;
}

/* ============ Dialog ============ */
.custom-dialog :deep(.el-dialog) {
  border-radius: 20px !important;
  overflow: hidden;
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
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.invite-icon { background: linear-gradient(135deg, #f093fb, #f5576c); }
.join-icon { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.detail-icon { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.members-icon { background: linear-gradient(135deg, #fa709a, #fee140); }

.dialog-title {
  font-size: 17px;
  font-weight: 600;
  color: #1a1a2e;
}

.dialog-subtitle {
  font-size: 13px;
  color: #8c8c9a;
  margin-top: 2px;
}

.dialog-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #5a5a6a;
}

.dialog-form :deep(.el-input__wrapper) {
  border-radius: 10px;
}

/* ============ Type Selector ============ */
.type-selector {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.type-opt {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 20px;
  background: #fff;
  color: #5a5a6a;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.type-opt:hover {
  border-color: #667eea;
}

.type-opt.selected {
  border-color: #667eea;
  background: #667eea;
  color: #fff;
}

.type-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

/* ============ Join Methods ============ */
.join-method-group {
  display: flex;
  gap: 10px;
}

.join-method-opt {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  background: #fff;
  color: #5a5a6a;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.join-method-opt input {
  display: none;
}

.join-method-opt:hover {
  border-color: #667eea;
}

.join-method-opt.checked {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.06);
  color: #667eea;
}

/* ============ Invite ============ */
.invite-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  padding: 4px;
  background: #f1f1f7;
  border-radius: 12px;
}

.invite-tab {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 16px;
  border: none;
  background: transparent;
  border-radius: 9px;
  color: #8c8c9a;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.invite-tab:hover {
  color: #667eea;
}

.invite-tab.active {
  background: #fff;
  color: #667eea;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.invite-box {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.invite-box--qr {
  align-items: center;
  justify-content: center;
  padding: 28px 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.06) 0%, rgba(118, 75, 162, 0.06) 100%);
  border: 1px solid rgba(102, 126, 234, 0.12);
  border-radius: 16px;
}

.qr-loading-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 50px 0;
  color: #8c8c9a;
  font-size: 13px;
}

.team-qr-image {
  width: 200px;
  height: 200px;
  padding: 10px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.invite-code-box {
  text-align: center;
  padding: 28px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.06) 0%, rgba(118, 75, 162, 0.06) 100%);
  border: 1px solid rgba(102, 126, 234, 0.12);
  border-radius: 16px;
}

.invite-label {
  display: block;
  font-size: 12px;
  color: #8c8c9a;
  margin-bottom: 12px;
  letter-spacing: 0.5px;
}

.invite-code-text {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: 'SF Mono', 'Monaco', 'Roboto Mono', monospace;
  margin-bottom: 16px;
}

.btn-copy {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 10px;
  background: #fff;
  color: #5a5a6a;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-copy:hover {
  border-color: #667eea;
  color: #667eea;
}

.qr-box {
  text-align: center;
  padding: 20px;
  background: #f8f8fc;
  border-radius: 16px;
}

.qr-scan {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.qr-pattern {
  position: relative;
  width: 120px;
  height: 120px;
  background: #fff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.qr-corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border: 3px solid #667eea;
}

.qr-corner.tl { top: 8px; left: 8px; border-right: none; border-bottom: none; }
.qr-corner.tr { top: 8px; right: 8px; border-left: none; border-bottom: none; }
.qr-corner.bl { bottom: 8px; left: 8px; border-right: none; border-top: none; }

.qr-center {
  color: #667eea;
}

.qr-hint {
  font-size: 12px;
  color: #8c8c9a;
}

/* ============ Join Dialog ============ */
.join-box {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.join-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: #f8f8fc;
  border-radius: 14px;
}

.jc-icon {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 18px;
}

.jc-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.jc-name {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
}

.jc-meta {
  font-size: 13px;
  color: #8c8c9a;
}

.invite-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  padding: 4px 14px;
}

/* ============ Detail ============ */
.detail-hero {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 20px;
}

.dh-avatar {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 22px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.dh-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.dh-name {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a2e;
}

.dh-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #5a5a6a;
}

.dh-type {
  font-weight: 500;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 16px;
  background: #f8f8fc;
  border-radius: 12px;
}

.detail-item.highlight {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  grid-column: span 2;
}

.di-label {
  font-size: 12px;
  color: #8c8c9a;
  letter-spacing: 0.3px;
}

.di-value {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a2e;
}

/* ============ Members List ============ */
.members-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  background: #f8f8fc;
  border-radius: 14px;
  transition: all 0.2s ease;
}

.member-item:hover {
  background: rgba(102, 126, 234, 0.04);
}

.member-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #a8edea, #fed6e3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5a5a6a;
  font-weight: 600;
  font-size: 15px;
  flex-shrink: 0;
}

.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.member-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}

.member-role {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 500;
}

.role-leader {
  background: linear-gradient(135deg, rgba(240, 147, 251, 0.14), rgba(255, 138, 190, 0.14));
  color: #c44d8f;
}

.role-member {
  background: #eef0f5;
  color: #5a5a6a;
}

.member-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #8c8c9a;
}

.member-meta .dot {
  opacity: 0.5;
}

.btn-remove-member {
  margin-left: auto;
}

.empty-members {
  text-align: center;
  padding: 30px;
  color: #b0b0c0;
  font-size: 14px;
}

/* ============ Responsive ============ */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .page-stats {
    width: 100%;
  }
  .stat-card {
    flex: 1;
  }
  .filter-inner {
    flex-direction: column;
    align-items: stretch;
  }
  .filter-group {
    flex-direction: column;
  }
  .filter-item {
    width: 100%;
  }
  .filter-input {
    width: 100%;
  }
  .filter-divider {
    display: none;
  }
  .filter-actions {
    flex-wrap: wrap;
  }
  .detail-grid {
    grid-template-columns: 1fr;
  }
  .detail-item.highlight {
    grid-column: span 1;
  }
  .team-table {
    min-width: 800px;
  }
}
</style>