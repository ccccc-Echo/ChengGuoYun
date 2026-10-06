<template>
  <div class="login-container">
    <!-- 左侧品牌区 -->
    <div class="brand-panel">
      <div class="brand-content">
        <div class="logo-box">
          <el-icon :size="48"><Document /></el-icon>
        </div>
        <h1 class="brand-title">成果云</h1>
        <p class="brand-slogan">记录你的每一份成就</p>
        <div class="brand-line"></div>
        <p class="brand-desc">成果云系统</p>
      </div>
    </div>

    <!-- 右侧表单区 -->
    <div class="form-panel">
      <div class="form-wrapper">
        <h2 class="form-title">欢迎登录</h2>
        <p class="form-subtitle">请输入您的账号信息</p>

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
  display: flex;
  width: 100vw;
  height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #f5f7fa;
}

/* ========== 左侧品牌区 ========== */
.brand-panel {
  flex: 0 0 42%;
  background: linear-gradient(160deg, #1a6bc4 0%, #4095e5 40%, #5ba8f5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.brand-panel::before {
  content: '';
  position: absolute;
  top: -60%;
  right: -30%;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
}

.brand-panel::after {
  content: '';
  position: absolute;
  bottom: -40%;
  left: -20%;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.04);
}

.brand-content {
  text-align: center;
  color: #fff;
  position: relative;
  z-index: 1;
}

.logo-box {
  width: 88px;
  height: 88px;
  margin: 0 auto 32px;
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.brand-title {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 12px;
  letter-spacing: 4px;
}

.brand-slogan {
  font-size: 18px;
  font-weight: 300;
  opacity: 0.9;
  margin: 0 0 40px;
  letter-spacing: 2px;
}

.brand-line {
  width: 60px;
  height: 3px;
  background: rgba(255, 255, 255, 0.5);
  margin: 0 auto 20px;
}

.brand-desc {
  font-size: 14px;
  opacity: 0.7;
  margin: 0;
  letter-spacing: 1px;
}

/* ========== 右侧表单区 ========== */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
}

.form-wrapper {
  width: 400px;
  padding: 40px 0;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px;
}

.form-subtitle {
  font-size: 14px;
  color: #999;
  margin: 0 0 40px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 24px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 0;
  border: none;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: none;
  background: transparent;
  padding: 0 0 0 4px;
  transition: border-color 0.3s;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-bottom-color: #4095e5;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-bottom-color: #4095e5;
  border-bottom-width: 2px;
  box-shadow: none;
}

.login-form :deep(.el-input__inner) {
  height: 44px;
  line-height: 44px;
  font-size: 15px;
}

.login-form :deep(.el-input__prefix) {
  color: #aaa;
}

.form-extra {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.forgot-link {
  font-size: 13px;
  color: #4095e5;
  text-decoration: none;
}

.forgot-link:hover {
  color: #2a85d1;
}

.login-btn {
  width: 100%;
  height: 48px;
  border-radius: 0;
  background: #4095e5;
  border: none;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 4px;
  transition: all 0.3s;
}

.login-btn:hover {
  background: #2a85d1;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 149, 229, 0.3);
}

.register-tip {
  text-align: center;
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
}

.register-link:hover {
  color: #2a85d1;
  text-decoration: underline;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .brand-panel {
    display: none;
  }
  .form-panel {
    padding: 40px;
  }
  .form-wrapper {
    width: 100%;
  }
}
</style>