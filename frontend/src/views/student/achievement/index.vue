<template>
  <div class="student-achievement-container">
    <el-card class="stats-card">
      <el-row :gutter="16" class="stats-row">
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">总成果数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value approved">{{ stats.approved }}</div>
            <div class="stat-label">已通过</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value pending">{{ stats.pending }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value rejected">{{ stats.rejected }}</div>
            <div class="stat-label">已驳回</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="标题">
          <el-input v-model="filterForm.title" placeholder="请输入成果标题" clearable />
        </el-form-item>
        <el-form-item label="一级分类">
          <el-select v-model="filterForm.main_category" placeholder="请选择一级分类" clearable @change="handleMainCategoryChange">
            <el-option v-for="item in mainCategories" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="二级细分">
          <el-select v-model="filterForm.sub_category" placeholder="请选择二级细分" clearable :disabled="!filterForm.main_category">
            <el-option v-for="item in subCategories" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable>
            <el-option label="待审核" value="pending" />
            <el-option label="通过" value="approved" />
            <el-option label="驳回" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
          <el-button type="success" @click="goSubmit">
            <el-icon><Plus /></el-icon>
            录入成果
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table :data="achievements" stripe style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="title" label="成果标题" min-width="250" show-overflow-tooltip />
        <el-table-column label="一级分类" width="120">
          <template #default="{ row }">
            <span>{{ getMainCategoryLabel(row.main_category) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="二级细分" width="120">
          <template #default="{ row }">
            <span>{{ getSubCategoryLabel(row.sub_category) || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="level" label="级别" width="100">
          <template #default="{ row }">
            <el-tag :type="levelType[row.level]">{{ getLevelLabel(row.level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="auditor_name" label="审核人" width="100">
          <template #default="{ row }">
            <span>{{ row.auditor_name || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType[row.status]">{{ statusText[row.status] }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="submitted_at" label="提交时间" width="120" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link @click="handleView(row)">详情</el-button>
            <el-button v-if="row.status === 'pending'" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">
              {{ row.status === 'approved' ? '撤回' : '删除' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadAchievements"
        @current-change="loadAchievements"
        class="pagination"
      />
    </el-card>

    <el-dialog v-model="showDetailDialog" title="成果详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="成果标题">{{ detailData.title }}</el-descriptions-item>
        <el-descriptions-item label="一级分类">{{ getMainCategoryLabel(detailData.main_category) }}</el-descriptions-item>
        <el-descriptions-item label="二级细分">{{ getSubCategoryLabel(detailData.sub_category) || '-' }}</el-descriptions-item>
        <el-descriptions-item label="级别">{{ getLevelLabel(detailData.level) }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ detailData.description }}</el-descriptions-item>
        <el-descriptions-item label="证明材料">
          <div v-if="detailData.attachments && detailData.attachments.length > 0" class="proof-files">
            <div v-for="file in detailData.attachments" :key="file.id" class="proof-card">
              <template v-if="isImageFile(file)">
                <el-image
                  :src="getFileUrl(file.file_path)"
                  :preview-src-list="previewImageList"
                  :initial-index="previewImageIndex(file)"
                  fit="contain"
                  class="proof-image"
                  preview-teleported
                  hide-on-click-modal
                >
                  <template #error>
                    <div class="image-error">
                      <el-icon :size="28"><Picture /></el-icon>
                      <span>图片加载失败</span>
                      <el-button type="primary" link @click="downloadFile(file)">点击下载</el-button>
                    </div>
                  </template>
                </el-image>
              </template>
              <template v-else>
                <div class="file-icon-wrap">
                  <el-icon :size="36" class="file-icon"><Document /></el-icon>
                </div>
              </template>
              <div class="proof-actions">
                <span class="file-name" :title="file.file_name">{{ file.file_name }}</span>
                <span class="file-size">{{ formatFileSize(file.file_size) }}</span>
                <el-button type="primary" size="small" circle @click="downloadFile(file)">
                  <el-icon><Download /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
          <span v-else>无</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">{{ statusText[detailData.status] }}</el-descriptions-item>
        <el-descriptions-item label="审核人">{{ detailData.auditor_name || '无' }}</el-descriptions-item>
        <el-descriptions-item v-if="detailData.status === 'approved' || detailData.status === 'rejected'" label="审核时间">{{ detailData.reviewed_at || '无' }}</el-descriptions-item>
        <el-descriptions-item label="审核意见">{{ detailData.review_comment || '无' }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ detailData.submitted_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Picture, Document } from '@element-plus/icons-vue'
import { achievementsApi } from '@/api'
import { getMainCategoryLabel, getSubCategoryLabel, getLevelLabel } from '@/utils/constants'

const router = useRouter()
const loading = ref(false)
const achievements = ref([])
const showDetailDialog = ref(false)
const detailData = ref({})

const stats = reactive({
  total: 0,
  approved: 0,
  pending: 0,
  rejected: 0
})

const mainCategories = [
  { label: '学科竞赛类', value: '学科竞赛类' },
  { label: '学术论文类', value: '学术论文类' },
  { label: '知识产权类', value: '知识产权类' },
  { label: '科研项目类', value: '科研项目类' },
  { label: '荣誉表彰类', value: '荣誉表彰类' },
  { label: '技能证书类', value: '技能证书类' },
  { label: '社会实践类', value: '社会实践类' }
]

const categorySubCategories = {
  '学科竞赛类': [
    { label: 'ACM', value: 'ACM' },
    { label: '数学建模', value: '数学建模' },
    { label: '互联网+', value: '互联网+' },
    { label: '挑战杯', value: '挑战杯' },
    { label: '电子设计', value: '电子设计' },
    { label: '智能车', value: '智能车' },
    { label: '其他', value: '其他' }
  ],
  '学术论文类': [
    { label: 'SCI', value: 'SCI' },
    { label: 'EI', value: 'EI' },
    { label: '核心期刊', value: '核心期刊' },
    { label: '普通期刊', value: '普通期刊' },
    { label: '会议论文', value: '会议论文' }
  ],
  '知识产权类': [
    { label: '发明专利', value: '发明专利' },
    { label: '实用新型', value: '实用新型' },
    { label: '外观设计', value: '外观设计' },
    { label: '软件著作权', value: '软件著作权' }
  ],
  '科研项目类': [
    { label: '国家级大创', value: '国家级大创' },
    { label: '省级大创', value: '省级大创' },
    { label: '校级大创', value: '校级大创' },
    { label: '参与教师科研', value: '参与教师科研' }
  ],
  '荣誉表彰类': [
    { label: '国家奖学金', value: '国家奖学金' },
    { label: '励志奖学金', value: '励志奖学金' },
    { label: '三好学生', value: '三好学生' },
    { label: '优秀干部', value: '优秀干部' },
    { label: '优秀团员', value: '优秀团员' }
  ],
  '技能证书类': [
    { label: '英语四六级', value: '英语四六级' },
    { label: '计算机等级', value: '计算机等级' },
    { label: '教师资格证', value: '教师资格证' },
    { label: '普通话', value: '普通话' },
    { label: '职业资格证', value: '职业资格证' }
  ],
  '社会实践类': [
    { label: '志愿服务', value: '志愿服务' },
    { label: '社会实践', value: '社会实践' },
    { label: '社团活动', value: '社团活动' }
  ]
}

const subCategories = computed(() => {
  return categorySubCategories[filterForm.main_category] || []
})

const filterForm = reactive({
  title: '',
  main_category: '',
  sub_category: '',
  status: ''
})

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

const statusText = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已驳回'
}

const statusType = {
  pending: 'warning',
  approved: 'success',
  rejected: 'danger'
}

const levelType = {
  '国家级': 'danger',
  '省级': 'warning',
  '校级': '',
  '院级': 'info'
}

const handleMainCategoryChange = () => {
  filterForm.sub_category = ''
}

const loadAchievements = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      title: filterForm.title || undefined,
      main_category: filterForm.main_category || undefined,
      sub_category: filterForm.sub_category || undefined,
      status: filterForm.status || undefined
    }
    
    const res = await achievementsApi.list(params)
    achievements.value = res.achievements || []
    pagination.total = res.pagination?.total || 0
    
    stats.total = pagination.total
    stats.approved = achievements.value.filter(a => a.status === 'approved').length
    stats.pending = achievements.value.filter(a => a.status === 'pending').length
    stats.rejected = achievements.value.filter(a => a.status === 'rejected').length
    
    loadStats()
  } catch (error) {
    console.error('加载成果列表失败:', error)
    ElMessage.error('加载成果列表失败')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const res = await achievementsApi.list({ page_size: 1000 })
    const all = res.achievements || []
    stats.total = all.length
    stats.approved = all.filter(a => a.status === 'approved').length
    stats.pending = all.filter(a => a.status === 'pending').length
    stats.rejected = all.filter(a => a.status === 'rejected').length
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadAchievements()
}

const resetFilter = () => {
  filterForm.title = ''
  filterForm.main_category = ''
  filterForm.sub_category = ''
  filterForm.status = ''
  pagination.page = 1
  loadAchievements()
}

const handleView = async (row) => {
  try {
    const res = await achievementsApi.get(row.id)
    detailData.value = res.achievement || row
  } catch (error) {
    console.error('获取成果详情失败:', error)
    detailData.value = row
  }
  showDetailDialog.value = true
}

const getFileUrl = (filePath) => {
  if (!filePath) return '#'
  if (filePath.startsWith('http')) return filePath
  return `${import.meta.env.VITE_API_BASE_URL || ''}${filePath}`
}

const formatFileSize = (bytes) => {
  if (!bytes) return ''
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

const isImageFile = (file) => {
  if (!file) return false
  if (file.file_type && file.file_type.startsWith('image/')) return true
  const ext = file.file_name ? file.file_name.split('.').pop().toLowerCase() : ''
  return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'].includes(ext)
}

// 当前成果的所有图片 URL（用于 el-image 预览列表）
const previewImageList = computed(() => {
  const list = detailData.value.attachments || []
  return list.filter(isImageFile).map(f => getFileUrl(f.file_path))
})

// 点击某张图片时，预览从该图片开始
const previewImageIndex = (file) => {
  const url = getFileUrl(file.file_path)
  return Math.max(0, previewImageList.value.indexOf(url))
}

const downloadFile = async (file) => {
  const url = getFileUrl(file.file_path)
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error('下载失败')
    const blob = await response.blob()
    const blobUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = file.file_name || '下载文件'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(blobUrl)
    ElMessage.success('下载成功')
  } catch {
    const link = document.createElement('a')
    link.href = url
    link.download = file.file_name || '下载文件'
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.info('浏览器即将开始下载...')
  }
}

const goSubmit = () => {
  router.push('/student/submit')
}

const handleEdit = (row) => {
  router.push({
    path: '/student/submit',
    query: { id: row.id }
  })
}

const handleDelete = (row) => {
  const isApproved = row.status === 'approved'
  const title = isApproved ? '确认撤回该成果吗？' : '确认删除该成果吗？'
  const message = isApproved
    ? '该成果已审核通过，撤回后状态将变为"已驳回"，可重新修改后提交。'
    : '此操作不可恢复，确认删除吗？'
  
  ElMessageBox.confirm(message, title, {
    confirmButtonText: isApproved ? '确认撤回' : '确认删除',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      if (isApproved) {
        await achievementsApi.audit(row.id, {
          status: 'rejected',
          review_comment: '学生撤回已通过成果'
        })
        ElMessage.success('撤回成功')
      } else {
        await achievementsApi.delete(row.id)
        ElMessage.success('删除成功')
      }
      loadAchievements()
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  })
}

onMounted(() => {
  loadAchievements()
})
</script>

<style scoped>
.student-achievement-container {
  padding: 0;
}

.stats-card {
  margin-bottom: 24px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.stats-row {
  text-align: center;
}

.stat-item {
  padding: 8px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #333;
}

.stat-value.approved {
  color: #67c23a;
}

.stat-value.pending {
  color: #e6a23c;
}

.stat-value.rejected {
  color: #f56c6c;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.filter-card,
.table-card {
  margin-bottom: 24px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.filter-form {
  margin: 0;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.proof-files {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.proof-card {
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.proof-card:hover {
  border-color: rgba(64, 149, 229, 0.35);
  box-shadow: 0 4px 16px rgba(64, 149, 229, 0.12);
  transform: translateY(-2px);
}

.proof-image {
  width: 100%;
  height: 150px;
  display: block;
  background: #f5f7fa;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.proof-image:hover {
  opacity: 0.85;
}

.proof-image :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.file-icon-wrap {
  width: 100%;
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.06));
}

.file-icon {
  color: #667eea;
}

.proof-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  background: #fafbfc;
}

.file-name {
  flex: 1;
  font-size: 12px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 11px;
  color: #909399;
  flex-shrink: 0;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 150px;
  color: #909399;
  font-size: 12px;
  background: #f5f7fa;
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
  padding: 20px 24px;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table th) {
  background: rgba(64, 149, 229, 0.03);
  color: #666;
  font-weight: 500;
  font-size: 13px;
}

:deep(.el-table tr:hover > td) {
  background: rgba(64, 149, 229, 0.03);
}
</style>
