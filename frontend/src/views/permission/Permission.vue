<template>
  <div class="permission-page">
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
              <el-icon :size="22"><Lock /></el-icon>
            </div>
            <div class="icon-pulse"></div>
          </div>
          <div class="page-title-text">
            <h1 class="page-title">权限管理</h1>
            <p class="page-subtitle">配置角色权限 · 精细控制 · 安全可控</p>
          </div>
        </div>
        <div class="page-stats">
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <el-icon :size="18"><User /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedTotal }}</span>
              <span class="stat-label">角色总数</span>
            </div>
          </div>
          <div class="stat-card stat-card--orange">
            <div class="stat-icon">
              <el-icon :size="18"><Setting /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedPermissions }}</span>
              <span class="stat-label">权限项数</span>
            </div>
          </div>
          <div class="stat-card stat-card--green">
            <div class="stat-icon">
              <el-icon :size="18"><SwitchButton /></el-icon>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ animatedActivePerms }}</span>
              <span class="stat-label">已启用权限</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Filter Card (with create button) -->
      <div class="glass-card filter-card">
        <div class="filter-glow"></div>
        <div class="filter-inner">
          <div class="filter-hint">
            <el-icon :size="16"><InfoFilled /></el-icon>
            <span>在此管理系统的所有角色及其对应的权限配置</span>
          </div>
          <div class="filter-divider"></div>
          <div class="filter-actions">
            <button class="btn-create-effect" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              <span>添加角色</span>
              <div class="btn-shine"></div>
            </button>
          </div>
        </div>
      </div>

      <!-- Table Card -->
      <div class="glass-card table-card">
        <div class="table-header">
          <div class="header-title">
            <span class="title-text">角色列表</span>
            <span class="result-summary">
              共 <b>{{ roles.length }}</b> 个角色
            </span>
          </div>
        </div>

        <!-- Skeleton Loading -->
        <div v-if="loading && roles.length === 0" class="skeleton-wrap">
          <div v-for="n in 4" :key="n" class="skeleton-row">
            <div class="skeleton-item" style="width: 40px"></div>
            <div class="skeleton-item" style="width: 160px"></div>
            <div class="skeleton-item" style="width: 80px"></div>
            <div class="skeleton-item" style="width: 130px"></div>
            <div class="skeleton-item" style="width: 180px"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="roles.length === 0" class="empty-state">
          <div class="empty-illustration">
            <div class="empty-circle">
              <el-icon :size="48" color="#c0c0d0"><Lock /></el-icon>
            </div>
            <div class="empty-orbit"></div>
          </div>
          <h3 class="empty-title">暂无角色数据</h3>
          <p class="empty-desc">点击「添加角色」创建第一个角色，开始配置权限体系</p>
          <button class="btn-create-effect btn-empty" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            <span>添加角色</span>
          </button>
        </div>

        <!-- Table -->
        <div v-else class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-name">角色信息</th>
                <th class="col-perms">权限数量</th>
                <th class="col-time">创建时间</th>
                <th class="col-action">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, idx) in roles"
                :key="row.id"
                class="table-row"
                :style="{ '--accent-color': getRoleColor(row.name), animationDelay: idx * 40 + 'ms' }"
              >
                <td class="col-index">
                  <span class="index-num">{{ String(idx + 1).padStart(2, '0') }}</span>
                </td>
                <td class="col-name">
                  <div class="role-cell">
                    <div class="role-avatar" :style="{ background: getRoleColor(row.name) }">
                      <el-icon :size="16"><UserFilled /></el-icon>
                    </div>
                    <div class="role-info">
                      <span class="role-name">{{ row.name }}</span>
                      <span class="role-desc">{{ getRoleDesc(row.name) }}</span>
                    </div>
                  </div>
                </td>
                <td class="col-perms">
                  <span class="perm-count" :class="getPermLevelClass(row.permissions?.length || 0)">
                    {{ row.permissions?.length || 0 }} 项
                  </span>
                </td>
                <td class="col-time">
                  <span class="time-text">{{ row.created_at || '-' }}</span>
                </td>
                <td class="col-action">
                  <div class="action-group">
                    <button
                      class="action-btn action-btn--primary"
                      @click="handleEdit(row)"
                    >
                      <el-icon><View /></el-icon>
                      编辑权限
                    </button>
                    <button
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
      </div>

      <!-- Add Role Dialog -->
      <el-dialog v-model="showAddDialog" width="480px" class="custom-dialog" align-center>
        <template #header>
          <div class="dialog-header">
            <div class="dialog-header-icon add-icon">
              <el-icon :size="20"><Plus /></el-icon>
            </div>
            <div>
              <div class="dialog-title">添加角色</div>
              <div class="dialog-subtitle">创建新角色并配置对应的权限</div>
            </div>
          </div>
        </template>
        <el-form ref="addFormRef" :model="addForm" :rules="addRules" label-width="100px" class="dialog-form">
          <el-form-item label="角色名称" prop="name">
            <el-input v-model="addForm.name" placeholder="请输入角色名称，如：院系负责人" size="large" />
          </el-form-item>
          <div class="dialog-tip">
            <el-icon :size="14"><InfoFilled /></el-icon>
            <span>添加后可在权限配置弹窗中为该角色分配具体权限</span>
          </div>
        </el-form>
        <template #footer>
          <button class="btn-ghost-effect" @click="showAddDialog = false">取消</button>
          <button class="btn-create-effect" :disabled="saving" @click="handleAddSubmit">
            <span v-if="!saving">确认添加</span>
            <span v-else>添加中...</span>
          </button>
        </template>
      </el-dialog>

      <!-- Permission Modal -->
      <PermissionModal
        v-if="showEditModal"
        :role="currentRole"
        :permission-groups="permissionGroups"
        @close="showEditModal = false"
        @save="handleSavePermissions"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus, Lock, UserFilled, User, Setting, Delete, View,
  SwitchButton, InfoFilled
} from '@element-plus/icons-vue'
import { permissionApi } from '@/api'
import PermissionModal from './PermissionModal.vue'

const loading = ref(false)
const saving = ref(false)
const roles = ref([])
const permissionGroups = ref([])
const showAddDialog = ref(false)
const showEditModal = ref(false)
const currentRole = ref(null)
const addFormRef = ref(null)

const addForm = ref({
  name: ''
})

const addRules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' }
  ]
}

// Animated counters
const animatedTotal = ref(0)
const animatedPermissions = ref(0)
const animatedActivePerms = ref(0)

const totalPermissionsCount = computed(() => {
  return permissionGroups.value.reduce((sum, g) => sum + (g.permissions?.length || 0), 0)
})

const activePermissionsCount = computed(() => {
  return roles.value.reduce((sum, r) => sum + (r.permissions?.length || 0), 0)
})

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

watch(() => roles.value.length, (val) => {
  animateValue(val, animatedTotal)
})

watch(totalPermissionsCount, (val) => {
  animateValue(val, animatedPermissions)
})

watch(activePermissionsCount, (val) => {
  animateValue(val, animatedActivePerms)
})

// Role color mapping
const roleColors = {
  '院系负责人': 'linear-gradient(135deg, #667eea, #764ba2)',
  '辅导员': 'linear-gradient(135deg, #fa709a, #fee140)',
  '教师': 'linear-gradient(135deg, #4facfe, #00f2fe)',
  '教务管理员': 'linear-gradient(135deg, #43e97b, #38f9d7)',
  'admin': 'linear-gradient(135deg, #f093fb, #f5576c)',
  'teacher': 'linear-gradient(135deg, #667eea, #764ba2)',
  'student': 'linear-gradient(135deg, #4facfe, #00f2fe)'
}

const getRoleColor = (name) => {
  return roleColors[name] || 'linear-gradient(135deg, #a8edea, #fed6e3)'
}

const getRoleDesc = (name) => {
  const map = {
    '院系负责人': '负责院系级权限管理',
    '辅导员': '负责学生日常管理',
    '教师': '基础教师教学权限',
    '教务管理员': '教务相关管理权限',
    'admin': '系统管理员 · 全部权限',
    'teacher': '教师角色 · 教学相关',
    'student': '学生角色 · 学习相关'
  }
  return map[name] || '自定义角色'
}

const getPermLevelClass = (count) => {
  if (count >= 8) return 'perm-count--high'
  if (count >= 4) return 'perm-count--medium'
  if (count > 0) return 'perm-count--low'
  return 'perm-count--empty'
}

const fetchRoles = async () => {
  loading.value = true
  try {
    const res = await permissionApi.getRoles()
    roles.value = res.roles || []
    permissionGroups.value = res.permission_groups || []
  } catch (error) {
    console.error('获取角色列表失败:', error)
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  addForm.value = { name: '' }
  showAddDialog.value = true
}

const handleAddSubmit = async () => {
  if (!addFormRef.value) return

  await addFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      saving.value = true
      const res = await permissionApi.createRole(addForm.value)
      if (res.message) {
        ElMessage.success(res.message)
        showAddDialog.value = false
        addForm.value = { name: '' }
        await fetchRoles()
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || '添加角色失败'
      ElMessage.error(errorMsg)
    } finally {
      saving.value = false
    }
  })
}

const handleEdit = (row) => {
  currentRole.value = { ...row }
  showEditModal.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定删除角色「${row.name}」吗？<br/><span style="color:#8c8c9a;font-size:12px;">删除后该角色关联的权限配置将一并清除。</span>`,
    '确认删除',
    {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      await permissionApi.deleteRole(row.id)
      ElMessage.success('角色删除成功')
      await fetchRoles()
    } catch (error) {
      const errorMsg = error.response?.data?.error || '删除角色失败'
      ElMessage.error(errorMsg)
    }
  })
}

const handleSavePermissions = async (roleId, permissions) => {
  try {
    await permissionApi.updatePermissions(roleId, { permissions })
    ElMessage.success('权限更新成功')
    showEditModal.value = false
    await fetchRoles()
  } catch (error) {
    const errorMsg = error.response?.data?.error || '更新权限失败'
    ElMessage.error(errorMsg)
  }
}

onMounted(() => {
  fetchRoles()
})
</script>

<style scoped>
/* ============ Page Container ============ */
.permission-page {
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
  padding: 20px 28px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.filter-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-size: 13px;
  font-weight: 500;
}

.filter-hint .el-icon {
  opacity: 0.7;
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

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-text {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
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

@keyframes rowFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.data-table tbody tr {
  animation: rowFadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) both;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.data-table tbody tr:hover {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.015) 100%);
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
/* Center: 序号 / 权限数量 / 创建时间 */
.data-table thead th.col-index,
.data-table thead th.col-perms,
.data-table thead th.col-time,
.data-table tbody td.col-index,
.data-table tbody td.col-perms,
.data-table tbody td.col-time {
  text-align: center;
}

/* Left: 角色信息 */
.data-table thead th.col-name,
.data-table tbody td.col-name {
  text-align: left;
}

/* Left: 操作（与其他管理页面一致） */
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

.role-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.role-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.role-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.role-name {
  font-weight: 600;
  color: #1a1a2e;
  font-size: 14px;
}

.role-desc {
  font-size: 12px;
  color: #8c8c9a;
}

.perm-count {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}

.perm-count--high {
  background: linear-gradient(135deg, rgba(67, 233, 123, 0.12), rgba(67, 233, 123, 0.06));
  color: #2ecc71;
}

.perm-count--medium {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.06));
  color: #667eea;
}

.perm-count--low {
  background: linear-gradient(135deg, rgba(230, 162, 60, 0.12), rgba(230, 162, 60, 0.06));
  color: #e6a23c;
}

.perm-count--empty {
  background: rgba(0, 0, 0, 0.04);
  color: #909399;
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

.action-btn--danger {
  color: #ef4444;
}

.action-btn--danger:hover {
  background: rgba(239, 68, 68, 0.08);
  transform: translateY(-1px);
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

.dialog-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.04), rgba(118, 75, 162, 0.04));
  border-radius: 10px;
  font-size: 12px;
  color: #667eea;
  margin-top: 8px;
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
}

@media (max-width: 768px) {
  .page-stats {
    flex-wrap: wrap;
  }

  .filter-inner {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-actions {
    margin-left: 0;
    width: 100%;
  }
}
</style>
