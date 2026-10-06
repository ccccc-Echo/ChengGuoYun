<template>
  <div class="course-detail-container">
    <div class="page-header">
      <el-button @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>{{ course.name }}</h2>
      <div class="header-actions">
        <el-button v-if="$hasPermission('course:edit')" type="text" @click="toggleEditMode">{{ isEditMode ? '取消编辑' : '详情' }}</el-button>
        <el-button v-if="$hasPermission('course:delete')" type="text" style="color: #f56c6c;" @click="handleDelete">删除</el-button>
      </div>
    </div>

    <div v-if="!isEditMode" class="detail-content">
      <div class="course-info-section">
        <h3>班级信息</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">班级代码</span>
            <span class="info-value">{{ course.code }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">学期</span>
            <span class="info-value">{{ course.semester || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">最大人数</span>
            <span class="info-value">{{ course.max_students }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">当前人数</span>
            <span class="info-value">{{ course.student_count }}</span>
          </div>
          <div class="info-item full-width">
            <span class="info-label">课程描述</span>
            <span class="info-value">{{ course.description || '-' }}</span>
          </div>
        </div>
      </div>

      <div class="students-section">
        <div class="section-header">
          <h3>班级学生名单</h3>
          <el-button type="primary" size="small" @click="showAddStudentDialog = true">
            <el-icon><Plus /></el-icon>
            录入学生
          </el-button>
        </div>

        <el-table :data="students" border style="width: 100%;" v-loading="loading">
          <el-table-column prop="student_no" label="学号" width="120" />
          <el-table-column prop="name" label="姓名" width="100" />
          <el-table-column prop="major" label="专业" width="150" />
          <el-table-column prop="class_name" label="班级" width="150" />
          <el-table-column prop="joined_at" label="加入时间" width="180" />
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button type="danger" size="small" @click="handleRemoveStudent(scope.row.student_id)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="students.length === 0 && !loading" class="empty-table">
          暂无班级学生
        </div>
      </div>
    </div>

    <div v-else class="edit-content">
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="120px">
        <div class="edit-form-section">
          <h3>编辑班级信息</h3>
          <el-form-item label="课程名称" prop="name">
            <el-input v-model="editForm.name" placeholder="请输入课程名称" />
          </el-form-item>
          <el-form-item label="学期" prop="semester">
            <el-input v-model="editForm.semester" placeholder="如：2024-2025学年第一学期" />
          </el-form-item>
          <el-form-item label="课程描述">
            <el-input v-model="editForm.description" type="textarea" :rows="3" placeholder="请输入课程描述" />
          </el-form-item>
          <el-form-item label="最大人数" prop="max_students">
            <el-input-number v-model="editForm.max_students" :min="1" :max="500" placeholder="最大课程人数" />
          </el-form-item>
        </div>
      </el-form>
      <div class="edit-actions">
        <el-button @click="toggleEditMode">取消</el-button>
        <el-button type="primary" @click="handleSaveEdit">保存</el-button>
      </div>
    </div>

    <el-dialog v-model="showAddStudentDialog" title="录入学生" width="450px" :close-on-click-modal="false">
      <el-form :model="addStudentForm" :rules="addStudentRules" ref="addStudentFormRef" label-width="80px">
        <el-form-item label="学号" prop="student_no">
          <el-input v-model="addStudentForm.student_no" placeholder="请输入学生学号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddStudentDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAddStudent">录入学生</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus } from '@element-plus/icons-vue'
import { getUserInfo } from '@/utils/auth'

const route = useRoute()
const router = useRouter()
const course = ref({})
const students = ref([])
const loading = ref(false)
const showAddStudentDialog = ref(false)
const addStudentFormRef = ref(null)
const addStudentForm = ref({
  student_no: ''
})

const isEditMode = ref(false)
const editFormRef = ref(null)
const editForm = ref({
  name: '',
  semester: '',
  description: '',
  max_students: 50
})

const addStudentRules = {
  student_no: [
    { required: true, message: '请输入学生学号', trigger: 'blur' }
  ]
}

const editRules = {
  name: [
    { required: true, message: '请输入班级名称', trigger: 'blur' }
  ],
  max_students: [
    { required: true, message: '请输入最大人数', trigger: 'blur' },
    { type: 'number', min: 1, message: '最大人数必须大于0', trigger: 'blur' }
  ]
}

const fetchCourseDetail = async () => {
  try {
    const res = await fetch(`/api/courses/${route.params.id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    const data = await res.json()
    if (data.course) {
      course.value = data.course
      editForm.value = {
        name: data.course.name,
        semester: data.course.semester || '',
        description: data.course.description || '',
        max_students: data.course.max_students || 50
      }
    }
  } catch (error) {
    console.error('获取课程详情失败:', error)
    ElMessage.error('获取课程详情失败')
  }
}

const fetchStudents = async () => {
  loading.value = true
  try {
    const res = await fetch(`/api/courses/${route.params.id}/students`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    const data = await res.json()
    if (data.students) {
      students.value = data.students
    }
  } catch (error) {
    console.error('获取学生列表失败:', error)
    ElMessage.error('获取学生列表失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  const userInfo = getUserInfo()
  // 管理员从「课程管理」(/dashboard/classes) 进入，教师从「我的课程」(/dashboard/courses) 进入
  router.push(userInfo?.role === 'admin' ? '/dashboard/classes' : '/dashboard/courses')
}

const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
  if (!isEditMode.value) {
    editForm.value = {
      name: course.value.name,
      semester: course.value.semester || '',
      description: course.value.description || '',
      max_students: course.value.max_students || 50
    }
  }
}

const handleSaveEdit = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      const res = await fetch(`/api/courses/${route.params.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(editForm.value)
      })
      const data = await res.json()
      
      if (res.ok) {
        ElMessage.success('班级信息修改成功')
        isEditMode.value = false
        course.value = data.course
      } else {
        ElMessage.error(data.error || '修改班级信息失败')
      }
    } catch (error) {
      console.error('修改班级信息失败:', error)
      ElMessage.error('修改班级信息失败')
    }
  })
}

const handleDelete = () => {
  ElMessageBox.confirm(
    '确认要删除该班级吗？\n删除后，该班级下的学生和未审核成果将被清除。\n已审核通过的成果仍可在成果管理中查看。',
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
      dangerouslyUseHTMLString: true
    }
  ).then(async () => {
    try {
      const res = await fetch(`/api/courses/${route.params.id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (res.ok) {
        ElMessage.success('课程删除成功')
        const userInfo = getUserInfo()
        router.push(userInfo?.role === 'admin' ? '/dashboard/classes' : '/dashboard/courses')
      } else {
        const data = await res.json()
        ElMessage.error(data.error || '删除课程失败')
      }
    } catch (error) {
      console.error('删除课程失败:', error)
      ElMessage.error('删除课程失败')
    }
  })
}

const handleAddStudent = async () => {
  if (!addStudentFormRef.value) return
  
  await addStudentFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      const res = await fetch(`/api/courses/${route.params.id}/students`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(addStudentForm.value)
      })
      const data = await res.json()
      
      if (res.ok) {
        ElMessage.success('学生录入成功')
        showAddStudentDialog.value = false
        addStudentForm.value = { student_no: '' }
        await fetchStudents()
      } else {
        ElMessage.error(data.error || '录入学生失败')
      }
    } catch (error) {
      console.error('录入学生失败:', error)
      ElMessage.error('录入学生失败')
    }
  })
}

const handleRemoveStudent = async (studentId) => {
  try {
    const res = await fetch(`/api/courses/${route.params.id}/students/${studentId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    if (res.ok) {
      ElMessage.success('删除学生成功')
      await fetchStudents()
    } else {
      const data = await res.json()
      ElMessage.error(data.error || '删除学生失败')
    }
  } catch (error) {
    console.error('删除学生失败:', error)
    ElMessage.error('删除学生失败')
  }
}

onMounted(() => {
  fetchCourseDetail()
  fetchStudents()
})
</script>

<style scoped>
.course-detail-container {
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  flex: 1;
}

.header-actions {
  display: flex;
  gap: 16px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.course-info-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.06);
}

.course-info-section h3 {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 14px;
  color: #909399;
  font-weight: 500;
  min-width: 80px;
}

.info-value {
  font-size: 14px;
  color: #333;
}

.students-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.empty-table {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.edit-content {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.06);
}

.edit-form-section {
  margin-bottom: 24px;
}

.edit-form-section h3 {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}
</style>