<template>
  <div class="login-container">
    <!-- 左侧装饰区 -->
    <div class="hero-panel">
      <div class="hero-bg">
        <div class="dot dot-1"></div>
        <div class="dot dot-2"></div>
        <div class="dot dot-3"></div>
        <div class="dot dot-4"></div>
        <div class="dot dot-5"></div>
        <div class="dot dot-6"></div>
      </div>
      <div class="hero-content">
        <div class="hero-icon">
          <el-icon :size="44"><Document /></el-icon>
        </div>
        <h1 class="hero-title">成果云</h1>
        <p class="hero-desc">成果云系统</p>
        <div class="hero-divider"></div>
        <p class="hero-tagline">记录每一份努力，见证每一次成长</p>
      </div>
    </div>

    <!-- 右侧重置密码卡片 -->
    <div class="form-panel">
      <div class="login-card">
        <div class="card-accent"></div>

        <div class="card-header">
          <div class="card-badge">
            <span class="badge-dot"></span>
            <span>找回密码</span>
          </div>
          <h2 class="card-title">忘记密码</h2>
          <p class="card-subtitle">通过邮箱或手机号重置您的密码</p>
          <div class="card-divider"></div>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          class="login-form"
        >
          <div class="field-group">
            <label class="field-label">
              <el-icon class="label-icon"><Message /></el-icon>
              <span>邮箱 / 手机号</span>
            </label>
            <el-form-item prop="account">
              <el-input
                v-model="form.account"
                placeholder="请输入邮箱或手机号"
                size="large"
                clearable
              />
            </el-form-item>
          </div>

          <div class="field-group">
            <label class="field-label">
              <el-icon class="label-icon"><Key /></el-icon>
              <span>验证码</span>
            </label>
            <el-form-item prop="code">
              <div class="code-row">
                <el-input
                  v-model="form.code"
                  placeholder="请输入验证码"
                  size="large"
                />
                <el-button
                  class="code-btn"
                  size="large"
                  @click="handleSendCode"
                >获取验证码</el-button>
              </div>
            </el-form-item>
          </div>

          <div class="field-group">
            <label class="field-label">
              <el-icon class="label-icon"><Lock /></el-icon>
              <span>新密码</span>
            </label>
            <el-form-item prop="newPassword">
              <el-input
                v-model="form.newPassword"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入新密码"
                size="large"
              >
                <template #suffix>
                  <span class="toggle-pwd" @click="showPassword = !showPassword">
                    <el-icon><component :is="showPassword ? 'View' : 'Hide'" /></el-icon>
                  </span>
                </template>
              </el-input>
            </el-form-item>
          </div>

          <div class="field-group">
            <label class="field-label">
              <el-icon class="label-icon"><Lock /></el-icon>
              <span>确认新密码</span>
            </label>
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="form.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                size="large"
              />
            </el-form-item>
          </div>

          <el-button
            type="primary"
            size="large"
            class="login-btn"
            @click="handleReset"
          >
            <span class="btn-text">重置密码</span>
            <el-icon class="btn-arrow"><Check /></el-icon>
          </el-button>
        </el-form>

        <div class="register-tip">
          <a href="javascript:void(0)" class="register-link" @click="goBack">返回登录</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, Message, Key, Lock, View, Hide, Check } from '@element-plus/icons-vue'

const router = useRouter()
const formRef = ref(null)
const showPassword = ref(false)

const form = ref({
  account: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const rules = {
  account: [
    { required: true, message: '请输入邮箱或手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const goBack = () => {
  router.push('/login')
}

const handleSendCode = () => {
  ElMessage.info('功能开发中')
}

const handleReset = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    ElMessage.info('功能开发中')
  } catch (e) {
    // 校验失败，无需额外处理
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #eef4fb;
}

/* ========== 左侧装饰区 ========== */
.hero-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(160deg, #dceeff 0%, #e8f4fd 40%, #f0f7ff 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.dot {
  position: absolute;
  border-radius: 50%;
  background: #4095e5;
  opacity: 0.08;
}

.dot-1 {
  width: 300px;
  height: 300px;
  top: -80px;
  left: -60px;
}

.dot-2 {
  width: 180px;
  height: 180px;
  top: 20%;
  right: 10%;
  opacity: 0.06;
}

.dot-3 {
  width: 120px;
  height: 120px;
  bottom: 15%;
  left: 20%;
  opacity: 0.1;
}

.dot-4 {
  width: 80px;
  height: 80px;
  top: 50%;
  left: 40%;
  opacity: 0.05;
}

.dot-5 {
  width: 200px;
  height: 200px;
  bottom: -60px;
  right: -40px;
  opacity: 0.07;
}

.dot-6 {
  width: 60px;
  height: 60px;
  top: 30%;
  left: 15%;
  opacity: 0.09;
}

.hero-content {
  text-align: center;
  position: relative;
  z-index: 1;
}

.hero-icon {
  width: 88px;
  height: 88px;
  margin: 0 auto 28px;
  background: #fff;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4095e5;
  box-shadow: 0 4px 20px rgba(64, 149, 229, 0.1);
}

.hero-title {
  font-size: 36px;
  font-weight: 700;
  color: #1a2a3a;
  margin: 0 0 8px;
  letter-spacing: 3px;
}

.hero-desc {
  font-size: 15px;
  color: #7a8b9e;
  margin: 0;
  letter-spacing: 1px;
}

.hero-divider {
  width: 40px;
  height: 3px;
  background: #4095e5;
  border-radius: 2px;
  margin: 24px auto;
  opacity: 0.5;
}

.hero-tagline {
  font-size: 14px;
  color: #a0b0c0;
  margin: 0;
  letter-spacing: 1px;
}

/* ========== 右侧表单区 ========== */
.form-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 80px;
  background: transparent;
}

.login-card {
  position: relative;
  width: 430px;
  background: #fff;
  border-radius: 24px;
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.03),
    0 2px 6px rgba(0, 0, 0, 0.02),
    0 8px 24px rgba(64, 149, 229, 0.05),
    0 24px 56px rgba(64, 149, 229, 0.09);
  overflow: hidden;
}

.card-accent {
  height: 3px;
  background: linear-gradient(90deg, #4095e5, #6db3f2, #a0d2ff, #6db3f2, #4095e5);
  background-size: 200% 100%;
  animation: accentShimmer 4s ease-in-out infinite;
}

@keyframes accentShimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* ========== 卡片头部 ========== */
.card-header {
  padding: 36px 44px 0;
  text-align: center;
}

.card-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 16px;
  background: linear-gradient(135deg, #eef6ff, #e3f0ff);
  border: 1px solid rgba(64, 149, 229, 0.12);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #4095e5;
  letter-spacing: 0.5px;
  margin-bottom: 20px;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #4095e5;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

.card-title {
  font-size: 26px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 6px;
  letter-spacing: -0.3px;
}

.card-subtitle {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}

.card-divider {
  width: 32px;
  height: 3px;
  background: #4095e5;
  border-radius: 2px;
  margin: 20px auto 0;
  opacity: 0.4;
}

/* ========== 表单 ========== */
.login-form {
  padding: 28px 44px 0;
}

.field-group {
  margin-bottom: 2px;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
  letter-spacing: 0.2px;
}

.label-icon {
  font-size: 14px;
  color: #4095e5;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 18px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 12px;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  box-shadow: none;
  padding: 2px 14px;
  transition: all 0.2s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  border-color: #4095e5;
  box-shadow:
    0 0 0 1px #4095e5,
    0 0 0 4px rgba(64, 149, 229, 0.08),
    0 2px 8px rgba(64, 149, 229, 0.06);
}

.login-form :deep(.el-input__inner) {
  height: 46px;
  line-height: 46px;
  font-size: 14px;
  color: #111827;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: #c4c8cf;
  font-size: 13px;
}

.login-form :deep(.el-input__suffix) {
  color: #9ca3af;
}

.toggle-pwd {
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #9ca3af;
  transition: color 0.2s;
}

.toggle-pwd:hover {
  color: #4095e5;
}

.code-row {
  display: flex;
  gap: 10px;
}

.code-row :deep(.el-input) {
  flex: 1;
}

.code-btn {
  width: 108px;
  flex-shrink: 0;
  border-radius: 12px;
  background: linear-gradient(135deg, #4095e5, #2563eb);
  border: none;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s;
}

.code-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(64, 149, 229, 0.3);
}

.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 50px;
  border-radius: 14px;
  background: linear-gradient(135deg, #4095e5, #2563eb);
  border: none;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #fff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    0 2px 8px rgba(64, 149, 229, 0.25),
    0 0 0 0 rgba(64, 149, 229, 0);
}

.btn-arrow {
  font-size: 18px;
  transition: transform 0.3s;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow:
    0 6px 20px rgba(64, 149, 229, 0.35),
    0 0 0 4px rgba(64, 149, 229, 0.08);
}

.login-btn:hover .btn-arrow {
  transform: translateX(3px);
}

.login-btn:active {
  transform: translateY(0);
}

.register-tip {
  text-align: center;
  padding: 24px 44px 32px;
  font-size: 14px;
  color: #9ca3af;
}

.register-link {
  color: #4095e5;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin-left: 4px;
  padding: 0;
  text-decoration: none;
  transition: color 0.2s;
}

.register-link:hover {
  color: #2563eb;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .hero-panel {
    display: none;
  }
  .form-panel {
    flex: 1;
    padding: 24px;
  }
  .login-card {
    width: 100%;
    border-radius: 16px;
  }
  .card-header {
    padding: 32px 28px 0;
  }
  .login-form {
    padding: 24px 28px 0;
  }
  .register-tip {
    padding: 20px 28px 28px;
  }
}
</style>