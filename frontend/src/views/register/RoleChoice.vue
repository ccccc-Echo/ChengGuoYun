<template>
  <div class="role-choice-container">
    <div class="role-choice-wrapper">
      <div class="logo-section">
        <div class="logo">
          <el-icon :size="48"><School /></el-icon>
        </div>
        <h1>成果云系统</h1>
        <p class="subtitle">选择您的身份开始注册</p>
      </div>

      <div class="role-cards">
        <div 
          class="role-card teacher-card" 
          @click="router.push({ name: 'Register', query: { role: 'teacher' } })"
        >
          <div class="card-icon">
            <el-icon :size="40"><UserFilled /></el-icon>
          </div>
          <h3>我是老师</h3>
          <p>作为教师/辅导员，管理学生成果审核</p>
          <div class="card-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>

        <div 
          class="role-card student-card" 
          @click="router.push({ name: 'Register', query: { role: 'student' } })"
        >
          <div class="card-icon">
            <el-icon :size="40"><School /></el-icon>
          </div>
          <h3>我是学生</h3>
          <p>作为学生，录入和管理个人成果</p>
          <div class="card-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>

      <div class="login-link">
        <span>已有账号？</span>
        <router-link to="/login">去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { School, UserFilled, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<style scoped>
.role-choice-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.role-choice-wrapper {
  width: 100%;
  max-width: 800px;
  text-align: center;
}

.logo-section {
  margin-bottom: 40px;
}

.logo {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.logo :deep(.el-icon) {
  color: #fff;
}

h1 {
  font-size: 28px;
  color: #fff;
  margin-bottom: 10px;
  font-weight: 600;
}

.subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
}

.role-cards {
  display: flex;
  gap: 30px;
  justify-content: center;
  margin-bottom: 40px;
}

.role-card {
  flex: 1;
  max-width: 320px;
  background: #fff;
  border-radius: 16px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  position: relative;
  overflow: hidden;
}

.role-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.teacher-card .card-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.student-card .card-icon {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.card-icon :deep(.el-icon) {
  color: #fff;
}

.role-card h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
  font-weight: 600;
}

.role-card p {
  color: #999;
  font-size: 14px;
  line-height: 1.6;
}

.card-arrow {
  position: absolute;
  right: 20px;
  bottom: 20px;
  color: #ccc;
  transition: all 0.3s ease;
}

.role-card:hover .card-arrow {
  color: #667eea;
  transform: translateX(5px);
}

.login-link {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

.login-link a {
  color: #fff;
  text-decoration: underline;
  margin-left: 5px;
}

.login-link a:hover {
  opacity: 0.8;
}
</style>