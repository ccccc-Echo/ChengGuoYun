<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-circle bg-circle-1"></div>
      <div class="bg-circle bg-circle-2"></div>
      <div class="bg-circle bg-circle-3"></div>
    </div>

    <!-- 毛玻璃卡片 -->
    <div class="glass-card">
      <div class="card-icon">
        <el-icon :size="36"><Document /></el-icon>
      </div>
      <h1 class="card-title">成果云</h1>
      <p class="card-subtitle">成果云系统</p>

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
          <el-checkbox v-model="loginForm.remember" class="remember-check">
            <span class="remember-text">记住我</span>
          </el-checkbox>
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
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0c1929 0%, #152238 30%, #1a3a5c 60%, #0f2847 100%);
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  position: relative;
  overflow: hidden;
}

/* ========== 背景装饰圆 ========== */
.bg-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.06;
}

.bg-circle-1 {
  width: 600px;
  height: 600px;
  background: #4095e5;
  top: -200px;
  right: -150px;
  animation: float1 20s ease-in-out infinite;
}

.bg-circle-2 {
  width: 400px;
  height: 400px;
  background: #e6a23c;
  bottom: -150px;
  left: -100px;
  animation: float2 25s ease-in-out infinite;
}

.bg-circle-3 {
  width: 300px;
  height: 300px;
  background: #4095e5;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: float3 18s ease-in-out infinite;
}

@keyframes float1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-30px, 30px) scale(1.05); }
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -20px) scale(1.08); }
}

@keyframes float3 {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.1); }
}

/* ========== 毛玻璃卡片 ========== */
.glass-card {
  width: 440px;
  padding: 48px 44px 40px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
  text-align: center;
}

.card-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, #4095e5, #2a85d1);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 8px 24px rgba(64, 149, 229, 0.35);
}

.card-title {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px;
  letter-spacing: 3px;
}

.card-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.55);
  margin: 0 0 36px;
  letter-spacing: 1px;
}

/* ========== 表单 ========== */
.login-form :deep(.el-form-item) {
  margin-bottom: 22px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: none;
  transition: all 0.3s;
  padding: 2px 12px;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.12);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(64, 149, 229, 0.6);
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0 0 3px rgba(64, 149, 229, 0.15);
}

.login-form :deep(.el-input__inner) {
  height: 44px;
  line-height: 44px;
  color: #fff;
  font-size: 15px;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.35);
}

.login-form :deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.4);
}

.login-form :deep(.el-input__suffix) {
  color: rgba(255, 255, 255, 0.4);
}

.form-extra {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.remember-check {
  --el-checkbox-checked-bg-color: #4095e5;
  --el-checkbox-checked-input-border-color: #4095e5;
}

.remember-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
}

.forgot-link {
  font-size: 13px;
  color: #e6a23c;
  text-decoration: none;
  transition: color 0.3s;
}

.forgot-link:hover {
  color: #f0b84c;
}

.login-btn {
  width: 100%;
  height: 48px;
  border-radius: 10px;
  background: linear-gradient(135deg, #4095e5, #2a85d1);
  border: none;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  color: #fff;
  transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(64, 149, 229, 0.3);
}

.login-btn:hover {
  background: linear-gradient(135deg, #5ba8f5, #4095e5);
  box-shadow: 0 6px 24px rgba(64, 149, 229, 0.5);
  transform: translateY(-1px);
}

.register-tip {
  margin-top: 24px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.45);
}

.register-link {
  color: #e6a23c;
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
  color: #f0b84c;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .glass-card {
    width: 92%;
    padding: 36px 28px 32px;
  }
}
</style>