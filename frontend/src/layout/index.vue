<template>
  <div class="layout-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-row">
          <div class="logo-icon">
            <el-icon :size="28"><Cloudy /></el-icon>
          </div>
          <h2>成果云</h2>
        </div>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        router
        background-color="transparent"
        text-color="#555"
        active-text-color="#1677ff"
      >
        <el-menu-item v-if="userInfo.role === 'student'" index="/student/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>

        <el-menu-item v-if="userInfo.role !== 'student'" index="/dashboard">
          <el-icon><House /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>

        <el-menu-item v-if="userInfo.role === 'student'" index="/student/achievement">
          <el-icon><Document /></el-icon>
          <span>个人成果</span>
        </el-menu-item>

        <el-menu-item v-if="userInfo.role === 'student'" index="/student/submit">
          <el-icon><Plus /></el-icon>
          <span>录入成果</span>
        </el-menu-item>

        <el-menu-item v-if="userInfo.role === 'student'" index="/student/courses">
          <el-icon><FolderOpened /></el-icon>
          <span>加入课程</span>
        </el-menu-item>

        <el-menu-item v-if="showAchievementMenu" index="/dashboard/achievements">
          <el-icon><Document /></el-icon>
          <span>成果管理</span>
        </el-menu-item>

        <el-menu-item v-if="showClassMenu" index="/dashboard/classes">
          <el-icon><OfficeBuilding /></el-icon>
          <span>课程管理</span>
        </el-menu-item>

        <el-menu-item v-if="showStudentMenu" index="/dashboard/students">
          <el-icon><User /></el-icon>
          <span>学生管理</span>
        </el-menu-item>

        <el-menu-item v-if="showTeamMenu" index="/dashboard/team-management">
          <el-icon><UserFilled /></el-icon>
          <span>团队管理</span>
        </el-menu-item>

        <el-menu-item v-if="userInfo.role === 'teacher'" index="/dashboard/courses">
          <el-icon><FolderOpened /></el-icon>
          <span>我的课程</span>
        </el-menu-item>

        <el-menu-item v-if="showTeacherMenu" index="/dashboard/teachers">
          <el-icon><UserFilled /></el-icon>
          <span>教师管理</span>
        </el-menu-item>

        <el-menu-item v-if="userInfo.role === 'admin'" index="/dashboard/permission">
          <el-icon><Lock /></el-icon>
          <span>权限管理</span>
        </el-menu-item>

        <el-menu-item v-if="userInfo.role !== 'student'" index="/dashboard/stats">
          <el-icon><TrendCharts /></el-icon>
          <span>统计报表</span>
        </el-menu-item>

        <el-menu-item v-if="showProfileMenu" :index="userInfo.role === 'student' ? '/student/center' : '/dashboard/profile'">
          <el-icon><UserFilled /></el-icon>
          <span>个人中心</span>
        </el-menu-item>

        <el-menu-item v-if="showSettingsMenu" index="/dashboard/settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>

        <el-menu-item v-if="showSettingsMenu" index="/dashboard/logs">
          <el-icon><DocumentChecked /></el-icon>
          <span>系统日志</span>
        </el-menu-item>

        <el-menu-item v-if="showSettingsMenu" index="/dashboard/backup">
          <el-icon><FolderChecked /></el-icon>
          <span>数据备份</span>
        </el-menu-item>
      </el-menu>
    </aside>
    <div class="main-content">
      <header class="top-header">
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item v-for="item in breadcrumbItems" :key="item.path" :to="item.path">
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="user-info">
          <span>{{ userInfo.name }}</span>
          <el-tag type="info" size="small">{{ roleText }}</el-tag>
          <el-popover
            v-if="userInfo.role !== 'admin'"
            placement="bottom-end"
            :width="360"
            trigger="click"
            popper-class="notification-popper"
          >
            <template #reference>
              <div class="notification-trigger">
                <el-icon :size="19"><Bell /></el-icon>
                <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
              </div>
            </template>
            <div class="notification-panel">
              <div class="notification-header">
                <span class="notification-title">消息通知</span>
                <el-button v-if="unreadCount > 0" link type="primary" size="small" @click="readAll">全部已读</el-button>
              </div>
              <div class="notification-list">
                <div v-if="notifications.length === 0" class="notification-empty">暂无消息</div>
                <div
                  v-for="item in notifications"
                  :key="item.id"
                  class="notification-item"
                  :class="{ 'is-unread': !item.is_read }"
                  @click="markRead(item)"
                >
                  <div class="notification-item-title">
                    <span class="notification-item-name">{{ item.title }}</span>
                    <span v-if="!item.is_read" class="notification-dot"></span>
                  </div>
                  <div v-if="item.content" class="notification-item-content">{{ item.content }}</div>
                  <div class="notification-item-time">{{ item.created_at }}</div>
                </div>
              </div>
            </div>
          </el-popover>
          <el-button link @click="logout">
            <el-icon><SwitchButton /></el-icon>
            退出
          </el-button>
        </div>
      </header>
      <main class="content-area" :class="{ 'no-top-padding': route.path.startsWith('/home') }">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { House, Document, Plus, OfficeBuilding, User, TrendCharts, SwitchButton, UserFilled, Setting, HomeFilled, FolderOpened, Lock, Cloudy, DocumentChecked, FolderChecked, Bell } from '@element-plus/icons-vue'
import { getUserInfo, removeToken, removeUserInfo, setUserInfo } from '@/utils/auth'
import { authApi, notificationApi } from '@/api'
import permission from '@/utils/permission'
import { normalizeRole, roleCodeToName } from '@/utils/role'

const route = useRoute()
const router = useRouter()
const userInfo = ref(getUserInfo() || {})

const notifications = ref([])
const unreadCount = ref(0)

const loadNotifications = async () => {
  try {
    const res = await notificationApi.list({ page: 1, page_size: 20 })
    const data = res.data
    if (Array.isArray(data.notifications)) {
      notifications.value = data.notifications
    }
    if (typeof data.unread_count === 'number') {
      unreadCount.value = data.unread_count
    }
  } catch (error) {
    console.error('加载消息通知失败:', error)
  }
}

const markRead = async (item) => {
  try {
    if (!item.is_read) {
      await notificationApi.markRead(item.id)
      item.is_read = true
      if (unreadCount.value > 0) unreadCount.value -= 1
      loadNotifications()
    }
  } catch (error) {
    console.error('标记已读失败:', error)
  }
}

const readAll = async () => {
  try {
    await notificationApi.readAll()
    notifications.value = notifications.value.map(n => ({ ...n, is_read: true }))
    unreadCount.value = 0
  } catch (error) {
    console.error('全部已读失败:', error)
  }
}

const refreshUserInfo = async () => {
  try {
    const res = await authApi.getMe()
    if (res.user) {
      setUserInfo(res.user)
      userInfo.value = res.user
    }
  } catch (error) {
    console.error('刷新用户信息失败:', error)
  }
}

onMounted(() => {
  refreshUserInfo()
  if (userInfo.value.role !== 'admin') {
    loadNotifications()
  }

  window.addEventListener('userInfoUpdated', () => {
    refreshUserInfo()
  })
})

const activeMenu = computed(() => route.path)

const breadcrumbItems = computed(() => {
  const items = []
  const role = userInfo.value?.role
  
  if (route.path === '/dashboard/profile') {
    if (role === 'student') {
      items.push({ path: '/home', title: '首页' })
    }
    items.push({ path: '/dashboard/profile', title: '个人中心' })
  } else if (route.path === '/dashboard') {
    items.push({ path: '/dashboard', title: '仪表盘' })
  } else {
    const matched = route.matched
    matched.forEach(item => {
      if (item.meta.title) {
        items.push({
          path: item.path,
          title: item.meta.title
        })
      }
    })
  }
  return items
})

const currentRole = computed(() => {
  if (userInfo.value.role === 'teacher' && userInfo.value.teacher_role) {
    return normalizeRole(userInfo.value.teacher_role)
  }
  return normalizeRole(userInfo.value.role)
})

const roleText = computed(() => {
  const role = currentRole.value
  return roleCodeToName(role)
})

const showAchievementMenu = computed(() => {
  const role = currentRole.value
  if (role === 'admin') return true
  return permission.hasPermission('achievement:view') || permission.hasPermission('achievement:audit')
})

const showClassMenu = computed(() => {
  const role = currentRole.value
  if (role === 'admin') return true
  return permission.hasPermission('course:create') || permission.hasPermission('course:edit') || permission.hasPermission('course:delete')
})

const showStudentMenu = computed(() => {
  const role = currentRole.value
  if (role === 'admin') return true
  return permission.hasPermission('student:add') || permission.hasPermission('student:delete') || permission.hasPermission('student:reset_pwd')
})

const showTeamMenu = computed(() => {
  const role = currentRole.value
  if (role === 'admin') return true
  return permission.hasPermission('team:create') || permission.hasPermission('team:delete') || permission.hasPermission('team:remove_member')
})

const showTeacherMenu = computed(() => {
  const role = currentRole.value
  if (role === 'admin') {
    return true
  }
  if (['head', 'advisor', 'faculty', 'teaching_admin'].includes(role)) {
    return permission.hasPermission('teacher:add') || permission.hasPermission('teacher:edit')
  }
  return false
})

const showSettingsMenu = computed(() => {
  const role = currentRole.value
  return ['admin'].includes(role)
})

const showProfileMenu = computed(() => {
  const role = currentRole.value
  return ['teacher', 'head', 'advisor', 'faculty', 'student', 'teaching_admin'].includes(role)
})

const logout = () => {
  ElMessageBox.confirm('确定退出登录？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    removeToken()
    removeUserInfo()
    ElMessage.success('退出成功')
    router.push('/login')
  })
}
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #dceeff 0%, #ffffff 100%);
}

.sidebar {
  width: 220px;
  background: #fff;
  color: #333;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e8ecf0;
}

.sidebar-header {
  padding: 12px 20px;
  text-align: center;
  background: linear-gradient(135deg, #1677ff 0%, #4096ff 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(22, 119, 255, 0.15);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background: transparent;
  padding-top: 12px;
}

:deep(.el-menu-item) {
  margin: 4px 12px;
  border-radius: 6px;
  height: 42px;
  line-height: 42px;
  position: relative;
  transition: all 0.3s ease;
}

:deep(.el-menu-item:hover) {
  background: rgba(22, 119, 255, 0.06);
  color: #1677ff;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, rgba(22, 119, 255, 0.25) 0%, rgba(64, 150, 255, 0.18) 100%);
  color: #1677ff;
  border-left: 4px solid #1677ff;
}



.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e8ecf0;
}

.breadcrumb {
  font-size: 14px;
}

:deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: #1677ff;
  font-weight: 500;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info span:first-child {
  font-size: 14px;
  font-weight: 500;
}

.notification-trigger {
  position: relative;
  display: flex;
  align-items: center;
  padding: 6px;
  border-radius: 8px;
  cursor: pointer;
  color: #555;
  transition: all 0.25s ease;
}

.notification-trigger:hover {
  color: #1677ff;
  background: rgba(22, 119, 255, 0.08);
}

.notification-badge {
  position: absolute;
  top: -2px;
  right: -4px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  line-height: 16px;
  text-align: center;
  font-size: 11px;
  border-radius: 8px;
  background: #f5222d;
  color: #fff;
  box-shadow: 0 0 0 2px #fff;
}

.notification-panel {
  display: flex;
  flex-direction: column;
}

.notification-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 4px 10px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 6px;
}

.notification-title {
  font-size: 15px;
  font-weight: 600;
}

.notification-list {
  max-height: 320px;
  overflow-y: auto;
}

.notification-empty {
  padding: 30px 0;
  text-align: center;
  color: #999;
  font-size: 13px;
}

.notification-item {
  padding: 10px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.notification-item:hover {
  background: rgba(22, 119, 255, 0.05);
}

.notification-item.is-unread {
  background: rgba(22, 119, 255, 0.06);
}

.notification-item.is-unread:hover {
  background: rgba(22, 119, 255, 0.10);
}

.notification-item-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
}

.notification-item.is-unread .notification-item-name {
  font-weight: 600;
  color: #1677ff;
}

.notification-item-time {
  margin-top: 4px;
  font-size: 12px;
  color: #999;
}

.notification-item-content {
  margin-top: 2px;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

.notification-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #f5222d;
  flex-shrink: 0;
}

.content-area {
  flex: 1;
  padding: 24px;
  overflow: auto;
}

.content-area.no-top-padding {
  padding-top: 0;
}
</style>