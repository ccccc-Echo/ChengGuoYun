<template>
  <div class="login-container">
    <!-- 顶部装饰条 -->
    <div class="top-accent"></div>

    <!-- 主卡片 -->
    <div class="login-card">
      <!-- 左侧插图区 -->
      <div class="card-illustration">
        <div class="illustration-bg">
          <div class="illu-circle illu-c1"></div>
          <div class="illu-circle illu-c2"></div>
          <div class="illu-circle illu-c3"></div>
        </div>
        <div class="illustration-content">
          <div class="illu-icon">
            <el-icon :size="52"><Document /></el-icon>
          </div>
          <h2 class="illu-title">成果云</h2>
          <p class="illu-desc">记录成长 · 见证卓越</p>
        </div>
      </div>

      <!-- 右侧表单区 -->
      <div class="card-form">
        <h3 class="form-title">欢迎回来</h3>
        <p class="form-subtitle">登录您的账户以继续</p>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="学号 / 用户名"
              size="large"
              clearable
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="密码"
              size="large"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
              <template #suffix>
                <el-icon
                  class="toggle-pwd"
                  @click="showPassword = !showPassword"
                >
                  <component :is="showPassword ? 'View' : 'Hide'" />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <div class="form-extra">
            <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
            <a href="#" class="forgot-link">忘记密码？</a>
          </div>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-btn"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-tip">
          <span>还没有账号？</span>
          <button type="button" class="register-link" @click="goToRegister">立即注册</button>
        </div>
      </div>
    </div>

    <!-- 底部版权 -->
    <p class="footer-text">© 2024 成果云系统</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Document, View, Hide } from '@element-plus/icons-vue'
import { authApi } from '@/api'
import { setToken, setUserInfo } from '@/utils/auth'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const showPassword = ref(false)

const loginForm = ref({
  username: '',
  password: '',
  remember: false
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const goToRegister = () => {
  router.push('/register/identity')
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  try {
    await loginFormRef.value.validate()
    loading.value = true
    const res = await authApi.login({
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    if (res.access_token && res.user) {
      setToken(res.access_token)
      setUserInfo(res.user)
      ElMessage.success('登录成功')
      const role = res.user.role || ''
      const teacherRole = res.user.teacher_role || ''
      let redirectPath = '/dashboard'
      if (role === 'admin') {
        redirectPath = '/dashboard'
      } else if (role === 'teacher') {
        const teacherRedirectMap = {
          head: '/dashboard/classes',
          advisor: '/dashboard/students',
          faculty: '/dashboard/achievements',
          teaching_admin: '/dashboard/students'
        }
        redirectPath = teacherRedirectMap[teacherRole] || '/dashboard'
      } else if (role === 'student') {
        redirectPath = '/student/dashboard'
      }
      router.push(redirectPath)
    } else {
      ElMessage.error('登录失败，未获取到 token 或用户信息')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error(error.message || '登录失败')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #eef3f8;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  position: relative;
  overflow: hidden;
}

/* ========== 顶部装饰条 ========== */
.top-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4095e5, #5ba8f5, #4095e5);
}

/* ========== 主卡片 ========== */
.login-card {
  display: flex;
  width: 880px;
  min-height: 520px;
  background: #fff;
  border-radius: 16px;
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.04),
    0 16px 40px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  position: relative;
  z-index: 1;
}

/* ========== 左侧插图区 ========== */
.card-illustration {
  flex: 0 0 380px;
  background: linear-gradient(160deg, #e8f4fd 0%, #f0f7ff 50%, #e3effb 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.illustration-bg {
  position: absolute;
  inset: 0;
}

.illu-circle {
  position: absolute;
  border-radius: 50%;
}

.illu-c1 {
  width: 200px;
  height: 200px;
  background: rgba(64, 149, 229, 0.08);
  top: -60px;
  right: -40px;
}

.illu-c2 {
  width: 160px;
  height: 160px;
  background: rgba(64, 149, 229, 0.06);
  bottom: -40px;
  left: -30px;
}

.illu-c3 {
  width: 100px;
  height: 100px;
  background: rgba(64, 149, 229, 0.1);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.illustration-content {
  text-align: center;
  position: relative;
  z-index: 1;
}

.illu-icon {
  width: 96px;
  height: 96px;
  margin: 0 auto 24px;
  background: #fff;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4095e5;
  box-shadow: 0 8px 32px rgba(64, 149, 229, 0.12);
}

.illu-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 12px;
  letter-spacing: 2px;
}

.illu-desc {
  font-size: 14px;
  color: #888;
  margin: 0;
  letter-spacing: 1px;
}

/* ========== 右侧表单区 ========== */
.card-form {
  flex: 1;
  padding: 56px 52px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 6px;
}

.form-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0 0 36px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 22px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  background: #f7f8fa;
  border: 1px solid transparent;
  box-shadow: none;
  padding: 2px 14px;
  transition: all 0.3s;
}

.login-form :deep(.el-input__wrapper:hover) {
  background: #f0f2f5;
  border-color: #e0e3e8;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  border-color: #4095e5;
  box-shadow: 0 0 0 3px rgba(64, 149, 229, 0.08);
}

.login-form :deep(.el-input__inner) {
  height: 44px;
  line-height: 44px;
  font-size: 15px;
  color: #333;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: #bbb;
}

.login-form :deep(.el-input__prefix) {
  color: #bbb;
}

.form-extra {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.forgot-link {
  font-size: 13px;
  color: #4095e5;
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-link:hover {
  color: #2a85d1;
}

.login-btn {
  width: 100%;
  height: 48px;
  border-radius: 10px;
  background: #4095e5;
  border: none;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  color: #fff;
  transition: all 0.3s;
}

.login-btn:hover {
  background: #357abd;
  box-shadow: 0 6px 20px rgba(64, 149, 229, 0.3);
  transform: translateY(-1px);
}

.register-tip {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #999;
}

.register-link {
  color: #4095e5;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-left: 4px;
  padding: 0;
  transition: color 0.3s;
}

.register-link:hover {
  color: #2a85d1;
}

/* ========== 底部版权 ========== */
.footer-text {
  margin-top: 32px;
  font-size: 12px;
  color: #bbb;
  position: relative;
  z-index: 1;
}

/* ========== 响应式 ========== */
@media (max-width: 920px) {
  .login-card {
    width: 94%;
    flex-direction: column;
  }
  .card-illustration {
    flex: 0 0 auto;
    padding: 40px 0;
  }
  .card-form {
    padding: 36px 32px 40px;
  }
}
</style>