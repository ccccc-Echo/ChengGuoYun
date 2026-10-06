<template>
  <div class="profile-container">
    <el-row :gutter="24" class="basic-info-row">
      <el-col :span="14">
        <div class="info-card">
          <div class="card-header">
            <el-icon :size="18"><User /></el-icon>
            <span>基本信息</span>
          </div>
          <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="form.username" disabled />
            </el-form-item>

            <el-form-item label="姓名">
              <el-input v-model="form.name" disabled />
            </el-form-item>

            <el-form-item label="角色">
              <el-tag :type="roleTagType" size="small">{{ roleText }}</el-tag>
            </el-form-item>

            <template v-if="userInfo.role === 'student'">
              <el-form-item label="学号" prop="student_no">
                <el-input v-model="form.student_no" placeholder="请输入学号" />
              </el-form-item>

              <el-form-item label="班级">
                <el-input v-model="form.class_name" disabled />
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
              <el-button type="primary" :loading="saving" @click="handleSave" class="save-btn">
                保存修改
              </el-button>
              <el-button @click="handleReset" class="reset-btn">
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>

      <el-col :span="10">
        <div class="avatar-card">
          <div class="avatar-wrapper">
            <div class="avatar-circle">
              <img v-if="form.avatar" :src="fullAvatarUrl" class="avatar-img" />
              <el-icon v-else :size="48"><UserFilled /></el-icon>
            </div>
          </div>
          <div class="avatar-info">
            <div class="avatar-name">{{ form.name || '用户' }}</div>
            <div class="avatar-major">{{ userInfo.role === 'student' ? form.major : form.department || '--' }}</div>
          </div>
          <el-button type="primary" class="upload-btn" @click="triggerAvatarUpload">
            <el-icon><Upload /></el-icon>
            更换头像
          </el-button>
          <input ref="avatarInputRef" type="file" accept="image/*" style="display:none" @change="handleAvatarFileChange" />
        </div>

        <div class="security-card">
          <div class="card-header">
            <el-icon :size="18"><Lock /></el-icon>
            <span>账号安全</span>
          </div>
          <div class="security-list">
            <div class="security-item" @click="showPasswordDialog = true">
              <span class="security-label">修改登录密码</span>
              <span class="security-action">去修改</span>
            </div>
            <div class="security-item" @click="showPhoneDialog = true">
              <span class="security-label">绑定手机号</span>
              <span class="security-action">{{ form.phone ? form.phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2') : '去绑定' }}</span>
            </div>
            <div class="security-item danger" @click="handleLogout">
              <span class="security-label">安全退出</span>
              <span class="security-action">退出登录</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="export-card">
      <div class="card-header">
        <el-icon :size="18"><Download /></el-icon>
        <span>我的档案导出</span>
      </div>
      <div class="export-buttons">
        <el-button type="primary" plain class="export-btn">
          <el-icon><Document /></el-icon>
          导出全部成果PDF
        </el-button>
        <el-button type="primary" plain class="export-btn">
          <el-icon><Trophy /></el-icon>
          导出获奖证书汇总
        </el-button>
        <el-button type="primary" plain class="export-btn">
          <el-icon><User /></el-icon>
          导出个人信息表
        </el-button>
      </div>
    </div>

    <el-dialog title="修改密码" v-model="showPasswordDialog" width="420px">
      <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="100px">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="passwordForm.old_password" type="password" placeholder="请输入旧密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordForm.new_password" type="password" placeholder="请输入新密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" :loading="passwordSaving" @click="handleChangePassword">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog title="更换手机号" v-model="showPhoneDialog" width="420px">
      <el-form ref="phoneFormRef" :model="phoneForm" :rules="phoneRules" label-width="100px">
        <el-form-item label="新手机号" prop="phone">
          <el-input v-model="phoneForm.phone" placeholder="请输入新手机号" />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-input v-model="phoneForm.code" placeholder="请输入验证码">
            <template #append>
              <el-button @click="sendCode">发送验证码</el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPhoneDialog = false">取消</el-button>
        <el-button type="primary" :loading="phoneSaving" @click="handleChangePhone">确定</el-button>
      </template>
    </el-dialog>

    <!-- 头像裁剪弹窗 -->
    <el-dialog title="裁剪头像" v-model="showCropperDialog" width="600px" :close-on-click-modal="false" @close="handleCropperClose">
      <div class="cropper-container">
        <div class="cropper-area">
          <VueCropper
            ref="cropperRef"
            :img="cropperImg"
            :output-size="1"
            :output-type="'png'"
            :info="true"
            :full="false"
            :can-scale="true"
            :auto-crop="true"
            :fixed="true"
            :fixed-number="[1, 1]"
            :center-box="true"
            :high="true"
            mode="contain"
            @realTime="realTime"
          />
        </div>
        <div class="cropper-preview">
          <div class="preview-title">预览</div>
          <div class="preview-88">
            <div class="preview-box" :style="previewBoxStyle">
              <img
                v-if="cropperImg"
                :src="cropperImg"
                :style="previewImgStyle"
                alt="头像预览"
              />
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showCropperDialog = false">取消</el-button>
        <el-button type="primary" :loading="uploadingAvatar" @click="confirmCropAndUpload">确定上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, UserFilled, Lock, Download, Document, Trophy, Upload } from '@element-plus/icons-vue'
import { authApi } from '@/api'
import { getUserInfo, setUserInfo, removeToken, removeUserInfo } from '@/utils/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const formRef = ref(null)
const passwordFormRef = ref(null)
const phoneFormRef = ref(null)
const saving = ref(false)
const passwordSaving = ref(false)
const phoneSaving = ref(false)
const userInfo = ref(getUserInfo() || {})

const showPasswordDialog = ref(false)
const showPhoneDialog = ref(false)

// 头像相关
const avatarInputRef = ref(null)
const showCropperDialog = ref(false)
const cropperImg = ref('')
const cropperRef = ref(null)
const uploadingAvatar = ref(false)
const previews = ref({})

// vue-cropper 实时预览回调，data.url 为裁剪区域的图片（base64 或 blob URL）
const realTime = (data) => {
  previews.value = data || {}
}

// 关闭弹窗：释放预览产生的临时 blob URL，但保留 previews / cropperImg，保证再次打开时预览仍显示
const handleCropperClose = () => {
  const url = previews.value?.url
  if (url && typeof url === 'string' && url.startsWith('blob:')) {
    URL.revokeObjectURL(url)
  }
}

// 预览图裁剪框尺寸（正方形 1:1），按 88px 放大缩小
const previewScale = computed(() => {
  const w = previews.value?.w || 1
  return 88 / w
})

// 裁剪框容器：固定为裁剪区域大小，随真实裁剪框同步
const previewBoxStyle = computed(() => {
  const p = previews.value || {}
  return {
    width: (p.w || 88) + 'px',
    height: (p.h || 88) + 'px',
    transform: `scale(${previewScale.value})`,
    transformOrigin: '0 0'
  }
})

// 原图位移/缩放变换（与 vue-cropper 自带预览一致，img 变换原点为中心），由外层 box 统一缩放到 88px
const previewImgStyle = computed(() => {
  const p = previews.value || {}
  return {
    width: (p.img?.width || '100%'),
    height: (p.img?.height || '100%'),
    transform: (p.img?.transform || ''),
    transformOrigin: '50% 50%'
  }
})

const fullAvatarUrl = computed(() => {
  if (!form.avatar) return ''
  return form.avatar
})

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
  phone: '',
  avatar: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const phoneForm = reactive({
  phone: '',
  code: ''
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

const passwordRules = {
  old_password: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
    { pattern: /^(?=.*[A-Za-z])(?=.*\d).+$/, message: '密码必须包含字母和数字', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const phoneRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ]
}

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

const handleReset = () => {
  loadProfile()
  ElMessage.info('已重置')
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    
    passwordSaving.value = true

    await authApi.changePassword(passwordForm)
    
    showPasswordDialog.value = false
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    ElMessage.success('密码修改成功')
  } catch (error) {
    if (error !== false) {
      console.error('修改密码失败:', error)
      ElMessage.error(error.message || '修改密码失败')
    }
  } finally {
    passwordSaving.value = false
  }
}

const sendCode = () => {
  if (!phoneForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  ElMessage.success('验证码已发送')
}

const handleChangePhone = async () => {
  if (!phoneFormRef.value) return

  try {
    await phoneFormRef.value.validate()
    
    phoneSaving.value = true

    await authApi.updateProfile({ phone: phoneForm.phone })
    
    showPhoneDialog.value = false
    phoneForm.phone = ''
    phoneForm.code = ''
    loadProfile()
    ElMessage.success('手机号修改成功')
  } catch (error) {
    if (error !== false) {
      console.error('修改手机号失败:', error)
      ElMessage.error(error.message || '修改手机号失败')
    }
  } finally {
    phoneSaving.value = false
  }
}

const handleLogout = () => {
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

// 头像相关方法
const triggerAvatarUpload = () => {
  avatarInputRef.value?.click()
}

const handleAvatarFileChange = (e) => {
  const file = e.target.files?.[0]
  if (!file) return

  if (!['image/png', 'image/jpeg', 'image/jpg', 'image/gif'].includes(file.type)) {
    ElMessage.error('请选择 png/jpg/jpeg/gif 格式的图片')
    e.target.value = ''
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    e.target.value = ''
    return
  }

  const reader = new FileReader()
  reader.onload = (event) => {
    cropperImg.value = event.target.result
    showCropperDialog.value = true
  }
  reader.readAsDataURL(file)
  e.target.value = ''
}

const confirmCropAndUpload = () => {
  if (!cropperRef.value) return

  cropperRef.value.getCropData((data) => {
    uploadingAvatar.value = true

    const byteString = atob(data.split(',')[1])
    const mimeString = data.split(',')[0].split(':')[1].split(';')[0]
    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i)
    }
    const blob = new Blob([ab], { type: mimeString })
    const file = new File([blob], 'avatar.png', { type: 'image/png' })

    const formData = new FormData()
    formData.append('avatar', file)

    fetch('/api/user/avatar', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      },
      body: formData
    })
      .then(async (res) => {
        const result = await res.json()
        if (res.ok) {
          form.avatar = result.avatar
          showCropperDialog.value = false
          ElMessage.success('头像更新成功')
        } else {
          ElMessage.error(result.error || '上传失败')
        }
      })
      .catch((err) => {
        console.error('头像上传失败:', err)
        ElMessage.error('头像上传失败')
      })
      .finally(() => {
        uploadingAvatar.value = false
      })
  })
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-container {
  min-height: 100%;
  background: transparent;
}

.basic-info-row {
  margin-bottom: 24px;
}

.info-card,
.avatar-card,
.security-card,
.export-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.info-card:hover,
.avatar-card:hover,
.security-card:hover,
.export-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}

:deep(.el-form-item__label) {
  color: #666;
  font-weight: 500;
  text-align: left;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 1px solid #e8ecf0;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}

:deep(.el-input.is-disabled .el-input__wrapper) {
  background: #f7f8fa;
  border-color: #e8ecf0;
}

:deep(.el-input.is-disabled .el-input__inner) {
  color: #86909c;
}

.save-btn {
  border-radius: 6px;
  background: linear-gradient(135deg, #1677ff, #4096ff);
  border: none;
  padding: 8px 24px;
  transition: all 0.3s ease;
}

.save-btn:hover {
  background: linear-gradient(135deg, #0d66d0, #3085ff);
  transform: translateY(-1px);
}

.reset-btn {
  border-radius: 6px;
  border: 1px solid #d9d9d9;
  color: #666;
  padding: 8px 24px;
  margin-left: 12px;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  border-color: #1677ff;
  color: #1677ff;
}

.avatar-card {
  text-align: center;
  margin-bottom: 24px;
}

.avatar-wrapper {
  margin-bottom: 16px;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #eaf4ff 0%, #d6e4ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  color: #1677ff;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-info {
  margin-bottom: 20px;
}

.avatar-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.avatar-major {
  font-size: 13px;
  color: #86909c;
}

.upload-btn {
  border-radius: 6px;
  background: linear-gradient(135deg, #1677ff, #4096ff);
  border: none;
  padding: 8px 20px;
  transition: all 0.3s ease;
}

.upload-btn:hover {
  background: linear-gradient(135deg, #0d66d0, #3085ff);
}

.security-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: all 0.3s ease;
}

.security-item:last-child {
  border-bottom: none;
}

.security-item:hover {
  background: rgba(22, 119, 255, 0.04);
}

.security-item.danger:hover {
  background: rgba(245, 63, 63, 0.04);
}

.security-label {
  font-size: 14px;
  color: #333;
}

.security-action {
  font-size: 13px;
  color: #1677ff;
}

.security-item.danger .security-action {
  color: #f53f3f;
}

.export-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.export-btn {
  border-radius: 6px;
  border-color: #1677ff;
  color: #1677ff;
  padding: 10px 20px;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background: rgba(22, 119, 255, 0.08);
  border-color: #4096ff;
}

:deep(.el-dialog) {
  border-radius: 12px;
}

:deep(.el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-dialog__title) {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}

:deep(.el-tag--success) {
  background: rgba(0, 180, 42, 0.1);
  color: #00b42a;
  border-color: rgba(0, 180, 42, 0.2);
}

/* 裁剪弹窗样式 */
.cropper-container {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.cropper-area {
  flex: 1;
  width: 400px;
  height: 400px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.cropper-preview {
  width: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.preview-title {
  font-size: 13px;
  color: #666;
}

.preview-88 {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  border: 2px dashed #d9d9d9;
  overflow: hidden;
  background: #f5f5f5;
  position: relative;
}

.preview-box {
  position: absolute;
  top: 0;
  left: 0;
  margin: 0;
  overflow: hidden;
  transform-origin: 0 0;
}

.preview-box img {
  display: block;
}
</style>
