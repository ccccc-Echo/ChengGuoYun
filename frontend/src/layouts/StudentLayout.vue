<template>
  <div class="student-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-row">
          <div class="logo-icon">
            <el-icon :size="28"><Cloudy /></el-icon>
          </div>
          <div class="logo-text">
            <h2>成果云</h2>
            <p>学生中心</p>
          </div>
        </div>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        router
        background-color="transparent"
        text-color="#555"
        active-text-color="#4095e5"
      >
        <el-menu-item index="/student/home">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>

        <el-menu-item index="/student/dashboard">
          <el-icon><Odometer /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>

        <el-menu-item index="/student/achievement">
          <el-icon><Document /></el-icon>
          <span>个人成果</span>
        </el-menu-item>

        <el-menu-item index="/student/submit">
          <el-icon><Plus /></el-icon>
          <span>录入成果</span>
        </el-menu-item>

        <el-menu-item index="/student/courses">
          <el-icon><FolderOpened /></el-icon>
          <span>加入课程</span>
        </el-menu-item>

        <el-menu-item index="/student/center">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
      </el-menu>
    </aside>
    <div class="main-content">
      <header class="top-header">
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item v-for="item in breadcrumbItems" :key="item.path">
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="user-info">
          <span class="user-name">{{ userInfo.name }}</span>
          <el-tag type="success" size="small">学生</el-tag>
          <el-popover
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
      <main class="content-area">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { House, Document, Plus, FolderOpened, User, SwitchButton, Cloudy, Bell, Odometer } from '@element-plus/icons-vue'
import { getUserInfo, removeToken, removeUserInfo, setUserInfo } from '@/utils/auth'
import { authApi, notificationApi } from '@/api'

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
  loadNotifications()
  window.addEventListener('userInfoUpdated', refreshUserInfo)
})

const activeMenu = computed(() => route.path)

const breadcrumbItems = computed(() => {
  const items = []
  const matched = route.matched
  matched.forEach(item => {
    if (item.meta && item.meta.title && item.path !== '/student') {
      items.push({ title: item.meta.title })
    }
  })
  // 确保面包屑至少有一项
  if (items.length === 0) {
    items.push({ title: '首页' })
  }
  return items
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
.student-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #e8f4fd 0%, #ffffff 100%);
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
  background: linear-gradient(135deg, #4095e5 0%, #5ba8f5 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(64, 149, 229, 0.15);
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

.logo-text {
  text-align: left;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  line-height: 1.2;
}

.sidebar-header p {
  margin: 1px 0 0;
  font-size: 11px;
  opacity: 0.85;
  letter-spacing: 0.5px;
  line-height: 1.1;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background: transparent;
  padding-top: 12px;
}

:deep(.el-menu-item) {
  margin: 4px 12px;
  border-radius: 8px;
  height: 44px;
  line-height: 44px;
  transition: all 0.3s ease;
}

:deep(.el-menu-item:hover) {
  background: rgba(64, 149, 229, 0.06);
  color: #4095e5;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, rgba(64, 149, 229, 0.2) 0%, rgba(91, 168, 245, 0.12) 100%);
  color: #4095e5;
  border-left: 4px solid #4095e5;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
  overflow: hidden;
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
  color: #4095e5;
  font-weight: 500;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
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
  color: #4095e5;
  background: rgba(64, 149, 229, 0.08);
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
  background: rgba(64, 149, 229, 0.05);
}

.notification-item.is-unread {
  background: rgba(64, 149, 229, 0.06);
}

.notification-item.is-unread:hover {
  background: rgba(64, 149, 229, 0.1);
}

.notification-item-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
}

.notification-item.is-unread .notification-item-name {
  font-weight: 600;
  color: #4095e5;
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
  overflow-y: auto;
}

/* 页面切换过渡动画 */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
