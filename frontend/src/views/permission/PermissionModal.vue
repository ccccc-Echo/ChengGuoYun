<template>
  <el-dialog
    v-model="visible"
    width="680px"
    class="permission-modal custom-dialog"
    align-center
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <template #header>
      <div class="dialog-header">
        <div class="dialog-header-icon edit-icon">
          <el-icon :size="20"><Lock /></el-icon>
        </div>
        <div>
          <div class="dialog-title">编辑角色权限</div>
          <div class="dialog-subtitle">
            角色：<span class="role-highlight">{{ role?.name }}</span> · 勾选以下权限分配给该角色
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-pill">
            <span class="stat-pill-value">{{ enabledCount }}</span>
            <span class="stat-pill-label">已启用</span>
          </div>
          <div class="stat-pill stat-pill--total">
            <span class="stat-pill-value">{{ totalPermissions }}</span>
            <span class="stat-pill-label">总权限</span>
          </div>
        </div>
      </div>
    </template>

    <div class="permission-body">
      <div v-for="(group, gIdx) in permissionGroups" :key="group.group" class="perm-group" :style="{ animationDelay: gIdx * 80 + 'ms' }">
        <div class="group-header">
          <div class="group-title">
            <span class="group-indicator"></span>
            <span class="group-name">{{ group.group }}</span>
            <span class="group-count">{{ getGroupEnabledCount(group) }}/{{ group.permissions?.length || 0 }}</span>
          </div>
          <button
            class="select-all-btn"
            :class="{ active: isGroupAllSelected(group) }"
            @click="handleSelectAll(group)"
          >
            <span>{{ isGroupAllSelected(group) ? '取消全选' : '全选' }}</span>
          </button>
        </div>
        <div class="perm-items">
          <div
            v-for="(perm, pIdx) in group.permissions"
            :key="perm.code"
            class="perm-item"
            :class="{ active: permissions.includes(perm.code) }"
            :style="{ animationDelay: (gIdx * 80 + pIdx * 40) + 'ms' }"
            @click="handlePermissionToggle(perm.code)"
          >
            <div class="perm-check">
              <div class="check-box" :class="{ checked: permissions.includes(perm.code) }">
                <el-icon v-if="permissions.includes(perm.code)" :size="12" color="#fff"><Check /></el-icon>
              </div>
            </div>
            <div class="perm-info">
              <span class="perm-name">{{ perm.name }}</span>
              <span class="perm-code">{{ perm.code }}</span>
            </div>
            <div class="perm-switch-wrap">
              <el-switch
                :model-value="permissions.includes(perm.code)"
                active-color="#667eea"
                inactive-color="#d0d0d8"
                @change="handlePermissionChange(perm.code, $event)"
                @click.stop
              />
            </div>
          </div>
        </div>
      </div>

      <div v-if="permissionGroups.length === 0" class="modal-empty">
        <div class="empty-icon">
          <el-icon :size="40" color="#c0c0d0"><Setting /></el-icon>
        </div>
        <p>暂无可配置的权限组</p>
      </div>
    </div>

    <template #footer>
      <button class="btn-ghost-effect" @click="handleClose">取消</button>
      <button class="btn-create-effect" @click="handleSave">
        <el-icon><Check /></el-icon>
        <span>保存配置</span>
        <div class="btn-shine"></div>
      </button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Lock, Check, Setting } from '@element-plus/icons-vue'

const props = defineProps({
  role: {
    type: Object,
    required: true
  },
  permissionGroups: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'save'])

const visible = ref(true)
const permissions = ref([])

watch(() => props.role, (newRole) => {
  if (newRole) {
    permissions.value = [...(newRole.permissions || [])]
  }
}, { immediate: true })

const totalPermissions = computed(() => {
  return props.permissionGroups.reduce((sum, g) => sum + (g.permissions?.length || 0), 0)
})

const enabledCount = computed(() => permissions.value.length)

const getGroupEnabledCount = (group) => {
  return group.permissions.filter(p => permissions.value.includes(p.code)).length
}

const isGroupAllSelected = (group) => {
  const groupPerms = group.permissions.map(p => p.code)
  return groupPerms.length > 0 && groupPerms.every(code => permissions.value.includes(code))
}

const handlePermissionToggle = (code) => {
  if (permissions.value.includes(code)) {
    permissions.value = permissions.value.filter(c => c !== code)
  } else {
    permissions.value = [...permissions.value, code]
  }
}

const handlePermissionChange = (code, value) => {
  if (value) {
    if (!permissions.value.includes(code)) {
      permissions.value.push(code)
    }
  } else {
    const index = permissions.value.indexOf(code)
    if (index > -1) {
      permissions.value.splice(index, 1)
    }
  }
}

const handleSelectAll = (group) => {
  const groupPerms = group.permissions.map(p => p.code)
  const hasAll = groupPerms.every(code => permissions.value.includes(code))

  if (hasAll) {
    permissions.value = permissions.value.filter(code => !groupPerms.includes(code))
  } else {
    const newPerms = [...permissions.value]
    groupPerms.forEach(code => {
      if (!newPerms.includes(code)) {
        newPerms.push(code)
      }
    })
    permissions.value = newPerms
  }
}

const handleClose = () => {
  visible.value = false
  emit('close')
}

const handleSave = () => {
  emit('save', props.role.id, [...permissions.value])
}
</script>

<style scoped>
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
  padding: 0;
}

.custom-dialog :deep(.el-dialog__footer) {
  padding: 16px 28px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* ============ Dialog Header ============ */
.dialog-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 24px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.02), rgba(118, 75, 162, 0.02));
}

.dialog-header-icon {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
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

.role-highlight {
  color: #667eea;
  font-weight: 600;
}

.header-stats {
  margin-left: auto;
  display: flex;
  gap: 10px;
}

.stat-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 6px 14px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  border-radius: 10px;
}

.stat-pill-value {
  font-size: 18px;
  font-weight: 700;
  color: #667eea;
  font-variant-numeric: tabular-nums;
  line-height: 1;
}

.stat-pill-label {
  font-size: 11px;
  color: #8c8c9a;
  margin-top: 2px;
}

.stat-pill--total {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.04), rgba(0, 0, 0, 0.02));
}

.stat-pill--total .stat-pill-value {
  color: #5a5a6a;
}

/* ============ Permission Body ============ */
.permission-body {
  max-height: 520px;
  overflow-y: auto;
  padding: 20px 28px;
}

.permission-body::-webkit-scrollbar {
  width: 6px;
}

.permission-body::-webkit-scrollbar-track {
  background: transparent;
}

.permission-body::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.permission-body::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.2);
}

/* ============ Permission Group ============ */
.perm-group {
  margin-bottom: 18px;
  padding: 16px 18px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.6));
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 14px;
  animation: groupFadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) both;
}

@keyframes groupFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.perm-group:last-child {
  margin-bottom: 0;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.group-indicator {
  width: 4px;
  height: 18px;
  border-radius: 2px;
  background: linear-gradient(180deg, #667eea, #764ba2);
}

.group-name {
  font-weight: 600;
  color: #1a1a2e;
  font-size: 14px;
}

.group-count {
  font-size: 12px;
  color: #8c8c9a;
  font-variant-numeric: tabular-nums;
}

.select-all-btn {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.8);
  color: #667eea;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.select-all-btn:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.04);
}

.select-all-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border-color: transparent;
}

/* ============ Permission Items ============ */
.perm-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 8px;
}

.perm-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  animation: itemFadeIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) both;
}

@keyframes itemFadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.perm-item:hover {
  border-color: rgba(102, 126, 234, 0.3);
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.08);
}

.perm-item.active {
  border-color: rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.06), rgba(118, 75, 162, 0.04));
}

.perm-check {
  flex-shrink: 0;
}

.check-box {
  width: 18px;
  height: 18px;
  border: 1.5px solid rgba(0, 0, 0, 0.15);
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.check-box.checked {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: transparent;
}

.perm-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.perm-name {
  font-size: 13px;
  font-weight: 500;
  color: #2a2a3a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.perm-code {
  font-size: 11px;
  color: #b0b0c0;
  font-family: 'SF Mono', 'Monaco', monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.perm-switch-wrap {
  flex-shrink: 0;
}

.perm-switch-wrap :deep(.el-switch__core) {
  border-radius: 10px;
  height: 20px;
  min-width: 36px;
}

.perm-switch-wrap :deep(.el-switch__action) {
  width: 16px;
  height: 16px;
  top: 1px;
  left: 1px;
}

/* ============ Empty State ============ */
.modal-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #8c8c9a;
  font-size: 14px;
}

.empty-icon {
  margin-bottom: 12px;
}

/* ============ Buttons ============ */
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
}

.btn-ghost-effect:hover {
  border-color: #667eea;
  color: #667eea;
  background: rgba(102, 126, 234, 0.04);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.18);
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

.btn-create-effect:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(102, 126, 234, 0.5);
}

.btn-create-effect:active {
  transform: translateY(0);
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

/* ============ Responsive ============ */
@media (max-width: 768px) {
  .header-stats {
    display: none;
  }

  .perm-items {
    grid-template-columns: 1fr;
  }
}
</style>
