<template>
  <div class="add-achievement-container">
    <h2>录入成果</h2>
    
    <el-card class="form-card">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
        class="achievement-form"
      >
        <el-form-item label="所属学生" prop="student_id" v-if="userInfo.role !== 'student'">
          <el-select v-model="formData.student_id" placeholder="请选择学生" style="width: 100%;">
            <el-option v-for="student in students" :key="student.id" :label="student.name" :value="student.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="成果标题" prop="title">
          <el-input
            v-model="formData.title"
            placeholder="请输入成果标题"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="一级分类" prop="main_category">
          <el-select v-model="formData.main_category" placeholder="请选择一级分类" style="width: 100%;" @change="handleMainCategoryChange">
            <el-option v-for="item in mainCategories" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>

        <el-form-item label="二级细分" prop="sub_category">
          <el-select v-model="formData.sub_category" placeholder="请选择二级细分" style="width: 100%;" :disabled="!formData.main_category">
            <el-option v-for="item in subCategories" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>

        <el-form-item label="成果级别" prop="level">
          <el-select v-model="formData.level" placeholder="请选择成果级别" style="width: 100%;">
            <el-option label="校级" value="Xiao Ji" />
            <el-option label="省级" value="Sheng Ji" />
            <el-option label="国家级" value="Guo Jia Ji" />
            <el-option label="国际级" value="Guo Ji Ji" />
          </el-select>
        </el-form-item>

        <el-form-item label="获得日期" prop="achieved_date">
          <el-date-picker
            v-model="formData.achieved_date"
            type="date"
            placeholder="请选择获得日期"
            style="width: 100%;"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item label="成果描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="6"
            placeholder="请输入成果描述"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="审核教师" v-if="userInfo.role === 'student'">
          <el-select
            v-model="formData.reviewer_ids"
            multiple
            placeholder="请选择审核教师"
            style="width: 100%;"
          >
            <el-option
              v-for="reviewer in reviewers"
              :key="reviewer.id"
              :label="reviewer.name + (reviewer.title ? ` (${reviewer.title})` : '')"
              :value="reviewer.id"
            />
          </el-select>
          <div class="reviewer-tip">可选教师：已加入课程的任课教师 + 所在班级辅导员</div>
        </el-form-item>

        <el-form-item label="附件上传">
          <el-upload
            class="upload-demo"
            drag
            :http-request="handleUpload"
            :on-remove="handleFileRemove"
            :file-list="fileList"
            :before-upload="beforeUpload"
            multiple
          >
            <el-icon class="el-icon--upload"><Upload /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 jpg/png/pdf/doc/docx 文件，单个文件不超过 10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            {{ submitting ? '提交中...' : '提交' }}
          </el-button>
          <el-button @click="handleCancel">取消</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { achievementsApi, studentsApi } from '@/api'
import { getUserInfo } from '@/utils/auth'
import request from '@/utils/request'
import { mainCategoryMap, subCategoryMap, levelMap } from '@/utils/constants'

const router = useRouter()
const route = useRoute()
const formRef = ref(null)
const submitting = ref(false)
const fileList = ref([])
const attachmentIds = ref([])       // 已上传附件的ID列表
const fileAttachmentMap = ref({})   // file.uid → attachment.id 映射
const students = ref([])
const reviewers = ref([])
const userInfo = ref(getUserInfo() || {})

const mainCategories = [
  { label: '学科竞赛类', value: 'Xue Ke Jing Sai Lei' },
  { label: '学术论文类', value: 'Xue Shu Lun Wen Lei' },
  { label: '知识产权类', value: 'Zhi Shi Chan Quan Lei' },
  { label: '科研项目类', value: 'Ke Yan Xiang Mu Lei' },
  { label: '荣誉表彰类', value: 'Rong Yu Biao Zhang Lei' },
  { label: '技能证书类', value: 'Ji Neng Zheng Shu Lei' },
  { label: '社会实践类', value: 'She Hui Shi Jian Lei' }
]

const categorySubCategories = {
  'Xue Ke Jing Sai Lei': [
    { label: 'ACM', value: 'ACM' },
    { label: '数学建模', value: 'Shu Xue Jian Mo' },
    { label: '互联网+', value: 'Hu Lian Wang +' },
    { label: '挑战杯', value: 'Tiao Zhan Bei' },
    { label: '电子设计', value: 'Dian Zi She Ji' },
    { label: '智能车', value: 'Zhi Neng Che' },
    { label: '其他', value: '其他' }
  ],
  'Xue Shu Lun Wen Lei': [
    { label: 'SCI', value: 'SCI' },
    { label: 'EI', value: 'EI' },
    { label: '核心期刊', value: 'He Xin Qi Kan' },
    { label: '普通期刊', value: 'Pu Tong Qi Kan' },
    { label: '会议论文', value: 'Hui Yi Lun Wen' }
  ],
  'Zhi Shi Chan Quan Lei': [
    { label: '发明专利', value: 'Fa Ming Zhuan Li' },
    { label: '实用新型', value: 'Shi Yong Xin Xing' },
    { label: '外观设计', value: 'Wai Guan She Ji' },
    { label: '软件著作权', value: 'Ruan Jian Zhu Zuo Quan' }
  ],
  'Ke Yan Xiang Mu Lei': [
    { label: '国家级大创', value: 'Guo Jia Ji Da Chuang' },
    { label: '省级大创', value: 'Sheng Ji Da Chuang' },
    { label: '校级大创', value: 'Xiao Ji Da Chuang' },
    { label: '参与教师科研', value: 'Can Yu Jiao Shi Ke Yan' }
  ],
  'Rong Yu Biao Zhang Lei': [
    { label: '国家奖学金', value: 'Guo Jia Jiang Xue Jin' },
    { label: '励志奖学金', value: 'Li Zhi Jiang Xue Jin' },
    { label: '三好学生', value: 'San Hao Xue Sheng' },
    { label: '优秀干部', value: 'You Xiu Gan Bu' },
    { label: '优秀团员', value: 'You Xiu Tuan Yuan' }
  ],
  'Ji Neng Zheng Shu Lei': [
    { label: '英语四六级', value: 'Ying Yu Si Liu Ji' },
    { label: '计算机等级', value: 'Ji Suan Ji Deng Ji' },
    { label: '教师资格证', value: 'Jiao Shi Zi Ge Zheng' },
    { label: '普通话', value: 'Pu Tong Hua' },
    { label: '职业资格证', value: 'Zhi Ye Zi Ge Zheng' }
  ],
  'She Hui Shi Jian Lei': [
    { label: '志愿服务', value: 'Zhi Yuan Fu Wu' },
    { label: '社会实践', value: 'She Hui Shi Jian' },
    { label: '社团活动', value: 'She Tuan Huo Dong' }
  ]
}

const subCategories = computed(() => {
  return categorySubCategories[formData.value.main_category] || []
})

const formData = ref({
  student_id: '',
  title: '',
  main_category: '',
  sub_category: '',
  level: '',
  achieved_date: '',
  description: '',
  reviewer_ids: []
})

const formRules = {
  student_id: [
    { required: true, message: '请选择学生', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入成果标题', trigger: 'blur' },
    { min: 2, max: 200, message: '标题长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  main_category: [
    { required: true, message: '请选择一级分类', trigger: 'change' }
  ],
  sub_category: [
    { required: true, message: '请选择二级细分', trigger: 'change' }
  ],
  level: [
    { required: true, message: '请选择成果级别', trigger: 'change' }
  ],
  achieved_date: [
    { required: true, message: '请选择获得日期', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入成果描述', trigger: 'blur' },
    { min: 10, max: 1000, message: '描述长度在 10 到 1000 个字符', trigger: 'blur' }
  ]
}

const handleMainCategoryChange = () => {
  formData.value.sub_category = ''
}

onMounted(() => {
  if (userInfo.value.role !== 'student') {
    loadStudents()
  } else {
    loadReviewers()
  }
  
  if (route.query.id) {
    loadAchievement(route.query.id)
  }
})

const loadReviewers = async () => {
  try {
    const res = await achievementsApi.getReviewers()
    reviewers.value = res.reviewers || []
  } catch (error) {
    console.error('加载审核教师列表失败:', error)
  }
}

const loadStudents = async () => {
  try {
    const res = await studentsApi.list({ page_size: 100 })
    students.value = res.students || []
  } catch (error) {
    console.error('加载学生列表失败:', error)
  }
}

const loadAchievement = async (id) => {
  try {
    const res = await achievementsApi.get(id)
    const data = res.achievement
    formData.value = {
      student_id: data.student_id || '',
      title: data.title || '',
      main_category: data.main_category || '',
      sub_category: data.sub_category || '',
      level: data.level || '',
      achieved_date: data.achieved_date || '',
      description: data.description || ''
    }
  } catch (error) {
    console.error('加载成果详情失败:', error)
  }
}

const beforeUpload = (file) => {
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('上传文件大小不能超过 10MB!')
    return false
  }
  return true
}

const handleUpload = async (options) => {
  const { file, onProgress, onSuccess, onError } = options

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await request({
      url: '/achievements/upload/',
      method: 'post',
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    const attId = res.attachment.id
    fileAttachmentMap.value[file.uid] = attId
    attachmentIds.value.push(attId)
    onSuccess(res)
    ElMessage.success(`文件 ${file.name} 上传成功`)
  } catch (error) {
    onError(error)
    const msg = error.response?.data?.error || error.message || '上传失败'
    ElMessage.error(`文件 ${file.name} ${msg}`)
  }
}

const handleFileRemove = (file) => {
  const attId = fileAttachmentMap.value[file.uid]
  if (attId) {
    const idx = attachmentIds.value.indexOf(attId)
    if (idx > -1) {
      attachmentIds.value.splice(idx, 1)
    }
    delete fileAttachmentMap.value[file.uid]
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    const data = { ...formData.value }
    
    if (userInfo.value.role === 'student') {
      delete data.student_id
    }
    
    if (attachmentIds.value.length > 0) {
      data.attachment_ids = attachmentIds.value
    }
    
    if (route.query.id) {
      await achievementsApi.update(route.query.id, data)
      ElMessage.success('成果更新成功')
    } else {
      await achievementsApi.create(data)
      ElMessage.success('成果提交成功，等待审核')
    }
    
    router.push('/dashboard/achievements')
  } catch (error) {
    if (error !== false) {
      console.error('提交成果失败:', error)
      let errorMessage = '提交成果失败'
      if (error.response) {
        const { status, data } = error.response
        if (data && data.error) {
          errorMessage = data.error
        } else if (data && data.message) {
          errorMessage = data.message
        } else {
          errorMessage = `请求失败，状态码: ${status}`
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      ElMessage.error(errorMessage)
    }
  } finally {
    submitting.value = false
  }
}

const handleCancel = () => {
  router.back()
}

const handleReset = () => {
  formRef.value?.resetFields()
  fileList.value = []
  attachmentIds.value = []
  fileAttachmentMap.value = {}
}
</script>

<style scoped>
.add-achievement-container {
  padding: 0;
}

h2 {
  margin-bottom: 20px;
  color: #222;
  font-size: 22px;
  font-weight: 600;
}

.form-card {
  max-width: 800px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.achievement-form {
  margin-top: 24px;
}

.upload-demo {
  width: 100%;
}

:deep(.el-card) {
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
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

:deep(.el-input__wrapper:hover) {
  border-color: #4095e5;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(64, 149, 229, 0.08);
}

:deep(.el-upload-dragger) {
  padding: 30px;
  border-radius: 10px;
  border: 2px dashed rgba(64, 149, 229, 0.2);
}

:deep(.el-upload-dragger:hover) {
  border-color: #4095e5;
  background: rgba(64, 149, 229, 0.02);
}

:deep(.el-icon--upload) {
  font-size: 44px;
  margin-bottom: 12px;
  color: #4095e5;
}

:deep(.el-button--primary) {
  border-radius: 8px;
}

.reviewer-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}
</style>