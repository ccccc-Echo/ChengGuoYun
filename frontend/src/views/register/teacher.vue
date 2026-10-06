<template>
  <div class="register-container">
    <div class="hero-panel">
      <div class="hero-bg">
        <div class="dot dot-1"></div><div class="dot dot-2"></div>
        <div class="dot dot-3"></div><div class="dot dot-4"></div>
        <div class="dot dot-5"></div><div class="dot dot-6"></div>
      </div>
      <div class="hero-content">
        <div class="hero-icon">
          <el-icon :size="44"><Document /></el-icon>
        </div>
        <h1 class="hero-title">成果云</h1>
        <p class="hero-desc">成果云系统</p>
        <div class="hero-divider"></div>
        <p class="hero-tagline">加入我们，开启你的成果之旅</p>
      </div>
    </div>

    <div class="form-panel">
      <div class="register-card">
        <div class="card-accent"></div>

        <div class="card-header">
          <router-link to="/register/identity" class="back-link">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回选择身份</span>
          </router-link>
          <div class="card-badge">
            <span class="badge-dot"></span>
            <span>成果云</span>
          </div>
          <h2 class="card-title">教师注册</h2>
          <p class="card-subtitle">填写信息创建教师账户</p>
          <div class="card-divider"></div>
        </div>

        <div class="card-body">
          <el-tabs v-model="activeTab" class="register-tabs">
            <el-tab-pane label="普通注册" name="normal">
              <el-form
                ref="registerFormRef"
                :model="registerForm"
                :rules="registerRules"
                class="register-form"
                @submit.prevent="handleRegister"
              >
                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><User /></el-icon>
                    <span>姓名</span>
                  </label>
                  <el-form-item prop="name">
                    <el-input v-model="registerForm.name" placeholder="请输入姓名" size="large" clearable />
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><School /></el-icon>
                    <span>学校 / 机构</span>
                  </label>
                  <el-form-item prop="school">
                    <el-select v-model="registerForm.school" placeholder="请选择学校/机构" size="large" style="width:100%">
                      <el-option label="a校" value="a校" />
                      <el-option label="b校" value="b校" />
                      <el-option label="c校" value="c校" />
                    </el-select>
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><Document /></el-icon>
                    <span>教工号</span>
                  </label>
                  <el-form-item prop="teacherNo">
                    <el-input v-model="registerForm.teacherNo" placeholder="请输入教工号" size="large" clearable />
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><CreditCard /></el-icon>
                    <span>身份证号</span>
                  </label>
                  <el-form-item prop="idCard">
                    <el-input v-model="registerForm.idCard" placeholder="请输入身份证号" size="large" clearable />
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><Lock /></el-icon>
                    <span>密码</span>
                  </label>
                  <el-form-item prop="password">
                    <el-input
                      v-model="registerForm.password"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="请输入密码"
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
                    <span>确认密码</span>
                  </label>
                  <el-form-item prop="confirmPassword">
                    <el-input
                      v-model="registerForm.confirmPassword"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="请确认密码"
                      size="large"
                    />
                  </el-form-item>
                </div>

                <el-form-item prop="agreement">
                  <el-checkbox v-model="registerForm.agreement">
                    <span class="agreement-text">我已阅读并同意</span>
                    <a href="#" class="agreement-link">《XX协议》</a>
                  </el-checkbox>
                </el-form-item>

                <el-button
                  type="primary" size="large" :loading="loading"
                  class="submit-btn" @click="handleRegister"
                >
                  <span class="btn-text">{{ loading ? '注册中...' : '注 册' }}</span>
                  <el-icon v-if="!loading" class="btn-arrow"><ArrowRight /></el-icon>
                </el-button>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="手机号注册" name="phone">
              <el-form
                ref="phoneFormRef"
                :model="phoneForm"
                :rules="phoneRules"
                class="register-form"
                @submit.prevent="handlePhoneRegister"
              >
                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><User /></el-icon>
                    <span>姓名</span>
                  </label>
                  <el-form-item prop="name">
                    <el-input v-model="phoneForm.name" placeholder="请输入姓名" size="large" clearable />
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><School /></el-icon>
                    <span>学校 / 机构</span>
                  </label>
                  <el-form-item prop="school">
                    <el-select v-model="phoneForm.school" placeholder="请选择学校/机构" size="large" style="width:100%">
                      <el-option label="a校" value="a校" />
                      <el-option label="b校" value="b校" />
                      <el-option label="c校" value="c校" />
                    </el-select>
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><Document /></el-icon>
                    <span>教工号</span>
                  </label>
                  <el-form-item prop="teacherNo">
                    <el-input v-model="phoneForm.teacherNo" placeholder="请输入教工号" size="large" clearable />
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><Phone /></el-icon>
                    <span>手机号</span>
                  </label>
                  <el-form-item prop="phone">
                    <el-input v-model="phoneForm.phone" placeholder="请输入手机号" size="large" clearable />
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><Message /></el-icon>
                    <span>短信验证码</span>
                  </label>
                  <el-form-item prop="smsCode">
                    <div class="sms-code-wrapper">
                      <el-input v-model="phoneForm.smsCode" placeholder="短信验证码" size="large" />
                      <el-button size="large" type="primary" :disabled="smsDisabled" class="send-sms-btn">
                        {{ smsCountdown > 0 ? `${smsCountdown}s` : '发送验证码' }}
                      </el-button>
                    </div>
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><Lock /></el-icon>
                    <span>密码</span>
                  </label>
                  <el-form-item prop="password">
                    <el-input
                      v-model="phoneForm.password"
                      :type="showPhonePassword ? 'text' : 'password'"
                      placeholder="请输入密码"
                      size="large"
                    >
                      <template #suffix>
                        <span class="toggle-pwd" @click="showPhonePassword = !showPhonePassword">
                          <el-icon><component :is="showPhonePassword ? 'View' : 'Hide'" /></el-icon>
                        </span>
                      </template>
                    </el-input>
                  </el-form-item>
                </div>

                <div class="field-group">
                  <label class="field-label">
                    <el-icon class="label-icon"><Lock /></el-icon>
                    <span>确认密码</span>
                  </label>
                  <el-form-item prop="confirmPassword">
                    <el-input
                      v-model="phoneForm.confirmPassword"
                      :type="showPhonePassword ? 'text' : 'password'"
                      placeholder="请确认密码"
                      size="large"
                    />
                  </el-form-item>
                </div>

                <el-form-item prop="agreement">
                  <el-checkbox v-model="phoneForm.agreement">
                    <span class="agreement-text">我已阅读并同意</span>
                    <a href="#" class="agreement-link">《XX协议》</a>
                  </el-checkbox>
                </el-form-item>

                <el-button
                  type="primary" size="large" :loading="loading"
                  class="submit-btn" @click="handlePhoneRegister"
                >
                  <span class="btn-text">{{ loading ? '注册中...' : '注 册' }}</span>
                  <el-icon v-if="!loading" class="btn-arrow"><ArrowRight /></el-icon>
                </el-button>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="微信注册" name="wechat">
              <div class="wechat-placeholder">
                <el-icon :size="56" color="#4095e5"><ChatDotRound /></el-icon>
                <p>微信注册功能开发中</p>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>

        <div class="login-tip">
          <span>已有账号？</span>
          <router-link to="/login" class="login-link">去登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Document, User, Lock, View, Hide, CreditCard, Phone, Message, ChatDotRound, ArrowRight, ArrowLeft, School } from '@element-plus/icons-vue'
import { authApi } from '@/api'

const router = useRouter()
const registerFormRef = ref(null)
const phoneFormRef = ref(null)
const loading = ref(false)
const showPassword = ref(false)
const showPhonePassword = ref(false)
const activeTab = ref('normal')

const smsCountdown = ref(0)
const smsDisabled = ref(false)

const registerForm = ref({
  name: '',
  school: '',
  teacherNo: '',
  idCard: '',
  password: '',
  confirmPassword: '',
  captcha: '',
  agreement: false
})

const phoneForm = ref({
  name: '',
  school: '',
  teacherNo: '',
  phone: '',
  smsCode: '',
  password: '',
  confirmPassword: '',
  captcha: '',
  agreement: false
})

const registerRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  school: [{ required: true, message: '请选择学校/机构', trigger: 'change' }],
  teacherNo: [{ required: true, message: '请输入教工号', trigger: 'blur' }],
  idCard: [{ required: true, message: '请输入身份证号', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
    { pattern: /^(?=.*[A-Za-z])(?=.*\d).+$/, message: '密码必须包含字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  agreement: [{ validator: (rule, value, callback) => value ? callback() : callback(new Error('请同意协议')), trigger: 'change' }]
}

const phoneRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  school: [{ required: true, message: '请选择学校/机构', trigger: 'change' }],
  teacherNo: [{ required: true, message: '请输入教工号', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  smsCode: [{ required: true, message: '请输入短信验证码', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
    { pattern: /^(?=.*[A-Za-z])(?=.*\d).+$/, message: '密码必须包含字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== phoneForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  agreement: [{ validator: (rule, value, callback) => value ? callback() : callback(new Error('请同意协议')), trigger: 'change' }]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  try {
    await registerFormRef.value.validate()
    loading.value = true
    const res = await authApi.normalRegister({
      username: registerForm.value.teacherNo,
      password: registerForm.value.password,
      confirmPassword: registerForm.value.confirmPassword,
      name: registerForm.value.name,
      role: 'teacher',
      school: registerForm.value.school,
      teacherId: registerForm.value.teacherNo,
      idCard: registerForm.value.idCard
    })
    if (res.code === 200) {
      ElMessage.success(res.message)
      router.push('/login')
    } else {
      ElMessage.error(res.message || '注册失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error(error.response?.data?.message || error.message || '注册失败')
    }
  } finally {
    loading.value = false
  }
}

const handlePhoneRegister = async () => {
  if (!phoneFormRef.value) return
  try {
    await phoneFormRef.value.validate()
    loading.value = true
    const res = await authApi.phoneRegister({
      name: phoneForm.value.name,
      role: 'teacher',
      school: phoneForm.value.school,
      teacherId: phoneForm.value.teacherNo,
      phone: phoneForm.value.phone,
      smsCode: phoneForm.value.smsCode,
      password: phoneForm.value.password,
      confirmPassword: phoneForm.value.confirmPassword
    })
    if (res.code === 200) {
      ElMessage.success(res.message)
      router.push('/login')
    } else {
      ElMessage.error(res.message || '注册失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error(error.response?.data?.message || error.message || '注册失败')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #eef4fb;
}

.hero-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(160deg, #dceeff 0%, #e8f4fd 40%, #f0f7ff 100%);
}

.hero-bg { position: absolute; inset: 0; }

.dot { position: absolute; border-radius: 50%; background: #4095e5; }
.dot-1 { width: 300px; height: 300px; top: -80px; left: -60px; opacity: 0.08; }
.dot-2 { width: 180px; height: 180px; top: 20%; right: 10%; opacity: 0.06; }
.dot-3 { width: 120px; height: 120px; bottom: 15%; left: 20%; opacity: 0.1; }
.dot-4 { width: 80px; height: 80px; top: 50%; left: 40%; opacity: 0.05; }
.dot-5 { width: 200px; height: 200px; bottom: -60px; right: -40px; opacity: 0.07; }
.dot-6 { width: 60px; height: 60px; top: 30%; left: 15%; opacity: 0.09; }

.hero-content { text-align: center; position: relative; z-index: 1; }

.hero-icon {
  width: 88px; height: 88px; margin: 0 auto 28px;
  background: #fff; border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  color: #4095e5; box-shadow: 0 4px 20px rgba(64, 149, 229, 0.1);
}

.hero-title { font-size: 36px; font-weight: 700; color: #1a2a3a; margin: 0 0 8px; letter-spacing: 3px; }
.hero-desc { font-size: 15px; color: #7a8b9e; margin: 0; letter-spacing: 1px; }
.hero-divider { width: 40px; height: 3px; background: #4095e5; border-radius: 2px; margin: 24px auto; opacity: 0.5; }
.hero-tagline { font-size: 14px; color: #a0b0c0; margin: 0; letter-spacing: 1px; }

.form-panel {
  display: flex; align-items: center; justify-content: center;
  padding: 0 60px;
}

.register-card {
  position: relative; width: 500px; max-height: 92vh;
  background: #fff; border-radius: 24px;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.03), 0 2px 6px rgba(0,0,0,0.02), 0 8px 24px rgba(64,149,229,0.05), 0 24px 56px rgba(64,149,229,0.09);
  overflow: hidden; display: flex; flex-direction: column;
}

.card-accent {
  height: 3px; flex-shrink: 0;
  background: linear-gradient(90deg, #4095e5, #6db3f2, #a0d2ff, #6db3f2, #4095e5);
  background-size: 200% 100%;
  animation: accentShimmer 4s ease-in-out infinite;
}

@keyframes accentShimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.card-header { padding: 28px 44px 0; text-align: center; flex-shrink: 0; }

.back-link {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 13px; color: #4095e5; text-decoration: none;
  font-weight: 500; margin-bottom: 16px; transition: color 0.2s;
}
.back-link:hover { color: #2563eb; }

.card-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 5px 16px; background: linear-gradient(135deg, #eef6ff, #e3f0ff);
  border: 1px solid rgba(64,149,229,0.12); border-radius: 20px;
  font-size: 12px; font-weight: 600; color: #4095e5; letter-spacing: 0.5px;
  margin-bottom: 16px;
}

.badge-dot { width: 6px; height: 6px; border-radius: 50%; background: #4095e5; animation: pulse 2s ease-in-out infinite; }

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

.card-title { font-size: 24px; font-weight: 700; color: #111827; margin: 0 0 4px; }
.card-subtitle { font-size: 14px; color: #9ca3af; margin: 0; }
.card-divider { width: 32px; height: 3px; background: #4095e5; border-radius: 2px; margin: 16px auto 0; opacity: 0.4; }

.card-body { flex: 1; overflow-y: auto; padding: 0 44px; }
.card-body::-webkit-scrollbar { width: 4px; }
.card-body::-webkit-scrollbar-thumb { background: #e5e7eb; border-radius: 2px; }

.register-tabs { margin-top: 20px; }
.register-tabs :deep(.el-tabs__header) { margin-bottom: 20px; }
.register-tabs :deep(.el-tabs__nav-wrap::after) { height: 1px; background: #e5e7eb; }
.register-tabs :deep(.el-tabs__active-bar) { background: #4095e5; height: 2px; }
.register-tabs :deep(.el-tabs__item) { font-size: 14px; color: #9ca3af; font-weight: 500; }
.register-tabs :deep(.el-tabs__item.is-active) { color: #4095e5; font-weight: 600; }

.register-form { padding-bottom: 8px; }
.field-group { margin-bottom: 2px; }

.field-label {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; font-weight: 600; color: #374151;
  margin-bottom: 8px; letter-spacing: 0.2px;
}

.label-icon { font-size: 14px; color: #4095e5; }
.register-form :deep(.el-form-item) { margin-bottom: 16px; }

.register-form :deep(.el-input__wrapper),
.register-form :deep(.el-select .el-input__wrapper) {
  border-radius: 12px; background: #f9fafb;
  border: 1.5px solid #e5e7eb; box-shadow: none;
  padding: 2px 14px; transition: all 0.2s ease;
}

.register-form :deep(.el-input__wrapper:hover),
.register-form :deep(.el-select .el-input__wrapper:hover) {
  background: #f3f4f6; border-color: #d1d5db;
}

.register-form :deep(.el-input__wrapper.is-focus),
.register-form :deep(.el-select .el-input__wrapper.is-focus) {
  background: #fff; border-color: #4095e5;
  box-shadow: 0 0 0 1px #4095e5, 0 0 0 4px rgba(64,149,229,0.08), 0 2px 8px rgba(64,149,229,0.06);
}

.register-form :deep(.el-input__inner) { height: 44px; line-height: 44px; font-size: 14px; color: #111827; }
.register-form :deep(.el-input__inner::placeholder) { color: #c4c8cf; font-size: 13px; }
.register-form :deep(.el-select .el-input__inner) { height: 44px; line-height: 44px; }

.toggle-pwd { cursor: pointer; display: flex; align-items: center; color: #9ca3af; transition: color 0.2s; }
.toggle-pwd:hover { color: #4095e5; }

.sms-code-wrapper { display: flex; gap: 10px; }
.send-sms-btn { height: 44px; border-radius: 12px; font-size: 13px; font-weight: 500; flex-shrink: 0; }

.agreement-text { font-size: 13px; color: #6b7280; }
.agreement-link { color: #4095e5; text-decoration: none; font-size: 13px; }
.agreement-link:hover { color: #2563eb; }

.submit-btn {
  display: flex; align-items: center; justify-content: center;
  gap: 8px; width: 100%; height: 50px;
  border-radius: 14px;
  background: linear-gradient(135deg, #4095e5, #2563eb);
  border: none;
  font-size: 16px; font-weight: 600; letter-spacing: 2px; color: #fff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(64,149,229,0.25), 0 0 0 0 rgba(64,149,229,0);
  margin-bottom: 8px;
}

.btn-arrow { font-size: 18px; transition: transform 0.3s; }
.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(64,149,229,0.35), 0 0 0 4px rgba(64,149,229,0.08);
}
.submit-btn:hover .btn-arrow { transform: translateX(3px); }
.submit-btn:active { transform: translateY(0); }

.wechat-placeholder {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 48px 0; color: #9ca3af;
}
.wechat-placeholder p { margin-top: 12px; font-size: 14px; }

.login-tip {
  text-align: center; padding: 20px 44px 28px;
  font-size: 14px; color: #9ca3af; flex-shrink: 0;
  border-top: 1px solid #f3f4f6;
}

.login-link { color: #4095e5; text-decoration: none; font-weight: 600; margin-left: 4px; }
.login-link:hover { color: #2563eb; }

@media (max-width: 768px) {
  .hero-panel { display: none; }
  .form-panel { flex: 1; padding: 16px; }
  .register-card { width: 100%; max-height: 100vh; border-radius: 16px; }
  .card-header { padding: 24px 24px 0; }
  .card-body { padding: 0 24px; }
  .login-tip { padding: 16px 24px 24px; }
}
</style>