<template>
  <div class="profile-container">
    <h2>个人中心</h2>
    
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <el-icon :size="20"><User /></el-icon>
          <span>基本信息</span>
        </div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" disabled />
        </el-form-item>

        <el-form-item label="姓名">
          <el-input v-model="form.name" disabled />
        </el-form-item>

        <el-form-item label="角色">
          <el-tag :type="roleTagType">{{ roleText }}</el-tag>
        </el-form-item>

        <template v-if="userInfo.role === 'student'">
          <el-form-item label="学号" prop="student_no">
            <el-input v-model="form.student_no" placeholder="请输入学号" />
          </el-form-item>

          <el-form-item label="班级">
            <el-input v-model="form.class_name" disabled>
              <template #append>{{ form.class_id ? '' : '待分配' }}</template>
            </el-input>
          </el-form-item>

          <el-form-item label="专业" prop="major">
            <el-input v-model="form.major" placeholder="请输入专业" />
          </el-form-item>

          <el-form-item label="手机号">
            <el-input v-model="form.phone" placeholder="请输入手机号" />
          </el-form-item>
        </template>

        <template v-if="userInfo.role === 'teacher'">
          <el-form-item label="工号" prop="teacher_no">
            <el-input v-model="form.teacher_no" placeholder="请输入工号" />
          </el-form-item>

          <el-form-item label="院系" prop="department">
            <el-input v-model="form.department" placeholder="请输入院系" />
          </el-form-item>

          <el-form-item label="职称" prop="title">
            <el-select v-model="form.title" placeholder="请选择职称" style="width: 100%;">
              <el-option label="教授" value="教授" />
              <el-option label="副教授" value="副教授" />
              <el-option label="讲师" value="讲师" />
              <el-option label="助教" value="助教" />
            </el-select>
          </el-form-item>

          <el-form-item label="手机号">
            <el-input v-model="form.phone" placeholder="请输入手机号" />
          </el-form-item>
        </template>

        <el-form-item>
          <el-button type="primary" :loading="saving" @click="handleSave">
            保存修改
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { authApi } from '@/api'
import { getUserInfo, setUserInfo } from '@/utils/auth'

const formRef = ref(null)
const saving = ref(false)
const userInfo = ref(getUserInfo() || {})

const form = reactive({
  username: '',
  name: '',
  student_no: '',
  class_id: '',
  class_name: '',
  major: '',
  teacher_no: '',
  department: '',
  title: '',
  phone: ''
})

const rules = computed(() => {
  if (userInfo.value.role === 'student') {
    return {
      student_no: [
        { required: true, message: '请输入学号', trigger: 'blur' }
      ],
      major: [
        { required: true, message: '请输入专业', trigger: 'blur' }
      ]
    }
  } else if (userInfo.value.role === 'teacher') {
    return {
      teacher_no: [
        { required: true, message: '请输入工号', trigger: 'blur' }
      ],
      department: [
        { required: true, message: '请输入院系', trigger: 'blur' }
      ],
      title: [
        { required: true, message: '请选择职称', trigger: 'change' }
      ]
    }
  }
  return {}
})

const roleText = computed(() => {
  const roles = {
    admin: '管理员',
    teacher: '辅导员',
    student: '学生'
  }
  return roles[userInfo.value.role] || '未知'
})

const roleTagType = computed(() => {
  const types = {
    admin: 'danger',
    teacher: 'primary',
    student: 'success'
  }
  return types[userInfo.value.role] || 'info'
})

const loadProfile = async () => {
  try {
    const res = await authApi.getProfile()
    const user = res.user || res
    
    form.username = user.username || ''
    form.name = user.name || ''
    form.student_no = user.student_no || ''
    form.class_id = user.class_id || ''
    form.class_name = user.class_name || ''
    form.major = user.major || ''
    form.teacher_no = user.teacher_no || ''
    form.department = user.department || ''
    form.title = user.title || ''
    form.phone = user.phone || ''
  } catch (error) {
    console.error('加载个人信息失败:', error)
  }
}

const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    saving.value = true

    let data
    if (userInfo.value.role === 'student') {
      data = {
        student_no: form.student_no,
        major: form.major,
        phone: form.phone
      }
    } else if (userInfo.value.role === 'teacher') {
      data = {
        teacher_no: form.teacher_no,
        department: form.department,
        title: form.title,
        phone: form.phone
      }
    }

    const res = await authApi.updateProfile(data)
    
    const updatedUser = res.user || res
    const currentUser = getUserInfo() || {}
    const newUserInfo = { ...currentUser, ...updatedUser }
    setUserInfo(newUserInfo)
    userInfo.value = newUserInfo

    ElMessage.success('保存成功')
  } catch (error) {
    if (error !== false) {
      console.error('保存失败:', error)
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-container {
  padding: 0;
}

h2 {
  margin-bottom: 20px;
  color: #222;
  font-size: 22px;
  font-weight: 600;
}

.profile-card {
  max-width: 600px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

:deep(.el-card) {
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

:deep(.el-card__header) {
  padding: 18px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

:deep(.el-card__body) {
  padding: 24px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  color: #555;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

:deep(.el-button--primary) {
  border-radius: 8px;
}
</style>