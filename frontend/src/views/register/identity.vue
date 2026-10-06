<template>
  <div class="register-container">
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
        <p class="hero-tagline">加入我们，开启你的成果之旅</p>
      </div>
    </div>

    <!-- 右侧身份选择 -->
    <div class="form-panel">
      <div class="register-card">
        <div class="card-accent"></div>

        <div class="card-header">
          <div class="card-badge">
            <span class="badge-dot"></span>
            <span>成果云</span>
          </div>
          <h2 class="card-title">创建账户</h2>
          <p class="card-subtitle">请选择您的身份以继续</p>
          <div class="card-divider"></div>
        </div>

        <div class="identity-cards">
          <div class="identity-card" @click="selectIdentity('student')">
            <div class="id-icon student-icon">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="id-info">
              <h3>我是学生</h3>
              <p>加入课程、录入成果、展示个人成就</p>
            </div>
            <el-icon class="id-arrow"><ArrowRight /></el-icon>
          </div>

          <div class="identity-card" @click="selectIdentity('teacher')">
            <div class="id-icon teacher-icon">
              <el-icon :size="32"><UserFilled /></el-icon>
            </div>
            <div class="id-info">
              <h3>我是教师</h3>
              <p>管理班级、审核成果、查看教学数据</p>
            </div>
            <el-icon class="id-arrow"><ArrowRight /></el-icon>
          </div>
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
import { useRouter } from 'vue-router'
import { Document, User, UserFilled, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()

const selectIdentity = (identity) => {
  router.push(`/register/${identity}`)
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

.hero-bg { position: absolute; inset: 0; }

.dot {
  position: absolute;
  border-radius: 50%;
  background: #4095e5;
}

.dot-1 { width: 300px; height: 300px; top: -80px; left: -60px; opacity: 0.08; }
.dot-2 { width: 180px; height: 180px; top: 20%; right: 10%; opacity: 0.06; }
.dot-3 { width: 120px; height: 120px; bottom: 15%; left: 20%; opacity: 0.1; }
.dot-4 { width: 80px; height: 80px; top: 50%; left: 40%; opacity: 0.05; }
.dot-5 { width: 200px; height: 200px; bottom: -60px; right: -40px; opacity: 0.07; }
.dot-6 { width: 60px; height: 60px; top: 30%; left: 15%; opacity: 0.09; }

.hero-content {
  text-align: center;
  position: relative;
  z-index: 1;
}

.hero-icon {
  width: 88px; height: 88px;
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
  font-size: 36px; font-weight: 700;
  color: #1a2a3a; margin: 0 0 8px;
  letter-spacing: 3px;
}

.hero-desc {
  font-size: 15px; color: #7a8b9e;
  margin: 0; letter-spacing: 1px;
}

.hero-divider {
  width: 40px; height: 3px;
  background: #4095e5; border-radius: 2px;
  margin: 24px auto; opacity: 0.5;
}

.hero-tagline {
  font-size: 14px; color: #a0b0c0;
  margin: 0; letter-spacing: 1px;
}

/* ========== 右侧卡片 ========== */
.form-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 80px;
}

.register-card {
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

.card-header {
  padding: 36px 44px 0;
  text-align: center;
}

.card-badge {
  display: inline-flex;
  align-items: center; gap: 8px;
  padding: 5px 16px;
  background: linear-gradient(135deg, #eef6ff, #e3f0ff);
  border: 1px solid rgba(64, 149, 229, 0.12);
  border-radius: 20px;
  font-size: 12px; font-weight: 600;
  color: #4095e5; letter-spacing: 0.5px;
  margin-bottom: 20px;
}

.badge-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #4095e5;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.3); }
}

.card-title {
  font-size: 26px; font-weight: 700;
  color: #111827; margin: 0 0 6px;
  letter-spacing: -0.3px;
}

.card-subtitle {
  font-size: 14px; color: #9ca3af;
  margin: 0;
}

.card-divider {
  width: 32px; height: 3px;
  background: #4095e5; border-radius: 2px;
  margin: 20px auto 0; opacity: 0.4;
}

/* ========== 身份卡片 ========== */
.identity-cards {
  padding: 32px 44px 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.identity-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.identity-card:hover {
  background: #fff;
  border-color: #4095e5;
  box-shadow: 0 4px 16px rgba(64, 149, 229, 0.1);
  transform: translateY(-1px);
}

.identity-card:hover .id-arrow {
  color: #4095e5;
  transform: translateX(3px);
}

.id-icon {
  width: 56px; height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #fff;
}

.student-icon {
  background: linear-gradient(135deg, #67c23a, #85ce61);
}

.teacher-icon {
  background: linear-gradient(135deg, #4095e5, #6db3f2);
}

.id-info { flex: 1; }

.id-info h3 {
  font-size: 16px; font-weight: 600;
  color: #111827; margin: 0 0 4px;
}

.id-info p {
  font-size: 13px; color: #9ca3af;
  margin: 0; line-height: 1.5;
}

.id-arrow {
  font-size: 18px;
  color: #d1d5db;
  transition: all 0.25s;
}

/* ========== 底部链接 ========== */
.login-tip {
  text-align: center;
  padding: 28px 44px 36px;
  font-size: 14px; color: #9ca3af;
}

.login-link {
  color: #4095e5; text-decoration: none;
  font-weight: 600; margin-left: 4px;
}

.login-link:hover { color: #2563eb; }

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .hero-panel { display: none; }
  .form-panel { flex: 1; padding: 24px; }
  .register-card { width: 100%; border-radius: 16px; }
  .card-header { padding: 32px 28px 0; }
  .identity-cards { padding: 28px 28px 0; }
  .login-tip { padding: 24px 28px 32px; }
}
</style>