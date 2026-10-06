<template>
  <div class="teacher-export-container">
    <div class="page-card">
      <!-- 搜索栏 -->
      <div class="search-bar">
        <div class="search-item">
          <span class="search-label">开始日期</span>
          <el-date-picker
            v-model="searchForm.start_date"
            type="date"
            placeholder="按审核通过时间"
            value-format="YYYY-MM-DD"
            style="width: 155px"
          />
        </div>
        <div class="search-item">
          <span class="search-label">结束日期</span>
          <el-date-picker
            v-model="searchForm.end_date"
            type="date"
            placeholder="按审核通过时间"
            value-format="YYYY-MM-DD"
            style="width: 155px"
          />
        </div>
        <div class="search-item">
          <span class="search-label">分类</span>
          <el-select v-model="searchForm.category" placeholder="奖项类型" clearable filterable style="width: 170px">
            <el-option v-for="c in categoryOptions" :key="c.code" :label="c.name" :value="c.code" />
          </el-select>
        </div>
        <div class="search-item">
          <span class="search-label">级别</span>
          <el-select v-model="searchForm.level" placeholder="赛事级别" clearable style="width: 150px">
            <el-option v-for="l in levelOptions" :key="l.code" :label="l.name" :value="l.code" />
          </el-select>
        </div>
        <div class="search-item">
          <span class="search-label">学号</span>
          <el-input v-model="searchForm.student_no" placeholder="学号搜索" clearable style="width: 160px" @keyup.enter="handleSearch" />
        </div>
        <div class="search-actions">
          <el-button type="primary" :loading="loading" @click="handleSearch">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </div>
      </div>

      <!-- 学生列表 -->
      <el-table
        v-loading="loading"
        :data="students"
        empty-text="暂无所带班级的学生，请先在班级管理中为该教师设置班级"
        row-key="student_id"
        style="width: 100%"
      >
        <el-table-column prop="student_no" label="学号" width="140" show-overflow-tooltip />
        <el-table-column prop="name" label="姓名" width="130">
          <template #default="{ row }">
            <span class="student-name">
              <el-icon v-if="row.achievement_count > 0"><Trophy /></el-icon>
              {{ row.name || '-' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="class_name" label="班级" width="170" show-overflow-tooltip />
        <el-table-column label="成果数" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.achievement_count > 0 ? 'primary' : 'info'" size="small" effect="plain">
              {{ row.achievement_count }} 项
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="220" align="center">
          <template #default="{ row }">
            <el-button
              type="primary"
              plain
              size="small"
              :loading="exportingAllId === row.student_id"
              @click="handleExportAll(row)"
            >
              <el-icon><Download /></el-icon>
              全部导出
            </el-button>
            <el-button
              type="warning"
              plain
              size="small"
              :disabled="row.achievement_count === 0"
              @click="openItemDialog(row)"
            >
              <el-icon><Collection /></el-icon>
              单项导出
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 单项导出弹窗 -->
    <el-dialog
      :title="itemDialogTitle"
      v-model="showItemDialog"
      width="820px"
      :close-on-click-modal="false"
    >
      <el-table
        :data="itemAchievements"
        v-loading="loadingItems"
        height="380"
        empty-text="该学生暂无已通过成果"
        row-key="achievement_id"
        @row-click="handleRowExport"
        style="width: 100%; cursor: pointer"
      >
        <el-table-column prop="student_no" label="学号" width="120" show-overflow-tooltip />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="class_name" label="班级" width="140" show-overflow-tooltip />
        <el-table-column prop="title" label="成果名" min-width="200" show-overflow-tooltip />
        <el-table-column label="成果类型" min-width="140">
          <template #default="{ row }">
            {{ row.main_category || '' }}{{ row.sub_category ? ' · ' + row.sub_category : '' }}
          </template>
        </el-table-column>
        <el-table-column label="级别" width="90" align="center">
          <template #default="{ row }">
            <el-tag size="small" effect="plain">{{ row.level || '-' }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div class="item-dialog-tip">点击任意成果行即可导出该条成果的 PDF</div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh, Download, Collection, Trophy } from '@element-plus/icons-vue'
import { teacherExportApi } from '@/api'

const loading = ref(false)
const students = ref([])
const exportingAllId = ref(null)

const levelOptions = [
  { code: 'Xiao Ji', name: '校级' },
  { code: 'Sheng Ji', name: '省级' },
  { code: 'Guo Jia Ji', name: '国家级' },
  { code: 'Guo Ji Ji', name: '国际级' }
]
const categoryOptions = ref([])

// 搜索表单
const searchForm = reactive({
  start_date: '',
  end_date: '',
  category: '',
  level: '',
  student_no: ''
})

const buildParams = () => {
  const params = {}
  if (searchForm.start_date) params.start_date = searchForm.start_date
  if (searchForm.end_date) params.end_date = searchForm.end_date
  if (searchForm.category) params.category = searchForm.category
  if (searchForm.level) params.level = searchForm.level
  if (searchForm.student_no) params.student_no = searchForm.student_no
  return params
}

const loadCategories = async () => {
  try {
    const res = await teacherExportApi.listAwardTypes()
    categoryOptions.value = res.categories || []
  } catch (error) {
    console.error('加载奖项类型失败:', error)
  }
}

const loadStudents = async () => {
  loading.value = true
  try {
    const res = await teacherExportApi.listStudents(buildParams())
    students.value = res.students || []
  } catch (error) {
    console.error('加载学生列表失败:', error)
    ElMessage.error(error?.message || '加载学生列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadStudents()
}

const handleReset = () => {
  searchForm.start_date = ''
  searchForm.end_date = ''
  searchForm.category = ''
  searchForm.level = ''
  searchForm.student_no = ''
  loadStudents()
}

// 通用：处理下载 blob
const downloadBlob = (blob, filename) => {
  if (blob instanceof Blob && blob.type && blob.type.includes('application/json')) {
    return blob.text().then((text) => {
      const err = JSON.parse(text)
      ElMessage.error(err.error || err.message || '导出失败')
      return false
    })
  }
  const url = window.URL.createObjectURL(
    blob instanceof Blob ? blob : new Blob([blob], { type: 'application/pdf' })
  )
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
  return true
}

// 全部导出
const handleExportAll = async (row) => {
  if (row.achievement_count === 0) {
    ElMessage.warning('该学生暂无已通过成果，无法导出')
    return
  }
  exportingAllId.value = row.student_id
  try {
    const blob = await teacherExportApi.exportStudentCertificates(row.student_id)
    const ok = await downloadBlob(blob, `获奖证书汇总_${row.name}_${row.student_no}.pdf`)
    if (ok) ElMessage.success(`已导出 ${row.name} 的全部获奖证书`)
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error(error?.message || '导出失败')
  } finally {
    exportingAllId.value = null
  }
}

// 单项导出
const showItemDialog = ref(false)
const loadingItems = ref(false)
const itemAchievements = ref([])
const itemStudent = ref({})

const itemDialogTitle = computed(() => {
  const s = itemStudent.value
  return `单项导出 - ${s.name || ''}（${s.student_no || ''}）`
})

const openItemDialog = async (row) => {
  showItemDialog.value = true
  loadingItems.value = true
  itemStudent.value = row
  itemAchievements.value = []
  try {
    const res = await teacherExportApi.listStudentAchievements(row.student_id)
    itemStudent.value = {
      ...itemStudent.value,
      student_no: res.student_no || row.student_no,
      name: res.name || row.name,
      class_name: res.class_name || row.class_name
    }
    itemAchievements.value = res.achievements || []
  } catch (error) {
    console.error('加载学生成果失败:', error)
    ElMessage.error(error?.message || '加载学生成果失败')
  } finally {
    loadingItems.value = false
  }
}

const handleRowExport = async (row) => {
  try {
    const blob = await teacherExportApi.exportStudentAchievement(row.achievement_id)
    const ok = await downloadBlob(blob, `获奖证书_${row.title}_${itemStudent.value.student_no || ''}.pdf`)
    if (ok) ElMessage.success(`已导出「${row.title}」的证书`)
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error(error?.message || '导出失败')
  }
}

onMounted(() => {
  loadCategories()
  loadStudents()
})
</script>

<style scoped>
.teacher-export-container {
  padding: 4px 8px;
}

.page-card {
  background: #fff;
  border-radius: 12px;
  padding: 18px 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.search-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
  padding: 4px 0 18px;
  margin-bottom: 14px;
  border-bottom: 1px solid #f0f0f0;
}

.search-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.search-label {
  font-size: 13px;
  color: #5b6472;
  white-space: nowrap;
}

.search-actions {
  display: flex;
  gap: 10px;
  margin-left: auto;
}

.student-name {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #1a1a2e;
}

.item-dialog-tip {
  margin-top: 12px;
  font-size: 12px;
  color: #a0a0b0;
  text-align: right;
}

:deep(.el-dialog) {
  border-radius: 12px;
}
</style>